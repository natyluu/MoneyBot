"""
paso_a_paso.py - Guía interactiva paso a paso para conectar a MT5

Este script te guía paso a paso en el proceso de configuración.
"""

import sys
import os
import subprocess

def print_step(num, title):
    """Imprime un paso numerado"""
    print("\n" + "=" * 70)
    print(f"PASO {num}: {title}")
    print("=" * 70)

def check_python():
    """Verifica que Python esté instalado"""
    print_step(1, "VERIFICANDO PYTHON")
    
    version = sys.version_info
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Necesitas Python 3.7 o superior")
        return False
    
    return True

def install_dependencies():
    """Instala las dependencias necesarias"""
    print_step(2, "INSTALANDO DEPENDENCIAS")
    
    dependencies = [
        ("python-dotenv", "python-dotenv"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("MetaTrader5", "MetaTrader5")
    ]
    
    print("📦 Instalando dependencias...")
    print("   Esto puede tomar unos minutos...\n")
    
    for name, package in dependencies:
        print(f"   Instalando {name}...", end=" ")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package, "--quiet"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                print("✅")
            else:
                print(f"❌ Error: {result.stderr[:100]}")
                return False
        except subprocess.TimeoutExpired:
            print("⏱️ Tardó mucho, pero continuando...")
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    print("\n✅ Todas las dependencias instaladas")
    return True

def verify_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print_step(3, "VERIFICANDO DEPENDENCIAS")
    
    modules = {
        "dotenv": "python-dotenv",
        "pandas": "pandas",
        "numpy": "numpy",
        "MetaTrader5": "MetaTrader5"
    }
    
    all_ok = True
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} NO instalado")
            all_ok = False
    
    if not all_ok:
        print("\n⚠️ Algunas dependencias faltan. Ejecuta:")
        print("   python3 -m pip install python-dotenv pandas numpy MetaTrader5")
        return False
    
    return True

def check_mt5_installed():
    """Verifica si MT5 está instalado en el sistema"""
    print_step(4, "VERIFICANDO METATRADER 5")
    
    # Rutas comunes donde puede estar MT5
    mt5_paths = [
        "/Applications/MetaTrader 5.app",
        "C:/Program Files/MetaTrader 5",
        "C:/Program Files (x86)/MetaTrader 5",
        os.path.expanduser("~/Applications/MetaTrader 5.app")
    ]
    
    found = False
    for path in mt5_paths:
        if os.path.exists(path):
            print(f"   ✅ MT5 encontrado en: {path}")
            found = True
            break
    
    if not found:
        print("   ⚠️ MetaTrader 5 no encontrado en las rutas comunes")
        print("\n   Por favor:")
        print("   1. Descarga MetaTrader 5 desde: https://www.metatrader5.com/es/download")
        print("   2. Instálalo en tu computadora")
        print("   3. Ábrelo y conéctate a tu cuenta Zeven")
        print("\n   Presiona Enter cuando hayas instalado MT5...")
        input()
    
    return True

