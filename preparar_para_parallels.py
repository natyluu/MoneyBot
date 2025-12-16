"""
preparar_para_parallels.py - Prepara el proyecto para copiar a Windows/Parallels

Este script crea un paquete listo para copiar a Windows en Parallels.
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_windows_package():
    """Crea un paquete del proyecto listo para Windows"""
    print("=" * 70)
    print("PREPARANDO PROYECTO PARA WINDOWS (PARALLELS)")
    print("=" * 70)
    
    # Archivos y carpetas a incluir
    include_items = [
        "backtest",
        "live",
        "strategy",
        "utils",
        "config.py",
        "requirements.txt",
        "setup_mt5.py",
        "test_mt5_connection.py",
        "COMANDOS_WINDOWS.bat",
        "COMANDOS_WINDOWS.ps1",
        "INSTRUCCIONES_WINDOWS.txt",
        "README.md"
    ]
    
    # Excluir
    exclude_items = [
        "__pycache__",
        "*.pyc",
        ".env",
        "data",  # Los datos se pueden regenerar o copiar por separado
        ".git"
    ]
    
    # Crea carpeta temporal
    package_name = f"trading-bot-windows-{datetime.now().strftime('%Y%m%d')}"
    package_path = os.path.join("..", package_name)
    
    if os.path.exists(package_path):
        shutil.rmtree(package_path)
    
    os.makedirs(package_path, exist_ok=True)
    
    print(f"\n📦 Creando paquete en: {package_path}")
    
    # Copia archivos
    copied = 0
    for item in include_items:
        src = item
        dst = os.path.join(package_path, item)
        
        if os.path.exists(src):
            if os.path.isdir(src):
                # Copia directorio
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))
                print(f"   ✅ Copiado: {item}/")
                copied += 1
            else:
                # Copia archivo
                shutil.copy2(src, dst)
                print(f"   ✅ Copiado: {item}")
                copied += 1
        else:
            print(f"   ⚠️ No encontrado: {item}")
    
    # Crea archivo .env.example
    env_example = """# Configuración MetaTrader 5 (Zeven)
# Copia este archivo a .env y completa con tus credenciales

MT5_LOGIN=tu_numero_cuenta
MT5_PASSWORD=tu_password
MT5_SERVER=ZevenGlobal-Demo
MT5_SYMBOL=XAUUSD

RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=2.0
"""
    
    with open(os.path.join(package_path, ".env.example"), "w") as f:
        f.write(env_example)
    print(f"   ✅ Creado: .env.example")
    
    # Crea README para Windows
    windows_readme = """# Bot de Trading - Instrucciones para Windows

## Instalación Rápida

1. **Instala Python:**
   - Descarga desde: https://www.python.org/downloads/
   - Marca "Add Python to PATH" durante instalación

2. **Instala dependencias:**
   ```powershell
   pip install MetaTrader5 python-dotenv pandas numpy
   ```

3. **Configura credenciales:**
   ```powershell
   python setup_mt5.py
   ```

4. **Prueba conexión (con MT5 abierto):**
   ```powershell
   python test_mt5_connection.py
   ```

5. **Ejecuta el bot:**
   ```powershell
   python live/mt5_trading.py
   ```

## Archivos Importantes

- `setup_mt5.py` - Configura credenciales
- `test_mt5_connection.py` - Prueba conexión
- `live/mt5_trading.py` - Bot de trading
- `backtest/backtest.py` - Backtesting

## Más Información

Ver `INSTRUCCIONES_WINDOWS.txt` para guía detallada.
"""
    
    with open(os.path.join(package_path, "README_WINDOWS.md"), "w", encoding="utf-8") as f:
        f.write(windows_readme)
    print(f"   ✅ Creado: README_WINDOWS.md")
    
    # Crea script de instalación rápida
    install_script = """@echo off
echo Instalando dependencias...
pip install MetaTrader5 python-dotenv pandas numpy
echo.
echo Instalacion completada!
echo.
echo Siguiente paso: python setup_mt5.py
pause
"""
    
    with open(os.path.join(package_path, "INSTALAR.bat"), "w") as f:
        f.write(install_script)
    print(f"   ✅ Creado: INSTALAR.bat")
    
    print(f"\n✅ Paquete creado: {package_path}")
    print(f"   {copied} items copiados")
    
    # Crea ZIP opcional
    zip_name = f"{package_name}.zip"
    zip_path = os.path.join("..", zip_name)
    
    respuesta = input("\n¿Deseas crear un archivo ZIP del paquete? (s/n): ")
    if respuesta.lower() == 's':
        print(f"\n📦 Creando ZIP: {zip_path}")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(package_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(package_path))
                    zipf.write(file_path, arcname)
        print(f"   ✅ ZIP creado: {zip_path}")
    
    print("\n" + "=" * 70)
    print("PRÓXIMOS PASOS")
    print("=" * 70)
    print(f"\n1. Copia la carpeta '{package_name}' a Windows:")
    print(f"   - Opción A: Usa carpeta compartida de Parallels")
    print(f"   - Opción B: Crea ZIP y transfiere")
    print(f"   - Opción C: Usa USB/disco externo")
    print(f"\n2. En Windows, descomprime (si es ZIP) y sigue:")
    print(f"   - Lee README_WINDOWS.md")
    print(f"   - Ejecuta INSTALAR.bat")
    print(f"   - Ejecuta python setup_mt5.py")
    print("\n" + "=" * 70)
    
    return package_path

if __name__ == "__main__":
    try:
        package_path = create_windows_package()
        print(f"\n✅ Proyecto preparado en: {package_path}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()









