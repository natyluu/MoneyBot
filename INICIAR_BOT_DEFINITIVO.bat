@echo off
REM ======================================================================
REM SCRIPT DEFINITIVO PARA INICIAR EL BOT - RESUELVE TODOS LOS PROBLEMAS
REM ======================================================================

REM Configurar encoding UTF-8
chcp 65001 >nul 2>&1

REM Cambiar al directorio del proyecto
cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'" 2>nul
if errorlevel 1 (
    echo.
    echo [ERROR] No se pudo cambiar al directorio del proyecto
    echo Verifica que la ruta existe: C:\BOT\trading-bot-windows-20251210 on 'Mac'
    echo.
    pause
    exit /b 1
)

REM Verificar archivos críticos
if not exist "live\mt5_trading.py" (
    echo [ERROR] No se encontro live\mt5_trading.py
    pause
    exit /b 1
)

if not exist ".env" (
    echo [ADVERTENCIA] No se encontro .env
    echo El bot puede no funcionar sin credenciales
    echo.
    timeout /t 3 /nobreak >nul
)

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    pause
    exit /b 1
)

REM Verificar MT5
tasklist /FI "IMAGENAME eq terminal64.exe" 2>NUL | find /I /N "terminal64.exe">NUL
if errorlevel 1 (
    echo.
    echo ======================================================================
    echo ADVERTENCIA: MetaTrader 5 no esta abierto
    echo ======================================================================
    echo.
    echo El bot necesita MT5 abierto y conectado.
    echo.
    echo Pasos:
    echo 1. Abre MetaTrader 5
    echo 2. Conectate a tu cuenta (94342)
    echo 3. Verifica que XAUUSD.vip este visible
    echo.
    echo Presiona cualquier tecla para continuar de todos modos...
    pause >nul
    echo.
)

REM Configurar variables de entorno para unbuffered output
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

REM Limpiar pantalla
cls

echo ======================================================================
echo BOT DE TRADING AUTOMATICO - INICIANDO
echo ======================================================================
echo.
echo Directorio: %CD%
echo Python: 
python --version
echo.
echo IMPORTANTE:
echo - MetaTrader 5 debe estar ABIERTO y CONECTADO
echo - Presiona Ctrl+C para detener el bot
echo.
echo ======================================================================
echo.

REM Iniciar el bot con output unbuffered
REM Usar pythonw para evitar problemas de buffering en algunos casos
python -u live\mt5_trading.py

REM Si llegamos aquí, el bot se detuvo
echo.
echo ======================================================================
echo Bot detenido
echo ======================================================================
echo.
pause




