"""
Script de diagnóstico completo para el bot de trading
Este script verifica todos los componentes necesarios antes de iniciar el bot
"""

import sys
import os
import traceback

print("=" * 70)
print("🔍 DIAGNÓSTICO COMPLETO DEL BOT DE TRADING")
print("=" * 70)

# 1. Verificar directorio actual
print("\n1️⃣ VERIFICANDO DIRECTORIO ACTUAL...")
current_dir = os.getcwd()
print(f"   Directorio actual: {current_dir}")

# 2. Verificar archivos necesarios
print("\n2️⃣ VERIFICANDO ARCHIVOS NECESARIOS...")
files_to_check = [
    "config.py",
    ".env",
    "live/mt5_trading.py",
    "strategy/ict_hybrid_strategy.py"
]

all_files_exist = True
for file_path in files_to_check:
    full_path = os.path.join(current_dir, file_path)
    exists = os.path.exists(full_path)
    status = "✓" if exists else "❌"
    print(f"   {status} {file_path}: {'EXISTE' if exists else 'NO EXISTE'}")
    if not exists:
        all_files_exist = False
        print(f"      Ruta completa: {full_path}")

if not all_files_exist:
    print("\n⚠️ ADVERTENCIA: Faltan algunos archivos. El bot puede no funcionar correctamente.")

# 3. Verificar Python y versiones
print("\n3️⃣ VERIFICANDO PYTHON...")
print(f"   Versión de Python: {sys.version}")
print(f"   Ejecutable: {sys.executable}")

# 4. Verificar módulos instalados
print("\n4️⃣ VERIFICANDO MÓDULOS INSTALADOS...")
modules_to_check = [
    "MetaTrader5",
    "pandas",
    "numpy",
    "dotenv"
]

for module_name in modules_to_check:
    try:
        if module_name == "dotenv":
            __import__("dotenv")
        elif module_name == "MetaTrader5":
            import MetaTrader5 as mt5
            print(f"   ✓ {module_name}: INSTALADO (versión: {mt5.__version__ if hasattr(mt5, '__version__') else 'N/A'})")
        else:
            mod = __import__(module_name)
            version = getattr(mod, '__version__', 'N/A')
            print(f"   ✓ {module_name}: INSTALADO (versión: {version})")
    except ImportError as e:
        print(f"   ❌ {module_name}: NO INSTALADO - {e}")

# 5. Verificar .env
print("\n5️⃣ VERIFICANDO ARCHIVO .env...")
env_path = os.path.join(current_dir, ".env")
if os.path.exists(env_path):
    print(f"   ✓ .env existe en: {env_path}")
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"   ✓ .env tiene {len(lines)} líneas")
            
            # Verificar variables importantes
            required_vars = ["MT5_LOGIN", "MT5_PASSWORD", "MT5_SERVER", "MT5_SYMBOL"]
            env_vars = {}
            for line in lines:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    env_vars[key] = value
            
            print("\n   Variables encontradas en .env:")
            for var in required_vars:
                if var in env_vars:
                    if var == "MT5_PASSWORD":
                        print(f"   ✓ {var}: {'*' * len(env_vars[var])} (oculto)")
                    else:
                        print(f"   ✓ {var}: {env_vars[var]}")
                else:
                    print(f"   ❌ {var}: NO ENCONTRADO")
    except Exception as e:
        print(f"   ❌ Error al leer .env: {e}")
        traceback.print_exc()
else:
    print(f"   ❌ .env NO EXISTE en: {env_path}")

# 6. Verificar config.py
print("\n6️⃣ VERIFICANDO config.py...")
config_path = os.path.join(current_dir, "config.py")
if os.path.exists(config_path):
    try:
        # Intentar importar config
        sys.path.insert(0, current_dir)
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_path)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)
        
        print("   ✓ config.py se puede importar correctamente")
        
        # Verificar variables importantes
        required_config_vars = ["MT5_LOGIN", "MT5_PASSWORD", "MT5_SERVER", "MT5_SYMBOL", 
                                "RISK_PER_TRADE", "MAX_CONCURRENT_TRADES", "MIN_RR"]
        
        print("\n   Variables de configuración:")
        for var in required_config_vars:
            if hasattr(config_module, var):
                value = getattr(config_module, var)
                if var == "MT5_PASSWORD":
                    print(f"   ✓ {var}: {'*' * len(str(value))} (oculto)")
                else:
                    print(f"   ✓ {var}: {value}")
            else:
                print(f"   ❌ {var}: NO DEFINIDO")
    except Exception as e:
        print(f"   ❌ Error al importar config.py: {e}")
        traceback.print_exc()
