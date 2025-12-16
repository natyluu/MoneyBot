"""
Script de debug para ver qué está pasando con el bot
"""
import sys
import os

print("=" * 70)
print("DEBUG: Iniciando diagnóstico...")
print("=" * 70)
print()

# Configurar encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    print("✓ Encoding configurado")
else:
    print("⚠️ No es Windows")

print(f"✓ Directorio actual: {os.getcwd()}")
print()

# Cambiar al directorio del proyecto
project_path = r"C:\BOT\trading-bot-windows-20251210 on 'Mac'"
if os.path.exists(project_path):
    os.chdir(project_path)
    print(f"✓ Cambiado a: {project_path}")
else:
    print(f"❌ No se encontró: {project_path}")
    sys.exit(1)

print()

# Verificar archivos
print("Verificando archivos...")
config_file = "config.py"
bot_file = "live/mt5_trading.py"

if not os.path.exists(config_file):
    print(f"❌ No existe: {config_file}")
    sys.exit(1)
else:
    print(f"✓ {config_file} existe")

if not os.path.exists(bot_file):
    print(f"❌ No existe: {bot_file}")
    sys.exit(1)
else:
    print(f"✓ {bot_file} existe")

print()

# Intentar importar módulos básicos
print("Verificando imports...")
try:
    import MetaTrader5 as mt5
    print("✓ MetaTrader5 importado")
except Exception as e:
    print(f"❌ Error al importar MetaTrader5: {e}")
    sys.exit(1)

try:
    import pandas as pd
    print("✓ pandas importado")
except Exception as e:
    print(f"❌ Error al importar pandas: {e}")
    sys.exit(1)

print()

# Cargar config
print("Cargando config.py...")
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("config", config_file)
    config = importlib.util.module_from_spec(spec)
    sys.modules["config"] = config
    spec.loader.exec_module(config)
    print(f"✓ Config cargado")
    print(f"  MT5_LOGIN: {config.MT5_LOGIN}")
    print(f"  MT5_SERVER: {config.MT5_SERVER}")
except Exception as e:
    print(f"❌ Error al cargar config: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Verificar MT5
print("Verificando MetaTrader 5...")
try:
    if not mt5.initialize():
        print(f"❌ Error al inicializar MT5: {mt5.last_error()}")
        print("⚠️ Asegúrate de que MetaTrader 5 esté abierto")
    else:
        print("✓ MT5 inicializado")
        mt5.shutdown()
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print()

# Intentar ejecutar el bot línea por línea
print("=" * 70)
print("Intentando ejecutar el bot...")
print("=" * 70)
print()

sys.path.insert(0, os.getcwd())

try:
    print("Leyendo archivo del bot...")
    with open(bot_file, 'r', encoding='utf-8') as f:
        bot_code = f.read()
    print(f"✓ Archivo leído ({len(bot_code)} caracteres)")
    print()
    
    print("Compilando código...")
    compiled = compile(bot_code, bot_file, 'exec')
    print("✓ Código compilado")
    print()
    
    print("Ejecutando bot (esto puede tardar unos segundos)...")
    print()
    
    # Crear namespace con __file__ definido
    namespace = {
        '__file__': os.path.abspath(bot_file),
        '__name__': '__main__',
        '__package__': None
    }
    
    exec(compiled, namespace)
    
except KeyboardInterrupt:
    print("\n\nBot detenido por el usuario")
except Exception as e:
    print(f"\n❌ ERROR al ejecutar: {e}")
    import traceback
    traceback.print_exc()




