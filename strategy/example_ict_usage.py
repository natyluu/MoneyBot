"""
strategy/example_ict_usage.py - Ejemplo de uso de la estrategia ICT Híbrida

Este script muestra cómo usar la estrategia ICT Híbrida con análisis multi-temporal.
"""

import pandas as pd
from strategy.ict_hybrid_strategy import ICTHybridStrategy
from utils.data_loader import load_historical_data


def example_ict_analysis():
    """
    Ejemplo completo de análisis multi-temporal con la estrategia ICT.
    """
    print("=" * 70)
    print("EJEMPLO DE USO: Estrategia ICT Híbrida 2022")
    print("=" * 70)
    
    # Inicializa la estrategia
    strategy = ICTHybridStrategy()
    
    # NOTA: En un caso real, necesitarías cargar datos de múltiples timeframes
    # Por ahora, usamos el mismo DataFrame para todos (solo como ejemplo)
    
    print("\n📊 Cargando datos históricos...")
    # Carga datos (ajusta según tus datos disponibles)
    # En producción, cargarías datos de D1, H4, H1, M15, M5, M3, M1 por separado
    
    # Ejemplo: cargar datos del timeframe principal
    data = load_historical_data(symbol="XAUUSD", timeframe="1h")
    
    if data.empty:
        print("⚠️ No hay datos disponibles. Asegúrate de tener datos históricos.")
        print("   Para esta estrategia necesitas datos de múltiples timeframes:")
        print("   - D1 (diario)")
        print("   - H4 (4 horas)")
        print("   - H1 (1 hora)")
        print("   - M15 (15 minutos)")
        print("   - M5 (5 minutos)")
        print("   - M3 (3 minutos)")
        print("   - M1 (1 minuto)")
        return
    
    print(f"✓ Datos cargados: {len(data)} velas")
    
    # Para el ejemplo, usamos los mismos datos para todos los timeframes
    # (en producción, cargarías cada timeframe por separado)
    df_D1 = data.resample('D').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()
    
    df_H4 = data.resample('4H').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()
    
    df_H1 = data.resample('1H').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()
    
    df_M15 = data.resample('15T').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()
    
    df_M5 = data.resample('5T').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()
    
    df_M3 = data.resample('3T').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()
    
    df_M1 = data.resample('1T').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()
    
    print("\n" + "=" * 70)
    print("ANÁLISIS MULTI-TEMPORAL")
    print("=" * 70)
    
    # 1. Análisis D1
    print("\n📅 ANÁLISIS D1 (Diario)")
    print("-" * 70)
    d1_results = strategy.analyze_D1(df_D1)
    
    # 2. Análisis H4
    print("\n📅 ANÁLISIS H4 (4 Horas)")
    print("-" * 70)
    h4_results = strategy.analyze_H4(df_H4)
    
    # 3. Análisis H1
    print("\n📅 ANÁLISIS H1 (1 Hora)")
    print("-" * 70)
    h1_results = strategy.analyze_H1(df_H1)
    
    # 4. Análisis M15/M5
    print("\n📅 ANÁLISIS M15/M5 (15 y 5 Minutos)")
    print("-" * 70)
    m15_m5_results = strategy.analyze_M15_M5(df_M15, df_M5)
    
    # 5. Búsqueda de entrada sniper
    print("\n🎯 BÚSQUEDA DE ENTRADA SNIPER (M1/M3)")
    print("-" * 70)
    signal = strategy.find_sniper_entry(df_M1, df_M3, strategy.context)
    
    if signal:
        print("\n" + "=" * 70)
        print("✅ SEÑAL DE TRADING GENERADA")
        print("=" * 70)
        print(f"\nDirección: {signal.direction}")
        print(f"Operación: {signal.operation_type}")
        print(f"\nPrecios:")
        print(f"  Entrada: ${signal.entry_price:.2f}")
        print(f"  Stop Loss: ${signal.stop_loss:.2f}")
        print(f"  Take Profit 1: ${signal.take_profit_1:.2f}")
        print(f"  Take Profit 2: ${signal.take_profit_2:.2f}")
        print(f"  Take Profit Final: ${signal.take_profit_final:.2f}")
        print(f"\nRisk:Reward: 1:{signal.risk_reward:.2f}")
        print(f"\nZonas Institucionales Activas: {len(signal.active_zones)}")
        print(f"\nJustificaciones:")
        for i, justification in enumerate(signal.justifications, 1):
            print(f"  {i}. {justification}")
    else:
        print("\n❌ No se generó señal de trading")
        print("   Las confirmaciones requeridas no se cumplieron.")
    
    print("\n" + "=" * 70)
    print("Análisis completado")
    print("=" * 70)


if __name__ == "__main__":
    example_ict_analysis()













