"""
setup_mt5.py - Configuración guiada para conectar a MT5 con Zeven

Este script te ayuda a configurar la conexión con MetaTrader 5 paso a paso.
"""

import os
import sys

def create_env_file():
    """Crea el archivo .env con las credenciales de MT5"""
    
    print("=" * 70)
    print("CONFIGURACIÓN DE CONEXIÓN A METATRADER 5 (ZEVEN)")
    print("=" * 70)
    print("\nEste script te ayudará a configurar tu conexión con MT5.")
    print("Necesitarás tus credenciales de cuenta Zeven.\n")
    
    # Verifica si ya existe .env
    if os.path.exists('.env'):
        respuesta = input("⚠️ Ya existe un archivo .env. ¿Deseas sobrescribirlo? (s/n): ")
        if respuesta.lower() != 's':
            print("Operación cancelada.")
            return False
    
    # Solicita credenciales
    print("\n📝 Ingresa tus credenciales de MetaTrader 5:\n")
    
    login = input("Número de cuenta MT5: ").strip()
    if not login:
        print("❌ El número de cuenta es requerido")
        return False
    
    password = input("Contraseña MT5: ").strip()
    if not password:
        print("❌ La contraseña es requerida")
        return False
    
    print("\n¿Qué tipo de cuenta tienes?")
    print("1. Demo (recomendado para empezar)")
    print("2. Real")
    tipo = input("Selecciona (1 o 2): ").strip()
    
    if tipo == "1":
        server = "ZevenGlobal-Demo"
        print("✓ Usando servidor DEMO")
    elif tipo == "2":
        server = "ZevenGlobal-Real"
        print("⚠️ Usando servidor REAL - Ten cuidado")
    else:
        server = input("Ingresa el nombre exacto del servidor: ").strip()
        if not server:
            server = "ZevenGlobal-Demo"
            print(f"✓ Usando servidor por defecto: {server}")
    
    symbol = input("\nSímbolo a operar (default: XAUUSD): ").strip()
    if not symbol:
        symbol = "XAUUSD"
    
    # Configuración de riesgo
    print("\n⚙️ Configuración de riesgo:")
    risk = input("Riesgo por operación en % (default: 1.0): ").strip()
    if not risk:
        risk = "0.01"
    else:
        try:
            risk = str(float(risk) / 100)  # Convierte porcentaje a decimal
        except:
            risk = "0.01"
    
    max_trades = input("Máximo de operaciones simultáneas (default: 3): ").strip()
    if not max_trades:
        max_trades = "3"
    
    min_rr = input("Risk:Reward mínimo requerido (default: 2.0): ").strip()
    if not min_rr:
        min_rr = "2.0"
    
    # Crea el archivo .env
    env_content = f"""# Configuración MetaTrader 5 (Zeven)
# Generado automáticamente por setup_mt5.py

MT5_LOGIN={login}
MT5_PASSWORD={password}
MT5_SERVER={server}
MT5_SYMBOL={symbol}

# Configuración de riesgo
RISK_PER_TRADE={risk}
MAX_CONCURRENT_TRADES={max_trades}
MIN_RR={min_rr}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ Archivo .env creado exitosamente!")
        print(f"   Ubicación: {os.path.abspath('.env')}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error al crear archivo .env: {e}")
        return False


def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("\n🔍 Verificando dependencias...")
    
    missing = []
    
    # Verifica python-dotenv
    try:
        import dotenv
        print("   ✅ python-dotenv instalado")
    except ImportError:
        print("   ❌ python-dotenv NO instalado")
        missing.append("python-dotenv")
    
    # Verifica MetaTrader5
    try:
        import MetaTrader5
        print("   ✅ MetaTrader5 instalado")
    except ImportError:
        print("   ❌ MetaTrader5 NO instalado")
        missing.append("MetaTrader5")
    
    # Verifica pandas
    try:
        import pandas
        print("   ✅ pandas instalado")
    except ImportError:
        print("   ❌ pandas NO instalado")
        missing.append("pandas")
    
    if missing:
        print(f"\n⚠️ Faltan dependencias: {', '.join(missing)}")
        print("   Instala con: pip install " + " ".join(missing))
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True


def main():
    """Función principal"""
    print("\n🚀 Configuración de MT5 para Zeven\n")
    
    # 1. Verifica dependencias
    if not check_dependencies():
        print("\n❌ Por favor instala las dependencias faltantes primero")
        print("   Ejecuta: pip install -r requirements.txt")
        return
    
    # 2. Crea archivo .env
    if create_env_file():
        print("\n" + "=" * 70)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("=" * 70)
        print("\nPróximos pasos:")
        print("1. Abre MetaTrader 5 y conéctate a tu cuenta Zeven")
        print("2. Verifica que el símbolo XAUUSD esté disponible")
        print("3. Ejecuta el script de prueba:")
        print("   python3 test_mt5_connection.py")
        print("\nSi la prueba es exitosa, puedes ejecutar el bot:")
        print("   python3 live/mt5_trading.py")
    else:
        print("\n❌ Error en la configuración")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Configuración cancelada")
        sys.exit(0)













