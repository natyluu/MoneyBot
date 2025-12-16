"""
intentar_conexion_mt5.py - Intenta conectar a MT5 en macOS

Este script prueba diferentes métodos para conectar a MT5 cuando está
instalado en macOS a través de Wine.
"""

import sys
import os
import subprocess

print("=" * 70)
print("INTENTANDO CONECTAR A MT5 EN MACOS")
print("=" * 70)

# Verifica que MT5 esté instalado
mt5_path = "/Applications/MetaTrader 5.app"
if os.path.exists(mt5_path):
    print(f"✅ MT5 encontrado en: {mt5_path}")
else:
    print("❌ MT5 no encontrado")
    sys.exit(1)

# Método 1: Intentar instalar MetaTrader5 con flags especiales
print("\n1️⃣ Intentando instalar MetaTrader5 con método alternativo...")
try:
    # Intenta instalar desde source o con flags especiales
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "MetaTrader5", "--no-binary", ":all:"],
        capture_output=True,
        text=True,
        timeout=60
    )
    if result.returncode == 0:
        print("   ✅ Instalación exitosa")
    else:
        print(f"   ❌ Error: {result.stderr[:200]}")
except Exception as e:
    print(f"   ⚠️ No se pudo instalar: {e}")

# Método 2: Intentar importar
print("\n2️⃣ Intentando importar MetaTrader5...")
try:
    import MetaTrader5 as mt5
    print("   ✅ MetaTrader5 importado!")
    
    # Intenta inicializar
    print("\n3️⃣ Intentando inicializar MT5...")
    print("   ⚠️ Asegúrate de que MT5 esté ABIERTO")
    
    if mt5.initialize():
        print("   ✅ MT5 inicializado exitosamente!")
        
        # Obtiene información
        terminal_info = mt5.terminal_info()
        if terminal_info:
            print(f"\n   📊 Información del Terminal:")
            print(f"      Nombre: {terminal_info.name}")
            print(f"      Versión: {terminal_info.version}")
            print(f"      Compilación: {terminal_info.build}")
        
        account_info = mt5.account_info()
        if account_info:
            print(f"\n   💰 Información de la Cuenta:")
            print(f"      Balance: ${account_info.balance:,.2f}")
            print(f"      Servidor: {account_info.server}")
        
        mt5.shutdown()
        print("\n   ✅ Conexión exitosa!")
        
    else:
        error = mt5.last_error()
        print(f"   ❌ Error al inicializar: {error}")
        print("\n   Posibles soluciones:")
        print("   1. Asegúrate de que MT5 esté ABIERTO")
        print("   2. Verifica que estés conectado a tu cuenta")
        print("   3. Intenta reiniciar MT5")
        
except ImportError:
    print("   ❌ MetaTrader5 no se puede importar")
    print("\n   💡 SOLUCIÓN: Necesitas instalar MetaTrader5 en Windows")
    print("   Opciones:")
    print("   1. Usar Parallels Desktop con Windows")
    print("   2. Usar VPS Windows")
    print("   3. Verificar si Zeven tiene API REST")

print("\n" + "=" * 70)









