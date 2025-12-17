"""
news/provider.py - Proveedor de eventos de noticias económicas

Proporciona eventos de noticias económicas desde diferentes fuentes.
Por ahora usa un mock que lee desde JSON, pero puede extenderse a APIs reales.
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime, date
from pathlib import Path


class MockNewsProvider:
    """
    Proveedor mock de noticias que lee desde un archivo JSON.
    
    En el futuro puede reemplazarse por integraciones reales con:
    - ForexFactory API
    - Investing.com
    - TradingEconomics
    - etc.
    """
    
    def __init__(self, json_path: str = "data/news_events.json"):
        """
        Inicializa el proveedor mock.
        
        Args:
            json_path: Ruta al archivo JSON con eventos de noticias
        """
        self.json_path = json_path
        self.project_root = Path(__file__).parent.parent
        self.full_path = self.project_root / json_path
        
    def get_events_for_day(self, date_utc: date) -> List[Dict]:
        """
        Obtiene todos los eventos de noticias para un día específico.
        
        Args:
            date_utc: Fecha en UTC para la cual obtener eventos
        
        Returns:
            Lista de eventos, cada uno con:
            {
                "timestamp_utc": "2025-12-17T13:00:00Z",
                "currency": "USD",
                "impact": "LOW|MED|HIGH",
                "title": "EIA Crude Oil Stocks"
            }
        """
        if not self.full_path.exists():
            # Si no existe el archivo, retorna lista vacía
            return []
        
        try:
            with open(self.full_path, 'r', encoding='utf-8') as f:
                all_events = json.load(f)
            
            # Filtra eventos del día solicitado
            target_date_str = date_utc.strftime('%Y-%m-%d')
            day_events = []
            
            for event in all_events:
                event_timestamp = event.get('timestamp_utc', '')
                if event_timestamp.startswith(target_date_str):
                    day_events.append(event)
            
            return day_events
            
        except Exception as e:
            # Si hay error leyendo el archivo, retorna lista vacía
            print(f"⚠️ Error al leer eventos de noticias: {e}")
            return []
    
    def get_events_for_timeframe(self, start_utc: datetime, end_utc: datetime) -> List[Dict]:
        """
        Obtiene eventos en un rango de tiempo.
        
        Args:
            start_utc: Inicio del rango (datetime UTC)
            end_utc: Fin del rango (datetime UTC)
        
        Returns:
            Lista de eventos en el rango
        """
        if not self.full_path.exists():
            return []
        
        try:
            with open(self.full_path, 'r', encoding='utf-8') as f:
                all_events = json.load(f)
            
            timeframe_events = []
            
            for event in all_events:
                event_timestamp_str = event.get('timestamp_utc', '')
                try:
                    # Parsear timestamp (formato ISO: "2025-12-17T13:00:00Z")
                    if event_timestamp_str.endswith('Z'):
                        event_timestamp_str = event_timestamp_str[:-1] + '+00:00'
                    event_dt = datetime.fromisoformat(event_timestamp_str.replace('Z', '+00:00'))
                    
                    if start_utc <= event_dt <= end_utc:
                        timeframe_events.append(event)
                except Exception:
                    continue
            
            return timeframe_events
            
        except Exception as e:
            print(f"⚠️ Error al leer eventos de noticias: {e}")
            return []


# Instancia global del proveedor
_news_provider = None

def get_news_provider() -> MockNewsProvider:
    """Obtiene la instancia global del proveedor de noticias"""
    global _news_provider
    if _news_provider is None:
        _news_provider = MockNewsProvider()
    return _news_provider

