"""
utils/daily_pivots.py - Módulo de Pivots Diarios (Fibonacci)

Calcula y gestiona pivots diarios usando High/Low/Close del día anterior.
Los pivots se actualizan una vez por día al cambio de día UTC.
"""

from datetime import datetime, date, timedelta, UTC
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

try:
    from utils.logger import logger
except ImportError:
    logger = None

try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None


@dataclass
class DailyPivots:
    """Estructura de pivots diarios"""
    date: date
    symbol: str
    pivot: float          # Pivot Point (PP)
    r1: float            # Resistance 1
    r2: float            # Resistance 2
    r3: float            # Resistance 3
    s1: float            # Support 1
    s2: float            # Support 2
    s3: float            # Support 3
    high: float          # High del día anterior
    low: float           # Low del día anterior
    close: float         # Close del día anterior
    calculated_at: datetime


class DailyPivotsManager:
    """
    Gestiona pivots diarios:
    - Calcula pivots usando High/Low/Close del día anterior
    - Guarda en memoria y base de datos
    - Actualiza una vez por día (al cambio de día UTC)
    """
    
    def __init__(self, db=None):
        """
        Inicializa el gestor de pivots.
        
        Args:
            db: Instancia de TradingDatabase (opcional)
        """
        self.db = db
        self.pivots_cache: Dict[str, DailyPivots] = {}  # symbol -> DailyPivots
        self.last_update_date: Optional[date] = None
    
    def calculate_pivots(self, high: float, low: float, close: float) -> Dict[str, float]:
        """
        Calcula pivots usando la fórmula estándar de Fibonacci.
        
        Fórmulas:
        - Pivot Point (PP) = (High + Low + Close) / 3
        - R1 = 2 * PP - Low
        - R2 = PP + (High - Low)
        - R3 = High + 2 * (PP - Low)
        - S1 = 2 * PP - High
        - S2 = PP - (High - Low)
        - S3 = Low - 2 * (High - PP)
        
        Args:
            high: High del día anterior
            low: Low del día anterior
            close: Close del día anterior
        
        Returns:
            Diccionario con todos los niveles de pivot
        """
        pivot = (high + low + close) / 3
        
        r1 = 2 * pivot - low
        r2 = pivot + (high - low)
        r3 = high + 2 * (pivot - low)
        
        s1 = 2 * pivot - high
        s2 = pivot - (high - low)
        s3 = low - 2 * (high - pivot)
        
        return {
            'pivot': pivot,
            'r1': r1,
            'r2': r2,
            'r3': r3,
            's1': s1,
            's2': s2,
            's3': s3
        }
    
    def get_previous_day_data(self, symbol: str) -> Optional[Tuple[float, float, float]]:
        """
        Obtiene High/Low/Close del día anterior desde MT5.
        
        Args:
            symbol: Símbolo a operar
        
        Returns:
            Tupla (high, low, close) o None si hay error
        """
        if mt5 is None:
            if logger:
                logger.warning("MetaTrader5 no está disponible")
            return None
        
        try:
            # Obtiene datos del día anterior (D1)
            today_utc = datetime.now(UTC).date()
            yesterday_utc = today_utc - timedelta(days=1)
            
            # Obtiene velas diarias (D1)
            rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_D1, yesterday_utc, 1)
            
            if rates is None or len(rates) == 0:
                if logger:
                    logger.warning(f"No se pudieron obtener datos D1 para {symbol} del día {yesterday_utc}")
                return None
            
            # Toma la última vela (debería ser la del día anterior)
            last_candle = rates[-1]
            
            high = float(last_candle['high'])
            low = float(last_candle['low'])
            close = float(last_candle['close'])
            
            return (high, low, close)
        
        except Exception as e:
            if logger:
                logger.error(f"Error al obtener datos del día anterior para {symbol}: {e}")
            return None
    
    def update_pivots(self, symbol: str, force_update: bool = False) -> Optional[DailyPivots]:
        """
        Actualiza pivots para un símbolo.
        Solo actualiza si cambió el día UTC o si se fuerza.
        
        Args:
            symbol: Símbolo a operar
            force_update: Si True, fuerza actualización aunque no haya cambiado el día
        
        Returns:
            DailyPivots actualizado o None si hay error
        """
        today_utc = datetime.utcnow().date()
        
        # Verifica si necesita actualizar
        if not force_update:
            # Si ya hay pivots en cache y es el mismo día, no actualiza
            if symbol in self.pivots_cache:
                cached_pivots = self.pivots_cache[symbol]
                if cached_pivots.date == today_utc:
                    if logger:
                        logger.debug(f"Pivots para {symbol} ya están actualizados para hoy")
                    return cached_pivots
            
            # Si el día no cambió desde la última actualización, no actualiza
            if self.last_update_date == today_utc:
                if symbol in self.pivots_cache:
                    return self.pivots_cache[symbol]
        
        # Obtiene datos del día anterior
        day_data = self.get_previous_day_data(symbol)
        if day_data is None:
            return None
        
        high, low, close = day_data
        
        # Calcula pivots
        pivots = self.calculate_pivots(high, low, close)
        
        # Crea objeto DailyPivots
        daily_pivots = DailyPivots(
            date=today_utc,
            symbol=symbol,
            pivot=pivots['pivot'],
            r1=pivots['r1'],
            r2=pivots['r2'],
            r3=pivots['r3'],
            s1=pivots['s1'],
            s2=pivots['s2'],
            s3=pivots['s3'],
            high=high,
            low=low,
            close=close,
            calculated_at=datetime.now(UTC)
        )
        
        # Guarda en cache
        self.pivots_cache[symbol] = daily_pivots
        self.last_update_date = today_utc
        
        # Guarda en base de datos
        if self.db:
            try:
                self.db.save_daily_pivots(daily_pivots)
            except Exception as e:
                if logger:
                    logger.warning(f"Error al guardar pivots en BD: {e}")
        
        if logger:
            logger.info(f"✅ Pivots actualizados para {symbol} - PP: {pivots['pivot']:.2f}, R1: {pivots['r1']:.2f}, S1: {pivots['s1']:.2f}")
        
        return daily_pivots
    
    def get_pivots(self, symbol: str) -> Optional[DailyPivots]:
        """
        Obtiene pivots actuales para un símbolo.
        Si no están en cache o están desactualizados, los calcula.
        
        Args:
            symbol: Símbolo a operar
        
        Returns:
            DailyPivots o None si hay error
        """
        # Intenta obtener de cache primero
        if symbol in self.pivots_cache:
            cached = self.pivots_cache[symbol]
            today_utc = datetime.utcnow().date()
            
            # Si son de hoy, devuelve cache
            if cached.date == today_utc:
                return cached
        
        # Si no hay en cache o están desactualizados, actualiza
        return self.update_pivots(symbol)
    
    def check_price_near_level(self, price: float, level: float, tolerance_pct: float = 0.1) -> bool:
        """
        Verifica si el precio está cerca de un nivel de pivot.
        
        Args:
            price: Precio actual
            level: Nivel de pivot a verificar
            tolerance_pct: Porcentaje de tolerancia (default: 0.1%)
        
        Returns:
            True si el precio está dentro de la tolerancia
        """
        if level == 0:
            return False
        
        distance_pct = abs((price - level) / level) * 100
        return distance_pct <= tolerance_pct
    
    def get_nearest_level(self, price: float, pivots: DailyPivots) -> Tuple[Optional[str], Optional[float], float]:
        """
        Obtiene el nivel de pivot más cercano al precio.
        
        Args:
            price: Precio actual
            pivots: Objeto DailyPivots
        
        Returns:
            Tupla (tipo_nivel, precio_nivel, distancia_pct)
            tipo_nivel: 'R3', 'R2', 'R1', 'PP', 'S1', 'S2', 'S3' o None
        """
        levels = {
            'R3': pivots.r3,
            'R2': pivots.r2,
            'R1': pivots.r1,
            'PP': pivots.pivot,
            'S1': pivots.s1,
            'S2': pivots.s2,
            'S3': pivots.s3
        }
        
        nearest_level = None
        nearest_price = None
        min_distance = float('inf')
        
        for level_name, level_price in levels.items():
            if level_price > 0:
                distance = abs(price - level_price)
                if distance < min_distance:
                    min_distance = distance
                    nearest_level = level_name
                    nearest_price = level_price
        
        if nearest_price:
            distance_pct = (min_distance / nearest_price) * 100
            return (nearest_level, nearest_price, distance_pct)
        
        return (None, None, float('inf'))
    
    def check_pivot_confluence(self, price: float, direction: str, pivots: DailyPivots, 
                              tolerance_pct: float = 0.15) -> Tuple[bool, Optional[str], float]:
        """
        Verifica confluencia con pivots.
        
        Para BUY: precio cerca de S-levels (S1, S2, S3)
        Para SELL: precio cerca de R-levels (R1, R2, R3)
        
        Args:
            price: Precio actual
            direction: 'BUY' o 'SELL'
            pivots: Objeto DailyPivots
            tolerance_pct: Porcentaje de tolerancia (default: 0.15%)
        
        Returns:
            Tupla (hay_confluencia, nivel, distancia_pct)
        """
        if direction == 'BUY':
            # Para BUY, busca cerca de Support levels
            support_levels = {
                'S1': pivots.s1,
                'S2': pivots.s2,
                'S3': pivots.s3
            }
            
            for level_name, level_price in support_levels.items():
                if self.check_price_near_level(price, level_price, tolerance_pct):
                    distance_pct = abs((price - level_price) / level_price) * 100
                    return (True, level_name, distance_pct)
        
        elif direction == 'SELL':
            # Para SELL, busca cerca de Resistance levels
            resistance_levels = {
                'R1': pivots.r1,
                'R2': pivots.r2,
                'R3': pivots.r3
            }
            
            for level_name, level_price in resistance_levels.items():
                if self.check_price_near_level(price, level_price, tolerance_pct):
                    distance_pct = abs((price - level_price) / level_price) * 100
                    return (True, level_name, distance_pct)
        
        return (False, None, float('inf'))

