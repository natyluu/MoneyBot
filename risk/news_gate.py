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
            # Parsear timestamp UTC (formato ISO con Z)
            if event_timestamp_str.endswith('Z'):
                event_timestamp_str = event_timestamp_str[:-1] + '+00:00'
            elif '+' not in event_timestamp_str and 'Z' not in event_timestamp_str:
                # Si no tiene timezone, asumir UTC
                event_timestamp_str = event_timestamp_str + '+00:00'
            else:
                event_timestamp_str = event_timestamp_str.replace('Z', '+00:00')
            
            event_dt = datetime.fromisoformat(event_timestamp_str)
            # Convertir a naive datetime (sin timezone) para comparar
            if event_dt.tzinfo is not None:
                event_dt = event_dt.replace(tzinfo=None)
            
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


def is_fed_speech_event(event: Dict) -> bool:
    """
    Verifica si un evento es un discurso de la Fed.
    
    Args:
        event: Diccionario con información del evento
    
    Returns:
        True si es discurso de Fed
    """
    title = event.get('title', '').upper()
    fed_keywords = ['FED', 'FOMC', 'POWELL', 'SPEECH', 'TESTIMONY', 'BOSTIC', 'WALLER']
    return any(keyword in title for keyword in fed_keywords)


def is_high_impact_event(event: Dict) -> bool:
    """
    Verifica si un evento es de alto impacto económico.
    
    Args:
        event: Diccionario con información del evento
    
    Returns:
        True si es evento de alto impacto
    """
    impact = event.get('impact', '').upper()
    if impact == 'HIGH':
        return True
    
    # También considerar eventos MED importantes
    title = event.get('title', '').upper()
    high_impact_keywords = [
        'CPI', 'INFLATION', 'NFP', 'NON-FARM PAYROLLS', 'GDP',
        'INTEREST RATE', 'RATE DECISION', 'FOMC', 'FED',
        'EMPLOYMENT', 'UNEMPLOYMENT', 'RETAIL SALES'
    ]
    return any(keyword in title for keyword in high_impact_keywords)


