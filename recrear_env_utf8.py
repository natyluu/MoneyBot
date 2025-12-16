"""
Script para recrear el archivo .env con encoding UTF-8 correcto
"""

import os

# Contenido del archivo .env
env_content = """MT5_LOGIN=94338
MT5_PASSWORD=Santos2025!
MT5_SERVER=ZevenGlobal-Live
MT5_SYMBOL=XAUUSD.vip
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=2.0
"""

def main():
    """Crea el archivo .env con encoding UTF-8 sin BOM"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    try:
        # Elimina el archivo anterior si existe
        if os.path.exists(env_path):
            os.remove(env_path)
            print("✅ Archivo .env anterior eliminado")
        
        # Crea el nuevo archivo con UTF-8 sin BOM
        with open(env_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(env_content)
        
        print("✅ Archivo .env creado correctamente con encoding UTF-8")
        print(f"   Ubicación: {os.path.abspath(env_path)}")
        print("\n📋 Contenido:")
        print(env_content)
        print("\n✅ ¡Listo para probar la conexión!")
        print("   Ejecuta: python test_mt5_connection.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear archivo .env: {e}")
        return False

if __name__ == "__main__":
    main()





