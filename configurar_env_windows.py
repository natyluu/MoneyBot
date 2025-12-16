"""
Script rápido para configurar .env con credenciales de Zeven
"""

import os

# Credenciales proporcionadas
MT5_LOGIN = "94338"
MT5_PASSWORD = "Santos2025!"
MT5_SERVER = "ZevenGlobal-Live"  # Basado en la imagen de MT5
MT5_SYMBOL = "XAUUSD.vip"  # Basado en la imagen de MT5

# Configuración de riesgo (valores por defecto)
RISK_PER_TRADE = "0.01"  # 1% de riesgo por operación
MAX_CONCURRENT_TRADES = "3"
MIN_RR = "2.0"

# Contenido del archivo .env
env_content = f"""# Configuración MetaTrader 5 (Zeven)
# Generado automáticamente

MT5_LOGIN={MT5_LOGIN}
MT5_PASSWORD={MT5_PASSWORD}
MT5_SERVER={MT5_SERVER}
MT5_SYMBOL={MT5_SYMBOL}

# Configuración de riesgo
RISK_PER_TRADE={RISK_PER_TRADE}
MAX_CONCURRENT_TRADES={MAX_CONCURRENT_TRADES}
MIN_RR={MIN_RR}
"""

def main():
    """Crea el archivo .env"""
    try:
        # Verifica si ya existe
        if os.path.exists('.env'):
            print("⚠️ Ya existe un archivo .env")
            respuesta = input("¿Deseas sobrescribirlo? (s/n): ")
            if respuesta.lower() != 's':
                print("Operación cancelada.")
                return
        
        # Crea el archivo
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ Archivo .env creado exitosamente!")
        print(f"   Ubicación: {os.path.abspath('.env')}")
        print("\n📋 Configuración:")
        print(f"   Cuenta: {MT5_LOGIN}")
        print(f"   Servidor: {MT5_SERVER}")
        print(f"   Símbolo: {MT5_SYMBOL}")
        print(f"   Riesgo: {float(RISK_PER_TRADE)*100}% por operación")
        print(f"   RR mínimo: {MIN_RR}")
        print("\n✅ ¡Listo para probar la conexión!")
        print("   Ejecuta: python test_mt5_connection.py")
        
    except Exception as e:
        print(f"\n❌ Error al crear archivo .env: {e}")

if __name__ == "__main__":
    main()





