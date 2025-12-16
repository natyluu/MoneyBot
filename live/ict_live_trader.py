"""
live/ict_live_trader.py - Trader en Vivo para Estrategia ICT

Sistema completo para operar la estrategia ICT en tiempo real con:
- Modo Paper Trading (simulación)
- Sistema de alertas
- Análisis multi-temporal en tiempo real
- Preparado para integración con API de broker
"""

import time
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional
import threading

from strategy.ict_hybrid_strategy import ICTHybridStrategy, TradingSignal
from live.paper_trader import PaperTrader
from live.alert_system import AlertSystem
from utils.multi_timeframe_loader import load_multi_timeframe_data
from config import SYMBOL, INITIAL_CAPITAL, COMMISSION


class ICTLiveTrader:
    """
    Trader en vivo para la estrategia ICT Híbrida.
    
    Modos de operación:
    - PAPER: Simula operaciones sin riesgo real
    - ALERT: Solo envía alertas, no ejecuta operaciones
    - LIVE: Ejecuta operaciones reales (requiere API de broker)
    """
    
    def __init__(self, symbol: str = None, mode: str = "PAPER",
                 alert_file: Optional[str] = None,
                 webhook_url: Optional[str] = None,
                 email_config: Optional[Dict] = None):
        """
        Inicializa el trader en vivo.
        
        Args:
            symbol: Símbolo a operar (default: XAUUSD)
            mode: Modo de operación ('PAPER', 'ALERT', o 'LIVE')
            alert_file: Archivo para guardar alertas
            webhook_url: URL de webhook para alertas
            email_config: Configuración de email
        """
        self.symbol = symbol or SYMBOL
        self.mode = mode.upper()
        
        if self.mode not in ['PAPER', 'ALERT', 'LIVE']:
            raise ValueError(f"Modo inválido: {mode}. Debe ser 'PAPER', 'ALERT', o 'LIVE'")
        
        # Inicializa componentes
        self.strategy = ICTHybridStrategy()
        
        if self.mode == 'PAPER':
            self.paper_trader = PaperTrader(
                initial_capital=INITIAL_CAPITAL,
                commission=COMMISSION
            )
            print("✅ Modo PAPER TRADING activado")
        else:
            self.paper_trader = None
        
        self.alert_system = AlertSystem(
            alert_file=alert_file or f"alerts_{self.symbol}_{datetime.now().strftime('%Y%m%d')}.json",
            webhook_url=webhook_url,
            email_config=email_config
        )
        
        # Estado del trader
        self.running = False
        self.last_analysis_time = None
        self.last_signal_time = None
        self.data_cache: Dict[str, pd.DataFrame] = {}
        
        # Para datos en tiempo real (placeholder - se implementaría con API)
        self.api_client = None  # Se inicializaría con la API del broker
        
        print(f"🚀 ICT Live Trader inicializado")
        print(f"   Símbolo: {self.symbol}")
        print(f"   Modo: {self.mode}")
    
    def start(self, analysis_interval: int = 300, update_interval: int = 60):
        """
        Inicia el loop principal de trading en vivo.
        
        Args:
            analysis_interval: Segundos entre análisis multi-temporales completos (default: 300 = 5 min)
            update_interval: Segundos entre actualizaciones de precios (default: 60 = 1 min)
        """
        if self.running:
            print("⚠️ El trader ya está en ejecución")
            return
        
        self.running = True
        print("\n" + "=" * 70)
        print("INICIANDO TRADER EN VIVO")
        print("=" * 70)
        print(f"Modo: {self.mode}")
        print(f"Análisis cada: {analysis_interval}s")
        print(f"Actualización cada: {update_interval}s")
        print("Presiona Ctrl+C para detener")
        print("=" * 70 + "\n")
        
        try:
            while self.running:
                current_time = datetime.now()
                
                # Ejecuta análisis multi-temporal periódicamente
                if (self.last_analysis_time is None or 
                    (current_time - self.last_analysis_time).total_seconds() >= analysis_interval):
                    self._run_multi_timeframe_analysis()
                    self.last_analysis_time = current_time
                
                # Actualiza posiciones y busca señales
                if (self.last_signal_time is None or 
                    (current_time - self.last_signal_time).total_seconds() >= update_interval):
                    self._update_and_check_signals()
                    self.last_signal_time = current_time
                
                # Espera antes de la siguiente iteración
                time.sleep(min(update_interval, 10))  # Mínimo 10 segundos
        
        except KeyboardInterrupt:
            print("\n\n⏹️ Deteniendo trader...")
            self.stop()
        except Exception as e:
            print(f"\n❌ Error en el loop principal: {e}")
            import traceback
            traceback.print_exc()
            self.stop()
    
    def stop(self):
        """Detiene el trader"""
        self.running = False
        
        if self.mode == 'PAPER' and self.paper_trader:
            # Cierra todas las posiciones abiertas
            positions = self.paper_trader.get_positions()
            current_prices = self._get_current_prices()
            
            for symbol in list(positions.keys()):
                if symbol in current_prices:
                    self.paper_trader.close_position(symbol, current_prices[symbol], 'TRADER_STOPPED')
            
            # Muestra estadísticas finales
            stats = self.paper_trader.get_statistics(current_prices)
            print("\n" + "=" * 70)
            print("ESTADÍSTICAS FINALES (PAPER TRADING)")
            print("=" * 70)
            print(f"Capital inicial: ${stats['initial_capital']:,.2f}")
            print(f"Capital final: ${stats['current_capital']:,.2f}")
            print(f"Equity: ${stats['equity']:,.2f}")
            print(f"Retorno: {stats['total_return_pct']:+.2f}%")
            print(f"Total trades: {stats['total_trades']}")
            print(f"Tasa de acierto: {stats['win_rate_pct']:.2f}%")
            print(f"P&L Total: ${stats['total_pnl']:+,.2f}")
            print("=" * 70)
        
        print("✅ Trader detenido")
    
    def _run_multi_timeframe_analysis(self):
        """Ejecuta análisis multi-temporal completo"""
        try:
            print(f"\n🔍 Ejecutando análisis multi-temporal ({datetime.now().strftime('%H:%M:%S')})...")
            
            # Carga datos históricos (en producción, esto vendría de la API en tiempo real)
            data_dict = self._get_multi_timeframe_data()
            
            if not data_dict:
                print("⚠️ No se pudieron cargar datos. Intentando desde archivos...")
                data_dict = load_multi_timeframe_data(self.symbol)
            
            if not data_dict:
                print("❌ No hay datos disponibles para análisis")
                return
            
            # Ejecuta análisis por timeframe
            if 'D1' in data_dict and len(data_dict['D1']) > 10:
                self.strategy.analyze_D1(data_dict['D1'])
            
            if 'H4' in data_dict and len(data_dict['H4']) > 10:
                self.strategy.analyze_H4(data_dict['H4'])
            
            if 'H1' in data_dict and len(data_dict['H1']) > 10:
                self.strategy.analyze_H1(data_dict['H1'])
            
            if 'M15' in data_dict and 'M5' in data_dict:
                if len(data_dict['M15']) > 10 and len(data_dict['M5']) > 10:
                    self.strategy.analyze_M15_M5(data_dict['M15'], data_dict['M5'])
            
            print("✓ Análisis multi-temporal completado")
            
        except Exception as e:
            print(f"⚠️ Error en análisis multi-temporal: {e}")
    
    def _update_and_check_signals(self):
        """Actualiza posiciones y busca nuevas señales"""
        try:
            # Obtiene datos de M1/M3 para buscar señales
            m1_data, m3_data = self._get_execution_data()
            
            if m1_data is None or m3_data is None:
                return
            
            # Actualiza posiciones en paper trading
            if self.mode == 'PAPER' and self.paper_trader:
                current_prices = self._get_current_prices()
                closed_trades = self.paper_trader.update_positions(current_prices)
                
                if closed_trades:
                    for trade in closed_trades:
                        print(f"\n📉 Trade cerrado: {trade.symbol} {trade.direction}")
                        print(f"   P&L: ${trade.pnl:+.2f} ({trade.pnl_pct:+.2f}%)")
            
            # Busca nuevas señales
            signal = self.strategy.find_sniper_entry(m1_data, m3_data, self.strategy.context)
            
            if signal:
                self._handle_signal(signal)
        
        except Exception as e:
            print(f"⚠️ Error al actualizar y buscar señales: {e}")
    
    def _handle_signal(self, signal: TradingSignal):
        """Maneja una señal de trading detectada"""
        print(f"\n🎯 Señal detectada: {signal.operation_type} {self.symbol}")
        
        # Envía alerta siempre
        self.alert_system.send_alert(signal)
        
        # Ejecuta según el modo
        if self.mode == 'PAPER' and self.paper_trader:
            # Verifica que no haya posición abierta
            if self.symbol in self.paper_trader.get_positions():
                print("⚠️ Ya hay una posición abierta. Señal ignorada.")
                return
            
            # Calcula tamaño de posición
            balance = self.paper_trader.get_balance()
            position_value = balance * 0.1  # 10% del capital
            size = position_value / signal.entry_price
            
            # Abre posición en paper trading
            success = self.paper_trader.open_position(
                symbol=self.symbol,
                direction=signal.operation_type,
                entry_price=signal.entry_price,
                size=size,
                stop_loss=signal.stop_loss,
                take_profit_1=signal.take_profit_1,
                take_profit_2=signal.take_profit_2,
                take_profit_final=signal.take_profit_final
            )
            
            if success:
                print("✅ Posición abierta en paper trading")
        
        elif self.mode == 'LIVE':
            # TODO: Implementar ejecución real con API del broker
            print("⚠️ Modo LIVE no implementado aún. Se requiere integración con API del broker.")
            print("   Por ahora, solo se envían alertas.")
        
        # Modo ALERT solo envía alertas (ya enviado arriba)
    
    def _get_multi_timeframe_data(self) -> Dict[str, pd.DataFrame]:
        """
        Obtiene datos multi-temporales.
        
        En producción, esto se conectaría a la API del broker.
        Por ahora, carga desde archivos o cache.
        """
        # TODO: Implementar obtención de datos en tiempo real desde API
        # Por ahora, usa datos históricos
        return {}
    
    def _get_execution_data(self) -> tuple:
        """
        Obtiene datos de M1 y M3 para búsqueda de señales.
        
        Returns:
            Tupla (m1_data, m3_data) o (None, None) si no hay datos
        """
        # TODO: Implementar obtención en tiempo real
        # Por ahora, retorna None (se usará desde archivos si están disponibles)
        return None, None
    
    def _get_current_prices(self) -> Dict[str, float]:
        """
        Obtiene precios actuales de los símbolos.
        
        Returns:
            Diccionario {symbol: price}
        """
        # TODO: Implementar obtención de precios en tiempo real desde API
        # Por ahora, retorna precio simulado o desde último dato disponible
        return {self.symbol: 0.0}  # Placeholder
    
    def get_status(self) -> Dict:
        """Obtiene el estado actual del trader"""
        status = {
            'running': self.running,
            'mode': self.mode,
            'symbol': self.symbol,
            'last_analysis': self.last_analysis_time.isoformat() if self.last_analysis_time else None,
            'last_signal': self.last_signal_time.isoformat() if self.last_signal_time else None
        }
        
        if self.mode == 'PAPER' and self.paper_trader:
            current_prices = self._get_current_prices()
            stats = self.paper_trader.get_statistics(current_prices)
            status['paper_trading'] = stats
            status['open_positions'] = len(self.paper_trader.get_positions())
        
        return status


def main():
    """Función principal para ejecutar el trader en modo standalone"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ICT Live Trader')
    parser.add_argument('--symbol', default='XAUUSD', help='Símbolo a operar')
    parser.add_argument('--mode', choices=['PAPER', 'ALERT', 'LIVE'], default='PAPER',
                       help='Modo de operación')
    parser.add_argument('--alert-file', help='Archivo para guardar alertas')
    parser.add_argument('--webhook', help='URL de webhook para alertas')
    
    args = parser.parse_args()
    
    # Configuración de email (opcional)
    email_config = None
    # email_config = {
    #     'smtp_server': 'smtp.gmail.com',
    #     'port': 587,
    #     'user': 'tu_email@gmail.com',
    #     'password': 'tu_password',
    #     'to': 'destinatario@gmail.com'
    # }
    
    trader = ICTLiveTrader(
        symbol=args.symbol,
        mode=args.mode,
        alert_file=args.alert_file,
        webhook_url=args.webhook,
        email_config=email_config
    )
    
    trader.start()


if __name__ == "__main__":
    main()