else:
    print(f"   ❌ config.py NO EXISTE")

# 7. Verificar MT5 (si está instalado)
print("\n7️⃣ VERIFICANDO CONEXIÓN CON MT5...")
try:
    import MetaTrader5 as mt5
    
    # Intentar inicializar
    if mt5.initialize():
        print("   ✓ MT5 se puede inicializar")
        
        # Intentar obtener información de la cuenta (sin login)
        terminal_info = mt5.terminal_info()
        if terminal_info:
            print(f"   ✓ Terminal MT5: {terminal_info.name}")
            print(f"   ✓ Versión: {terminal_info.build}")
            print(f"   ✓ Ruta: {terminal_info.path}")
        
        mt5.shutdown()
    else:
        error = mt5.last_error()
        print(f"   ❌ MT5 NO se puede inicializar")
        print(f"      Error: {error}")
        print("\n   POSIBLES CAUSAS:")
        print("      - MetaTrader 5 no está instalado")
        print("      - MetaTrader 5 no está abierto")
        print("      - MetaTrader 5 está en otra ubicación")
        
except ImportError:
    print("   ⚠️ MetaTrader5 no está instalado (no se puede verificar)")
except Exception as e:
    print(f"   ❌ Error al verificar MT5: {e}")
    traceback.print_exc()

# 8. Verificar estrategia
print("\n8️⃣ VERIFICANDO ESTRATEGIA...")
strategy_path = os.path.join(current_dir, "strategy", "ict_hybrid_strategy.py")
if os.path.exists(strategy_path):
    try:
        sys.path.insert(0, current_dir)
        from strategy.ict_hybrid_strategy import ICTHybridStrategy
        strategy = ICTHybridStrategy()
        print("   ✓ ICTHybridStrategy se puede importar e instanciar")
    except Exception as e:
        print(f"   ❌ Error al importar estrategia: {e}")
        traceback.print_exc()
else:
    print(f"   ❌ Estrategia no encontrada en: {strategy_path}")

# 9. Intentar importar mt5_trading
print("\n9️⃣ VERIFICANDO live/mt5_trading.py...")
mt5_trading_path = os.path.join(current_dir, "live", "mt5_trading.py")
if os.path.exists(mt5_trading_path):
    try:
        # Solo verificar que se puede leer y parsear
        with open(mt5_trading_path, 'r', encoding='utf-8') as f:
            code = f.read()
            compile(code, mt5_trading_path, 'exec')
        print("   ✓ live/mt5_trading.py se puede leer y parsear correctamente")
    except SyntaxError as e:
        print(f"   ❌ Error de sintaxis en mt5_trading.py: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"   ❌ Error al verificar mt5_trading.py: {e}")
        traceback.print_exc()
else:
    print(f"   ❌ live/mt5_trading.py NO EXISTE")

# 10. Resumen y recomendaciones
print("\n" + "=" * 70)
print("📋 RESUMEN Y RECOMENDACIONES")
print("=" * 70)

print("\n✅ Si todos los checks pasaron, el bot debería funcionar.")
print("\n🔧 COMANDO PARA INICIAR EL BOT:")
print(f"   cd \"{current_dir}\"")
print("   python -u live\\mt5_trading.py")
print("\n⚠️ IMPORTANTE:")
print("   1. Asegúrate de que MetaTrader 5 esté ABIERTO")
print("   2. Asegúrate de estar conectado a tu cuenta en MT5")
print("   3. Usa el flag -u para ver mensajes en tiempo real")
print("   4. Si hay errores, revisa los mensajes de arriba")

print("\n" + "=" * 70)