def create_env_file():
    """Crea el archivo .env con las credenciales"""
    print_step(5, "CONFIGURANDO CREDENCIALES")
    
    if os.path.exists('.env'):
        respuesta = input("\n⚠️ Ya existe un archivo .env. ¿Sobrescribirlo? (s/n): ")
        if respuesta.lower() != 's':
            print("   Usando archivo .env existente")
            return True
    
    print("\n📝 Necesito tus credenciales de MetaTrader 5 (Zeven):\n")
    
    login = input("   Número de cuenta MT5: ").strip()
    if not login:
        print("   ❌ El número de cuenta es requerido")
        return False
    
    password = input("   Contraseña MT5: ").strip()
    if not password:
        print("   ❌ La contraseña es requerida")
        return False
    
    print("\n   ¿Qué tipo de cuenta tienes?")
    print("   1. Demo (recomendado para empezar)")
    print("   2. Real")
    tipo = input("   Selecciona (1 o 2): ").strip()
    
    if tipo == "1":
        server = "ZevenGlobal-Demo"
    elif tipo == "2":
        server = "ZevenGlobal-Real"
        print("   ⚠️ ADVERTENCIA: Estás usando cuenta REAL")
        confirm = input("   ¿Estás seguro? (s/n): ")
        if confirm.lower() != 's':
            server = "ZevenGlobal-Demo"
            print("   ✓ Usando servidor DEMO por seguridad")
    else:
        server = input("   Ingresa el nombre exacto del servidor: ").strip()
        if not server:
            server = "ZevenGlobal-Demo"
    
    symbol = input("\n   Símbolo a operar (default: XAUUSD): ").strip()
    if not symbol:
        symbol = "XAUUSD"
    
    # Configuración de riesgo
    print("\n   ⚙️ Configuración de riesgo (puedes usar valores por defecto):")
    risk = input("   Riesgo por operación en % (default: 1.0): ").strip()
    if not risk:
        risk = "0.01"
    else:
        try:
            risk = str(float(risk) / 100)
        except:
            risk = "0.01"
    
    max_trades = input("   Máximo de operaciones simultáneas (default: 3): ").strip()
    if not max_trades:
        max_trades = "3"
    
    min_rr = input("   Risk:Reward mínimo requerido (default: 2.0): ").strip()
    if not min_rr:
        min_rr = "2.0"
    
    # Crea el archivo
    env_content = f"""# Configuración MetaTrader 5 (Zeven)
# Generado automáticamente por paso_a_paso.py

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
        
        print(f"\n   ✅ Archivo .env creado en: {os.path.abspath('.env')}")
        return True
    except Exception as e:
        print(f"   ❌ Error al crear .env: {e}")
        return False

def test_connection():
    """Prueba la conexión con MT5"""
    print_step(6, "PROBANDO CONEXIÓN CON MT5")
    
    print("\n   ⚠️ IMPORTANTE: Asegúrate de que MetaTrader 5 esté ABIERTO")
    print("   y conectado a tu cuenta Zeven antes de continuar.\n")
    
    input("   Presiona Enter cuando MT5 esté abierto y conectado...")
    
    try:
        import MetaTrader5 as mt5
        from dotenv import load_dotenv
        load_dotenv()
        
        from config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER, MT5_SYMBOL
        
        print("\n   🔌 Inicializando MT5...")
        if not mt5.initialize():
            error = mt5.last_error()
            print(f"   ❌ Error: {error}")
            print("\n   Posibles soluciones:")
            print("   1. Verifica que MT5 esté abierto")
            print("   2. Intenta ejecutar como administrador")
            return False
        
        print("   ✅ MT5 inicializado")
        
        print(f"\n   🔐 Conectando a cuenta {MT5_LOGIN}...")
        if not mt5.login(MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
            error = mt5.last_error()
            print(f"   ❌ Error de conexión: {error}")
            print("\n   Verifica:")
            print("   1. Que las credenciales sean correctas")
            print("   2. Que el servidor sea el correcto")
            print("   3. Que la cuenta esté activa")
            mt5.shutdown()
            return False
        
        print("   ✅ Conexión exitosa!")
        
        account_info = mt5.account_info()
        if account_info:
            print(f"\n   📊 Información de la cuenta:")
            print(f"      Balance: ${account_info.balance:,.2f}")
            print(f"      Equity: ${account_info.equity:,.2f}")
            print(f"      Servidor: {account_info.server}")
        
        symbol_info = mt5.symbol_info(MT5_SYMBOL)
        if symbol_info is None:
            print(f"\n   ⚠️ Símbolo {MT5_SYMBOL} no encontrado")
            print("   Verifica el nombre en MT5 (puede ser XAUUSD o XAUUSD.m)")
        else:
            print(f"\n   ✅ Símbolo {MT5_SYMBOL} disponible")
            tick = mt5.symbol_info_tick(MT5_SYMBOL)
            if tick:
                print(f"      Precio actual: ${tick.bid:.2f} / ${tick.ask:.2f}")
        
        mt5.shutdown()
        print("\n   ✅ Prueba de conexión exitosa!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("🚀 GUÍA PASO A PASO: CONECTAR A MT5 CON ZEVEN")
    print("=" * 70)
    print("\nEste script te guiará en el proceso completo de configuración.\n")
    
    # Paso 1: Verificar Python
    if not check_python():
        return
    
    # Paso 2: Instalar dependencias
    respuesta = input("\n¿Deseas instalar las dependencias ahora? (s/n): ")
    if respuesta.lower() == 's':
        if not install_dependencies():
            print("\n❌ Error al instalar dependencias")
            print("   Intenta manualmente: python3 -m pip install python-dotenv pandas numpy MetaTrader5")
            return
    else:
        print("   ⚠️ Asegúrate de instalar las dependencias antes de continuar")
        input("   Presiona Enter cuando hayas instalado las dependencias...")
    
    # Paso 3: Verificar dependencias
    if not verify_dependencies():
        return
    
    # Paso 4: Verificar MT5
    check_mt5_installed()
    
    # Paso 5: Crear .env
    if not create_env_file():
        return
    
    # Paso 6: Probar conexión
    if not test_connection():
        print("\n❌ La conexión falló. Revisa los errores arriba.")
        return
    
    # Resumen final
    print("\n" + "=" * 70)
    print("✅ CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print("\n🎉 ¡Todo está listo!")
    print("\nPróximos pasos:")
    print("1. Para probar la conexión nuevamente:")
    print("   python3 test_mt5_connection.py")
    print("\n2. Para ejecutar el bot de trading:")
    print("   python3 live/mt5_trading.py")
    print("\n3. Para detener el bot, presiona Ctrl+C")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Proceso cancelado por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)












