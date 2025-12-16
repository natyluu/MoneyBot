"""
test_mt5_macos.py - Prueba de conexión a MT5 en macOS

Este script intenta diferentes métodos para conectar a MT5 en macOS.
"""

import sys
import os

print("=" * 70)
print("PRUEBA DE CONEXIÓN A MT5 EN MACOS")
print("=" * 70)

# Método 1: Intentar importar MetaTrader5 directamente
print("\n1️⃣ Intentando importar MetaTrader5...")
try:
    import MetaTrader5 as mt5
    print("   ✅ MetaTrader5 importado exitosamente!")
    
    # Intenta inicializar
    if mt5.initialize():
        print("   ✅ MT5 inicializado correctamente")
        terminal_info = mt5.terminal_info()
        if terminal_info:
            print(f"   ✅ Terminal: {terminal_info.name}")
            print(f"   ✅ Versión: {terminal_info.version}")
        mt5.shutdown()
    else:
        error = mt5.last_error()
        print(f"   ⚠️ Error al inicializar: {error}")
        print("   💡 Asegúrate de que MT5 esté abierto")
    
except ImportError as e:
    print(f"   ❌ No se puede importar MetaTrader5: {e}")
    print("   💡 El paquete no está disponible para macOS")

# Método 2: Buscar MT5 instalado
print("\n2️⃣ Buscando MetaTrader 5 instalado...")
mt5_paths = [
    "/Applications/MetaTrader 5.app",
    "/Applications/MetaTrader5.app",
    os.path.expanduser("~/Applications/MetaTrader 5.app"),
    "/Applications/Trading/MetaTrader 5.app"
]

found = False
for path in mt5_paths:
    if os.path.exists(path):
        print(f"   ✅ MT5 encontrado en: {path}")
        found = True
        break

if not found:
    print("   ⚠️ MT5 no encontrado en ubicaciones comunes")
    print("   💡 Verifica que MT5 esté instalado en /Applications/")

# Método 3: Verificar si hay API alternativa
print("\n3️⃣ Verificando alternativas...")
print("   💡 Si MT5 está instalado pero el paquete Python no funciona,")
print("      puedes usar:")
print("      - MQL5 Bridge (si está disponible)")
print("      - API REST del broker (si Zeven la tiene)")
print("      - Conexión por socket local")

# Método 4: Intentar conexión por socket (si MT5 tiene servidor local)
print("\n4️⃣ Intentando conexión alternativa...")
print("   💡 Algunas versiones de MT5 tienen servidor local")
print("      que se puede acceder por socket")

print("\n" + "=" * 70)
print("RECOMENDACIÓN")
print("=" * 70)
print("\nSi tienes MT5 instalado pero el paquete Python no funciona:")
print("1. Verifica que MT5 esté ABIERTO")
print("2. Intenta usar una máquina virtual Windows con Parallels")
print("3. O verifica si Zeven tiene API REST disponible")
print("\n" + "=" * 70)









