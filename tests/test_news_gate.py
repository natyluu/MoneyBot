"""
tests/test_news_gate.py - Tests para News Risk Gate
"""

import unittest
from datetime import datetime, timedelta
from risk.news_gate import (
    detect_usd_yellow_cluster,
    is_eia_event,
    should_block_new_entries
)


class TestNewsGate(unittest.TestCase):
    """Tests para el News Risk Gate"""
    
    def test_detect_usd_yellow_cluster(self):
        """Test detección de cluster de noticias USD"""
        now = datetime.utcnow()
        
        # Crear eventos de prueba dentro de la ventana (45 minutos antes y después de now)
        # La ventana es ±45 minutos (90/2)
        events = [
            {
                "timestamp_utc": (now - timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "currency": "USD",
                "impact": "LOW",
                "title": "Test Event 1"
            },
            {
                "timestamp_utc": (now - timedelta(minutes=20)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "currency": "USD",
                "impact": "MED",
                "title": "Test Event 2"
            }
        ]
        
        # Debe detectar cluster (2 eventos en ventana de 90 minutos centrada en now)
        result = detect_usd_yellow_cluster(events, now, window_minutes=90, min_events=2)
        self.assertTrue(result, f"Debería detectar cluster con 2 eventos en ventana. Now: {now}, Events: {events}")
        
        # No debe detectar cluster con solo 1 evento
        result = detect_usd_yellow_cluster(events[:1], now, window_minutes=90, min_events=2)
        self.assertFalse(result)
    
    def test_is_eia_event(self):
        """Test detección de eventos EIA"""
        # Evento EIA
        eia_event = {
            "title": "EIA Crude Oil Stocks",
            "currency": "USD",
            "impact": "MED"
        }
        self.assertTrue(is_eia_event(eia_event))
        
        # Evento no EIA
        normal_event = {
            "title": "Retail Sales",
            "currency": "USD",
            "impact": "HIGH"
        }
        self.assertFalse(is_eia_event(normal_event))
    
    def test_should_block_spread(self):
        """Test bloqueo por spread alto"""
        config = {
            'SPREAD_MAX': 50.0,
            'ATR_MAX_RATIO': 2.0,
            'DAILY_DD_LIMIT': -5.0,
            'NEWS_USD_WINDOW_MINUTES': 90,
            'NEWS_MIN_EVENTS_FOR_CLUSTER': 2,
            'NEWS_BLOCK_PRE_MINUTES': 15,
            'NEWS_BLOCK_POST_MINUTES': 30,
            'NEWS_COOLDOWN_MINUTES': 20,
            'EIA_BLOCK_PRE_MINUTES': 30,
            'EIA_BLOCK_POST_MINUTES': 30
        }
        
        blocked, mode, reasons, cooldown = should_block_new_entries(
            now_utc=datetime.utcnow(),
            symbol="XAUUSD",
            events_today=[],
            spread=60.0,  # Spread alto
            atr_ratio=1.0,
            open_positions_count=0,
            daily_dd_pct=0.0,
            config=config
        )
        
        self.assertTrue(blocked)
        self.assertEqual(mode, "BLOCKED")
        self.assertTrue(any("Spread alto" in r for r in reasons))
    
    def test_should_block_atr(self):
        """Test bloqueo por volatilidad alta"""
        config = {
            'SPREAD_MAX': 50.0,
            'ATR_MAX_RATIO': 2.0,
            'DAILY_DD_LIMIT': -5.0,
            'NEWS_USD_WINDOW_MINUTES': 90,
            'NEWS_MIN_EVENTS_FOR_CLUSTER': 2,
            'NEWS_BLOCK_PRE_MINUTES': 15,
            'NEWS_BLOCK_POST_MINUTES': 30,
            'NEWS_COOLDOWN_MINUTES': 20,
            'EIA_BLOCK_PRE_MINUTES': 30,
            'EIA_BLOCK_POST_MINUTES': 30
        }
        
        blocked, mode, reasons, cooldown = should_block_new_entries(
            now_utc=datetime.utcnow(),
            symbol="XAUUSD",
            events_today=[],
            spread=10.0,
            atr_ratio=3.0,  # Volatilidad alta
            open_positions_count=0,
            daily_dd_pct=0.0,
            config=config
        )
        
        self.assertTrue(blocked)
        self.assertEqual(mode, "BLOCKED")
        self.assertTrue(any("Volatilidad alta" in r for r in reasons))
    
    def test_should_block_eia(self):
        """Test bloqueo por evento EIA"""
        now = datetime.utcnow()
        config = {
            'SPREAD_MAX': 50.0,
            'ATR_MAX_RATIO': 2.0,
            'DAILY_DD_LIMIT': -5.0,
            'NEWS_USD_WINDOW_MINUTES': 90,
            'NEWS_MIN_EVENTS_FOR_CLUSTER': 2,
            'NEWS_BLOCK_PRE_MINUTES': 15,
            'NEWS_BLOCK_POST_MINUTES': 30,
            'NEWS_COOLDOWN_MINUTES': 20,
            'EIA_BLOCK_PRE_MINUTES': 30,
            'EIA_BLOCK_POST_MINUTES': 30
        }
        
        # Evento EIA dentro de la ventana de bloqueo
        # El evento fue hace 10 minutos, estamos dentro de la ventana [-30m, +30m]
        eia_time = now - timedelta(minutes=10)  # Evento hace 10 minutos
        events = [
            {
                "timestamp_utc": eia_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "currency": "USD",
                "impact": "MED",
                "title": "EIA Crude Oil Stocks"
            }
        ]
        
        blocked, mode, reasons, cooldown = should_block_new_entries(
            now_utc=now,
            symbol="XAUUSD",
            events_today=events,
            spread=10.0,
            atr_ratio=1.0,
            open_positions_count=0,
            daily_dd_pct=0.0,
            config=config
        )
        
        self.assertTrue(blocked, f"Debería estar bloqueado. Now: {now}, EIA time: {eia_time}, Reasons: {reasons}")
        self.assertTrue(any("EIA" in r for r in reasons), f"Debería mencionar EIA en reasons: {reasons}")


if __name__ == '__main__':
    unittest.main()

