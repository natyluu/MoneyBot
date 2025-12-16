@echo off
REM ======================================================================
REM SCRIPT SIMPLE PARA INICIAR EL BOT DE TRADING
REM ======================================================================

REM Configurar encoding UTF-8
chcp 65001 >nul 2>&1

REM Cambiar al directorio del proyecto
cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

REM Verificar que estamos en el directorio correcto
if not exist "live\mt5_trading.py" (
    echo.
    echo ERROR: No se encontro live\mt5_trading.py
    echo Verifica que estas en el directorio correcto
    echo.
    pause
    exit /b 1
)

REM Configurar variables de entorno para output inmediato
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

REM Limpiar pantalla
cls

echo ======================================================================
echo INICIANDO BOT DE TRADING AUTOMATICO
echo ======================================================================
echo.
echo Directorio: %CD%
echo.
echo IMPORTANTE:
echo - MetaTrader 5 debe estar ABIERTO
echo - Debes estar CONECTADO a tu cuenta (94342)
echo - XAUUSD.vip debe estar visible en Market Watch
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
