"""
strategy/ict_utils.py - Utilidades para análisis ICT (Inner Circle Trader)

Este módulo contiene funciones para detectar patrones institucionales ICT:
- Swings (máximos y mínimos)
- BOS (Break of Structure) y CHoCH (Change of Character)
- Liquidity Sweeps (barridas de liquidez)
- Order Blocks (OB)
- Fair Value Gaps (FVG)
- Mitigation Blocks
- Breaker Blocks
- Rejection Blocks
- Liquidity Voids
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple
from enum import Enum


class TrendDirection(Enum):
    """Dirección de la tendencia"""
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


class BlockType(Enum):
    """Tipos de bloques institucionales"""
    ORDER_BLOCK = "ORDER_BLOCK"
    FAIR_VALUE_GAP = "FAIR_VALUE_GAP"
    MITIGATION_BLOCK = "MITIGATION_BLOCK"
    BREAKER_BLOCK = "BREAKER_BLOCK"
    REJECTION_BLOCK = "REJECTION_BLOCK"
    LIQUIDITY_VOID = "LIQUIDITY_VOID"


@dataclass
class SwingPoint:
    """Punto de swing (máximo o mínimo)"""
    index: int
    price: float
    timestamp: pd.Timestamp
    swing_type: str  # 'HIGH' o 'LOW'
    strength: float  # Fuerza del swing (1-5)


@dataclass
class StructureBreak:
    """Ruptura de estructura (BOS o CHoCH)"""
    index: int
    timestamp: pd.Timestamp
    break_type: str  # 'BOS' o 'CHoCH'
    direction: str  # 'BULLISH' o 'BEARISH'
    price: float
    strength: float


@dataclass
class LiquiditySweep:
    """Barrida de liquidez"""
    index: int
    timestamp: pd.Timestamp
    sweep_type: str  # 'HIGH_SWEEP' o 'LOW_SWEEP'
    price: float
    target_price: float  # Precio del swing barrido
    confirmed: bool


@dataclass
class InstitutionalBlock:
    """Bloque institucional (OB, FVG, etc.)"""
    block_type: BlockType
    start_index: int
    end_index: int
    start_price: float
    end_price: float
    timestamp: pd.Timestamp
    direction: str  # 'BULLISH' o 'BEARISH'
    mitigated: bool
    mitigation_index: Optional[int] = None
    strength: float = 1.0  # Fuerza del bloque (1-5)


@dataclass
class InstitutionalZone:
    """Zona institucional activa"""
    zone_type: str
    price_level: float
    origin_timestamp: pd.Timestamp
    origin_timeframe: str
    direction: str
    blocks: List[InstitutionalBlock]
    active: bool


def detect_swings(data: pd.DataFrame, lookback: int = 5) -> Tuple[List[SwingPoint], List[SwingPoint]]:
    """
    Detecta puntos de swing (máximos y mínimos locales).
    
    Un swing high es un máximo local rodeado de velas más bajas.
    Un swing low es un mínimo local rodeado de velas más altas.
    
    Args:
        data: DataFrame con datos OHLCV
        lookback: Número de velas a cada lado para confirmar el swing
    
    Returns:
        Tupla con (lista de swing highs, lista de swing lows)
    """
    highs = []
    lows = []
    
    for i in range(lookback, len(data) - lookback):
        # Detecta swing high
        current_high = data.iloc[i]['high']
        is_swing_high = True
        
        # Verifica que las velas anteriores y posteriores tengan highs menores
        for j in range(i - lookback, i + lookback + 1):
            if j != i and data.iloc[j]['high'] >= current_high:
                is_swing_high = False
                break
        
        if is_swing_high:
            # Calcula fuerza del swing (cuánto más alto es respecto a los alrededores)
            avg_surrounding = (data.iloc[i-lookback:i]['high'].mean() + 
                             data.iloc[i+1:i+lookback+1]['high'].mean()) / 2
            strength = (current_high - avg_surrounding) / avg_surrounding * 100
            
            highs.append(SwingPoint(
                index=i,
                price=current_high,
                timestamp=data.index[i],
                swing_type='HIGH',
                strength=min(strength, 5.0)  # Limita a 5
            ))
        
        # Detecta swing low
        current_low = data.iloc[i]['low']
        is_swing_low = True
        
        # Verifica que las velas anteriores y posteriores tengan lows mayores
        for j in range(i - lookback, i + lookback + 1):
            if j != i and data.iloc[j]['low'] <= current_low:
                is_swing_low = False
                break
        
        if is_swing_low:
            # Calcula fuerza del swing
            avg_surrounding = (data.iloc[i-lookback:i]['low'].mean() + 
                             data.iloc[i+1:i+lookback+1]['low'].mean()) / 2
            strength = (avg_surrounding - current_low) / avg_surrounding * 100
            
            lows.append(SwingPoint(
                index=i,
                price=current_low,
                timestamp=data.index[i],
                swing_type='LOW',
                strength=min(strength, 5.0)
            ))
    
    return highs, lows


def detect_bos_choch(data: pd.DataFrame, swing_highs: List[SwingPoint], 
                     swing_lows: List[SwingPoint]) -> List[StructureBreak]:
    """
    Detecta Break of Structure (BOS) y Change of Character (CHoCH).
    
    BOS: Ruptura de un swing high/low previo (cambio de estructura)
    CHoCH: Cambio en la secuencia de máximos/mínimos (cambio de carácter)
    
    Args:
        data: DataFrame con datos OHLCV
        swing_highs: Lista de swing highs detectados
        swing_lows: Lista de swing lows detectados
    
    Returns:
        Lista de StructureBreak detectados
    """
    breaks = []
    
    # Detecta BOS alcista (ruptura de swing high)
    for i in range(len(data)):
        current_high = data.iloc[i]['high']
        
        # Busca swing highs anteriores que hayan sido rotos
        for swing in swing_highs:
            if swing.index < i and current_high > swing.price:
                # Verifica que no haya sido detectado ya
                already_detected = any(
                    b.index == i and b.break_type == 'BOS' and b.direction == 'BULLISH'
                    for b in breaks
                )
                
                if not already_detected:
                    breaks.append(StructureBreak(
                        index=i,
                        timestamp=data.index[i],
                        break_type='BOS',
                        direction='BULLISH',
                        price=current_high,
                        strength=swing.strength
                    ))
                    break  # Solo el primer swing roto cuenta
    
    # Detecta BOS bajista (ruptura de swing low)
    for i in range(len(data)):
        current_low = data.iloc[i]['low']
        
        for swing in swing_lows:
            if swing.index < i and current_low < swing.price:
                already_detected = any(
                    b.index == i and b.break_type == 'BOS' and b.direction == 'BEARISH'
                    for b in breaks
                )
                
                if not already_detected:
                    breaks.append(StructureBreak(
                        index=i,
                        timestamp=data.index[i],
                        break_type='BOS',
                        direction='BEARISH',
                        price=current_low,
                        strength=swing.strength
                    ))
                    break
    
    # Detecta CHoCH (Change of Character)
    # CHoCH alcista: secuencia de mínimos crecientes después de tendencia bajista
    # CHoCH bajista: secuencia de máximos decrecientes después de tendencia alcista
    
    if len(swing_lows) >= 3:
        # Verifica si hay cambio de carácter alcista
        recent_lows = [s for s in swing_lows if s.index >= len(data) - 50]  # Últimas 50 velas
        if len(recent_lows) >= 2:
            # Si el último mínimo es mayor que el anterior, posible CHoCH alcista
            if recent_lows[-1].price > recent_lows[-2].price:
                breaks.append(StructureBreak(
                    index=recent_lows[-1].index,
                    timestamp=recent_lows[-1].timestamp,
                    break_type='CHoCH',
                    direction='BULLISH',
                    price=recent_lows[-1].price,
                    strength=2.0
                ))
    
    if len(swing_highs) >= 3:
        # Verifica si hay cambio de carácter bajista
        recent_highs = [s for s in swing_highs if s.index >= len(data) - 50]
        if len(recent_highs) >= 2:
            if recent_highs[-1].price < recent_highs[-2].price:
                breaks.append(StructureBreak(
                    index=recent_highs[-1].index,
                    timestamp=recent_highs[-1].timestamp,
                    break_type='CHoCH',
                    direction='BEARISH',
                    price=recent_highs[-1].price,
                    strength=2.0
                ))
    
    return breaks


def detect_liquidity_sweeps(data: pd.DataFrame, swing_highs: List[SwingPoint],
                           swing_lows: List[SwingPoint]) -> List[LiquiditySweep]:
    """
    Detecta barridas de liquidez (liquidity sweeps).
    
    Una barrida de liquidez ocurre cuando el precio rompe un swing high/low
    pero luego revierte rápidamente, "barriendo" las órdenes stop loss.
    
    Args:
        data: DataFrame con datos OHLCV
        swing_highs: Lista de swing highs
        swing_lows: Lista de swing lows
    
    Returns:
        Lista de LiquiditySweep detectados
    """
    sweeps = []
    
    # Detecta barridas de swing highs (high sweeps)
    for swing in swing_highs:
        if swing.index >= len(data) - 20:  # Solo swings recientes
            continue
        
        # Busca si después del swing hubo una ruptura y reversión
        for i in range(swing.index + 1, min(swing.index + 20, len(data))):
            # Si el precio rompió el swing high
            if data.iloc[i]['high'] > swing.price:
                # Verifica si luego revirtió (cierre por debajo del swing)
                if data.iloc[i]['close'] < swing.price:
                    sweeps.append(LiquiditySweep(
                        index=i,
                        timestamp=data.index[i],
                        sweep_type='HIGH_SWEEP',
                        price=data.iloc[i]['high'],
                        target_price=swing.price,
                        confirmed=True
                    ))
                    break
    
    # Detecta barridas de swing lows (low sweeps)
    for swing in swing_lows:
        if swing.index >= len(data) - 20:
            continue
        
        for i in range(swing.index + 1, min(swing.index + 20, len(data))):
            if data.iloc[i]['low'] < swing.price:
                if data.iloc[i]['close'] > swing.price:
                    sweeps.append(LiquiditySweep(
                        index=i,
                        timestamp=data.index[i],
                        sweep_type='LOW_SWEEP',
                        price=data.iloc[i]['low'],
                        target_price=swing.price,
                        confirmed=True
                    ))
                    break
    
    return sweeps


def detect_fair_value_gaps(data: pd.DataFrame, lookback: int = 3) -> List[InstitutionalBlock]:
    """
    Detecta Fair Value Gaps (FVG).
    
    Un FVG es un gap en el precio donde no hubo negociación.
    Se forma cuando una vela tiene un cuerpo que no se solapa con la vela anterior.
    
    Args:
        data: DataFrame con datos OHLCV
        lookback: Número de velas para verificar el gap
    
    Returns:
        Lista de InstitutionalBlock de tipo FVG
    """
    fvgs = []
    
    for i in range(1, len(data) - 1):
        prev_candle = data.iloc[i - 1]
        current_candle = data.iloc[i]
        next_candle = data.iloc[i + 1]
        
        # FVG alcista: la vela actual tiene un gap hacia arriba
        # El low de la vela actual es mayor que el high de la vela anterior
        if current_candle['low'] > prev_candle['high']:
            # Verifica que la siguiente vela no haya mitigado el gap
            if next_candle['low'] > prev_candle['high']:
                fvgs.append(InstitutionalBlock(
                    block_type=BlockType.FAIR_VALUE_GAP,
                    start_index=i - 1,
                    end_index=i,
                    start_price=prev_candle['high'],
                    end_price=current_candle['low'],
                    timestamp=data.index[i],
                    direction='BULLISH',
                    mitigated=False,
                    strength=2.0
                ))
        
        # FVG bajista: la vela actual tiene un gap hacia abajo
        # El high de la vela actual es menor que el low de la vela anterior
        elif current_candle['high'] < prev_candle['low']:
            if next_candle['high'] < prev_candle['low']:
                fvgs.append(InstitutionalBlock(
                    block_type=BlockType.FAIR_VALUE_GAP,
                    start_index=i - 1,
                    end_index=i,
                    start_price=prev_candle['low'],
                    end_price=current_candle['high'],
                    timestamp=data.index[i],
                    direction='BEARISH',
                    mitigated=False,
                    strength=2.0
                ))
    
    return fvgs


def detect_order_blocks(data: pd.DataFrame, swing_highs: List[SwingPoint],
                        swing_lows: List[SwingPoint]) -> List[InstitutionalBlock]:
    """
    Detecta Order Blocks (OB).
    
    Un Order Block es la última vela de un movimiento antes de una reversión.
    Representa donde las instituciones colocaron sus órdenes.
    
    Args:
        data: DataFrame con datos OHLCV
        swing_highs: Lista de swing highs
        swing_lows: Lista de swing lows
    
    Returns:
        Lista de InstitutionalBlock de tipo ORDER_BLOCK
    """
    obs = []
    
    # Order Block alcista: última vela bajista antes de un swing low
    for swing_low in swing_lows:
        if swing_low.index > 0:
            prev_candle = data.iloc[swing_low.index - 1]
            # Si la vela anterior fue bajista (cierre < apertura)
            if prev_candle['close'] < prev_candle['open']:
                obs.append(InstitutionalBlock(
                    block_type=BlockType.ORDER_BLOCK,
                    start_index=swing_low.index - 1,
                    end_index=swing_low.index - 1,
                    start_price=prev_candle['low'],
                    end_price=prev_candle['high'],
                    timestamp=prev_candle.name,
                    direction='BULLISH',
                    mitigated=False,
                    strength=3.0
                ))
    
    # Order Block bajista: última vela alcista antes de un swing high
    for swing_high in swing_highs:
        if swing_high.index > 0:
            prev_candle = data.iloc[swing_high.index - 1]
            # Si la vela anterior fue alcista (cierre > apertura)
            if prev_candle['close'] > prev_candle['open']:
                obs.append(InstitutionalBlock(
                    block_type=BlockType.ORDER_BLOCK,
                    start_index=swing_high.index - 1,
                    end_index=swing_high.index - 1,
                    start_price=prev_candle['low'],
                    end_price=prev_candle['high'],
                    timestamp=prev_candle.name,
                    direction='BEARISH',
                    mitigated=False,
                    strength=3.0
                ))
    
    return obs


def detect_mitigation_blocks(data: pd.DataFrame, blocks: List[InstitutionalBlock]) -> List[InstitutionalBlock]:
    """
    Detecta Mitigation Blocks y marca bloques mitigados.
    
    Un Mitigation Block es cuando el precio vuelve a tocar un FVG u OB,
    "mitigando" o llenando el gap/bloque.
    
    Args:
        data: DataFrame con datos OHLCV
        blocks: Lista de bloques institucionales a verificar
    
    Returns:
        Lista actualizada de bloques con información de mitigación
    """
    mitigation_blocks = []
    
    for block in blocks:
        # Verifica si el bloque ha sido mitigado
        if not block.mitigated:
            for i in range(block.end_index + 1, len(data)):
                candle = data.iloc[i]
                
                # Verifica si el precio tocó el bloque
                if block.direction == 'BULLISH':
                    if candle['low'] <= block.end_price:
                        block.mitigated = True
                        block.mitigation_index = i
                        break
                else:  # BEARISH
                    if candle['high'] >= block.start_price:
                        block.mitigated = True
                        block.mitigation_index = i
                        break
    
    return blocks


def detect_breaker_blocks(data: pd.DataFrame, order_blocks: List[InstitutionalBlock]) -> List[InstitutionalBlock]:
    """
    Detecta Breaker Blocks.
    
    Un Breaker Block es un Order Block que fue roto y luego se convierte en soporte/resistencia.
    
    Args:
        data: DataFrame con datos OHLCV
        order_blocks: Lista de Order Blocks detectados
    
    Returns:
        Lista de Breaker Blocks
    """
    breakers = []
    
    for ob in order_blocks:
        # Verifica si el OB fue roto después de su formación
        for i in range(ob.end_index + 1, len(data)):
            candle = data.iloc[i]
            
            if ob.direction == 'BULLISH':
                # Si el precio rompió por debajo del OB
                if candle['low'] < ob.start_price:
                    # Y luego volvió a actuar como soporte
                    for j in range(i + 1, min(i + 10, len(data))):
                        if data.iloc[j]['low'] >= ob.start_price and data.iloc[j]['close'] > ob.start_price:
                            breakers.append(InstitutionalBlock(
                                block_type=BlockType.BREAKER_BLOCK,
                                start_index=ob.start_index,
                                end_index=ob.end_index,
                                start_price=ob.start_price,
                                end_price=ob.end_price,
                                timestamp=ob.timestamp,
                                direction='BULLISH',
                                mitigated=False,
                                strength=4.0
                            ))
                            break
                    break
            
            else:  # BEARISH
                if candle['high'] > ob.end_price:
                    for j in range(i + 1, min(i + 10, len(data))):
                        if data.iloc[j]['high'] <= ob.end_price and data.iloc[j]['close'] < ob.end_price:
                            breakers.append(InstitutionalBlock(
                                block_type=BlockType.BREAKER_BLOCK,
                                start_index=ob.start_index,
                                end_index=ob.end_index,
                                start_price=ob.start_price,
                                end_price=ob.end_price,
                                timestamp=ob.timestamp,
                                direction='BEARISH',
                                mitigated=False,
                                strength=4.0
                            ))
                            break
                    break
    
    return breakers


def detect_rejection_blocks(data: pd.DataFrame, lookback: int = 5) -> List[InstitutionalBlock]:
    """
    Detecta Rejection Blocks.
    
    Un Rejection Block es una zona donde el precio fue rechazado fuertemente,
    indicando interés institucional.
    
    Args:
        data: DataFrame con datos OHLCV
        lookback: Número de velas para verificar el rechazo
    
    Returns:
        Lista de Rejection Blocks
    """
    rejections = []
    
    for i in range(lookback, len(data) - lookback):
        candle = data.iloc[i]
        
        # Rechazo alcista: vela con mecha superior larga (wick)
        upper_wick = candle['high'] - max(candle['open'], candle['close'])
        body = abs(candle['close'] - candle['open'])
        
        if upper_wick > body * 2 and candle['close'] < candle['open']:
            # Verifica que el precio no volvió a esa zona
            rejected = True
            for j in range(i + 1, min(i + 10, len(data))):
                if data.iloc[j]['high'] >= candle['high']:
                    rejected = False
                    break
            
            if rejected:
                rejections.append(InstitutionalBlock(
                    block_type=BlockType.REJECTION_BLOCK,
                    start_index=i,
                    end_index=i,
                    start_price=candle['high'] - upper_wick * 0.5,
                    end_price=candle['high'],
                    timestamp=candle.name,
                    direction='BEARISH',
                    mitigated=False,
                    strength=2.5
                ))
        
        # Rechazo bajista: vela con mecha inferior larga
        lower_wick = min(candle['open'], candle['close']) - candle['low']
        
        if lower_wick > body * 2 and candle['close'] > candle['open']:
            rejected = True
            for j in range(i + 1, min(i + 10, len(data))):
                if data.iloc[j]['low'] <= candle['low']:
                    rejected = False
                    break
            
            if rejected:
                rejections.append(InstitutionalBlock(
                    block_type=BlockType.REJECTION_BLOCK,
                    start_index=i,
                    end_index=i,
                    start_price=candle['low'],
                    end_price=candle['low'] + lower_wick * 0.5,
                    timestamp=candle.name,
                    direction='BULLISH',
                    mitigated=False,
                    strength=2.5
                ))
    
    return rejections


def detect_liquidity_voids(data: pd.DataFrame, fvgs: List[InstitutionalBlock]) -> List[InstitutionalBlock]:
    """
    Detecta Liquidity Voids.
    
    Un Liquidity Void es similar a un FVG pero más grande y significativo.
    Representa una zona donde no hay liquidez disponible.
    
    Args:
        data: DataFrame con datos OHLCV
        fvgs: Lista de FVGs detectados (los voids son FVGs grandes)
    
    Returns:
        Lista de Liquidity Voids
    """
    voids = []
    
    for fvg in fvgs:
        gap_size = abs(fvg.end_price - fvg.start_price)
        avg_price = (fvg.start_price + fvg.end_price) / 2
        gap_pct = (gap_size / avg_price) * 100
        
        # Un void es un FVG grande (más del 0.5% del precio)
        if gap_pct > 0.5:
            voids.append(InstitutionalBlock(
                block_type=BlockType.LIQUIDITY_VOID,
                start_index=fvg.start_index,
                end_index=fvg.end_index,
                start_price=fvg.start_price,
                end_price=fvg.end_price,
                timestamp=fvg.timestamp,
                direction=fvg.direction,
                mitigated=fvg.mitigated,
                strength=4.0
            ))
    
    return voids


def detect_trend(data: pd.DataFrame, swing_highs: List[SwingPoint],
                 swing_lows: List[SwingPoint]) -> TrendDirection:
    """
    Detecta la tendencia macro basándose en la secuencia de swings.
    
    Tendencia alcista: máximos crecientes y mínimos crecientes
    Tendencia bajista: máximos decrecientes y mínimos decrecientes
    
    Args:
        data: DataFrame con datos OHLCV
        swing_highs: Lista de swing highs
        swing_lows: Lista de swing lows
    
    Returns:
        TrendDirection (BULLISH, BEARISH, o NEUTRAL)
    """
    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return TrendDirection.NEUTRAL
    
    # Obtiene los últimos swings
    recent_highs = sorted([s for s in swing_highs if s.index >= len(data) - 100], 
                          key=lambda x: x.index)[-2:]
    recent_lows = sorted([s for s in swing_lows if s.index >= len(data) - 100],
                         key=lambda x: x.index)[-2:]
    
    if len(recent_highs) < 2 or len(recent_lows) < 2:
        return TrendDirection.NEUTRAL
    
    # Verifica tendencia alcista
    higher_highs = recent_highs[-1].price > recent_highs[-2].price
    higher_lows = recent_lows[-1].price > recent_lows[-2].price
    
    if higher_highs and higher_lows:
        return TrendDirection.BULLISH
    
    # Verifica tendencia bajista
    lower_highs = recent_highs[-1].price < recent_highs[-2].price
    lower_lows = recent_lows[-1].price < recent_lows[-2].price
    
    if lower_highs and lower_lows:
        return TrendDirection.BEARISH
    
    return TrendDirection.NEUTRAL


def detect_equal_highs_lows(data: pd.DataFrame, swing_highs: List[SwingPoint],
                            swing_lows: List[SwingPoint], tolerance: float = 0.001) -> List[Tuple[float, str]]:
    """
    Detecta zonas de liquidez mayor (máximos/mínimos iguales).
    
    Estas son zonas donde múltiples swings están al mismo nivel,
    indicando alta concentración de órdenes stop loss.
    
    Args:
        data: DataFrame con datos OHLCV
        swing_highs: Lista de swing highs
        swing_lows: Lista de swing lows
        tolerance: Tolerancia para considerar swings "iguales" (0.1% por defecto)
    
    Returns:
        Lista de tuplas (precio, tipo) donde hay liquidez mayor
    """
    liquidity_zones = []
    
    # Agrupa swings highs similares
    for i, swing1 in enumerate(swing_highs):
        similar_swings = [swing1]
        for swing2 in swing_highs[i+1:]:
            price_diff = abs(swing1.price - swing2.price) / swing1.price
            if price_diff <= tolerance:
                similar_swings.append(swing2)
        
        if len(similar_swings) >= 2:
            avg_price = sum(s.price for s in similar_swings) / len(similar_swings)
            liquidity_zones.append((avg_price, 'HIGH'))
    
    # Agrupa swings lows similares
    for i, swing1 in enumerate(swing_lows):
        similar_swings = [swing1]
        for swing2 in swing_lows[i+1:]:
            price_diff = abs(swing1.price - swing2.price) / swing1.price
            if price_diff <= tolerance:
                similar_swings.append(swing2)
        
        if len(similar_swings) >= 2:
            avg_price = sum(s.price for s in similar_swings) / len(similar_swings)
            liquidity_zones.append((avg_price, 'LOW'))
    
    return liquidity_zones













