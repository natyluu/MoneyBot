"""
backtest/run_ict_backtest.py - Script para ejecutar backtests de la estrategia ICT

Este script ejecuta backtests completos de la estrategia ICT Híbrida con análisis multi-temporal.
"""

import pandas as pd
from strategy.ict_hybrid_strategy import ICTHybridStrategy
from backtest.ict_backtest_engine import ICTBacktestEngine
from utils.multi_timeframe_loader import (
    load_multi_timeframe_data,
    resample_to_timeframes,
    align_timeframes,
    validate_multi_timeframe_data
)
from config import START_DATE, END_DATE, INITIAL_CAPITAL, COMMISSION


def run_ict_backtest(symbol: str = "XAUUSD", start_date: str = None, end_date: str = None,
                    initial_capital: float = None, commission: float = None,
                    use_resampling: bool = False):
    """
    Ejecuta un backtest completo de la estrategia ICT.
    
    Args:
        symbol: Par de trading (default: "XAUUSD")
        start_date: Fecha de inicio (formato: "YYYY-MM-DD")
        end_date: Fecha de fin (formato: "YYYY-MM-DD")
        initial_capital: Capital inicial
        commission: Comisión por operación
        use_resampling: Si True, re-muestrea desde un timeframe base si faltan datos
    """
    print("=" * 70)
    print("BACKTEST: ESTRATEGIA ICT HÍBRIDA 2022")
    print("=" * 70)
    print(f"Símbolo: {symbol}")
    print(f"Período: {start_date or START_DATE} a {end_date or END_DATE}")
    print()
    
    # 1. Carga datos multi-temporales
    print("📊 Cargando datos multi-temporales...")
    print("-" * 70)
    
    data_dict = load_multi_timeframe_data(symbol, start_date, end_date)
    
    # Si faltan datos y se permite re-muestreo, intenta re-muestrear
    if use_resampling and len(data_dict) < 5:
        print("\n⚠️ Faltan datos. Intentando re-muestreo desde timeframe base...")
        # Intenta cargar cualquier timeframe disponible
        base_timeframes = ['1h', '15m', '5m', '1m']
        base_data = None
        
        for tf in base_timeframes:
            from utils.data_loader import load_historical_data
            base_data = load_historical_data(symbol, tf, start_date, end_date)
            if not base_data.empty:
                print(f"✓ Usando {tf} como base para re-muestreo")
                break
        
        if base_data is not None and not base_data.empty:
            resampled = resample_to_timeframes(base_data, base_timeframes[0])
            # Combina con datos existentes
            for key, df in resampled.items():
                if key not in data_dict:
                    data_dict[key] = df
        else:
            print("❌ No se encontraron datos base para re-muestreo")
            return None
    
    # Valida datos
    if not validate_multi_timeframe_data(data_dict):
        print("⚠️ Advertencia: Algunos timeframes faltan, pero continuando...")
    
    if not data_dict:
        print("❌ No hay datos disponibles para el backtest")
        return None
    
    # Alinea timeframes
    data_dict = align_timeframes(data_dict, 'M1' if 'M1' in data_dict else 'M3' if 'M3' in data_dict else 'M5')
    
    print(f"\n✓ Datos cargados para {len(data_dict)} timeframes")
    for key, df in data_dict.items():
        print(f"   {key}: {len(df)} velas ({df.index[0]} a {df.index[-1]})")
    
    # 2. Inicializa estrategia
    print("\n📈 Inicializando estrategia ICT...")
    strategy = ICTHybridStrategy()
    
    # 3. Inicializa motor de backtesting
    print("\n⚙️ Inicializando motor de backtesting...")
    engine = ICTBacktestEngine(
        initial_capital=initial_capital or INITIAL_CAPITAL,
        commission=commission or COMMISSION,
        slippage=0.0001,  # 0.01% de slippage
        position_size_pct=0.1  # 10% del capital por operación
    )
    
    # 4. Ejecuta backtest
    print("\n🚀 Ejecutando backtest...")
    print("-" * 70)
    
    results = engine.run(
        data_dict=data_dict,
        strategy=strategy,
        start_date=start_date or START_DATE,
        end_date=end_date or END_DATE
    )
    
    # 5. Muestra resultados
    print("\n" + "=" * 70)
    print("RESULTADOS DEL BACKTEST")
    print("=" * 70)
    
    print(f"\n💰 Capital:")
    print(f"   Inicial: ${results.initial_capital:,.2f}")
    print(f"   Final: ${results.final_capital:,.2f}")
    print(f"   Retorno: {results.total_return_pct:+.2f}%")
    print(f"   P&L Total: ${results.total_pnl:+,.2f}")
    
    print(f"\n📊 Operaciones:")
    print(f"   Total: {results.total_trades}")
    print(f"   Ganadoras: {results.winning_trades}")
    print(f"   Perdedoras: {results.losing_trades}")
    print(f"   Tasa de acierto: {results.win_rate_pct:.2f}%")
    
    print(f"\n📈 Métricas:")
    print(f"   Ganancia promedio: ${results.avg_win:,.2f}")
    print(f"   Pérdida promedio: ${results.avg_loss:,.2f}")
    print(f"   Profit Factor: {results.profit_factor:.2f}")
    print(f"   Sharpe Ratio: {results.sharpe_ratio:.2f}")
    print(f"   Max Drawdown: {results.max_drawdown_pct:.2f}%")
    print(f"   Duración Max DD: {results.max_drawdown_duration} velas")
    
    print(f"\n🎯 Señales:")
    print(f"   Generadas: {results.signals_generated}")
    print(f"   Ejecutadas: {results.signals_executed}")
    if results.signals_generated > 0:
        execution_rate = (results.signals_executed / results.signals_generated) * 100
        print(f"   Tasa de ejecución: {execution_rate:.1f}%")
    
    # Muestra detalles de las primeras y últimas operaciones
    if results.trades:
        print(f"\n📋 Primeras 3 operaciones:")
        for i, trade in enumerate(results.trades[:3], 1):
            print(f"\n   Operación {i}:")
            print(f"      {trade.direction} - {trade.entry_time}")
            print(f"      Entrada: ${trade.entry_price:.2f} → Salida: ${trade.exit_price:.2f}")
            print(f"      P&L: ${trade.pnl:+.2f} ({trade.pnl_pct:+.2f}%)")
            print(f"      Razón: {trade.exit_reason}")
        
        if len(results.trades) > 3:
            print(f"\n📋 Últimas 3 operaciones:")
            for i, trade in enumerate(results.trades[-3:], len(results.trades)-2):
                print(f"\n   Operación {i}:")
                print(f"      {trade.direction} - {trade.entry_time}")
                print(f"      Entrada: ${trade.entry_price:.2f} → Salida: ${trade.exit_price:.2f}")
                print(f"      P&L: ${trade.pnl:+.2f} ({trade.pnl_pct:+.2f}%)")
                print(f"      Razón: {trade.exit_reason}")
    
    print("\n" + "=" * 70)
    
    return results


if __name__ == "__main__":
    # Ejecuta backtest con parámetros por defecto
    results = run_ict_backtest(
        symbol="XAUUSD",
        start_date="2023-01-01",
        end_date="2024-01-01",
        use_resampling=True  # Permite re-muestreo si faltan datos
    )
    
    if results:
        print("\n✅ Backtest completado exitosamente")
    else:
        print("\n❌ Backtest falló. Verifica los datos disponibles.")













