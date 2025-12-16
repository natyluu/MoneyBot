"""
utils/generate_sample_data.py - Genera datos de ejemplo para backtesting

Este script genera datos históricos sintéticos de XAUUSD para que puedas
probar el backtesting inmediatamente sin tener que descargar datos reales.

NOTA: Estos son datos sintéticos (simulados). Para resultados reales,
necesitas datos históricos reales del mercado.
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime, timedelta

# Agrega el directorio raíz al path para importar config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR

def generate_sample_data(symbol="XAUUSD", days=365):
    """
    Genera datos históricos sintéticos de XAUUSD.
    
    Args:
        symbol: Símbolo a generar (default: XAUUSD)
        days: Número de días de datos a generar (default: 365 = 1 año)
    """
    print(f"📊 Generando datos sintéticos de {symbol} para {days} días...")
    print("⚠️ NOTA: Estos son datos simulados. Para resultados reales, usa datos históricos reales.\n")
    
    # Crea la carpeta data si no existe
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Precio base de XAUUSD (ejemplo: alrededor de $2000)
    base_price = 2000.0
    
    # Timeframes a generar
    timeframes = {
        "1d": {"period": "1D", "name": "D1"},
        "4h": {"period": "4H", "name": "H4"},
        "1h": {"period": "1H", "name": "H1"},
        "15m": {"period": "15T", "name": "M15"},
        "5m": {"period": "5T", "name": "M5"},
        "3m": {"period": "3T", "name": "M3"},
        "1m": {"period": "1T", "name": "M1"}
    }
    
    # Fecha de inicio (hace N días)
    start_date = datetime.now() - timedelta(days=days)
    
    generated_files = []
    
    for tf_file, tf_info in timeframes.items():
        print(f"   Generando {tf_info['name']} ({tf_file})...", end=" ")
        
        # Crea rango de fechas según el timeframe
        if tf_file == "1d":
            date_range = pd.date_range(start=start_date, end=datetime.now(), freq=tf_info['period'])
        elif tf_file == "4h":
            date_range = pd.date_range(start=start_date, end=datetime.now(), freq=tf_info['period'])
        elif tf_file == "1h":
            date_range = pd.date_range(start=start_date, end=datetime.now(), freq=tf_info['period'])
        else:
            # Para timeframes menores, genera datos de los últimos 30 días
            recent_start = datetime.now() - timedelta(days=30)
            date_range = pd.date_range(start=recent_start, end=datetime.now(), freq=tf_info['period'])
        
        # Genera datos sintéticos con movimiento de precio realista
        n = len(date_range)
        
        # Genera retornos aleatorios con tendencia
        np.random.seed(42)  # Para reproducibilidad
        returns = np.random.normal(0.0001, 0.01, n)  # Pequeña tendencia alcista
        
        # Crea serie de precios
        prices = [base_price]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        # Genera OHLCV
        data = []
        for i, (timestamp, price) in enumerate(zip(date_range, prices)):
            # Volatilidad aleatoria
            volatility = np.random.uniform(0.001, 0.005)
            
            # Genera OHLC
            high = price * (1 + volatility * np.random.uniform(0.3, 1.0))
            low = price * (1 - volatility * np.random.uniform(0.3, 1.0))
            open_price = prices[i-1] if i > 0 else price
            close_price = price
            
            # Asegura que high >= max(open, close) y low <= min(open, close)
            high = max(high, open_price, close_price)
            low = min(low, open_price, close_price)
            
            # Volumen aleatorio
            volume = np.random.uniform(100, 10000)
            
            data.append({
                'timestamp': timestamp,
                'open': open_price,
                'high': high,
                'low': low,
                'close': close_price,
                'volume': volume
            })
        
        # Crea DataFrame
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        
        # Guarda en CSV
        csv_path = os.path.join(DATA_DIR, f"{symbol}_{tf_file}.csv")
        df.to_csv(csv_path)
        
        generated_files.append(csv_path)
        print(f"✅ {len(df)} velas")
    
    print(f"\n✅ Datos sintéticos generados en {DATA_DIR}/")
    print(f"   Archivos creados: {len(generated_files)}")
    print("\n⚠️ RECORDATORIO: Estos son datos sintéticos.")
    print("   Para backtesting real, descarga datos históricos reales de:")
    print("   - Binance (gratis)")
    print("   - Alpha Vantage (gratis con límites)")
    print("   - Tu broker directamente")
    
    return generated_files


if __name__ == "__main__":
    # Genera datos de ejemplo
    generate_sample_data(symbol="XAUUSD", days=365)

