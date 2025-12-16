"""
strategy/moving_average_strategy.py - Estrategia de cruce de medias móviles

Esta es una estrategia de ejemplo que usa el cruce de dos medias móviles.
Compra cuando la media rápida cruza por encima de la lenta (cruce alcista).
Vende cuando la media rápida cruza por debajo de la lenta (cruce bajista).
"""

import pandas as pd
from strategy.base_strategy import BaseStrategy
from utils.indicators import calculate_sma
from config import FAST_MA_PERIOD, SLOW_MA_PERIOD


class MovingAverageStrategy(BaseStrategy):
    """
    Estrategia de cruce de medias móviles.
    
    Lógica:
    - Compra cuando SMA rápida cruza por encima de SMA lenta
    - Vende cuando SMA rápida cruza por debajo de SMA lenta
    """
    
    def __init__(self, fast_period=None, slow_period=None):
        """
        Inicializa la estrategia con períodos de medias móviles.
        
        Args:
            fast_period: Período de la media móvil rápida
            slow_period: Período de la media móvil lenta
        """
        super().__init__("MovingAverageCrossover")
        self.fast_period = fast_period or FAST_MA_PERIOD
        self.slow_period = slow_period or SLOW_MA_PERIOD
    
    def generate_signals(self, data):
        """
        Genera señales de compra/venta basadas en el cruce de medias móviles.
        
        Args:
            data: DataFrame con datos OHLCV
        
        Returns:
            DataFrame con columna 'signal' añadida
        """
        # Calcula las medias móviles
        data['sma_fast'] = calculate_sma(data['close'], self.fast_period)
        data['sma_slow'] = calculate_sma(data['close'], self.slow_period)
        
        # Inicializa la columna de señales
        data['signal'] = 'HOLD'
        
        # Detecta cruces alcistas (compra)
        # Cruce alcista: SMA rápida cruza por encima de SMA lenta
        data.loc[
            (data['sma_fast'] > data['sma_slow']) & 
            (data['sma_fast'].shift(1) <= data['sma_slow'].shift(1)),
            'signal'
        ] = 'BUY'
        
        # Detecta cruces bajistas (venta)
        # Cruce bajista: SMA rápida cruza por debajo de SMA lenta
        data.loc[
            (data['sma_fast'] < data['sma_slow']) & 
            (data['sma_fast'].shift(1) >= data['sma_slow'].shift(1)),
            'signal'
        ] = 'SELL'
        
        return data
    
    def should_buy(self, data, current_index):
        """
        Verifica si se debe comprar en el índice actual.
        
        Args:
            data: DataFrame con datos e indicadores
            current_index: Índice actual
        
        Returns:
            True si hay señal de compra
        """
        if current_index < 1:
            return False
        
        # Verifica si hay señal de compra en el índice actual
        return data.iloc[current_index]['signal'] == 'BUY'
    
    def should_sell(self, data, current_index, position):
        """
        Verifica si se debe vender la posición actual.
        
        Args:
            data: DataFrame con datos e indicadores
            current_index: Índice actual
            position: Diccionario con información de la posición
        
        Returns:
            True si se debe vender
        """
        if current_index < 1:
            return False
        
        # Verifica si hay señal de venta
        if data.iloc[current_index]['signal'] == 'SELL':
            return True
        
        # También vende si se alcanza stop loss o take profit
        # (esto se maneja mejor en el backtest, pero aquí está como ejemplo)
        current_price = data.iloc[current_index]['close']
        entry_price = position['entry_price']
        
        # Stop loss: vende si el precio bajó más del límite
        if current_price <= entry_price * (1 - position.get('stop_loss', 0)):
            return True
        
        # Take profit: vende si el precio subió más del límite
        if current_price >= entry_price * (1 + position.get('take_profit', 0)):
            return True
        
        return False