def get_relevant_currencies_for_symbol(symbol: str) -> List[str]:
    """
    Obtiene las divisas relevantes para un símbolo.
    Para XAUUSD, las noticias de USD, GBP, EUR pueden afectar.
    
    Args:
        symbol: Símbolo a operar
    
    Returns:
        Lista de códigos de divisas relevantes
    """
    symbol_upper = symbol.upper()
    
    # Para XAUUSD, las noticias de USD, GBP, EUR son relevantes
    if 'XAU' in symbol_upper or 'GOLD' in symbol_upper:
        return ['USD', 'GBP', 'EUR']
    
    # Para otros símbolos, extraer las divisas del par
    # Por ejemplo, EURUSD -> ['EUR', 'USD']
    if len(symbol_upper) >= 6:
        base = symbol_upper[:3]
        quote = symbol_upper[3:6]
        return [base, quote]
    
    # Default: USD siempre relevante
    return ['USD']


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
    # Tiempos más largos para eventos HIGH
    high_news_block_pre = config.get('HIGH_NEWS_BLOCK_PRE_MINUTES', 30)
    high_news_block_post = config.get('HIGH_NEWS_BLOCK_POST_MINUTES', 60)
    eia_block_pre = config.get('EIA_BLOCK_PRE_MINUTES', 30)
    eia_block_post = config.get('EIA_BLOCK_POST_MINUTES', 30)
    news_cooldown_minutes = config.get('NEWS_COOLDOWN_MINUTES', 20)
    high_news_cooldown_minutes = config.get('HIGH_NEWS_COOLDOWN_MINUTES', 30)
    
    # Obtener divisas relevantes para el símbolo
    relevant_currencies = get_relevant_currencies_for_symbol(symbol)
    
    # Asegurar que now_utc es naive (sin timezone) para comparar
    if now_utc.tzinfo is not None:
        now_utc_naive = now_utc.replace(tzinfo=None)
    else:
        now_utc_naive = now_utc
    
    # (1) Verificar eventos HIGH individuales (cualquier divisa relevante)
    for event in events_today:
        event_currency = event.get('currency', '')
        event_impact = event.get('impact', '').upper()
        
        # Solo considerar eventos de divisas relevantes
        if event_currency not in relevant_currencies:
            continue
        
        # Bloquear eventos HIGH individuales
        if event_impact == 'HIGH' or is_high_impact_event(event):
            try:
                event_timestamp_str = event.get('timestamp_utc', '')
                # Parsear timestamp UTC
                if event_timestamp_str.endswith('Z'):
                    event_timestamp_str = event_timestamp_str[:-1] + '+00:00'
                elif '+' not in event_timestamp_str and 'Z' not in event_timestamp_str:
                    event_timestamp_str = event_timestamp_str + '+00:00'
                else:
                    event_timestamp_str = event_timestamp_str.replace('Z', '+00:00')
                
                event_dt = datetime.fromisoformat(event_timestamp_str)
                if event_dt.tzinfo is not None:
                    event_dt = event_dt.replace(tzinfo=None)
                
                # Usar tiempos más largos para eventos HIGH
                block_pre = high_news_block_pre if event_impact == 'HIGH' else news_block_pre
                block_post = high_news_block_post if event_impact == 'HIGH' else news_block_post
                
                block_start = event_dt - timedelta(minutes=block_pre)
                block_end = event_dt + timedelta(minutes=block_post)
                
                if block_start <= now_utc_naive <= block_end:
                    blocked = True
                    mode = "BLOCKED"
                    reasons.append(f"Evento HIGH {event_currency}: {event.get('title', 'evento')}")
                    
                    # Cooldown más largo para eventos HIGH
                    cooldown_mins = high_news_cooldown_minutes if event_impact == 'HIGH' else news_cooldown_minutes
                    cooldown_end = event_dt + timedelta(minutes=cooldown_mins)
                    if now_utc_naive < cooldown_end:
                        if cooldown_until_utc is None or cooldown_end > cooldown_until_utc:
                            cooldown_until_utc = cooldown_end
            except Exception as e:
                import sys
                print(f"⚠️ Error al procesar evento HIGH: {e}", file=sys.stderr)
                continue
    
    # (2) Verificar eventos MED importantes (Fed speeches, CPI, etc.)
    for event in events_today:
        event_currency = event.get('currency', '')
        event_impact = event.get('impact', '').upper()
        
        # Solo considerar eventos de divisas relevantes
        if event_currency not in relevant_currencies:
            continue
        
        # Bloquear eventos MED importantes
        if event_impact == 'MED' and (is_fed_speech_event(event) or is_high_impact_event(event)):
            try:
                event_timestamp_str = event.get('timestamp_utc', '')
                # Parsear timestamp UTC
                if event_timestamp_str.endswith('Z'):
                    event_timestamp_str = event_timestamp_str[:-1] + '+00:00'
                elif '+' not in event_timestamp_str and 'Z' not in event_timestamp_str:
                    event_timestamp_str = event_timestamp_str + '+00:00'
                else:
                    event_timestamp_str = event_timestamp_str.replace('Z', '+00:00')
                
                event_dt = datetime.fromisoformat(event_timestamp_str)
                if event_dt.tzinfo is not None:
                    event_dt = event_dt.replace(tzinfo=None)
                
                # Usar tiempos similares a HIGH para eventos MED importantes
                block_start = event_dt - timedelta(minutes=high_news_block_pre)
                block_end = event_dt + timedelta(minutes=high_news_block_post)
                
                if block_start <= now_utc_naive <= block_end:
                    blocked = True
                    mode = "BLOCKED"
                    reasons.append(f"Evento MED importante {event_currency}: {event.get('title', 'evento')}")
                    
                    cooldown_end = event_dt + timedelta(minutes=high_news_cooldown_minutes)
                    if now_utc_naive < cooldown_end:
                        if cooldown_until_utc is None or cooldown_end > cooldown_until_utc:
                            cooldown_until_utc = cooldown_end
            except Exception as e:
                import sys
                print(f"⚠️ Error al procesar evento MED importante: {e}", file=sys.stderr)
                continue
    
    # (3) Verificar cluster de noticias USD amarillas
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
                # Parsear timestamp UTC (formato ISO con Z)
                if event_timestamp_str.endswith('Z'):
                    event_timestamp_str = event_timestamp_str[:-1] + '+00:00'
                elif '+' not in event_timestamp_str and 'Z' not in event_timestamp_str:
                    # Si no tiene timezone, asumir UTC
                    event_timestamp_str = event_timestamp_str + '+00:00'
                else:
                    event_timestamp_str = event_timestamp_str.replace('Z', '+00:00')
                
                event_dt = datetime.fromisoformat(event_timestamp_str)
                # Convertir a naive datetime (sin timezone) para comparar
                if event_dt.tzinfo is not None:
                    event_dt = event_dt.replace(tzinfo=None)
                
                block_start = event_dt - timedelta(minutes=news_block_pre)
                block_end = event_dt + timedelta(minutes=news_block_post)
                
                if block_start <= now_utc_naive <= block_end:
                    blocked = True
                    reasons.append(f"Cluster de noticias USD cerca de {event.get('title', 'evento')}")
                    
                    # Activar cooldown después del evento
                    cooldown_end = event_dt + timedelta(minutes=news_cooldown_minutes)
                    if now_utc_naive < cooldown_end:
                        if cooldown_until_utc is None or cooldown_end > cooldown_until_utc:
                            cooldown_until_utc = cooldown_end
            except Exception as e:
                # Log error pero continúa
                import sys
                print(f"⚠️ Error al procesar evento USD: {e}", file=sys.stderr)
                continue
    
    # (4) Verificar eventos EIA para XAUUSD
    if symbol.upper() in ['XAUUSD', 'XAUUSD.VIP', 'GOLD']:
        for event in events_today:
            if is_eia_event(event):
                try:
                    event_timestamp_str = event.get('timestamp_utc', '')
                    # Parsear timestamp UTC (formato ISO con Z)
                    if event_timestamp_str.endswith('Z'):
                        event_timestamp_str = event_timestamp_str[:-1] + '+00:00'
                    elif '+' not in event_timestamp_str and 'Z' not in event_timestamp_str:
                        # Si no tiene timezone, asumir UTC
                        event_timestamp_str = event_timestamp_str + '+00:00'
                    else:
                        event_timestamp_str = event_timestamp_str.replace('Z', '+00:00')
                    
                    event_dt = datetime.fromisoformat(event_timestamp_str)
                    # Convertir a naive datetime (sin timezone) para comparar
                    if event_dt.tzinfo is not None:
                        event_dt = event_dt.replace(tzinfo=None)
                    
                    block_start = event_dt - timedelta(minutes=eia_block_pre)
                    block_end = event_dt + timedelta(minutes=eia_block_post)
                    
                    if block_start <= now_utc_naive <= block_end:
                        blocked = True
                        reasons.append(f"Evento EIA: {event.get('title', 'EIA')}")
                except Exception as e:
                    # Log error pero continúa
                    import sys
                    print(f"⚠️ Error al procesar evento EIA: {e}", file=sys.stderr)
                    continue
    
    # (5) Verificar spread
    if spread > spread_max:
        blocked = True
        mode = "BLOCKED"
        reasons.append(f"Spread alto: {spread:.2f} > {spread_max:.2f}")
    
    # (6) Verificar volatilidad (ATR)
    if atr_ratio > atr_max_ratio:
        blocked = True
        mode = "BLOCKED"
        reasons.append(f"Volatilidad alta: ATR ratio {atr_ratio:.2f} > {atr_max_ratio:.2f}")
    
    # (7) Verificar drawdown diario (kill switch)
    if daily_dd_pct <= daily_dd_limit:  # Negativo, así que <= significa más pérdida
        blocked = True
        mode = "BLOCKED"
        reasons.append(f"Drawdown diario excedido: {daily_dd_pct:.2f}% <= {daily_dd_limit:.2f}%")
    
    # Si hay cooldown activo, bloquear
    if cooldown_until_utc and now_utc_naive < cooldown_until_utc:
        blocked = True
        if "Cooldown post-noticia" not in reasons:
            reasons.append(f"Cooldown activo hasta {cooldown_until_utc.strftime('%H:%M:%S')} UTC")
    
    return blocked, mode, reasons, cooldown_until_utc
