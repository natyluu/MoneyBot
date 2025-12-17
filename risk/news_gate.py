"""
risk/news_gate.py - News Risk Gate

Sistema de protección que bloquea nuevas entradas durante eventos de noticias,
alta volatilidad, spreads altos o drawdown excesivo.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from news.provider import get_news_provider


def detect_usd_yellow_cluster(events: List[Dict], now_utc: datetime, 
                              window_minutes: int = 90, min_events: int = 2) -> bool:
    """
    Detecta si hay un cluster de noticias USD amarillas (LOW/MED) en una ventana de tiempo.
    
    Args:
        events: Lista de eventos de noticias
        now_utc: Tiempo actual en UTC
        window_minutes: Ventana de tiempo en minutos para buscar cluster
        min_events: Mínimo de eventos para considerar cluster
    
    Returns:
        True si hay cluster detectado
    """
    if not events:
        return False
    
    # Filtra eventos USD con impacto LOW o MED
    usd_yellow_events = [
        e for e in events
        if e.get('currency') == 'USD' and e.get('impact') in ['LOW', 'MED']
    ]
    
    if len(usd_yellow_events) < min_events:
        return False
    
    # Cuenta eventos en la ventana de tiempo (±window_minutes/2)
    window_start = now_utc - timedelta(minutes=window_minutes / 2)
    window_end = now_utc + timedelta(minutes=window_minutes / 2)
    
    events_in_window = 0
    for event in usd_yellow_events:
        try:
            event_timestamp_str = event.get('timestamp_utc', '')
            if event_timestamp_str.endswith('Z'):
                event_timestamp_str = event_timestamp_str[:-1] + '+00:00'
            event_dt = datetime.fromisoformat(event_timestamp_str.replace('Z', '+00:00'))
            
            if window_start <= event_dt <= window_end:
                events_in_window += 1
        except Exception:
            continue
    
    return events_in_window >= min_events


def is_eia_event(event: Dict) -> bool:
    """
    Verifica si un evento es de tipo EIA.
    
    Args:
        event: Diccionario con información del evento
    
    Returns:
        True si es evento EIA
    """
    title = event.get('title', '').upper()
    eia_keywords = ['EIA', 'CRUDE OIL STOCKS', 'GASOLINE STOCKS', 'DISTILLATE']
    return any(keyword in title for keyword in eia_keywords)


def should_block_new_entries(
    now_utc: datetime,
    symbol: str,
    events_today: List[Dict],
    spread: float,
    atr_ratio: float,
    open_positions_count: int,
    daily_dd_pct: float,
    config: Dict
) -> Tuple[bool, str, List[str], Optional[datetime]]:
    """
    Determina si se deben bloquear nuevas entradas basado en múltiples factores.
    
    Args:
        now_utc: Tiempo actual en UTC
        symbol: Símbolo a operar (ej: XAUUSD)
        events_today: Lista de eventos del día
        spread: Spread actual en puntos
        atr_ratio: Ratio ATR actual / ATR promedio
        open_positions_count: Número de posiciones abiertas
        daily_dd_pct: Drawdown diario porcentual
        config: Diccionario con configuración
    
    Returns:
        Tupla (blocked, mode, reasons, cooldown_until_utc):
        - blocked: True si se deben bloquear nuevas entradas
        - mode: Modo actual (NORMAL, CONSERVATIVE, BLOCKED)
        - reasons: Lista de razones del bloqueo
        - cooldown_until_utc: Fecha UTC hasta cuando está en cooldown (None si no aplica)
    """
    reasons = []
    mode = "NORMAL"
    blocked = False
    cooldown_until_utc = None
    
    # Obtener configuración
    spread_max = config.get('SPREAD_MAX', 50.0)
    atr_max_ratio = config.get('ATR_MAX_RATIO', 2.0)
    daily_dd_limit = config.get('DAILY_DD_LIMIT', -5.0)
    news_window_minutes = config.get('NEWS_USD_WINDOW_MINUTES', 90)
    news_min_events = config.get('NEWS_MIN_EVENTS_FOR_CLUSTER', 2)
    news_block_pre = config.get('NEWS_BLOCK_PRE_MINUTES', 15)
    news_block_post = config.get('NEWS_BLOCK_POST_MINUTES', 30)
    eia_block_pre = config.get('EIA_BLOCK_PRE_MINUTES', 30)
    eia_block_post = config.get('EIA_BLOCK_POST_MINUTES', 30)
    news_cooldown_minutes = config.get('NEWS_COOLDOWN_MINUTES', 20)
    
    # (1) Verificar cluster de noticias USD amarillas
    has_cluster = detect_usd_yellow_cluster(events_today, now_utc, news_window_minutes, news_min_events)
    
    if has_cluster:
        mode = "CONSERVATIVE"
        
        # Verifica si estamos dentro de la ventana de bloqueo de algún evento USD LOW/MED
        usd_yellow_events = [
            e for e in events_today
            if e.get('currency') == 'USD' and e.get('impact') in ['LOW', 'MED']
        ]
        
        for event in usd_yellow_events:
            try:
                event_timestamp_str = event.get('timestamp_utc', '')
                if event_timestamp_str.endswith('Z'):
                    event_timestamp_str = event_timestamp_str[:-1] + '+00:00'
                event_dt = datetime.fromisoformat(event_timestamp_str.replace('Z', '+00:00'))
                
                block_start = event_dt - timedelta(minutes=news_block_pre)
                block_end = event_dt + timedelta(minutes=news_block_post)
                
                if block_start <= now_utc <= block_end:
                    blocked = True
                    reasons.append(f"Cluster de noticias USD cerca de {event.get('title', 'evento')}")
                    
                    # Activar cooldown después del evento
                    cooldown_end = event_dt + timedelta(minutes=news_cooldown_minutes)
                    if now_utc < cooldown_end:
                        if cooldown_until_utc is None or cooldown_end > cooldown_until_utc:
                            cooldown_until_utc = cooldown_end
            except Exception:
                continue
    
    # (2) Verificar eventos EIA para XAUUSD
    if symbol.upper() in ['XAUUSD', 'XAUUSD.VIP', 'GOLD']:
        for event in events_today:
            if is_eia_event(event):
                try:
                    event_timestamp_str = event.get('timestamp_utc', '')
                    if event_timestamp_str.endswith('Z'):
                        event_timestamp_str = event_timestamp_str[:-1] + '+00:00'
                    event_dt = datetime.fromisoformat(event_timestamp_str.replace('Z', '+00:00'))
                    
                    block_start = event_dt - timedelta(minutes=eia_block_pre)
                    block_end = event_dt + timedelta(minutes=eia_block_post)
                    
                    if block_start <= now_utc <= block_end:
                        blocked = True
                        reasons.append(f"Evento EIA: {event.get('title', 'EIA')}")
                except Exception:
                    continue
    
    # (3) Verificar spread
    if spread > spread_max:
        blocked = True
        mode = "BLOCKED"
        reasons.append(f"Spread alto: {spread:.2f} > {spread_max:.2f}")
    
    # (4) Verificar volatilidad (ATR)
    if atr_ratio > atr_max_ratio:
        blocked = True
        mode = "BLOCKED"
        reasons.append(f"Volatilidad alta: ATR ratio {atr_ratio:.2f} > {atr_max_ratio:.2f}")
    
    # (5) Verificar drawdown diario (kill switch)
    if daily_dd_pct <= daily_dd_limit:  # Negativo, así que <= significa más pérdida
        blocked = True
        mode = "BLOCKED"
        reasons.append(f"Drawdown diario excedido: {daily_dd_pct:.2f}% <= {daily_dd_limit:.2f}%")
    
    # Si hay cooldown activo, bloquear
    if cooldown_until_utc and now_utc < cooldown_until_utc:
        blocked = True
        if "Cooldown post-noticia" not in reasons:
            reasons.append(f"Cooldown activo hasta {cooldown_until_utc.strftime('%H:%M:%S')} UTC")
    
    return blocked, mode, reasons, cooldown_until_utc

