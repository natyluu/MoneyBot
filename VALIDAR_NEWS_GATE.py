"""
VALIDAR_NEWS_GATE.py - Script de Validación del News Risk Gate

Valida que todos los componentes del News Risk Gate estén funcionando correctamente.
"""

import sys
import os
from datetime import datetime, date

# Agregar el directorio raíz al path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("=" * 70)
print("🔍 VALIDACIÓN DEL NEWS RISK GATE")
print("=" * 70)
print()

checks = {
    "imports": False,
    "news_provider": False,
    "news_gate": False,
    "config": False,
    "database": False,
    "indicators": False,
    "json_events": False,
    "tests": False
}

# ========================================
# 1. VERIFICAR IMPORTS
# ========================================
print("1️⃣ VERIFICANDO IMPORTS...")
print("-" * 70)

try:
    from news.provider import get_news_provider, MockNewsProvider
    from risk.news_gate import (
        detect_usd_yellow_cluster,
        is_eia_event,
        should_block_new_entries
    )
    from utils.indicators import calculate_atr, calculate_atr_ratio
    print("   ✅ Todos los imports OK")
    checks["imports"] = True
except Exception as e:
    print(f"   ❌ Error en imports: {e}")
    import traceback
    traceback.print_exc()

print()

# ========================================
# 2. VERIFICAR NEWS PROVIDER
# ========================================
print("2️⃣ VERIFICANDO NEWS PROVIDER...")
print("-" * 70)

try:
    provider = get_news_provider()
    today_utc = datetime.utcnow().date()
    events = provider.get_events_for_day(today_utc)
    
    print(f"   ✅ News Provider inicializado")
    print(f"   📅 Fecha actual UTC: {today_utc}")
    print(f"   📊 Eventos encontrados hoy: {len(events)}")
    
    if events:
        print(f"   📋 Eventos del día:")
        for event in events[:5]:  # Muestra máximo 5
            print(f"      - {event.get('title', 'N/A')} ({event.get('impact', 'N/A')}) - {event.get('timestamp_utc', 'N/A')}")
    
    checks["news_provider"] = True
except Exception as e:
    print(f"   ❌ Error en News Provider: {e}")
    import traceback
    traceback.print_exc()

print()

# ========================================
# 3. VERIFICAR NEWS GATE
# ========================================
print("3️⃣ VERIFICANDO NEWS GATE...")
print("-" * 70)

try:
    # Test básico de funciones
    test_event = {
        "timestamp_utc": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "currency": "USD",
        "impact": "MED",
        "title": "Test Event"
    }
    
    # Test is_eia_event
    eia_event = {"title": "EIA Crude Oil Stocks", "currency": "USD", "impact": "MED"}
    is_eia = is_eia_event(eia_event)
    print(f"   ✅ is_eia_event() funcionando: {is_eia}")
    
    # Test should_block_new_entries (sin bloqueo)
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
        atr_ratio=1.0,
        open_positions_count=0,
        daily_dd_pct=0.0,
        config=config
    )
    
    print(f"   ✅ should_block_new_entries() funcionando")
    print(f"      Bloqueado: {blocked}, Modo: {mode}")
    
    checks["news_gate"] = True
except Exception as e:
    print(f"   ❌ Error en News Gate: {e}")
    import traceback
    traceback.print_exc()

print()

# ========================================
# 4. VERIFICAR CONFIGURACIÓN
# ========================================
print("4️⃣ VERIFICANDO CONFIGURACIÓN...")
print("-" * 70)

try:
    from config import (
        SPREAD_MAX, ATR_MAX_RATIO, DAILY_DD_LIMIT,
        NEWS_USD_WINDOW_MINUTES, NEWS_MIN_EVENTS_FOR_CLUSTER,
        NEWS_BLOCK_PRE_MINUTES, NEWS_BLOCK_POST_MINUTES,
        NEWS_COOLDOWN_MINUTES, EIA_BLOCK_PRE_MINUTES,
        EIA_BLOCK_POST_MINUTES
    )
    
    print(f"   ✅ Configuración cargada:")
    print(f"      SPREAD_MAX: {SPREAD_MAX}")
    print(f"      ATR_MAX_RATIO: {ATR_MAX_RATIO}")
    print(f"      DAILY_DD_LIMIT: {DAILY_DD_LIMIT}%")
    print(f"      NEWS_USD_WINDOW_MINUTES: {NEWS_USD_WINDOW_MINUTES}")
    print(f"      NEWS_MIN_EVENTS_FOR_CLUSTER: {NEWS_MIN_EVENTS_FOR_CLUSTER}")
    
    checks["config"] = True
except Exception as e:
    print(f"   ❌ Error al cargar configuración: {e}")
    print(f"      ⚠️ Asegúrate de agregar las variables al .env")

print()

# ========================================
# 5. VERIFICAR BASE DE DATOS
# ========================================
print("5️⃣ VERIFICANDO BASE DE DATOS...")
print("-" * 70)

