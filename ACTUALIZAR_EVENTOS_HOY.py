"""
ACTUALIZAR_EVENTOS_HOY.py - Actualiza news_events.json con eventos de hoy (VERSIÓN SEGURA)

Ejecuta este script para agregar eventos de noticias para el día actual.
Usa file locking para evitar conflictos con el bot que está leyendo.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path


def update_news_events_safe(events_today: list, json_path: str = "data/news_events.json") -> bool:
    """
    Actualiza el archivo JSON de noticias de forma segura usando file locking.
    
    Args:
        events_today: Lista de eventos para hoy
        json_path: Ruta al archivo JSON
    
    Returns:
        True si se actualizó exitosamente, False si hubo error
    """
    project_root = Path(__file__).parent
    full_path = project_root / json_path
    lock_file_path = full_path.parent / f"{full_path.name}.lock"
    
    # Crear directorio si no existe
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    max_retries = 10
    retry_delay = 0.5  # 500ms
    
    for attempt in range(max_retries):
        try:
            # Verificar si hay lock (bot está leyendo)
            if lock_file_path.exists():
                if attempt < max_retries - 1:
                    print(f"⏳ Esperando... (intento {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    continue
                print(f"⚠️ No se pudo obtener lock después de {max_retries} intentos")
                return False
            
            # Crear lock file
            try:
                lock_file_path.touch()
            except Exception:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return False
            
            try:
                # Leer eventos existentes
                all_events = []
                if full_path.exists():
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if content.strip():
                                all_events = json.loads(content)
                    except (json.JSONDecodeError, IOError):
                        # Si el archivo está corrupto, empezar de nuevo
                        all_events = []
                
                # Filtrar eventos que no son de hoy
                today_str = datetime.utcnow().date().strftime('%Y-%m-%d')
                other_events = [
                    e for e in all_events 
                    if not e.get('timestamp_utc', '').startswith(today_str)
                ]
                
                # Combinar eventos
                updated_events = other_events + events_today
                updated_events.sort(key=lambda x: x.get('timestamp_utc', ''))
                
                # Escribir a archivo temporal primero
                temp_path = full_path.with_suffix('.tmp')
                with open(temp_path, 'w', encoding='utf-8') as f:
                    json.dump(updated_events, f, indent=2, ensure_ascii=False)
                
                # Reemplazar archivo original (operación atómica)
                if os.name == 'nt':  # Windows
                    # En Windows, reemplazar puede fallar si está abierto
                    # Intentar varias veces
                    for replace_attempt in range(3):
                        try:
                            if full_path.exists():
                                os.remove(full_path)
                            os.rename(temp_path, full_path)
                            break
                        except PermissionError:
                            if replace_attempt < 2:
                                time.sleep(0.2)
                            else:
                                raise
                else:  # Linux/Mac
                    temp_path.replace(full_path)
                
                print(f"✅ Actualizado: {len(events_today)} eventos para hoy")
                print(f"📊 Total de eventos: {len(updated_events)}")
                return True
                
            finally:
                # Siempre eliminar lock file
                try:
                    if lock_file_path.exists():
                        lock_file_path.unlink()
                except Exception:
                    pass
                    
        except Exception as e:
            print(f"⚠️ Error al actualizar noticias (intento {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                # Limpiar lock si existe
                try:
                    if lock_file_path.exists():
                        lock_file_path.unlink()
                except Exception:
                    pass
                return False
    
    return False


if __name__ == "__main__":
    # Obtener fecha de hoy en UTC
    today = datetime.utcnow().date()
    today_str = today.strftime('%Y-%m-%d')
    
    print(f"📅 Actualizando eventos para: {today_str} UTC")
    print()
    
    # Eventos de ejemplo para hoy
    # ⚠️ IMPORTANTE: Edita estos eventos según las noticias reales del día
    # Puedes obtenerlas de: https://www.forexfactory.com/calendar o similar
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
    
    # Actualizar de forma segura
    success = update_news_events_safe(events_today)
    
    if success:
        print()
        print("Eventos de hoy:")
        for event in events_today:
            print(f"  - {event.get('title', 'N/A')} a las {event.get('timestamp_utc', 'N/A')} ({event.get('impact', 'N/A')})")
        print()
        print("✅ ¡Listo! El bot puede leer estos eventos de forma segura.")
    else:
        print()
        print("❌ Error al actualizar. Intenta de nuevo en unos segundos.")





