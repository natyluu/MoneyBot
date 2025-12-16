"""
backtest/run_backtest.py - Script principal para ejecutar backtests

Este es el archivo que ejecutas para probar tu estrategia con datos históricos.
"""

from utils.data_loader import load_historical_data
from strategy.moving_average_strategy import MovingAverageStrategy
from backtest.backtest_engine import BacktestEngine
from config import START_DATE, END_DATE


def main():
    """
    Función principal que ejecuta el backtest completo.
    """
    print("=" * 60)
    print("INICIANDO BACKTEST")
    print("=" * 60)
    
    # 1. Carga los datos históricos
    print("\n1. Cargando datos históricos...")
    data = load_historical_data()
    
    if data.empty:
        print("ERROR: No se encontraron datos. Asegúrate de tener datos históricos.")
        return
    
    print(f"Datos cargados: {len(data)} velas")
    print(f"Período: {data.index[0]} a {data.index[-1]}")
    
    # 2. Crea una instancia de tu estrategia
    print("\n2. Inicializando estrategia...")
    strategy = MovingAverageStrategy()
    print(f"Estrategia: {strategy.name}")
    print(f"Parámetros: SMA rápida={strategy.fast_period}, SMA lenta={strategy.slow_period}")
    
    # 3. Crea el motor de backtesting
    print("\n3. Inicializando motor de backtesting...")
    engine = BacktestEngine()
    
    # 4. Ejecuta el backtest
    print("\n4. Ejecutando backtest...")
    print("-" * 60)
    results = engine.run(data, strategy)
    
    # 5. Muestra los resultados
    print("\n" + "=" * 60)
    print("RESULTADOS DEL BACKTEST")
    print("=" * 60)
    
    if 'error' in results:
        print(f"Error: {results['error']}")
        return
    
    print(f"\nCapital inicial: ${results['initial_capital']:,.2f}")
    print(f"Capital final: ${results['final_capital']:,.2f}")
    print(f"Retorno total: {results['total_return_pct']:.2f}%")
    print(f"P&L total: ${results['total_pnl']:,.2f}")
    print(f"\nTotal de operaciones: {results['total_trades']}")
    print(f"Operaciones ganadoras: {results['winning_trades']}")
    print(f"Operaciones perdedoras: {results['losing_trades']}")
    print(f"Tasa de acierto: {results['win_rate_pct']:.2f}%")
    print(f"\nGanancia promedio: ${results['avg_win']:,.2f}")
    print(f"Pérdida promedio: ${results['avg_loss']:,.2f}")
    print(f"Profit Factor: {results['profit_factor']:.2f}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()