try:
    from utils.database import TradingDatabase
    
    db = TradingDatabase()
    print("   ✅ Base de datos inicializada")
    
    # Verifica que la tabla bot_state existe
    cursor = db.conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='bot_state'
    """)
    
    if cursor.fetchone():
        print("   ✅ Tabla bot_state existe")
        
        # Prueba guardar un estado
        db.save_bot_state(
            symbol="XAUUSD",
            news_mode="NORMAL",
            blocked=False,
            reasons=[],
            spread=10.0,
            atr_ratio=1.0,
            daily_dd_pct=0.0
        )
        print("   ✅ save_bot_state() funcionando")
        
        # Verifica registros recientes
        cursor.execute("""
            SELECT COUNT(*) as count FROM bot_state
            WHERE DATE(timestamp_utc) = DATE('now')
        """)
        result = cursor.fetchone()
        count = result['count'] if result else 0
        print(f"   📊 Registros de hoy en bot_state: {count}")
        
        checks["database"] = True
    else:
        print("   ❌ Tabla bot_state NO existe")
        print("      ⚠️ La base de datos necesita ser inicializada")
    
    db.close()
except Exception as e:
    print(f"   ❌ Error en base de datos: {e}")
    import traceback
    traceback.print_exc()

print()

# ========================================
# 6. VERIFICAR INDICADORES
# ========================================
print("6️⃣ VERIFICANDO INDICADORES (ATR)...")
print("-" * 70)

try:
    import pandas as pd
    import numpy as np
    
    # Crea datos de prueba
    dates = pd.date_range(start='2025-01-01', periods=50, freq='H')
    np.random.seed(42)
    base_price = 2650.0
    prices = base_price + np.cumsum(np.random.randn(50) * 2)
    
    df = pd.DataFrame({
        'high': prices + np.random.rand(50) * 5,
        'low': prices - np.random.rand(50) * 5,
        'close': prices
    })
    
    atr = calculate_atr(df['high'], df['low'], df['close'], period=14)
    atr_ratio = calculate_atr_ratio(atr.iloc[-1], atr.iloc[-20:].mean())
    
    print(f"   ✅ calculate_atr() funcionando")
    print(f"      ATR actual: {atr.iloc[-1]:.2f}")
    print(f"      ATR promedio: {atr.iloc[-20:].mean():.2f}")
    print(f"      ATR ratio: {atr_ratio:.2f}")
    
    checks["indicators"] = True
except Exception as e:
    print(f"   ❌ Error en indicadores: {e}")
    import traceback
    traceback.print_exc()

print()

# ========================================
# 7. VERIFICAR JSON DE EVENTOS
# ========================================
print("7️⃣ VERIFICANDO JSON DE EVENTOS...")
print("-" * 70)

try:
    import json
    json_path = os.path.join(project_root, "data", "news_events.json")
    
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            events = json.load(f)
        
        print(f"   ✅ Archivo JSON existe")
        print(f"   📊 Total de eventos: {len(events)}")
        
        # Verifica eventos de hoy
        today_utc = datetime.utcnow().date()
        today_str = today_utc.strftime('%Y-%m-%d')
        
        today_events = [e for e in events if e.get('timestamp_utc', '').startswith(today_str)]
        print(f"   📅 Eventos de hoy ({today_str}): {len(today_events)}")
        
        if today_events:
            print(f"   📋 Eventos de hoy:")
            for event in today_events:
                print(f"      - {event.get('title', 'N/A')} a las {event.get('timestamp_utc', 'N/A')}")
        else:
            print(f"   ⚠️ No hay eventos para hoy en el JSON")
            print(f"      Actualiza data/news_events.json con eventos de {today_str}")
        
        checks["json_events"] = True
    else:
        print(f"   ❌ Archivo JSON no existe: {json_path}")
except Exception as e:
    print(f"   ❌ Error al verificar JSON: {e}")
    import traceback
    traceback.print_exc()

print()

# ========================================
# 8. EJECUTAR TESTS
# ========================================
print("8️⃣ EJECUTANDO TESTS...")
print("-" * 70)

try:
    import unittest
    import sys
    
    # Cargar tests
    sys.path.insert(0, os.path.join(project_root, 'tests'))
    from test_news_gate import TestNewsGate
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestNewsGate)
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("   ✅ Todos los tests pasaron")
        checks["tests"] = True
    else:
        print(f"   ⚠️ Algunos tests fallaron: {len(result.failures)} fallos, {len(result.errors)} errores")
except Exception as e:
    print(f"   ⚠️ Error al ejecutar tests: {e}")
    import traceback
    traceback.print_exc()

print()

# ========================================
# RESUMEN
# ========================================
print("=" * 70)
print("📊 RESUMEN DE VALIDACIÓN")
print("=" * 70)
print()

all_checks = [
    ("Imports", checks["imports"]),
    ("News Provider", checks["news_provider"]),
    ("News Gate", checks["news_gate"]),
    ("Configuración", checks["config"]),
    ("Base de Datos", checks["database"]),
    ("Indicadores", checks["indicators"]),
    ("JSON de Eventos", checks["json_events"]),
    ("Tests", checks["tests"]),
]

print("🔴 VERIFICACIONES:")
for name, status in all_checks:
    status_icon = "✅" if status else "❌"
    print(f"   {status_icon} {name}")

print()
print("=" * 70)

all_ok = all([status for _, status in all_checks])

if all_ok:
    print("✅ TODAS LAS VALIDACIONES PASARON")
    print()
    print("El News Risk Gate está listo para usar.")
    print()
    print("Próximos pasos:")
    print("1. Agrega las variables al .env en el VPS")
    print("2. Actualiza data/news_events.json con eventos reales")
    print("3. Reinicia el bot")
    print("4. Monitorea los logs para ver el gate en acción")
else:
    print("⚠️ ALGUNAS VALIDACIONES FALLARON")
    print()
    print("Revisa los errores arriba y corrígelos antes de usar el bot.")

print("=" * 70)

sys.exit(0 if all_ok else 1)






