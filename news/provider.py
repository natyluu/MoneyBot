"""
news/provider.py - Proveedor de eventos de noticias económicas

Proporciona eventos de noticias económicas desde diferentes fuentes.
Versión segura con cache y file locking para evitar conflictos de lectura/escritura.
"""

import json
import os
import time
import threading
from typing import List, Dict, Optional
from datetime import datetime, date
from pathlib import Path


class SafeNewsProvider:
    """
    Proveedor seguro de noticias con cache y file locking.
    
    Características:
    - Cache en memoria para evitar leer archivo constantemente
    - File locking para evitar conflictos de lectura/escritura
    - Fallback a cache si el archivo está bloqueado
    - Recarga automática del cache cada X minutos
    - Nunca bloquea el bot si hay errores
    """
    
    def __init__(self, json_path: str = "data/news_events.json", cache_ttl: int = 300):
        """
        Inicializa el proveedor seguro.
        
        Args:
            json_path: Ruta al archivo JSON con eventos de noticias
            cache_ttl: Tiempo de vida del cache en segundos (default: 5 minutos)
        """
        self.json_path = json_path
        self.project_root = Path(__file__).parent.parent
        self.full_path = self.project_root / json_path
        self.cache_ttl = cache_ttl
        
        # Cache en memoria
        self._cache: Optional[List[Dict]] = None
        self._cache_timestamp: float = 0
        self._cache_lock = threading.RLock()  # Lock para thread-safety
        
        # Lock file para escritura (Windows compatible)
        self._lock_file_path = self.full_path.parent / f"{self.full_path.name}.lock"
        
        # Cargar cache inicial
        self._reload_cache()
    
    def _is_cache_valid(self) -> bool:
        """Verifica si el cache es válido (no expirado)"""
        if self._cache is None:
            return False
        
        elapsed = time.time() - self._cache_timestamp
        return elapsed < self.cache_ttl
    
    def _reload_cache(self) -> bool:
        """
        Recarga el cache desde el archivo JSON de forma segura.
        
        Returns:
            True si se recargó exitosamente, False si hubo error
        """
        with self._cache_lock:
            # Si el archivo no existe, mantener cache vacío
            if not self.full_path.exists():
                self._cache = []
                self._cache_timestamp = time.time()
                return True
            
            # Intentar leer con file locking
            max_retries = 3
            retry_delay = 0.1  # 100ms
            
            for attempt in range(max_retries):
                try:
                    # Verificar si hay lock file (alguien está escribiendo)
                    if self._lock_file_path.exists():
                        # Esperar un poco si es el primer intento
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay)
                            continue
                        # Si después de retries sigue bloqueado, usar cache anterior
                        if self._cache is not None:
                            return True  # Usar cache anterior
                        return False
                    
                    # Leer archivo con timeout
                    start_time = time.time()
                    while time.time() - start_time < 1.0:  # Timeout de 1 segundo
                        try:
                            with open(self.full_path, 'r', encoding='utf-8') as f:
                                # Intentar leer todo el contenido de una vez
                                content = f.read()
                                if not content.strip():
                                    # Archivo vacío, usar cache anterior o lista vacía
                                    if self._cache is None:
                                        self._cache = []
                                    self._cache_timestamp = time.time()
                                    return True
                                
                                # Validar JSON
                                all_events = json.loads(content)
                                
                                # Validar estructura
                                if not isinstance(all_events, list):
                                    raise ValueError("JSON debe ser una lista")
                                
                                # Actualizar cache
                                self._cache = all_events
                                self._cache_timestamp = time.time()
                                return True
                                
                        except (json.JSONDecodeError, ValueError) as e:
                            # JSON corrupto, usar cache anterior si existe
                            if self._cache is not None:
                                print(f"⚠️ JSON corrupto, usando cache anterior: {e}")
                                return True
                            # Si no hay cache, retornar lista vacía
                            self._cache = []
                            self._cache_timestamp = time.time()
                            return False
                        except IOError:
                            # Archivo bloqueado, esperar un poco
                            if attempt < max_retries - 1:
                                time.sleep(retry_delay)
                                continue
                            # Usar cache anterior si existe
                            if self._cache is not None:
                                return True
                            return False
                    
                    # Timeout, usar cache anterior
                    if self._cache is not None:
                        return True
                    return False
                    
                except Exception as e:
                    # Cualquier otro error, usar cache anterior si existe
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    
                    if self._cache is not None:
                        print(f"⚠️ Error al recargar cache, usando cache anterior: {e}")
                        return True
                    # Si no hay cache, crear uno vacío
                    self._cache = []
                    self._cache_timestamp = time.time()
                    return False
            
            # Si llegamos aquí, todos los intentos fallaron
            if self._cache is not None:
                return True  # Usar cache anterior
            return False
    
    def get_events_for_day(self, date_utc: date) -> List[Dict]:
        """
        Obtiene todos los eventos de noticias para un día específico.
        
        Esta función es thread-safe y nunca lanza excepciones.
        Si hay error, retorna lista vacía.
        
        Args:
            date_utc: Fecha en UTC para la cual obtener eventos
        
        Returns:
            Lista de eventos del día, o lista vacía si hay error
        """
        try:
            # Verificar si el cache necesita recarga
            if not self._is_cache_valid():
                self._reload_cache()
            
            # Usar cache (siempre válido o fallback)
            with self._cache_lock:
                if self._cache is None:
                    # Si no hay cache, intentar cargar una vez más
                    if not self._reload_cache():
                        return []  # Fallback: lista vacía
                
                # Filtrar eventos del día solicitado
                target_date_str = date_utc.strftime('%Y-%m-%d')
                day_events = []
                
                for event in self._cache:
                    try:
                        event_timestamp = event.get('timestamp_utc', '')
                        if event_timestamp.startswith(target_date_str):
                            day_events.append(event)
                    except Exception:
                        # Ignorar eventos con formato inválido
                        continue
                
                return day_events
                
        except Exception as e:
            # NUNCA lanzar excepción, siempre retornar lista vacía
            print(f"⚠️ Error al obtener eventos del día: {e}")
            return []
    
    def get_events_for_timeframe(self, start_utc: datetime, end_utc: datetime) -> List[Dict]:
        """
        Obtiene eventos en un rango de tiempo.
        
        Esta función es thread-safe y nunca lanza excepciones.
        
        Args:
            start_utc: Inicio del rango (datetime UTC)
            end_utc: Fin del rango (datetime UTC)
        
        Returns:
            Lista de eventos en el rango, o lista vacía si hay error
        """
        try:
            # Verificar si el cache necesita recarga
            if not self._is_cache_valid():
                self._reload_cache()
            
            # Usar cache
            with self._cache_lock:
                if self._cache is None:
                    if not self._reload_cache():
                        return []
                
                timeframe_events = []
                
                for event in self._cache:
                    try:
                        event_timestamp_str = event.get('timestamp_utc', '')
                        if not event_timestamp_str:
                            continue
                        
                        # Parsear timestamp
                        if event_timestamp_str.endswith('Z'):
                            event_timestamp_str = event_timestamp_str[:-1] + '+00:00'
                        elif '+' not in event_timestamp_str and 'Z' not in event_timestamp_str:
                            event_timestamp_str = event_timestamp_str + '+00:00'
                        else:
                            event_timestamp_str = event_timestamp_str.replace('Z', '+00:00')
                        
                        event_dt = datetime.fromisoformat(event_timestamp_str)
                        if event_dt.tzinfo is not None:
                            event_dt = event_dt.replace(tzinfo=None)
                        
                        if start_utc <= event_dt <= end_utc:
                            timeframe_events.append(event)
                    except Exception:
                        # Ignorar eventos con timestamp inválido
                        continue
                
                return timeframe_events
                
        except Exception as e:
            print(f"⚠️ Error al obtener eventos del timeframe: {e}")
            return []
    
    def force_reload(self) -> bool:
        """
        Fuerza la recarga del cache desde el archivo.
        Útil cuando sabes que el archivo fue actualizado.
        
        Returns:
            True si se recargó exitosamente
        """
        return self._reload_cache()


# Instancia global del proveedor
_news_provider = None
_provider_lock = threading.Lock()

def get_news_provider() -> SafeNewsProvider:
    """
    Obtiene la instancia global del proveedor de noticias.
    Thread-safe singleton.
    """
    global _news_provider
    if _news_provider is None:
        with _provider_lock:
            if _news_provider is None:
                _news_provider = SafeNewsProvider()
    return _news_provider
