"""
strategy/base_strategy.py - Estrategia base de trading

Este archivo define la estructura base de una estrategia de trading.
Todas tus estrategias deben heredar de esta clase base.
"""

from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """
    Clase base abstracta para todas las estrategias de trading.
    
    Una estrategia define CUÁNDO comprar y CUÁNDO vender.
    Esta clase define la estructura que todas las estrategias deben seguir.
    """
    
    def __init__(self, name):
        """
        Inicializa la estrategia.
        
        Args:
            name: Nombre de la estrategia (ej: "MovingAverageCrossover")
        """
        self.name = name
        self.positions = []  # Lista de posiciones abiertas
    
    @abstractmethod
    def generate_signals(self, data):
        """
        Genera señales de trading basadas en los datos históricos.
        
        Esta función debe ser implementada por cada estrategia específica.
        Debe retornar señales: 'BUY', 'SELL', o 'HOLD'
        
        Args:
            data: DataFrame con datos OHLCV e indicadores calculados
        
        Returns:
            DataFrame con una columna 'signal' que contiene las señales
        """
        pass
    
    @abstractmethod
    def should_buy(self, data, current_index):
        """
        Determina si se debe comprar en el índice actual.
        
        Args:
            data: DataFrame con datos e indicadores
            current_index: Índice de la vela actual
        
        Returns:
            True si se debe comprar, False en caso contrario
        """
        pass
    
    @abstractmethod
    def should_sell(self, data, current_index, position):
        """
        Determina si se debe vender una posición existente.
        
        Args:
            data: DataFrame con datos e indicadores
            current_index: Índice de la vela actual
            position: Información de la posición abierta
        
        Returns:
            True si se debe vender, False en caso contrario
        """
        pass













