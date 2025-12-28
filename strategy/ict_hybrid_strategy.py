"""
strategy/ict_hybrid_strategy.py - Estrategia Institucional Híbrida ICT 2022

Estrategia multi-temporal basada en ICT (Inner Circle Trader) 2022 que combina:
- Análisis de estructura de mercado (BOS/CHoCH)
- Detección de bloques institucionales (OB, FVG, etc.)
- Barridas de liquidez
- Confluencias técnicas
- Entradas tipo sniper

Timeframes analizados:
- D1: Tendencia macro, zonas de liquidez mayor, FVG grandes, OB macro
- H4: BOS/CHoCH institucionales, acumulación/redistribución, FVG activos, OB
- H1: Zonas institucionales activas, validación de mitigaciones
- M15/M5: BOS/CHoCH limpios, barridas de liquidez, mitades de FVG
- M1/M3: Confirmación entrada sniper (sweep + BOS interno + mitigación + vela institucional)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from strategy.base_strategy import BaseStrategy
from strategy.ict_utils import (
    detect_swings, detect_bos_choch, detect_liquidity_sweeps,
    detect_fair_value_gaps, detect_order_blocks, detect_mitigation_blocks,
    detect_breaker_blocks, detect_rejection_blocks, detect_liquidity_voids,
    detect_trend, detect_equal_highs_lows,
    SwingPoint, StructureBreak, LiquiditySweep, InstitutionalBlock,
    InstitutionalZone, BlockType, TrendDirection
)
from utils.indicators import calculate_rsi

# Importar módulo de pivots (opcional, no bloquea si no está disponible)
try:
    from utils.daily_pivots import DailyPivotsManager, DailyPivots
    PIVOTS_AVAILABLE = True
except ImportError:
    PIVOTS_AVAILABLE = False
    DailyPivotsManager = None
    DailyPivots = None


@dataclass
class MultiTimeframeContext:
    """Contexto global del análisis multi-temporal"""
    d1_trend: Optional[TrendDirection] = None
    d1_liquidity_zones: List[Tuple[float, str]] = field(default_factory=list)
    d1_fvgs: List[InstitutionalBlock] = field(default_factory=list)
    d1_order_blocks: List[InstitutionalBlock] = field(default_factory=list)
    
    h4_bos_choch: List[StructureBreak] = field(default_factory=list)
    h4_accumulation_zones: List[InstitutionalZone] = field(default_factory=list)
    h4_fvgs: List[InstitutionalBlock] = field(default_factory=list)
    h4_order_blocks: List[InstitutionalBlock] = field(default_factory=list)
    
    h1_active_zones: List[InstitutionalZone] = field(default_factory=list)
    h1_validated_mitigations: List[InstitutionalBlock] = field(default_factory=list)
    
    m15_m5_bos_choch: List[StructureBreak] = field(default_factory=list)
    m15_m5_sweeps: List[LiquiditySweep] = field(default_factory=list)
    m15_m5_unmitigated_fvgs: List[InstitutionalBlock] = field(default_factory=list)


@dataclass
class TradingSignal:
    """Señal de trading estructurada con toda la información institucional"""
    direction: str  # 'BULLISH' o 'BEARISH'
    active_zones: List[InstitutionalZone]
    operation_type: str  # 'BUY' o 'SELL'
    entry_price: float
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    take_profit_final: float
    risk_reward: float
    justifications: List[str]
    chart_data: Dict  # Datos estructurados para generar SVG


class ICTHybridStrategy(BaseStrategy):
    """
    Estrategia Institucional Híbrida ICT 2022.
    
    Implementa análisis multi-temporal completo con detección de:
    - Estructura de mercado (BOS/CHoCH)
    - Bloques institucionales (OB, FVG, Mitigation, Breaker, Rejection, Void)
    - Barridas de liquidez
    - Confluencias técnicas
    """
    
    def __init__(self):
        """Inicializa la estrategia ICT Híbrida"""
        super().__init__("ICT Hybrid Strategy 2022")
        self.context = MultiTimeframeContext()
        self.signals_history = []
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Genera señales de trading basadas en análisis multi-temporal.
        
        NOTA: Esta estrategia requiere datos de múltiples timeframes.
        Para uso completo, debes pasar datos de D1, H4, H1, M15, M5, M1, M3.
        
        Args:
            data: DataFrame con datos OHLCV del timeframe principal
        
        Returns:
            DataFrame con columna 'signal' añadida
        """
        # Inicializa la columna de señales
        data['signal'] = 'HOLD'
        
        # Esta función se usa principalmente para backtesting simple
        # El análisis completo se hace con las funciones específicas por timeframe
        
        return data
    
    def should_buy(self, data: pd.DataFrame, current_index: int) -> bool:
        """Determina si se debe comprar (implementación básica)"""
        # La lógica completa está en find_sniper_entry()
        return False
    
    def should_sell(self, data: pd.DataFrame, current_index: int, position: Dict) -> bool:
        """Determina si se debe vender (implementación básica)"""
        # La lógica completa está en find_sniper_entry()
        return False
    
    # ==================== FUNCIONES DE ANÁLISIS MULTI-TEMPORAL ====================
    
    def analyze_D1(self, df_D1: pd.DataFrame) -> Dict:
        """
        Análisis del timeframe D1 (diario).
        
        Detecta:
        - Tendencia macro
        - Zonas de liquidez mayor (máximos/mínimos iguales)
        - FVG grandes
        - Order Blocks macro
        
        Args:
            df_D1: DataFrame con datos OHLCV del timeframe D1
        
        Returns:
            Diccionario con toda la información del análisis D1
        """
        print("🔍 Analizando D1: Tendencia macro y zonas institucionales mayores...")
        
        # 1. Detecta swings
        swing_highs, swing_lows = detect_swings(df_D1, lookback=3)
        print(f"   ✓ Swings detectados: {len(swing_highs)} highs, {len(swing_lows)} lows")
        
        # 2. Detecta tendencia macro
        trend = detect_trend(df_D1, swing_highs, swing_lows)
        self.context.d1_trend = trend
        print(f"   ✓ Tendencia macro: {trend.value}")
        
        # 3. Detecta zonas de liquidez mayor (máximos/mínimos iguales)
        liquidity_zones = detect_equal_highs_lows(df_D1, swing_highs, swing_lows, tolerance=0.002)
        self.context.d1_liquidity_zones = liquidity_zones
        print(f"   ✓ Zonas de liquidez mayor: {len(liquidity_zones)}")
        
        # 4. Detecta FVG grandes (solo los significativos)
        all_fvgs = detect_fair_value_gaps(df_D1, lookback=2)
        # Filtra solo FVGs grandes (más del 0.3% del precio)
        large_fvgs = []
        for fvg in all_fvgs:
            gap_size = abs(fvg.end_price - fvg.start_price)
            avg_price = (fvg.start_price + fvg.end_price) / 2
            gap_pct = (gap_size / avg_price) * 100
            if gap_pct > 0.3:  # FVG grande
                large_fvgs.append(fvg)
        
        self.context.d1_fvgs = large_fvgs
        print(f"   ✓ FVG grandes detectados: {len(large_fvgs)}")
        
        # 5. Detecta Order Blocks macro
        order_blocks = detect_order_blocks(df_D1, swing_highs, swing_lows)
        # Filtra solo los más fuertes
        strong_obs = [ob for ob in order_blocks if ob.strength >= 2.5]
        self.context.d1_order_blocks = strong_obs
        print(f"   ✓ Order Blocks macro: {len(strong_obs)}")
        
        # 6. Verifica mitigaciones
        self.context.d1_fvgs = detect_mitigation_blocks(df_D1, self.context.d1_fvgs)
        self.context.d1_order_blocks = detect_mitigation_blocks(df_D1, self.context.d1_order_blocks)
        
        return {
            'trend': trend,
            'liquidity_zones': liquidity_zones,
            'fvgs': large_fvgs,
            'order_blocks': strong_obs,
            'swing_highs': swing_highs,
            'swing_lows': swing_lows
        }
    
    def analyze_H4(self, df_H4: pd.DataFrame) -> Dict:
        """
        Análisis del timeframe H4 (4 horas).
        
        Detecta:
        - BOS/CHoCH institucionales
        - Estructuras de acumulación/redistribución
        - FVG activos
        - Order Blocks en desequilibrio
        
        Args:
            df_H4: DataFrame con datos OHLCV del timeframe H4
        
        Returns:
            Diccionario con toda la información del análisis H4
        """
        print("🔍 Analizando H4: BOS/CHoCH institucionales y estructuras...")
        
        # 1. Detecta swings
        swing_highs, swing_lows = detect_swings(df_H4, lookback=5)
        print(f"   ✓ Swings detectados: {len(swing_highs)} highs, {len(swing_lows)} lows")
        
        # 2. Detecta BOS/CHoCH institucionales
        bos_choch = detect_bos_choch(df_H4, swing_highs, swing_lows)
        self.context.h4_bos_choch = bos_choch
        print(f"   ✓ BOS/CHoCH detectados: {len(bos_choch)}")
        
        # 3. Detecta estructuras de acumulación/redistribución
        # Acumulación: múltiples Order Blocks alcistas cerca de un swing low
        # Redistribución: múltiples Order Blocks bajistas cerca de un swing high
        accumulation_zones = []
        redistribution_zones = []
        
        order_blocks = detect_order_blocks(df_H4, swing_highs, swing_lows)
        
        # Agrupa OBs cerca de swings para identificar acumulación/redistribución
        for swing_low in swing_lows[-5:]:  # Últimos 5 swing lows
            nearby_obs = [ob for ob in order_blocks 
                         if ob.direction == 'BULLISH' 
                         and abs(ob.end_price - swing_low.price) / swing_low.price < 0.01]
            if len(nearby_obs) >= 2:
                zone = InstitutionalZone(
                    zone_type='ACCUMULATION',
                    price_level=swing_low.price,
                    origin_timestamp=swing_low.timestamp,
                    origin_timeframe='H4',
                    direction='BULLISH',
                    blocks=nearby_obs,
                    active=True
                )
                accumulation_zones.append(zone)
        
        for swing_high in swing_highs[-5:]:  # Últimos 5 swing highs
            nearby_obs = [ob for ob in order_blocks 
                         if ob.direction == 'BEARISH' 
                         and abs(ob.start_price - swing_high.price) / swing_high.price < 0.01]
            if len(nearby_obs) >= 2:
                zone = InstitutionalZone(
                    zone_type='REDISTRIBUTION',
                    price_level=swing_high.price,
                    origin_timestamp=swing_high.timestamp,
                    origin_timeframe='H4',
                    direction='BEARISH',
                    blocks=nearby_obs,
                    active=True
                )
                redistribution_zones.append(zone)
        
        self.context.h4_accumulation_zones = accumulation_zones + redistribution_zones
        print(f"   ✓ Estructuras detectadas: {len(accumulation_zones)} acumulación, {len(redistribution_zones)} redistribución")
        
        # 4. Detecta FVG activos (no mitigados)
        fvgs = detect_fair_value_gaps(df_H4, lookback=3)
        fvgs = detect_mitigation_blocks(df_H4, fvgs)
        active_fvgs = [fvg for fvg in fvgs if not fvg.mitigated]
        self.context.h4_fvgs = active_fvgs
        print(f"   ✓ FVG activos: {len(active_fvgs)}")
        
        # 5. Detecta Order Blocks (filtra solo los no mitigados)
        obs = detect_order_blocks(df_H4, swing_highs, swing_lows)
        obs = detect_mitigation_blocks(df_H4, obs)
        active_obs = [ob for ob in obs if not ob.mitigated]
        self.context.h4_order_blocks = active_obs
        print(f"   ✓ Order Blocks activos: {len(active_obs)}")
        
        return {
            'bos_choch': bos_choch,
            'accumulation_zones': accumulation_zones,
            'redistribution_zones': redistribution_zones,
            'fvgs': active_fvgs,
            'order_blocks': active_obs,
            'swing_highs': swing_highs,
            'swing_lows': swing_lows
        }
    
    def analyze_H1(self, df_H1: pd.DataFrame) -> Dict:
        """
        Análisis del timeframe H1 (1 hora).
        
        Aterriza zonas institucionales activas y valida mitigaciones.
        
        Args:
            df_H1: DataFrame con datos OHLCV del timeframe H1
        
        Returns:
            Diccionario con zonas activas y mitigaciones validadas
        """
        print("🔍 Analizando H1: Aterrizando zonas institucionales activas...")
        
        # 1. Detecta swings
        swing_highs, swing_lows = detect_swings(df_H1, lookback=7)
        print(f"   ✓ Swings detectados: {len(swing_highs)} highs, {len(swing_lows)} lows")
        
        # 2. Aterriza zonas institucionales desde H4 y D1
        active_zones = []
        
        # Combina Order Blocks de H4 que están cerca del precio actual
        current_price = df_H1.iloc[-1]['close']
        for ob in self.context.h4_order_blocks:
            price_diff = abs(ob.start_price - current_price) / current_price
            if price_diff < 0.02:  # Dentro del 2% del precio actual
                zone = InstitutionalZone(
                    zone_type='ORDER_BLOCK',
                    price_level=ob.start_price,
                    origin_timestamp=ob.timestamp,
                    origin_timeframe='H4',
                    direction=ob.direction,
                    blocks=[ob],
                    active=True
                )
                active_zones.append(zone)
        
        # Combina FVGs activos de H4
        for fvg in self.context.h4_fvgs:
            price_diff = abs((fvg.start_price + fvg.end_price) / 2 - current_price) / current_price
            if price_diff < 0.02:
                zone = InstitutionalZone(
                    zone_type='FAIR_VALUE_GAP',
                    price_level=(fvg.start_price + fvg.end_price) / 2,
                    origin_timestamp=fvg.timestamp,
                    origin_timeframe='H4',
                    direction=fvg.direction,
                    blocks=[fvg],
                    active=True
                )
                active_zones.append(zone)
        
        self.context.h1_active_zones = active_zones
        print(f"   ✓ Zonas institucionales activas: {len(active_zones)}")
        
        # 3. Valida mitigaciones
        # Detecta Order Blocks y FVGs en H1
        obs_h1 = detect_order_blocks(df_H1, swing_highs, swing_lows)
        fvgs_h1 = detect_fair_value_gaps(df_H1, lookback=3)
        
        # Verifica si alguno de los bloques de H4 fue mitigado en H1
        validated_mitigations = []
        for block in self.context.h4_order_blocks + self.context.h4_fvgs:
            if not block.mitigated:
                # Verifica si fue mitigado en H1
                for i in range(len(df_H1)):
                    candle = df_H1.iloc[i]
                    if block.direction == 'BULLISH':
                        if candle['low'] <= block.end_price:
                            block.mitigated = True
                            block.mitigation_index = i
                            validated_mitigations.append(block)
                            break
                    else:
                        if candle['high'] >= block.start_price:
                            block.mitigated = True
                            block.mitigation_index = i
                            validated_mitigations.append(block)
                            break
        
        self.context.h1_validated_mitigations = validated_mitigations
        print(f"   ✓ Mitigaciones validadas: {len(validated_mitigations)}")
        
        return {
            'active_zones': active_zones,
            'validated_mitigations': validated_mitigations
        }
    
    def analyze_M15_M5(self, df_M15: pd.DataFrame, df_M5: pd.DataFrame) -> Dict:
        """
        Análisis de los timeframes M15 y M5 (15 y 5 minutos).
        
        Detecta:
        - BOS/CHoCH limpios
        - Barridas de liquidez previas
        - Mitades de FVG no mitigados
        
        Args:
            df_M15: DataFrame con datos OHLCV del timeframe M15
            df_M5: DataFrame con datos OHLCV del timeframe M5
        
        Returns:
            Diccionario con BOS/CHoCH, barridas y FVGs no mitigados
        """
        print("🔍 Analizando M15/M5: BOS/CHoCH limpios y barridas de liquidez...")
        
        results = {}
        
        # Análisis M15
        swing_highs_m15, swing_lows_m15 = detect_swings(df_M15, lookback=7)
        bos_choch_m15 = detect_bos_choch(df_M15, swing_highs_m15, swing_lows_m15)
        sweeps_m15 = detect_liquidity_sweeps(df_M15, swing_highs_m15, swing_lows_m15)
        fvgs_m15 = detect_fair_value_gaps(df_M15, lookback=3)
        fvgs_m15 = detect_mitigation_blocks(df_M15, fvgs_m15)
        unmitigated_fvgs_m15 = [fvg for fvg in fvgs_m15 if not fvg.mitigated]
        
        print(f"   ✓ M15 - BOS/CHoCH: {len(bos_choch_m15)}, Barridas: {len(sweeps_m15)}, FVG no mitigados: {len(unmitigated_fvgs_m15)}")
        
        # Análisis M5
        swing_highs_m5, swing_lows_m5 = detect_swings(df_M5, lookback=10)
        bos_choch_m5 = detect_bos_choch(df_M5, swing_highs_m5, swing_lows_m5)
        sweeps_m5 = detect_liquidity_sweeps(df_M5, swing_highs_m5, swing_lows_m5)
        fvgs_m5 = detect_fair_value_gaps(df_M5, lookback=3)
        fvgs_m5 = detect_mitigation_blocks(df_M5, fvgs_m5)
        unmitigated_fvgs_m5 = [fvg for fvg in fvgs_m5 if not fvg.mitigated]
        
        print(f"   ✓ M5 - BOS/CHoCH: {len(bos_choch_m5)}, Barridas: {len(sweeps_m5)}, FVG no mitigados: {len(unmitigated_fvgs_m5)}")
        
        # Combina resultados
        all_bos_choch = bos_choch_m15 + bos_choch_m5
        all_sweeps = sweeps_m15 + sweeps_m5
        all_unmitigated_fvgs = unmitigated_fvgs_m15 + unmitigated_fvgs_m5
        
        self.context.m15_m5_bos_choch = all_bos_choch
        self.context.m15_m5_sweeps = all_sweeps
        self.context.m15_m5_unmitigated_fvgs = all_unmitigated_fvgs
        
        return {
            'bos_choch': all_bos_choch,
            'sweeps': all_sweeps,
            'unmitigated_fvgs': all_unmitigated_fvgs
        }
    
    def find_sniper_entry(self, df_M1: pd.DataFrame, df_M3: pd.DataFrame,
                         contexto_global: MultiTimeframeContext) -> Optional[TradingSignal]:
        """
        Encuentra entrada tipo sniper en M1/M3.
        
        Confirmaciones requeridas (≥ 3 deben cumplirse):
        1. Sweep de liquidez
        2. Mitigación válida de OB o FVG
        3. BOS/CHoCH interno luego de la barrida
        4. Vela institucional + volumen alto
        5. Divergencia RSI (opcional)
        
        Args:
            df_M1: DataFrame con datos OHLCV del timeframe M1
            df_M3: DataFrame con datos OHLCV del timeframe M3
            contexto_global: Contexto multi-temporal completo
        
        Returns:
            TradingSignal si se cumplen las condiciones, None en caso contrario
        """
        print("🎯 Buscando entrada tipo sniper en M1/M3...")
        
        # Usa M3 como principal (más limpio que M1)
        df = df_M3.copy()
        
        if len(df) < 50:
            print("   ⚠️ Datos insuficientes en M3")
            return None
        
        # Calcula RSI para divergencias
        rsi = calculate_rsi(df['close'], period=14)
        
        # Detecta swings en M3
        swing_highs, swing_lows = detect_swings(df, lookback=5)
        
        # Detecta BOS/CHoCH internos
        bos_choch = detect_bos_choch(df, swing_highs, swing_lows)
        
        # Detecta barridas de liquidez
        sweeps = detect_liquidity_sweeps(df, swing_highs, swing_lows)
        
        # Detecta Order Blocks y FVGs
        obs = detect_order_blocks(df, swing_highs, swing_lows)
        fvgs = detect_fair_value_gaps(df, lookback=2)
        
        # Obtiene la última vela
        last_candle = df.iloc[-1]
        current_price = last_candle['close']
        current_index = len(df) - 1
        
        # Sistema de peso por confirmación (prioriza confirmaciones más importantes)
        CONFIRMATION_WEIGHTS = {
            'SWEEP': 2.0,              # Más importante - barrida de liquidez
            'MITIGATION': 2.0,         # Más importante - mitigación de OB/FVG
            'BOS_CHOCH': 1.5,          # Importante - ruptura de estructura
            'INSTITUTIONAL_CANDLE': 1.0,  # Normal - vela institucional
            'RSI_DIVERGENCE': 0.5      # Menos importante - divergencia (opcional)
        }
        
        # Verifica confirmaciones
        confirmations = []
        justifications = []
        
        # 1. Sweep de liquidez
        recent_sweeps = [s for s in sweeps if s.index >= current_index - 10]
        has_sweep = len(recent_sweeps) > 0
        if has_sweep:
            confirmations.append('SWEEP')
            justifications.append(f"Barrida de liquidez detectada: {recent_sweeps[-1].sweep_type}")
        
        # 2. Mitigación válida de OB o FVG
        has_mitigation = False
        mitigated_block = None
        
        # Verifica si algún OB o FVG fue mitigado recientemente
        # Ventana más amplia (10 velas) con tolerancia para mejor detección
        lookback_window = 10
        tolerance = 0.001  # 0.1% de tolerancia
        
        for ob in obs:
            if ob.end_index >= current_index - lookback_window:
                # Verifica si fue mitigado con tolerancia
                for i in range(ob.end_index + 1, current_index + 1):
                    candle = df.iloc[i]
                    if ob.direction == 'BULLISH' and candle['low'] <= ob.end_price * (1 + tolerance):
                        has_mitigation = True
                        mitigated_block = ob
                        break
                    elif ob.direction == 'BEARISH' and candle['high'] >= ob.start_price * (1 - tolerance):
                        has_mitigation = True
                        mitigated_block = ob
                        break
        
        for fvg in fvgs:
            if fvg.end_index >= current_index - lookback_window:
                for i in range(fvg.end_index + 1, current_index + 1):
                    candle = df.iloc[i]
                    if fvg.direction == 'BULLISH' and candle['low'] <= fvg.end_price * (1 + tolerance):
                        has_mitigation = True
                        mitigated_block = fvg
                        break
                    elif fvg.direction == 'BEARISH' and candle['high'] >= fvg.start_price * (1 - tolerance):
                        has_mitigation = True
                        mitigated_block = fvg
                        break
        
        if has_mitigation:
            confirmations.append('MITIGATION')
            justifications.append(f"Mitigación de {mitigated_block.block_type.value} detectada")
        
        # 3. BOS/CHoCH interno luego de la barrida
        has_bos_choch = False
        if has_sweep and len(bos_choch) > 0:
            last_sweep = recent_sweeps[-1]
            recent_bos = [b for b in bos_choch if b.index > last_sweep.index and b.index <= current_index]
            if len(recent_bos) > 0:
                has_bos_choch = True
                confirmations.append('BOS_CHOCH')
                justifications.append(f"BOS/CHoCH interno detectado: {recent_bos[-1].break_type}")
        
        # 4. Vela institucional + volumen alto
        # Vela institucional: cuerpo grande con mecha pequeña
        body = abs(last_candle['close'] - last_candle['open'])
        candle_range = last_candle['high'] - last_candle['low']
        body_ratio = body / candle_range if candle_range > 0 else 0
        
        # Volumen alto: comparado con promedio
        avg_volume = df['volume'].tail(20).mean()
        volume_ratio = last_candle['volume'] / avg_volume if avg_volume > 0 else 0
        
        # Tamaño absoluto de la vela (porcentaje del precio)
        candle_size_pct = candle_range / current_price * 100 if current_price > 0 else 0
        
        # Criterios mejorados y más flexibles para vela institucional
        has_institutional_candle = (
            (body_ratio > 0.6 and volume_ratio > 1.3) or  # Cuerpo grande + volumen
            (body_ratio > 0.5 and volume_ratio > 2.0) or  # Cuerpo medio + volumen muy alto
            (body_ratio > 0.8 and volume_ratio > 1.0)     # Cuerpo muy grande + volumen normal
        ) and candle_size_pct > 0.15  # Vela debe ser al menos 0.15% del precio
        
        if has_institutional_candle:
            confirmations.append('INSTITUTIONAL_CANDLE')
            justifications.append(f"Vela institucional detectada (body: {body_ratio:.2%}, volumen: {volume_ratio:.2f}x, tamaño: {candle_size_pct:.3f}%)")
        
        # 5. Divergencia RSI (opcional)
        has_rsi_divergence = False
        if len(swing_highs) >= 2 and len(swing_lows) >= 2:
            # Busca divergencia alcista (precio hace lower low, RSI hace higher low)
            if len(swing_lows) >= 2:
                last_low = swing_lows[-1]
                prev_low = swing_lows[-2]
                if last_low.price < prev_low.price:
                    last_rsi = rsi.iloc[last_low.index]
                    prev_rsi = rsi.iloc[prev_low.index]
                    if last_rsi > prev_rsi:
                        has_rsi_divergence = True
                        confirmations.append('RSI_DIVERGENCE')
                        justifications.append("Divergencia alcista RSI detectada")
            
            # Busca divergencia bajista (precio hace higher high, RSI hace lower high)
            if len(swing_highs) >= 2:
                last_high = swing_highs[-1]
                prev_high = swing_highs[-2]
                if last_high.price > prev_high.price:
                    last_rsi = rsi.iloc[last_high.index]
                    prev_rsi = rsi.iloc[prev_high.index]
                    if last_rsi < prev_rsi:
                        has_rsi_divergence = True
                        confirmations.append('RSI_DIVERGENCE')
                        justifications.append("Divergencia bajista RSI detectada")
        
        # Muestra información del precio y análisis actual
        print(f"   📊 Precio actual: ${current_price:.2f}")
        
        # Análisis de la última vela
        candle_body = abs(last_candle['close'] - last_candle['open'])
        candle_range = last_candle['high'] - last_candle['low']
        body_ratio = candle_body / candle_range if candle_range > 0 else 0
        is_bullish = last_candle['close'] > last_candle['open']
        candle_type = "🟢 Alcista" if is_bullish else "🔴 Bajista"
        
        # Volumen relativo
        avg_volume = df['volume'].tail(20).mean()
        volume_ratio = last_candle['volume'] / avg_volume if avg_volume > 0 else 1
        
        print(f"   📈 Última vela M3: {candle_type} | Cuerpo: {body_ratio:.1%} | Volumen: {volume_ratio:.2f}x")
        
        # RSI actual
        current_rsi = rsi.iloc[-1] if len(rsi) > 0 else 50
        rsi_status = "Sobrecomprado" if current_rsi > 70 else "Sobreventado" if current_rsi < 30 else "Neutral"
        print(f"   📉 RSI(14): {current_rsi:.1f} ({rsi_status})")
        
        # Swings más cercanos
        if len(swing_highs) > 0:
            nearest_high = min([s.price for s in swing_highs if s.price > current_price], default=None)
            if nearest_high:
                distance_high = ((nearest_high - current_price) / current_price) * 100
                print(f"   ⬆️ Swing High más cercano: ${nearest_high:.2f} (+{distance_high:.2f}%)")
        
        if len(swing_lows) > 0:
            nearest_low = max([s.price for s in swing_lows if s.price < current_price], default=None)
            if nearest_low:
                distance_low = ((current_price - nearest_low) / current_price) * 100
                print(f"   ⬇️ Swing Low más cercano: ${nearest_low:.2f} (-{distance_low:.2f}%)")
        
        # Muestra qué confirmaciones se encontraron y cuáles faltan
        found_confirmations = ', '.join(confirmations) if confirmations else "Ninguna"
        print(f"   ✓ Confirmaciones encontradas: {found_confirmations}")
        
        missing_confirmations = []
        if not has_sweep:
            missing_confirmations.append("Sweep de liquidez")
        if not has_mitigation:
            missing_confirmations.append("Mitigación OB/FVG")
        if not has_bos_choch:
            missing_confirmations.append("BOS/CHoCH interno")
        if not has_institutional_candle:
            missing_confirmations.append("Vela institucional")
        if len(missing_confirmations) > 0:
            print(f"   ⚠️ Faltan: {', '.join(missing_confirmations[:3])}")
        
        # Determina dirección basándose en el contexto
        direction = 'BULLISH'  # Por defecto
        if contexto_global.d1_trend == TrendDirection.BEARISH:
            direction = 'BEARISH'
        elif len(bos_choch) > 0:
            last_bos = bos_choch[-1]
            direction = last_bos.direction
        
        # Determina tipo de operación
        operation_type = 'BUY' if direction == 'BULLISH' else 'SELL'
        
        # 6. Confluencia con Pivots Diarios (confirmación adicional)
        pivot_score = 0.0
        pivot_justification = None
        pivot_level = None
        pivot_distance = 0.0
        
        if PIVOTS_AVAILABLE and contexto_global.pivots_manager:
            try:
                # Obtiene pivots (se actualizan automáticamente si es necesario)
                # Usa el símbolo del contexto o por defecto XAUUSD
                symbol = getattr(contexto_global, 'symbol', 'XAUUSD')
                pivots = contexto_global.pivots_manager.get_pivots(symbol=symbol)
                
                if pivots:
                    # Verifica confluencia con pivots
                    has_confluence, level, distance_pct = contexto_global.pivots_manager.check_pivot_confluence(
                        price=current_price,
                        direction=operation_type,
                        pivots=pivots,
                        tolerance_pct=0.15  # 0.15% de tolerancia
                    )
                    
                    if has_confluence:
                        # Confluencia encontrada: +1.0 al score si es nivel fuerte (S1/R1 o PP)
                        # +0.5 si es nivel débil (S2/R2, S3/R3)
                        if level in ['S1', 'R1', 'PP']:
                            pivot_score = 1.0
                            pivot_justification = f"Confluencia con {level} (distancia: {distance_pct:.2f}%)"
                        else:
                            pivot_score = 0.5
                            pivot_justification = f"Confluencia con {level} (distancia: {distance_pct:.2f}%)"
                        
                        confirmations.append('PIVOT_CONFLUENCE')
                        justifications.append(pivot_justification)
                        pivot_level = level
                        pivot_distance = distance_pct
                        
                        print(f"   ✅ Confluencia con pivot {level} detectada (distancia: {distance_pct:.2f}%)")
                    else:
                        # Verifica si está cerca pero no en confluencia (filtro direccional)
                        nearest_level, nearest_price, nearest_distance = contexto_global.pivots_manager.get_nearest_level(
                            current_price, pivots
                        )
                        
                        if nearest_distance <= 0.3:  # Muy cerca (0.3%)
                            # Filtro direccional: advierte si está cerca del nivel opuesto
                            if operation_type == 'BUY' and nearest_level in ['R1', 'R2', 'R3']:
                                print(f"   ⚠️ Precio cerca de {nearest_level} (resistencia) - no ideal para BUY")
                            elif operation_type == 'SELL' and nearest_level in ['S1', 'S2', 'S3']:
                                print(f"   ⚠️ Precio cerca de {nearest_level} (soporte) - no ideal para SELL")
            except Exception as e:
                # Si hay error, continúa sin pivots (no bloquea la señal)
                if logger:
                    logger.warning(f"Error al verificar pivots: {e}")
        
        # Sistema de peso: calcular score total de confirmaciones
        total_score = sum(CONFIRMATION_WEIGHTS.get(c, 1.0) for c in confirmations)
        
        # Agregar score de pivots si hay confluencia
        if pivot_score > 0:
            total_score += pivot_score
        
        min_score_required = 4.0  # Requiere al menos 2 confirmaciones fuertes (2.0 + 2.0)
        
        # Verifica score mínimo (equivalente a 2 confirmaciones fuertes o combinación equivalente)
        if total_score < min_score_required:
            print(f"   ❌ Score insuficiente: {total_score:.1f}/{min_score_required:.1f} (confirmaciones: {len(confirmations)})")
            print(f"      Confirmaciones: {', '.join(confirmations) if confirmations else 'Ninguna'}")
            return None
        
        print(f"   ✓ Score de confirmaciones: {total_score:.1f}/{min_score_required:.1f}")
        print(f"      Confirmaciones ({len(confirmations)}): {', '.join(confirmations)}")
        
        # Calcula niveles de entrada, SL y TP
        entry_price = current_price
        
        # Stop Loss: por encima/debajo del OB o FVG mitigado
        if mitigated_block:
            if direction == 'BULLISH':
                stop_loss = mitigated_block.start_price * 0.999  # 0.1% por debajo
            else:
                stop_loss = mitigated_block.end_price * 1.001  # 0.1% por encima
        else:
            # SL por defecto: 0.5% del precio
            stop_loss = entry_price * (0.995 if direction == 'BULLISH' else 1.005)
        
        # Take Profits (basados en estructura)
        risk = abs(entry_price - stop_loss)
        
        # TP1: 1:1.5 RR
        take_profit_1 = entry_price + (risk * 1.5) if direction == 'BULLISH' else entry_price - (risk * 1.5)
        
        # TP2: 1:2.5 RR
        take_profit_2 = entry_price + (risk * 2.5) if direction == 'BULLISH' else entry_price - (risk * 2.5)
        
        # TP Final: 1:4 RR o próximo swing
        take_profit_final = entry_price + (risk * 4) if direction == 'BULLISH' else entry_price - (risk * 4)
        
        # Ajusta TP Final al próximo swing si está más lejos (mejor RR)
        if direction == 'BULLISH' and len(swing_highs) > 0:
            # Para BUY: usar el swing más alto disponible (más lejos = mejor)
            next_swing = max([s.price for s in swing_highs if s.price > entry_price], default=None)
            if next_swing and next_swing > take_profit_final:
                take_profit_final = next_swing
            # Pero no usar swings que estén más cerca que el TP calculado
            closer_swings = [s.price for s in swing_highs if entry_price < s.price < take_profit_final]
            if closer_swings:
                # Usar el swing más lejano de los que están más cerca
                take_profit_final = max(closer_swings)
        elif direction == 'BEARISH' and len(swing_lows) > 0:
            # Para SELL: usar el swing más bajo disponible (más lejos = mejor)
            next_swing = min([s.price for s in swing_lows if s.price < entry_price], default=None)
            if next_swing and next_swing < take_profit_final:
                take_profit_final = next_swing
            # Pero no usar swings que estén más cerca que el TP calculado
            closer_swings = [s.price for s in swing_lows if take_profit_final < s.price < entry_price]
            if closer_swings:
                # Usar el swing más lejano de los que están más cerca
                take_profit_final = min(closer_swings)
        
        # Calcula Risk:Reward basado en TP1 (el que realmente se ejecuta primero)
        # Esto es importante porque el bot valida el RR mínimo basado en TP1
        if direction == 'BULLISH':
            reward = take_profit_1 - entry_price
        else:  # BEARISH
            reward = entry_price - take_profit_1
        
        risk_reward = reward / risk if risk > 0 else 0
        
        # También calcula RR del TP Final para referencia (opcional, no se usa para validación)
        if direction == 'BULLISH':
            reward_final = take_profit_final - entry_price
        else:  # BEARISH
            reward_final = entry_price - take_profit_final
        
        risk_reward_final = reward_final / risk if risk > 0 else 0
        
        # Crea zonas activas
        active_zones = []
        for zone in contexto_global.h1_active_zones:
            price_diff = abs(zone.price_level - entry_price) / entry_price
            if price_diff < 0.01:  # Dentro del 1%
                active_zones.append(zone)
        
        # Datos para gráfico SVG
        chart_data = {
            'support_levels': [s.price for s in swing_lows[-5:]],
            'resistance_levels': [s.price for s in swing_highs[-5:]],
            'order_blocks': [(ob.start_price, ob.end_price) for ob in obs[-5:]],
            'fair_value_gaps': [(fvg.start_price, fvg.end_price) for fvg in fvgs[-5:]],
            'liquidity_zones': [(s.target_price, s.price) for s in sweeps[-5:]],
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profits': [take_profit_1, take_profit_2, take_profit_final]
        }
        
        # Crea la señal
        signal = TradingSignal(
            direction=direction,
            active_zones=active_zones,
            operation_type=operation_type,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit_1=take_profit_1,
            take_profit_2=take_profit_2,
            take_profit_final=take_profit_final,
            risk_reward=risk_reward,
            justifications=justifications,
            chart_data=chart_data
        )
        
        self.signals_history.append(signal)
        
        print(f"   ✅ Señal {operation_type} generada")
        print(f"      Entrada: ${entry_price:.2f}")
        print(f"      SL: ${stop_loss:.2f}")
        print(f"      TP1: ${take_profit_1:.2f}, TP2: ${take_profit_2:.2f}, TP Final: ${take_profit_final:.2f}")
        print(f"      Risk:Reward: 1:{risk_reward:.2f}")
        if pivot_info:
            print(f"      🎯 Confluencia con Pivot {pivot_info['level']} (score: +{pivot_score:.1f})")
        
        return signal
    
    def generate_signal(self, contexto: Dict) -> Optional[Dict]:
        """
        Genera una señal de trading a partir de un contexto multi-temporal.
        
        Esta función es el punto de entrada principal para backtesting y trading en vivo.
        Toma un diccionario con datos de múltiples timeframes y retorna una señal estructurada.
        
        Args:
            contexto: Diccionario con DataFrames de cada timeframe:
                {
                    "D1": df_d1,
                    "H4": df_h4,
                    "H1": df_h1,
                    "M15": df_m15,
                    "M5": df_m5,
                    "M3": df_m3,
                    "M1": df_m1
                }
        
        Returns:
            Diccionario con la señal o None si no hay señal:
            {
                "signal": "BUY" | "SELL" | "HOLD",
                "entry_price": float,
                "stop_loss": float,
                "take_profit_1": float,
                "take_profit_2": float,
                "take_profit_final": float,
                "risk_reward": float,
                "direction": "BULLISH" | "BEARISH",
                "justifications": List[str],
                "active_zones": List[Dict]
            }
        """
        try:
            # Ejecuta análisis multi-temporal
            if "D1" in contexto and len(contexto["D1"]) > 10:
                self.analyze_D1(contexto["D1"])
            
            if "H4" in contexto and len(contexto["H4"]) > 10:
                self.analyze_H4(contexto["H4"])
            
            if "H1" in contexto and len(contexto["H1"]) > 10:
                self.analyze_H1(contexto["H1"])
            
            if "M15" in contexto and "M5" in contexto:
                if len(contexto["M15"]) > 10 and len(contexto["M5"]) > 10:
                    self.analyze_M15_M5(contexto["M15"], contexto["M5"])
            
            # Busca entrada sniper en M1/M3
            m1_data = contexto.get("M1")
            m3_data = contexto.get("M3")
            
            # Si no hay M1, usa M3. Si no hay M3, usa M5
            if m1_data is None or len(m1_data) < 50:
                if m3_data is not None and len(m3_data) >= 50:
                    m1_data = m3_data
                elif "M5" in contexto and len(contexto["M5"]) >= 50:
                    m1_data = contexto["M5"]
                else:
                    return {
                        "signal": "HOLD",
                        "entry_price": 0.0,
                        "stop_loss": 0.0,
                        "take_profit_1": 0.0,
                        "take_profit_2": 0.0,
                        "take_profit_final": 0.0,
                        "risk_reward": 0.0,
                        "direction": "NEUTRAL",
                        "justifications": ["Datos insuficientes para generar señal"],
                        "active_zones": []
                    }
            
            if m3_data is None or len(m3_data) < 50:
                m3_data = m1_data
            
            # Busca señal sniper
            signal = self.find_sniper_entry(m1_data, m3_data, self.context)
            
            if signal is None:
                return {
                    "signal": "HOLD",
                    "entry_price": 0.0,
                    "stop_loss": 0.0,
                    "take_profit_1": 0.0,
                    "take_profit_2": 0.0,
                    "take_profit_final": 0.0,
                    "risk_reward": 0.0,
                    "direction": "NEUTRAL",
                    "justifications": ["No se cumplieron las confirmaciones requeridas"],
                    "active_zones": []
                }
            
            # Convierte TradingSignal a diccionario
            signal_dict = {
                "signal": signal.operation_type,
                "entry_price": signal.entry_price,
                "stop_loss": signal.stop_loss,
                "take_profit_1": signal.take_profit_1,
                "take_profit_2": signal.take_profit_2,
                "take_profit_final": signal.take_profit_final,
                "risk_reward": signal.risk_reward,
                "direction": signal.direction,
                "justifications": signal.justifications,
                "active_zones": [
                    {
                        "zone_type": zone.zone_type,
                        "price_level": zone.price_level,
                        "origin_timeframe": zone.origin_timeframe,
                        "direction": zone.direction
                    }
                    for zone in signal.active_zones
                ]
            }
            
            # Agregar información de pivots si hay confluencia
            if signal.chart_data and "pivot_confluence" in signal.chart_data:
                signal_dict["pivot_confluence"] = signal.chart_data["pivot_confluence"]
            
            return signal_dict
        
        except Exception as e:
            print(f"⚠️ Error al generar señal: {e}")
            return {
                "signal": "HOLD",
                "entry_price": 0.0,
                "stop_loss": 0.0,
                "take_profit_1": 0.0,
                "take_profit_2": 0.0,
                "take_profit_final": 0.0,
                "risk_reward": 0.0,
                "direction": "NEUTRAL",
                "justifications": [f"Error: {str(e)}"],
                "active_zones": []
            }

