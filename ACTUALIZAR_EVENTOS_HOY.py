"""
ACTUALIZAR_EVENTOS_HOY.py - Actualiza news_events.json con eventos de hoy

Ejecuta este script para agregar eventos de noticias para el día actual.
"""

import json
import os
from datetime import datetime, timedelta

project_root = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(project_root, "data", "news_events.json")

# Obtener fecha de hoy en UTC
today = datetime.utcnow().date()
today_str = today.strftime('%Y-%m-%d')

print(f"📅 Actualizando eventos para: {today_str} UTC")
print()

# Eventos de ejemplo para hoy
# Ajusta estos según los eventos reales del día
events_today = [
    {
        "timestamp_utc": f"{today_str}T13:30:00Z",
        "currency": "USD",
        "impact": "MED",
        "title": "Retail Sales"
    },
    {
        "timestamp_utc": f"{today_str}T14:00:00Z",
        "currency": "USD",
        "impact": "LOW",
        "title": "Business Inventories"
    },
    {
        "timestamp_utc": f"{today_str}T15:30:00Z",
        "currency": "USD",
        "impact": "HIGH",
        "title": "EIA Crude Oil Stocks"
    }
]

# Cargar eventos existentes
all_events = []
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        all_events = json.load(f)

# Filtrar eventos que no son de hoy
other_events = [e for e in all_events if not e.get('timestamp_utc', '').startswith(today_str)]

# Combinar eventos de otros días con eventos de hoy
updated_events = other_events + events_today

# Ordenar por timestamp
updated_events.sort(key=lambda x: x.get('timestamp_utc', ''))

# Guardar
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(updated_events, f, indent=2, ensure_ascii=False)

print(f"✅ Actualizado: {len(events_today)} eventos para hoy")
print(f"📊 Total de eventos en JSON: {len(updated_events)}")
print()
print("Eventos de hoy:")
for event in events_today:
    print(f"  - {event.get('title', 'N/A')} a las {event.get('timestamp_utc', 'N/A')} ({event.get('impact', 'N/A')})")

