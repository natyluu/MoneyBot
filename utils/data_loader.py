"""
utils/data_loader.py - Cargador de datos históricos

Este módulo se encarga de cargar los datos históricos de precios (OHLCV).
Puedes obtenerlos de APIs gratuitas como Binance, Alpha Vantage, o archivos CSV.
"""

import pandas as pd
import os
from config import DATA_DIR, SYMBOL, TIMEFRAME


def load_historical_data(symbol=None, timeframe=None, start_date=None, end_date=None):
    """
    Carga datos históricos desde un archivo CSV o una API.
    
    Args:
        symbol: Par de trading (ej: "BTCUSDT")
        timeframe: Marco temporal (ej: "1h")
        start_date: Fecha de inicio (formato: "YYYY-MM-DD")
        end_date: Fecha de fin (formato: "YYYY-MM-DD")
    
    Returns:
        DataFrame de pandas con columnas: timestamp, open, high, low, close, volume
    """
    # Si no se pasan parámetros, usa los de config.py
    symbol = symbol or SYMBOL
    timeframe = timeframe or TIMEFRAME
    
    # Ruta del archivo CSV (si tienes datos guardados)
    csv_path = os.path.join(DATA_DIR, f"{symbol}_{timeframe}.csv")
    
    # Si el archivo existe, lo carga
    if os.path.exists(csv_path):
        print(f"Cargando datos desde {csv_path}")
        df = pd.read_csv(csv_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    
    # Si no existe, aquí podrías llamar a una API para descargar datos
    # Ejemplo con Binance (necesitarías instalar python-binance):
    # from binance.client import Client
    # client = Client()
    # klines = client.get_historical_klines(symbol, timeframe, start_date)
    # ... procesar klines a DataFrame ...
    
    print(f"Archivo no encontrado: {csv_path}")
    print("Nota: Necesitas descargar datos históricos primero")
    return pd.DataFrame()  # Retorna DataFrame vacío si no hay datos


def save_historical_data(df, symbol, timeframe):
    """
    Guarda datos históricos en un archivo CSV para uso futuro.
    
    Args:
        df: DataFrame con los datos OHLCV
        symbol: Par de trading
        timeframe: Marco temporal
    """
    # Crea la carpeta data si no existe
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Guarda el DataFrame en CSV
    csv_path = os.path.join(DATA_DIR, f"{symbol}_{timeframe}.csv")
    df.to_csv(csv_path)
    print(f"Datos guardados en {csv_path}")













