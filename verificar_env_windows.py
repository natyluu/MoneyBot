"""
Script temporal para verificar y cargar el .env en Windows
"""

import os

def load_env_manual():
    """Lee el archivo .env manualmente"""
    env_vars = {}
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        env_vars[key] = value
        except Exception as e:
            print(f"Error al leer .env: {e}")
    
    return env_vars

# Cargar variables
env_vars = load_env_manual()

print("=" * 70)
print("VERIFICACIÓN DE ARCHIVO .env")
print("=" * 70)
print(f"\n📁 Archivo .env encontrado: {os.path.exists('.env')}")
print(f"\n📋 Variables cargadas:")
for key, value in env_vars.items():
    if 'PASSWORD' in key:
        print(f"   {key} = {'*' * len(value)}")
    else:
        print(f"   {key} = {value}")

# Verificar que todas las variables necesarias estén presentes
required = ['MT5_LOGIN', 'MT5_PASSWORD', 'MT5_SERVER', 'MT5_SYMBOL']
missing = [key for key in required if key not in env_vars]

if missing:
    print(f"\n❌ Faltan variables: {', '.join(missing)}")
else:
    print("\n✅ Todas las variables necesarias están presentes")
    
    # Cargar en os.environ para que config.py las pueda leer
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("\n✅ Variables cargadas en os.environ")
    print("\nAhora puedes ejecutar: python test_mt5_connection.py")





