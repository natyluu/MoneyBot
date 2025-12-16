"""
backtest/backtest.py - Sistema de Backtesting Completo para Estrategia ICT

Este módulo realiza backtesting completo de la estrategia institucional ICT
usando datos históricos multi-temporales desde archivos CSV.

Para una trader ICT novata en Python:
- Este archivo simula cómo habría funcionado tu estrategia en el pasado
- Usa datos históricos reales de XAUUSD
- Ejecuta operaciones simuladas con SL y múltiples TPs
- Calcula métricas de rendimiento (winrate, profit factor, drawdown, etc.)
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from config import DATA_DIR, INITIAL_CAPITAL, COMMISSION
from strategy.ict_hybrid_strategy import ICTHybridStrategy


@dataclass
class Trade:
    """
    Representa una operación de trading individual.
    
    Para entender esto como trader ICT:
    - entry_time: Momento en que entraste a la operación
    - exit_time: Momento en que saliste (por SL o TP)
    - entry_price: Precio al que compraste/vendiste
    - exit_price: Precio al que cerraste la operación
    - direction: "BUY" (compra) o "SELL" (venta)
    - pnl: Ganancia o pérdida en dólares
    - pnl_pct: Ganancia o pérdida en porcentaje
    - exit_reason: Por qué saliste ("STOP_LOSS", "TAKE_PROFIT_1", etc.)
    """
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    entry_price: float
    exit_price: float
    direction: str  # "BUY" o "SELL"
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    take_profit_final: float
    size: float  # Tamaño de la posición
    pnl: float
    pnl_pct: float
    exit_reason: str
    risk_reward: float


@dataclass
class BacktestResult:
    """
    Resultados completos del backtest.
    
    Estas son las métricas que te dicen qué tan bien funcionó tu estrategia:
    - total_trades: Cuántas operaciones hiciste
    - winrate: Porcentaje de operaciones ganadoras
    - profit_factor: Ratio de ganancias vs pérdidas (idealmente > 1.5)
    - max_drawdown: Máxima caída desde un pico (cuánto bajó tu capital)
    - avg_rr: Risk:Reward promedio de tus operaciones
    """
    initial_capital: float
    final_capital: float
    total_return_pct: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    winrate: float
    profit_factor: float
    max_drawdown: float
    avg_rr: float
    total_pnl: float
    trades: List[Trade]
    equity_curve: List[Dict]


def load_multi_timeframe_data(symbol: str = "XAUUSD") -> Dict[str, pd.DataFrame]:
    """
    Carga datos históricos de múltiples timeframes desde archivos CSV.
    
    Como trader ICT, necesitas analizar el mercado en diferentes timeframes:
    - D1: Para ver la tendencia macro y zonas de liquidez mayor
    - H4: Para ver BOS/CHoCH institucionales y estructuras
    - H1: Para aterrizar zonas institucionales activas
    - M15/M5: Para ver BOS/CHoCH limpios y barridas de liquidez
    - M3/M1: Para confirmar entradas tipo sniper
    
    Args:
        symbol: Símbolo a cargar (default: "XAUUSD")
    
    Returns:
        Diccionario con DataFrames de cada timeframe:
        {
            "D1": df_d1,    # Datos diarios
            "H4": df_h4,    # Datos de 4 horas
            "H1": df_h1,    # Datos de 1 hora
            "M15": df_m15,  # Datos de 15 minutos
            "M5": df_m5,    # Datos de 5 minutos
            "M3": df_m3,    # Datos de 3 minutos
            "M1": df_m1     # Datos de 1 minuto
        }
    """
    print("📊 Cargando datos multi-temporales...")
    
    # Mapeo de timeframes a nombres de archivo
    timeframe_map = {
        "D1": "1d",
        "H4": "4h",
        "H1": "1h",
        "M15": "15m",
        "M5": "5m",
        "M3": "3m",
        "M1": "1m"
    }
    
    data_dict = {}
    
    # Carga cada timeframe desde su archivo CSV
    for tf_key, tf_file in timeframe_map.items():
        csv_path = os.path.join(DATA_DIR, f"{symbol}_{tf_file}.csv")
        
        if os.path.exists(csv_path):
            try:
                # Lee el CSV
                df = pd.read_csv(csv_path)
                
                # Asegura que tenga la columna 'timestamp'
                if 'timestamp' not in df.columns and 'time' in df.columns:
                    df.rename(columns={'time': 'timestamp'}, inplace=True)
                
                # Convierte timestamp a datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df.set_index('timestamp', inplace=True)
                
                # Verifica que tenga las columnas necesarias (OHLCV)
                required_cols = ['open', 'high', 'low', 'close', 'volume']
                if all(col in df.columns for col in required_cols):
                    data_dict[tf_key] = df
                    print(f"   ✓ {tf_key}: {len(df)} velas cargadas ({df.index[0]} a {df.index[-1]})")
                else:
                    print(f"   ✗ {tf_key}: Faltan columnas requeridas")
            
            except Exception as e:
                print(f"   ✗ {tf_key}: Error al cargar - {e}")
        else:
            print(f"   ⚠️ {tf_key}: Archivo no encontrado: {csv_path}")
    
    print(f"\n✓ Datos cargados para {len(data_dict)} timeframes")
    return data_dict


def synchronize_timeframes(data_dict: Dict[str, pd.DataFrame], 
                          base_timeframe: str = "M1") -> Dict[str, pd.DataFrame]:
    """
    Sincroniza los timeframes para que cada vela del timeframe base tenga
    el contexto exacto de todos los timeframes superiores.
    
    ¿Por qué es importante esto?
    Como trader ICT, cuando analizas una vela de M1, necesitas saber:
    - Qué está pasando en D1 (tendencia macro)
    - Qué está pasando en H4 (estructura institucional)
    - Qué está pasando en H1 (zonas activas)
    - Etc.
    
    Esta función asegura que para cada vela de M1, tengas acceso a las velas
    correspondientes de todos los timeframes superiores.
    
    Args:
        data_dict: Diccionario con DataFrames de cada timeframe
        base_timeframe: Timeframe base para sincronizar (default: "M1")
    
    Returns:
        Diccionario con DataFrames sincronizados
    """
    print(f"\n🔄 Sincronizando timeframes (base: {base_timeframe})...")
    
    if base_timeframe not in data_dict:
        print(f"⚠️ Timeframe base {base_timeframe} no encontrado")
        return data_dict
    
    base_df = data_dict[base_timeframe].copy()
    synchronized = {base_timeframe: base_df}
    
    # Orden de timeframes de mayor a menor
    timeframe_order = ["D1", "H4", "H1", "M15", "M5", "M3", "M1"]
    
    # Para cada timeframe superior, alinea con el base
    for tf in timeframe_order:
        if tf == base_timeframe:
            continue
        
        if tf not in data_dict:
            continue
        
        df = data_dict[tf].copy()
        
        # Re-muestrea al timeframe base usando forward fill
        # Esto significa que cada vela de M1 "hereda" los valores de la última
        # vela de D1/H4/etc. que se completó
        df_resampled = df.reindex(base_df.index, method='ffill')
        
        # Elimina filas donde no hay datos del timeframe superior
        df_resampled = df_resampled.dropna()
        
        if len(df_resampled) > 0:
            synchronized[tf] = df_resampled
            print(f"   ✓ {tf}: {len(df_resampled)} velas sincronizadas")
    
    # Filtra el base para que solo tenga velas donde todos los timeframes tienen datos
    if len(synchronized) > 1:
        # Encuentra la intersección de índices
        common_index = base_df.index
        for tf, df in synchronized.items():
            if tf != base_timeframe:
                common_index = common_index.intersection(df.index)
        
        # Filtra todos los DataFrames al índice común
        for tf in synchronized:
            synchronized[tf] = synchronized[tf].loc[common_index]
        
        print(f"   ✓ {len(common_index)} velas comunes después de sincronización")
    
    return synchronized


def run_backtest(data_dict: Dict[str, pd.DataFrame], 
                initial_capital: float = None,
                risk_per_trade: float = 0.01,
                commission: float = None) -> BacktestResult:
    """
    Ejecuta el backtest completo de la estrategia ICT.
    
    ¿Qué hace esta función?
    1. Recorre cada vela del timeframe base (M1 o M5)
    2. En cada vela, construye el contexto multi-temporal
    3. Llama a generate_signal() para obtener una señal
    4. Si hay señal BUY/SELL, simula la operación
    5. Gestiona SL y múltiples TPs automáticamente
    6. Registra todos los resultados
    
    Args:
        data_dict: Diccionario con DataFrames sincronizados de cada timeframe
        initial_capital: Capital inicial para el backtest
        risk_per_trade: Porcentaje de riesgo por operación (default: 1%)
        commission: Comisión por operación
    
    Returns:
        BacktestResult con todos los resultados del backtest
    """
    print("\n" + "=" * 70)
    print("INICIANDO BACKTEST COMPLETO")
    print("=" * 70)
    
    # Configuración
    initial_capital = initial_capital or INITIAL_CAPITAL
    commission = commission or COMMISSION
    capital = initial_capital
    
    # Inicializa la estrategia
    strategy = ICTHybridStrategy()
    
    # Selecciona timeframe base (M1 si está disponible, sino M5, sino M3)
    base_timeframe = None
    for tf in ["M1", "M5", "M3"]:
        if tf in data_dict and len(data_dict[tf]) > 100:
            base_timeframe = tf
            break
    
    if base_timeframe is None:
        print("❌ No hay timeframe base válido (M1, M5 o M3)")
        return None
    
    base_data = data_dict[base_timeframe]
    print(f"✓ Timeframe base: {base_timeframe} ({len(base_data)} velas)")
    print(f"✓ Capital inicial: ${initial_capital:,.2f}")
    print(f"✓ Riesgo por operación: {risk_per_trade*100:.1f}%")
    print(f"✓ Comisión: {commission*100:.3f}%")
    print("-" * 70)
    
    # Estado del backtest
    position = None  # Posición actual (None = sin posición)
    trades: List[Trade] = []
    equity_curve: List[Dict] = []
    
    # Recorre cada vela del timeframe base
    for i in range(len(base_data)):
        current_bar = base_data.iloc[i]
        current_time = base_data.index[i]
        
        # Construye el contexto multi-temporal para esta vela
        # Solo usa datos hasta el momento actual (no futuro)
        contexto = {}
        for tf_key, df in data_dict.items():
            # Filtra datos hasta el momento actual
            contexto[tf_key] = df[df.index <= current_time].copy()
        
        # Gestiona posición actual (verifica SL y TPs)
        if position is not None:
            exit_reason, exit_price = _check_exit_conditions(
                current_bar, position, current_time
            )
            
            if exit_reason:
                # Cierra la posición
                pnl, pnl_pct = _calculate_pnl(position, exit_price, commission)
                capital += position.size * exit_price * (1 - commission)
                
                trade = Trade(
                    entry_time=position.entry_time,
                    exit_time=current_time,
                    entry_price=position.entry_price,
                    exit_price=exit_price,
                    direction=position.direction,
                    stop_loss=position.stop_loss,
                    take_profit_1=position.take_profit_1,
                    take_profit_2=position.take_profit_2,
                    take_profit_final=position.take_profit_final,
                    size=position.size,
                    pnl=pnl,
                    pnl_pct=pnl_pct,
                    exit_reason=exit_reason,
                    risk_reward=position.risk_reward
                )
                
                trades.append(trade)
                position = None
                
                print(f"\n📉 Cierre: {trade.direction} | {exit_reason}")
                print(f"   Entrada: ${trade.entry_price:.2f} → Salida: ${exit_price:.2f}")
                print(f"   P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%) | Capital: ${capital:,.2f}")
        
        # Busca nuevas señales solo si no hay posición abierta
        if position is None:
            # Llama a generate_signal() con el contexto
            signal = strategy.generate_signal(contexto)
            
            if signal and signal["signal"] in ["BUY", "SELL"]:
                # Verifica que el RR sea razonable (mínimo 1:1.5)
                if signal["risk_reward"] >= 1.5:
                    # Calcula tamaño de posición basado en riesgo
                    entry_price = signal["entry_price"]
                    stop_loss = signal["stop_loss"]
                    risk_amount = capital * risk_per_trade
                    
                    # Calcula distancia al SL
                    if signal["signal"] == "BUY":
                        risk_distance = entry_price - stop_loss
                    else:  # SELL
                        risk_distance = stop_loss - entry_price
                    
                    # Calcula tamaño de posición
                    if risk_distance > 0:
                        size = risk_amount / risk_distance
                        
                        # Verifica que haya suficiente capital
                        cost = size * entry_price * (1 + commission)
                        if cost <= capital:
                            # Abre la posición
                            position = {
                                "entry_time": current_time,
                                "entry_price": entry_price,
                                "direction": signal["signal"],
                                "stop_loss": stop_loss,
                                "take_profit_1": signal["take_profit_1"],
                                "take_profit_2": signal["take_profit_2"],
                                "take_profit_final": signal["take_profit_final"],
                                "size": size,
                                "risk_reward": signal["risk_reward"]
                            }
                            
                            capital -= cost
                            
                            print(f"\n📈 Apertura: {signal['signal']} en {current_time}")
                            print(f"   Entrada: ${entry_price:.2f} | SL: ${stop_loss:.2f}")
                            print(f"   TP1: ${signal['take_profit_1']:.2f} | TP2: ${signal['take_profit_2']:.2f} | TP Final: ${signal['take_profit_final']:.2f}")
                            print(f"   RR: 1:{signal['risk_reward']:.2f} | Capital: ${capital:,.2f}")
                            if signal.get("justifications"):
                                print(f"   Razones: {', '.join(signal['justifications'][:2])}")
        
        # Registra equity
        current_equity = capital
        if position:
            current_price = current_bar['close']
            if position["direction"] == "BUY":
                current_equity += position["size"] * current_price
            else:
                current_equity += position["size"] * (2 * position["entry_price"] - current_price)
        
        equity_curve.append({
            "timestamp": current_time,
            "equity": current_equity
        })
    
    # Cierra posición abierta al final si existe
    if position:
        last_bar = base_data.iloc[-1]
        exit_price = last_bar['close']
        pnl, pnl_pct = _calculate_pnl(position, exit_price, commission)
        capital += position["size"] * exit_price * (1 - commission)
        
        trade = Trade(
            entry_time=position["entry_time"],
            exit_time=base_data.index[-1],
            entry_price=position["entry_price"],
            exit_price=exit_price,
            direction=position["direction"],
            stop_loss=position["stop_loss"],
            take_profit_1=position["take_profit_1"],
            take_profit_2=position["take_profit_2"],
            take_profit_final=position["take_profit_final"],
            size=position["size"],
            pnl=pnl,
            pnl_pct=pnl_pct,
            exit_reason="END_OF_DATA",
            risk_reward=position["risk_reward"]
        )
        trades.append(trade)
    
    # Calcula resultados finales
    results = _calculate_results(
        initial_capital, capital, trades, equity_curve
    )
    
    return results


def _check_exit_conditions(current_bar: pd.Series, position: Dict,
                          current_time: pd.Timestamp) -> tuple:
    """
    Verifica si se deben cumplir las condiciones de salida (SL o TPs).
    
    Args:
        current_bar: Vela actual
        position: Posición abierta
        current_time: Tiempo actual
    
    Returns:
        Tupla (exit_reason, exit_price) o (None, None) si no hay salida
    """
    high = current_bar['high']
    low = current_bar['low']
    close = current_bar['close']
    
    if position["direction"] == "BUY":
        # Verifica Stop Loss
        if low <= position["stop_loss"]:
            return ("STOP_LOSS", position["stop_loss"])
        
        # Verifica Take Profits (en orden de prioridad)
        if high >= position["take_profit_final"]:
            return ("TAKE_PROFIT_FINAL", position["take_profit_final"])
        elif high >= position["take_profit_2"]:
            return ("TAKE_PROFIT_2", position["take_profit_2"])
        elif high >= position["take_profit_1"]:
            return ("TAKE_PROFIT_1", position["take_profit_1"])
    
    else:  # SELL
        # Verifica Stop Loss
        if high >= position["stop_loss"]:
            return ("STOP_LOSS", position["stop_loss"])
        
        # Verifica Take Profits
        if low <= position["take_profit_final"]:
            return ("TAKE_PROFIT_FINAL", position["take_profit_final"])
        elif low <= position["take_profit_2"]:
            return ("TAKE_PROFIT_2", position["take_profit_2"])
        elif low <= position["take_profit_1"]:
            return ("TAKE_PROFIT_1", position["take_profit_1"])
    
    return (None, None)


def _calculate_pnl(position: Dict, exit_price: float, commission: float) -> tuple:
    """
    Calcula el P&L (profit and loss) de una operación.
    
    Args:
        position: Posición cerrada
        exit_price: Precio de salida
        commission: Comisión
    
    Returns:
        Tupla (pnl, pnl_pct)
    """
    entry_price = position["entry_price"]
    size = position["size"]
    
    # Calcula costos y ganancias
    entry_cost = size * entry_price * (1 + commission)
    exit_proceeds = size * exit_price * (1 - commission)
    
    if position["direction"] == "BUY":
        pnl = exit_proceeds - entry_cost
    else:  # SELL
        pnl = entry_cost - exit_proceeds
    
    pnl_pct = ((exit_price - entry_price) / entry_price) * 100
    if position["direction"] == "SELL":
        pnl_pct = -pnl_pct
    
    return (pnl, pnl_pct)


def _calculate_results(initial_capital: float, final_capital: float,
                      trades: List[Trade], equity_curve: List[Dict]) -> BacktestResult:
    """
    Calcula todas las métricas finales del backtest.
    
    Args:
        initial_capital: Capital inicial
        final_capital: Capital final
        trades: Lista de todas las operaciones
        equity_curve: Evolución del capital
    
    Returns:
        BacktestResult con todas las métricas
    """
    if not trades:
        return BacktestResult(
            initial_capital=initial_capital,
            final_capital=final_capital,
            total_return_pct=0,
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            winrate=0,
            profit_factor=0,
            max_drawdown=0,
            avg_rr=0,
            total_pnl=0,
            trades=[],
            equity_curve=equity_curve
        )
    
    # Métricas básicas
    total_trades = len(trades)
    winning_trades = len([t for t in trades if t.pnl > 0])
    losing_trades = len([t for t in trades if t.pnl < 0])
    winrate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    # P&L
    total_pnl = sum(t.pnl for t in trades)
    total_return = ((final_capital - initial_capital) / initial_capital) * 100
    
    # Profit Factor
    total_wins = sum(t.pnl for t in trades if t.pnl > 0)
    total_losses = abs(sum(t.pnl for t in trades if t.pnl < 0))
    profit_factor = total_wins / total_losses if total_losses > 0 else 0
    
    # Risk:Reward promedio
    avg_rr = np.mean([t.risk_reward for t in trades if t.risk_reward > 0])
    
    # Drawdown máximo
    equity_series = pd.Series([e["equity"] for e in equity_curve])
    running_max = equity_series.expanding().max()
    drawdown = (equity_series - running_max) / running_max * 100
    max_drawdown = abs(drawdown.min())
    
    return BacktestResult(
        initial_capital=initial_capital,
        final_capital=final_capital,
        total_return_pct=total_return,
        total_trades=total_trades,
        winning_trades=winning_trades,
        losing_trades=losing_trades,
        winrate=winrate,
        profit_factor=profit_factor,
        max_drawdown=max_drawdown,
        avg_rr=avg_rr,
        total_pnl=total_pnl,
        trades=trades,
        equity_curve=equity_curve
    )


def print_backtest_summary(results: BacktestResult):
    """
    Imprime un resumen completo de los resultados del backtest.
    
    Esta función muestra todas las métricas importantes de forma clara
    para que puedas evaluar el rendimiento de tu estrategia.
    """
    print("\n" + "=" * 70)
    print("RESUMEN DEL BACKTEST")
    print("=" * 70)
    
    print(f"\n💰 CAPITAL:")
    print(f"   Inicial: ${results.initial_capital:,.2f}")
    print(f"   Final: ${results.final_capital:,.2f}")
    print(f"   Retorno: {results.total_return_pct:+.2f}%")
    print(f"   P&L Total: ${results.total_pnl:+,.2f}")
    
    print(f"\n📊 OPERACIONES:")
    print(f"   Total: {results.total_trades}")
    print(f"   Ganadoras: {results.winning_trades}")
    print(f"   Perdedoras: {results.losing_trades}")
    print(f"   Winrate: {results.winrate:.2f}%")
    
    print(f"\n📈 MÉTRICAS:")
    print(f"   Profit Factor: {results.profit_factor:.2f}")
    print(f"   Max Drawdown: {results.max_drawdown:.2f}%")
    print(f"   Risk:Reward Promedio: 1:{results.avg_rr:.2f}")
    
    if results.trades:
        avg_win = np.mean([t.pnl for t in results.trades if t.pnl > 0])
        avg_loss = np.mean([t.pnl for t in results.trades if t.pnl < 0])
        print(f"   Ganancia Promedio: ${avg_win:,.2f}")
        print(f"   Pérdida Promedio: ${avg_loss:,.2f}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Ejecuta el backtest completo
    print("🚀 Iniciando Backtest de Estrategia ICT")
    
    # 1. Carga datos multi-temporales
    data_dict = load_multi_timeframe_data("XAUUSD")
    
    if not data_dict:
        print("❌ No se pudieron cargar los datos. Verifica que los archivos CSV estén en data/")
        exit(1)
    
    # 2. Sincroniza timeframes
    synchronized_data = synchronize_timeframes(data_dict, base_timeframe="M1")
    
    if not synchronized_data:
        print("❌ Error al sincronizar timeframes")
        exit(1)
    
    # 3. Ejecuta backtest
    results = run_backtest(
        synchronized_data,
        initial_capital=10000,
        risk_per_trade=0.01,  # 1% de riesgo por operación
        commission=0.0001  # 0.01% de comisión
    )
    
    if results:
        # 4. Muestra resumen
        print_backtest_summary(results)
    else:
        print("❌ Error al ejecutar el backtest")













