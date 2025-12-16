"""
Script para ejecutar el bot desde cualquier directorio
Ejecuta: python ejecutar_bot.py
"""
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Buscar el directorio del proyecto
project_dirs = [
    r"C:\BOT\trading-bot-windows-20251210 on 'Mac'",
    os.path.join(os.path.expanduser("~"), "BOT", "trading-bot-windows-20251210 on 'Mac'"),
    os.getcwd(),
    os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
]

project_root = None
for dir_path in project_dirs:
    config_file = os.path.join(dir_path, "config.py")
    if os.path.exists(config_file):
        project_root = dir_path
        break

if project_root is None:
    print("❌ ERROR: No se encontró el directorio del proyecto")
    print("   Buscado en:")
    for d in project_dirs:
        print(f"      - {d}")
    sys.exit(1)

# Cambiar al directorio del proyecto
os.chdir(project_root)
print(f"✓ Directorio del proyecto: {project_root}")

# Agregar al path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Cargar config.py
import importlib.util
config_file = os.path.join(project_root, "config.py")
spec = importlib.util.spec_from_file_location("config", config_file)
config = importlib.util.module_from_spec(spec)
sys.modules["config"] = config
spec.loader.exec_module(config)
print("✓ Config cargado")

# Ejecutar el bot
bot_file = os.path.join(project_root, "live", "mt5_trading.py")
if not os.path.exists(bot_file):
    print(f"❌ ERROR: No se encontró {bot_file}")
    sys.exit(1)

print(f"✓ Ejecutando bot desde: {bot_file}\n")

# Leer y ejecutar el bot
with open(bot_file, 'r', encoding='utf-8') as f:
    code = compile(f.read(), bot_file, 'exec')
    exec(code, {'__file__': bot_file})
