"""
Script de prueba para verificar que el bot puede iniciar
"""
import sys
import os

print("=" * 70)
print("PRUEBA DE INICIALIZACIÓN DEL BOT")
print("=" * 70)
print()

# Configurar encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("1. Verificando directorio...")
print(f"   Directorio actual: {os.getcwd()}")
print()

print("2. Verificando archivos...")
files_to_check = [
    "config.py",
    "live/mt5_trading.py",
    "strategy/ict_hybrid_strategy.py"
]

for file in files_to_check:
    exists = os.path.exists(file)
    status = "✓" if exists else "❌"
    print(f"   {status} {file}: {'Existe' if exists else 'NO EXISTE'}")

print()

print("3. Verificando imports...")
try:
    import MetaTrader5 as mt5
    print("   ✓ MetaTrader5 importado")
except Exception as e:
    print(f"   ❌ Error al importar MetaTrader5: {e}")

try:
    import pandas as pd
    print("   ✓ pandas importado")
except Exception as e:
    print(f"   ❌ Error al importar pandas: {e}")

try:
    import numpy as np
    print("   ✓ numpy importado")
except Exception as e:
    print(f"   ❌ Error al importar numpy: {e}")

print()

print("4. Intentando cargar config.py...")
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("config", "config.py")
    config = importlib.util.module_from_spec(spec)
    sys.modules["config"] = config
    spec.loader.exec_module(config)
    print("   ✓ config.py cargado")
    print(f"   ✓ MT5_LOGIN: {config.MT5_LOGIN}")
    print(f"   ✓ MT5_SERVER: {config.MT5_SERVER}")
except Exception as e:
    print(f"   ❌ Error al cargar config.py: {e}")
    import traceback
    traceback.print_exc()

print()

print("5. Intentando ejecutar el bot...")
try:
    exec(compile(open('live/mt5_trading.py', encoding='utf-8').read(), 'live/mt5_trading.py', 'exec'))
except Exception as e:
    print(f"   ❌ Error al ejecutar el bot: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)




