"""
utils/indicators.py - Indicadores técnicos

Este módulo contiene funciones para calcular indicadores técnicos comunes
como medias móviles, RSI, MACD, etc. Estos indicadores ayudan a tomar decisiones de trading.
"""

import pandas as pd
import numpy as np


def calculate_sma(prices, period):
    """
    Calcula la Media Móvil Simple (SMA).
    
    La SMA es el promedio de los últimos N precios de cierre.
    Si la SMA corta hacia arriba, puede indicar tendencia alcista.
    
    Args:
        prices: Serie de precios (normalmente 'close')
        period: Período de la media móvil (ej: 10, 20, 50)
    
    Returns:
        Serie con los valores de la SMA
    """
    return prices.rolling(window=period).mean()


def calculate_ema(prices, period):
    """
    Calcula la Media Móvil Exponencial (EMA).
    
    La EMA da más peso a los precios recientes que la SMA.
    Es más sensible a cambios de precio.
    
    Args:
        prices: Serie de precios
        period: Período de la EMA
    
    Returns:
        Serie con los valores de la EMA
    """
    return prices.ewm(span=period, adjust=False).mean()


def calculate_rsi(prices, period=14):
    """
    Calcula el Índice de Fuerza Relativa (RSI).
    
    El RSI mide la fuerza de los movimientos de precio.
    Valores > 70: posible sobrecompra (considera vender)
    Valores < 30: posible sobreventa (considera comprar)
    
    Args:
        prices: Serie de precios
        period: Período para el cálculo (default: 14)
    
    Returns:
        Serie con los valores del RSI (0-100)
    """
    delta = prices.diff()  # Diferencia entre precio actual y anterior
    
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(prices, fast=12, slow=26, signal=9):
    """
    Calcula el MACD (Moving Average Convergence Divergence).
    
    El MACD muestra la relación entre dos medias móviles.
    Cuando la línea MACD cruza la línea de señal hacia arriba: señal de compra
    Cuando cruza hacia abajo: señal de venta
    
    Args:
        prices: Serie de precios
        fast: Período de la EMA rápida (default: 12)
        slow: Período de la EMA lenta (default: 26)
        signal: Período de la línea de señal (default: 9)
    
    Returns:
        Tupla con (macd_line, signal_line, histogram)
    """
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def calculate_atr(high, low, close, period=14):
    """
    Calcula el Average True Range (ATR).
    
    El ATR mide la volatilidad del mercado.
    Valores altos indican alta volatilidad.
    
    Args:
        high: Serie de precios máximos
        low: Serie de precios mínimos
        close: Serie de precios de cierre
        period: Período para el cálculo (default: 14)
    
    Returns:
        Serie con los valores del ATR
    """
    # True Range = max(high - low, abs(high - close_prev), abs(low - close_prev))
    high_low = high - low
    high_close = abs(high - close.shift())
    low_close = abs(low - close.shift())
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    
    # ATR es la media móvil del True Range
    atr = true_range.rolling(window=period).mean()
    
    return atr


def calculate_atr_ratio(current_atr: float, average_atr: float) -> float:
    """
    Calcula la relación entre ATR actual y ATR promedio.
    
    Args:
        current_atr: ATR actual
        average_atr: ATR promedio (de un período más largo)
    
    Returns:
        Ratio (ej: 1.5 significa que el ATR actual es 1.5x el promedio)
    """
    if average_atr == 0:
        return 0.0
    return current_atr / average_atr













