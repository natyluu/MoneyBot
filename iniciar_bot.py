"""
Script para iniciar el bot desde el directorio raíz
Este script asegura que el path esté configurado correctamente
"""
import sys
import os

# Asegurar que estamos en el directorio correcto
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Agregar el directorio actual al path
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Verificar que config.py existe
config_path = os.path.join(script_dir, "config.py")
if not os.path.exists(config_path):
    print(f"❌ ERROR: No se encontró config.py en: {config_path}")
    print(f"   Directorio actual: {os.getcwd()}")
    print(f"   Archivos en el directorio:")
    for f in os.listdir(script_dir):
        print(f"      - {f}")
    sys.exit(1)

# Ahora ejecutar el bot
print(f"✓ Directorio de trabajo: {script_dir}")
print(f"✓ Config.py encontrado: {config_path}")
print(f"✓ Iniciando bot...\n")

# Importar y ejecutar el bot
try:
    # Cambiar al directorio live y ejecutar
    import subprocess
    import sys as sys_module
    
    # Ejecutar el script directamente
    bot_script = os.path.join(script_dir, "live", "mt5_trading.py")
    if os.path.exists(bot_script):
        # Cambiar al directorio raíz y ejecutar
        os.chdir(script_dir)
        # Leer con encoding UTF-8 para evitar errores
        with open(bot_script, 'r', encoding='utf-8') as f:
            exec(f.read())
    else:
        print(f"❌ No se encontró: {bot_script}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error al ejecutar el bot: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

