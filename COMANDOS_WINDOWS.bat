@echo off
REM COMANDOS_WINDOWS.bat - Script para ejecutar en Windows
REM Ejecuta este archivo en PowerShell o CMD después de instalar Python

echo ============================================================
echo  INSTALANDO DEPENDENCIAS PARA MT5
echo ============================================================
echo.

python --version
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
pip install MetaTrader5 python-dotenv pandas numpy

if errorlevel 1 (
    echo ERROR al instalar dependencias
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  CONFIGURANDO CREDENCIALES
echo ============================================================
echo.
python setup_mt5.py

echo.
echo ============================================================
echo  PROBANDO CONEXION
echo ============================================================
echo.
echo IMPORTANTE: Abre MetaTrader 5 y conectate a tu cuenta antes de continuar
pause
python test_mt5_connection.py

echo.
echo ============================================================
echo  LISTO PARA EJECUTAR EL BOT
echo ============================================================
echo.
echo Para ejecutar el bot, usa:
echo   python live\mt5_trading.py
echo.
pause










