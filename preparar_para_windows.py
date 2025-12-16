"""
preparar_para_windows.py - Prepara el proyecto para ejecutar en Windows

Este script verifica que todo esté listo para cuando ejecutes el bot en Windows.
"""

import os
import sys

def check_project_structure():
    """Verifica que la estructura del proyecto esté completa"""
    print("=" * 70)
    print("VERIFICANDO ESTRUCTURA DEL PROYECTO")
    print("=" * 70)
    
    required_files = [
        "config.py",
        "backtest/backtest.py",
        "live/mt5_trading.py",
        "live/paper_trader.py",
        "live/alert_system.py",
        "strategy/ict_hybrid_strategy.py",
        "strategy/ict_utils.py",
        "utils/data_loader.py",
        "utils/multi_timeframe_loader.py",
        "setup_mt5.py",
        "test_mt5_connection.py"
    ]
    
    all_ok = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - FALTA")
            all_ok = False
    
    return all_ok

def check_data_files():
    """Verifica que haya datos para backtesting"""
    print("\n" + "=" * 70)
    print("VERIFICANDO DATOS HISTÓRICOS")
    print("=" * 70)
    
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"   ⚠️ Carpeta {data_dir} no existe")
        return False
    
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if len(csv_files) == 0:
        print("   ⚠️ No hay archivos CSV en data/")
        print("   💡 Ejecuta: python3 utils/generate_sample_data.py")
        return False
    
    print(f"   ✅ {len(csv_files)} archivos CSV encontrados:")
    for f in csv_files[:10]:  # Muestra los primeros 10
        print(f"      - {f}")
    
    if len(csv_files) > 10:
        print(f"      ... y {len(csv_files) - 10} más")
    
    return True

def create_windows_instructions():
    """Crea instrucciones para Windows"""
    print("\n" + "=" * 70)
    print("INSTRUCCIONES PARA WINDOWS")
    print("=" * 70)
    
    instructions = """
═══════════════════════════════════════════════════════════════
  INSTRUCCIONES PARA EJECUTAR EN WINDOWS
═══════════════════════════════════════════════════════════════

PASO 1: INSTALAR PYTHON EN WINDOWS
───────────────────────────────────────────────────────────────
1. Descarga Python desde: https://www.python.org/downloads/
2. Durante instalación, marca "Add Python to PATH"
3. Verifica: Abre PowerShell y ejecuta:
   python --version
   pip --version

PASO 2: INSTALAR DEPENDENCIAS
───────────────────────────────────────────────────────────────
Abre PowerShell en la carpeta del proyecto y ejecuta:

   pip install MetaTrader5 python-dotenv pandas numpy

PASO 3: CONFIGURAR CREDENCIALES
───────────────────────────────────────────────────────────────
Ejecuta:

   python setup_mt5.py

Ingresa tus credenciales de MT5 cuando te las pida.

PASO 4: PROBAR CONEXIÓN
───────────────────────────────────────────────────────────────
1. Abre MetaTrader 5
2. Conéctate a tu cuenta Zeven
3. Ejecuta:

   python test_mt5_connection.py

Si ves "✅ PRUEBA COMPLETADA EXITOSAMENTE", todo está bien.

PASO 5: EJECUTAR EL BOT
───────────────────────────────────────────────────────────────
Ejecuta:

   python live/mt5_trading.py

El bot se conectará automáticamente y empezará a operar.

═══════════════════════════════════════════════════════════════
"""
    
    print(instructions)
    
    # Guarda en archivo
    with open("INSTRUCCIONES_WINDOWS.txt", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("✅ Instrucciones guardadas en: INSTRUCCIONES_WINDOWS.txt")

def main():
    """Función principal"""
    print("\n🔍 Verificando proyecto para ejecución en Windows...\n")
    
    # Verifica estructura
    structure_ok = check_project_structure()
    
    # Verifica datos
    data_ok = check_data_files()
    
    # Crea instrucciones
    create_windows_instructions()
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)
    
    if structure_ok:
        print("✅ Estructura del proyecto: COMPLETA")
    else:
        print("❌ Estructura del proyecto: FALTAN ARCHIVOS")
    
    if data_ok:
        print("✅ Datos históricos: DISPONIBLES")
    else:
        print("⚠️ Datos históricos: FALTAN (ejecuta generate_sample_data.py)")
    
    print("\n📋 Próximos pasos:")
    print("   1. Obtén acceso a Windows (Parallels, VPS, etc.)")
    print("   2. Sigue las instrucciones en: INSTRUCCIONES_WINDOWS.txt")
    print("   3. Ejecuta el bot desde Windows")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()










