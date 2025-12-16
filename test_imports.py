"""
Script de prueba para verificar que los imports funcionen correctamente
"""
import sys
import os

# Agregar el directorio raíz al path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = script_dir
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f"Directorio del script: {script_dir}")
print(f"Directorio raíz del proyecto: {project_root}")
print(f"sys.path[0]: {sys.path[0]}")
print()

# Verificar que config.py existe
config_path = os.path.join(project_root, "config.py")
print(f"Ruta de config.py: {config_path}")
print(f"¿Existe config.py? {os.path.exists(config_path)}")
print()

# Intentar importar
try:
    from config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER, MT5_SYMBOL
    print("✅ Import de config exitoso")
    print(f"   MT5_LOGIN: {MT5_LOGIN}")
    print(f"   MT5_SERVER: {MT5_SERVER}")
    print(f"   MT5_SYMBOL: {MT5_SYMBOL}")
except Exception as e:
    print(f"❌ Error al importar config: {e}")
    import traceback
    traceback.print_exc()

print()

# Verificar strategy
try:
    from strategy.ict_hybrid_strategy import ICTHybridStrategy
    print("✅ Import de strategy exitoso")
except Exception as e:
    print(f"❌ Error al importar strategy: {e}")
    import traceback
    traceback.print_exc()




