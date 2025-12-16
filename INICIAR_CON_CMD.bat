@echo off
REM Script para iniciar el bot usando CMD (mejor para mostrar mensajes)
chcp 65001 >nul 2>&1

cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'" 2>nul
if errorlevel 1 (
    echo ERROR: No se encontro el directorio
    pause
    exit /b 1
)

set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

echo ======================================================================
echo INICIANDO BOT DE TRADING
echo ======================================================================
echo.
echo Presiona Ctrl+C para detener
echo.
echo ======================================================================
echo.

python -u live\mt5_trading.py

pause




