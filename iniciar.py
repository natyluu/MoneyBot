#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

print("=" * 70)
print("INICIANDO BOT - MODO DEBUG")
print("=" * 70)
print()

# Configurar encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("1. Directorio actual:", os.getcwd())
print()

# Cambiar al directorio del proyecto si es necesario
project_path = r"C:\BOT\trading-bot-windows-20251210 on 'Mac'"
if os.path.exists(project_path):
    os.chdir(project_path)
    print(f"2. Cambiado a: {project_path}")
else:
    print(f"2. ⚠️ No se encontró: {project_path}")
    print(f"   Usando directorio actual: {os.getcwd()}")
print()

# Verificar archivos
print("3. Verificando archivos...")
config_file = os.path.join(os.getcwd(), "config.py")
bot_file = os.path.join(os.getcwd(), "live", "mt5_trading.py")

print(f"   config.py: {'✓' if os.path.exists(config_file) else '❌'} {config_file}")
print(f"   mt5_trading.py: {'✓' if os.path.exists(bot_file) else '❌'} {bot_file}")
print()

if not os.path.exists(bot_file):
    print("❌ ERROR: No se encontró live/mt5_trading.py")
    sys.exit(1)

# Agregar al path
sys.path.insert(0, os.getcwd())
print("4. Path configurado")
print()

# Cargar config
print("5. Cargando config.py...")
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("config", config_file)
    config = importlib.util.module_from_spec(spec)
    sys.modules["config"] = config
    spec.loader.exec_module(config)
    print(f"   ✓ Config cargado - Login: {config.MT5_LOGIN}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# Ejecutar bot
print("6. Ejecutando bot...")
print("=" * 70)
print()

try:
    with open(bot_file, 'r', encoding='utf-8') as f:
        code = f.read()
    # Definir __file__ para que funcione
    exec(compile(code, bot_file, 'exec'), {'__file__': bot_file, '__name__': '__main__'})
except KeyboardInterrupt:
    print("\n\nBot detenido por el usuario")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()




