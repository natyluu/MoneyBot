@echo off
REM ======================================================================
REM SCRIPT FINAL PARA INICIAR EL BOT DE TRADING
REM ======================================================================

REM Configurar encoding UTF-8
chcp 65001 >nul 2>&1

REM Cambiar al directorio del proyecto
cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'" 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: No se pudo cambiar al directorio del proyecto
    echo.
    echo Verifica que la ruta existe:
    echo C:\BOT\trading-bot-windows-20251210 on 'Mac'
    echo.
    pause
    exit /b 1
)

REM Mostrar directorio actual
echo.
echo Directorio: %CD%
echo.

REM Verificar que el archivo existe
if not exist "live\mt5_trading.py" (
    echo ERROR: No se encontro live\mt5_trading.py
    echo.
    echo Archivos en el directorio actual:
    dir /b
    echo.
    pause
    exit /b 1
)

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo.
    echo Instala Python 3.12 desde python.org
    echo.
    pause
    exit /b 1
)

echo Python encontrado:
python --version
echo.

REM Verificar MT5
tasklist /FI "IMAGENAME eq terminal64.exe" 2>NUL | find /I /N "terminal64.exe">NUL
if errorlevel 1 (
    echo.
    echo ======================================================================
    echo ADVERTENCIA: MetaTrader 5 no parece estar abierto
    echo ======================================================================
    echo.
    echo El bot necesita MT5 abierto y conectado para funcionar.
    echo.
    echo Pasos:
    echo 1. Abre MetaTrader 5
    echo 2. Conectate a tu cuenta (94342)
    echo 3. Verifica que XAUUSD.vip este visible en Market Watch
    echo.
    echo Presiona cualquier tecla para continuar de todos modos...
    pause >nul
    echo.
)

REM Configurar variables de entorno
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

echo ======================================================================
echo INICIANDO BOT DE TRADING AUTOMATICO
echo ======================================================================
echo.
echo Presiona Ctrl+C para detener el bot
echo.
echo ======================================================================
echo.

REM Iniciar el bot
python -u live\mt5_trading.py

REM Si llegamos aqui, el bot se detuvo
echo.
echo ======================================================================
echo Bot detenido
echo ======================================================================
echo.
pause




