"""
backtest/ict_backtest_engine.py - Motor de backtesting para estrategias ICT

Motor especializado para backtesting de estrategias multi-temporales ICT.
Soporta análisis de múltiples timeframes y señales complejas con múltiples TPs.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from config import INITIAL_CAPITAL, COMMISSION, MAX_POSITION_SIZE
from strategy.ict_hybrid_strategy import ICTHybridStrategy, TradingSignal


@dataclass
class Trade:
    """Representa una operación de trading"""
    entry_time: pd.Timestamp
    exit_time: Optional[pd.Timestamp]
    entry_price: float
    exit_price: Optional[float]
    direction: str  # 'BUY' o 'SELL'
    size: float  # Tamaño de la posición
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    take_profit_final: float
    pnl: Optional[float] = None
    pnl_pct: Optional[float] = None
    exit_reason: Optional[str] = None  # 'SL', 'TP1', 'TP2', 'TP_FINAL', 'SIGNAL'
    signal: Optional[TradingSignal] = None


@dataclass
class BacktestResults:
    """Resultados completos del backtest"""
    initial_capital: float
    final_capital: float
    total_return_pct: float
    total_pnl: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate_pct: float
    avg_win: float
    avg_loss: float
    profit_factor: float
    max_drawdown_pct: float
    max_drawdown_duration: int
    sharpe_ratio: float
    trades: List[Trade]
    equity_curve: List[Dict]
    signals_generated: int
    signals_executed: int


class ICTBacktestEngine:
    """
    Motor de backtesting especializado para estrategias ICT multi-temporales.
    
    Características:
    - Soporta análisis multi-temporal
    - Maneja múltiples Take Profits (TP1, TP2, TP Final)
    - Simula ejecución realista de órdenes
    - Calcula métricas avanzadas (Sharpe, Drawdown, etc.)
    """
    
    def __init__(self, initial_capital: float = None, commission: float = None,
                 slippage: float = 0.0001, position_size_pct: float = None):
        """
        Inicializa el motor de backtesting ICT.
        
        Args:
            initial_capital: Capital inicial
            commission: Comisión por operación (ej: 0.001 = 0.1%)
            slippage: Slippage estimado (ej: 0.0001 = 0.01%)
            position_size_pct: Porcentaje del capital por operación
        """
        from config import INITIAL_CAPITAL, COMMISSION, MAX_POSITION_SIZE
        
        self.initial_capital = initial_capital or INITIAL_CAPITAL
        self.commission = commission or COMMISSION
        self.slippage = slippage
        self.position_size_pct = position_size_pct or MAX_POSITION_SIZE
        
        self.capital = self.initial_capital
        self.position: Optional[Trade] = None
        self.trades: List[Trade] = []
        self.equity_curve: List[Dict] = []
        self.signals_generated = 0
        self.signals_executed = 0
    
    def run(self, data_dict: Dict[str, pd.DataFrame], strategy: ICTHybridStrategy,
           start_date: Optional[str] = None, end_date: Optional[str] = None) -> BacktestResults:
        """
        Ejecuta el backtest completo de la estrategia ICT.
        
        Args:
            data_dict: Diccionario con DataFrames de cada timeframe
            strategy: Instancia de la estrategia ICT
            start_date: Fecha de inicio (opcional)
            end_date: Fecha de fin (opcional)
        
        Returns:
            BacktestResults con todos los resultados
        """
        print("=" * 70)
        print("INICIANDO BACKTEST ICT MULTI-TEMPORAL")
        print("=" * 70)
        print(f"Capital inicial: ${self.initial_capital:,.2f}")
        print(f"Comisión: {self.commission*100:.3f}%")
        print(f"Slippage: {self.slippage*100:.3f}%")
        print(f"Tamaño de posición: {self.position_size_pct*100:.1f}%")
        
        # Valida que tengamos los timeframes necesarios
        required = ['D1', 'H4', 'H1', 'M15', 'M5']
        missing = [tf for tf in required if tf not in data_dict]
        if missing:
            print(f"⚠️ Timeframes faltantes: {', '.join(missing)}")
            print("   El backtest puede no ser preciso sin todos los timeframes")
        
        # Usa M1 o M3 como timeframe de ejecución (el más granular disponible)
        execution_tf = 'M1' if 'M1' in data_dict else 'M3' if 'M3' in data_dict else 'M5'
        execution_data = data_dict[execution_tf].copy()
        
        if start_date:
            execution_data = execution_data[execution_data.index >= pd.to_datetime(start_date)]
        if end_date:
            execution_data = execution_data[execution_data.index <= pd.to_datetime(end_date)]
        
        print(f"\nTimeframe de ejecución: {execution_tf}")
        print(f"Período: {execution_data.index[0]} a {execution_data.index[-1]}")
        print(f"Total de velas: {len(execution_data)}")
        
        # Ejecuta análisis multi-temporal periódicamente
        # (no en cada vela para optimizar rendimiento)
        analysis_interval = max(1, len(execution_data) // 100)  # Analiza ~100 veces
        
        print(f"\nAnálisis multi-temporal cada {analysis_interval} velas")
        print("-" * 70)
        
        # Itera sobre cada vela del timeframe de ejecución
        for i in range(len(execution_data)):
            current_bar = execution_data.iloc[i]
            current_time = execution_data.index[i]
            
            # Ejecuta análisis multi-temporal periódicamente
            if i % analysis_interval == 0 or i == 0:
                try:
                    # Actualiza datos para análisis (solo hasta el momento actual)
                    current_data_dict = {}
                    for tf_key, df in data_dict.items():
                        current_data_dict[tf_key] = df[df.index <= current_time].copy()
                    
                    # Ejecuta análisis multi-temporal
                    self._run_multi_timeframe_analysis(current_data_dict, strategy, current_time)
                except Exception as e:
                    print(f"⚠️ Error en análisis multi-temporal en {current_time}: {e}")
            
            # Gestiona posición actual
            if self.position is not None:
                self._manage_position(current_bar, current_time, execution_data)
            
            # Busca nuevas señales
            if self.position is None:
                signal = self._check_for_signals(strategy, current_time, execution_data, i)
                if signal:
                    self._execute_signal(signal, current_bar, current_time)
            
            # Registra equity
            current_equity = self._calculate_equity(current_bar['close'])
            self.equity_curve.append({
                'timestamp': current_time,
                'equity': current_equity,
                'capital': self.capital
            })
        
        # Cierra posición abierta al final
        if self.position is not None:
            last_bar = execution_data.iloc[-1]
            self._close_position(last_bar, execution_data.index[-1], 'END_OF_DATA')
        
        # Calcula resultados
        results = self._calculate_results()
        
        return results
    
    def _run_multi_timeframe_analysis(self, data_dict: Dict[str, pd.DataFrame],
                                     strategy: ICTHybridStrategy, current_time: pd.Timestamp):
        """Ejecuta análisis multi-temporal hasta el momento actual"""
        try:
            # D1
            if 'D1' in data_dict and len(data_dict['D1']) > 10:
                strategy.analyze_D1(data_dict['D1'])
            
            # H4
            if 'H4' in data_dict and len(data_dict['H4']) > 10:
                strategy.analyze_H4(data_dict['H4'])
            
            # H1
            if 'H1' in data_dict and len(data_dict['H1']) > 10:
                strategy.analyze_H1(data_dict['H1'])
            
            # M15/M5
            if 'M15' in data_dict and 'M5' in data_dict:
                if len(data_dict['M15']) > 10 and len(data_dict['M5']) > 10:
                    strategy.analyze_M15_M5(data_dict['M15'], data_dict['M5'])
        except Exception as e:
            # Silenciosamente maneja errores en análisis (puede ser por datos insuficientes)
            pass
    
    def _check_for_signals(self, strategy: ICTHybridStrategy, current_time: pd.Timestamp,
                          execution_data: pd.DataFrame, current_index: int) -> Optional[TradingSignal]:
        """Verifica si hay señales de trading en el momento actual"""
        try:
            # Solo busca señales en M1/M3 si están disponibles
            m1_data = None
            m3_data = None
            
            # Obtiene datos hasta el momento actual
            current_slice = execution_data.iloc[:current_index+1]
            
            # Si el timeframe de ejecución es M1 o M3, úsalo directamente
            if len(current_slice) >= 50:  # Necesita suficientes velas
                # Busca señal sniper
                signal = strategy.find_sniper_entry(current_slice, current_slice, strategy.context)
                
                if signal:
                    self.signals_generated += 1
                    return signal
        except Exception as e:
            # No hay señal disponible
            pass
        
        return None
    
    def _execute_signal(self, signal: TradingSignal, current_bar: pd.Series, current_time: pd.Timestamp):
        """Ejecuta una señal de trading"""
        entry_price = current_bar['close']
        
        # Aplica slippage
        if signal.operation_type == 'BUY':
            entry_price = entry_price * (1 + self.slippage)
        else:
            entry_price = entry_price * (1 - self.slippage)
        
        # Calcula tamaño de posición
        position_value = self.capital * self.position_size_pct
        size = position_value / entry_price
        
        # Calcula costos (comisión)
        cost = size * entry_price * (1 + self.commission)
        
        if cost > self.capital:
            # No hay suficiente capital
            return
        
        # Crea la posición
        self.position = Trade(
            entry_time=current_time,
            exit_time=None,
            entry_price=entry_price,
            exit_price=None,
            direction=signal.operation_type,
            size=size,
            stop_loss=signal.stop_loss,
            take_profit_1=signal.take_profit_1,
            take_profit_2=signal.take_profit_2,
            take_profit_final=signal.take_profit_final,
            signal=signal
        )
        
        self.capital -= cost
        self.signals_executed += 1
        
        print(f"\n📈 {signal.operation_type} en {current_time}")
        print(f"   Entrada: ${entry_price:.2f}")
        print(f"   Tamaño: {size:.4f}")
        print(f"   SL: ${signal.stop_loss:.2f}")
        print(f"   TP1: ${signal.take_profit_1:.2f}, TP2: ${signal.take_profit_2:.2f}, TP Final: ${signal.take_profit_final:.2f}")
    
    def _manage_position(self, current_bar: pd.Series, current_time: pd.Timestamp,
                        execution_data: pd.DataFrame):
        """Gestiona la posición actual (verifica SL y TPs)"""
        if self.position is None:
            return
        
        current_high = current_bar['high']
        current_low = current_bar['low']
        current_close = current_bar['close']
        
        exit_price = None
        exit_reason = None
        
        if self.position.direction == 'BUY':
            # Verifica Stop Loss
            if current_low <= self.position.stop_loss:
                exit_price = self.position.stop_loss * (1 - self.slippage)
                exit_reason = 'SL'
            
            # Verifica Take Profits (en orden)
            elif current_high >= self.position.take_profit_final:
                exit_price = self.position.take_profit_final * (1 - self.slippage)
                exit_reason = 'TP_FINAL'
            elif current_high >= self.position.take_profit_2:
                exit_price = self.position.take_profit_2 * (1 - self.slippage)
                exit_reason = 'TP2'
            elif current_high >= self.position.take_profit_1:
                exit_price = self.position.take_profit_1 * (1 - self.slippage)
                exit_reason = 'TP1'
        
        else:  # SELL
            # Verifica Stop Loss
            if current_high >= self.position.stop_loss:
                exit_price = self.position.stop_loss * (1 + self.slippage)
                exit_reason = 'SL'
            
            # Verifica Take Profits
            elif current_low <= self.position.take_profit_final:
                exit_price = self.position.take_profit_final * (1 + self.slippage)
                exit_reason = 'TP_FINAL'
            elif current_low <= self.position.take_profit_2:
                exit_price = self.position.take_profit_2 * (1 + self.slippage)
                exit_reason = 'TP2'
            elif current_low <= self.position.take_profit_1:
                exit_price = self.position.take_profit_1 * (1 + self.slippage)
                exit_reason = 'TP1'
        
        if exit_price:
            self._close_position(current_bar, current_time, exit_reason, exit_price)
    
    def _close_position(self, current_bar: pd.Series, current_time: pd.Timestamp,
                        exit_reason: str, exit_price: Optional[float] = None):
        """Cierra la posición actual"""
        if self.position is None:
            return
        
        if exit_price is None:
            exit_price = current_bar['close']
            if self.position.direction == 'BUY':
                exit_price *= (1 - self.slippage)
            else:
                exit_price *= (1 + self.slippage)
        
        # Calcula P&L
        proceeds = self.position.size * exit_price * (1 - self.commission)
        cost = self.position.size * self.position.entry_price * (1 + self.commission)
        pnl = proceeds - cost
        pnl_pct = ((exit_price - self.position.entry_price) / self.position.entry_price) * 100
        
        if self.position.direction == 'SELL':
            pnl = -pnl
            pnl_pct = -pnl_pct
        
        # Actualiza posición
        self.position.exit_time = current_time
        self.position.exit_price = exit_price
        self.position.pnl = pnl
        self.position.pnl_pct = pnl_pct
        self.position.exit_reason = exit_reason
        
        # Actualiza capital
        self.capital += proceeds
        
        # Guarda el trade
        self.trades.append(self.position)
        
        print(f"\n📉 Cierre en {current_time} - {exit_reason}")
        print(f"   Salida: ${exit_price:.2f}")
        print(f"   P&L: ${pnl:.2f} ({pnl_pct:+.2f}%)")
        print(f"   Capital: ${self.capital:,.2f}")
        
        self.position = None
    
    def _calculate_equity(self, current_price: float) -> float:
        """Calcula el equity actual (capital + valor de posición)"""
        if self.position is None:
            return self.capital
        
        position_value = self.position.size * current_price
        return self.capital + position_value
    
    def _calculate_results(self) -> BacktestResults:
        """Calcula métricas completas del backtest"""
        if not self.trades:
            return BacktestResults(
                initial_capital=self.initial_capital,
                final_capital=self.capital,
                total_return_pct=0,
                total_pnl=0,
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                win_rate_pct=0,
                avg_win=0,
                avg_loss=0,
                profit_factor=0,
                max_drawdown_pct=0,
                max_drawdown_duration=0,
                sharpe_ratio=0,
                trades=[],
                equity_curve=self.equity_curve,
                signals_generated=self.signals_generated,
                signals_executed=self.signals_executed
            )
        
        trades_df = pd.DataFrame([{
            'entry_time': t.entry_time,
            'exit_time': t.exit_time,
            'pnl': t.pnl,
            'pnl_pct': t.pnl_pct,
            'exit_reason': t.exit_reason
        } for t in self.trades])
        
        # Métricas básicas
        total_trades = len(self.trades)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = trades_df['pnl'].sum()
        total_return = (self.capital - self.initial_capital) / self.initial_capital * 100
        
        avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['pnl'] < 0]['pnl'].mean() if losing_trades > 0 else 0
        
        total_wins = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
        total_losses = abs(trades_df[trades_df['pnl'] < 0]['pnl'].sum())
        profit_factor = total_wins / total_losses if total_losses > 0 else 0
        
        # Drawdown
        equity_series = pd.Series([e['equity'] for e in self.equity_curve])
        running_max = equity_series.expanding().max()
        drawdown = (equity_series - running_max) / running_max * 100
        max_drawdown = drawdown.min()
        
        # Duración del drawdown máximo
        max_dd_idx = drawdown.idxmin()
        max_dd_duration = 0
        if max_dd_idx is not None:
            # Calcula cuántas velas duró el drawdown máximo
            for i in range(max_dd_idx, len(drawdown)):
                if drawdown.iloc[i] >= 0:
                    max_dd_duration = i - max_dd_idx
                    break
        
        # Sharpe Ratio (simplificado)
        returns = equity_series.pct_change().dropna()
        if len(returns) > 0 and returns.std() > 0:
            sharpe = (returns.mean() / returns.std()) * np.sqrt(252)  # Anualizado
        else:
            sharpe = 0
        
        return BacktestResults(
            initial_capital=self.initial_capital,
            final_capital=self.capital,
            total_return_pct=total_return,
            total_pnl=total_pnl,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate_pct=win_rate,
            avg_win=avg_win,
            avg_loss=avg_loss,
            profit_factor=profit_factor,
            max_drawdown_pct=abs(max_drawdown),
            max_drawdown_duration=max_dd_duration,
            sharpe_ratio=sharpe,
            trades=self.trades,
            equity_curve=self.equity_curve,
            signals_generated=self.signals_generated,
            signals_executed=self.signals_executed
        )













