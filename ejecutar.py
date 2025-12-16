#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para ejecutar el bot - Soluciona problemas de import
Ejecuta desde el directorio raíz: python ejecutar.py
"""
import sys
import os

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Obtener el directorio del script (directorio raíz del proyecto)
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Agregar el directorio raíz al path
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

print(f"✓ Directorio de trabajo: {script_dir}")
print(f"✓ Path configurado\n")

# Verificar archivos
config_file = os.path.join(script_dir, "config.py")
bot_file = os.path.join(script_dir, "live", "mt5_trading.py")

if not os.path.exists(config_file):
    print(f"❌ ERROR: No se encontró {config_file}")
    sys.exit(1)

if not os.path.exists(bot_file):
    print(f"❌ ERROR: No se encontró {bot_file}")
    sys.exit(1)

print(f"✓ Archivos encontrados")
print(f"  - {config_file}")
print(f"  - {bot_file}\n")

# Importar config primero para que esté disponible
import importlib.util

# Cargar config
spec = importlib.util.spec_from_file_location("config", config_file)
config = importlib.util.module_from_spec(spec)
sys.modules["config"] = config
spec.loader.exec_module(config)
print("✓ Config cargado\n")

# Ahora ejecutar el bot
print("=" * 70)
print("Iniciando bot...")
print("=" * 70)
print()

# Importar y ejecutar el bot usando importlib
spec = importlib.util.spec_from_file_location("mt5_trading", bot_file)
bot_module = importlib.util.module_from_spec(spec)
sys.modules["mt5_trading"] = bot_module

# Ejecutar el módulo
spec.loader.exec_module(bot_module)




