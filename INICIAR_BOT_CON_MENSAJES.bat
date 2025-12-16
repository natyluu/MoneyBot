@echo off
REM Script para iniciar el bot con mensajes visibles inmediatamente
chcp 65001 >nul 2>&1

cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'" 2>nul
if errorlevel 1 (
    echo ERROR: No se encontro el directorio
    pause
    exit /b 1
)

REM Configurar variables de entorno
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

REM Forzar que Python no use buffer
set PYTHONUNBUFFERED=1

echo ======================================================================
echo INICIANDO BOT - MENSAJES VISIBLES INMEDIATAMENTE
echo ======================================================================
echo.
echo IMPORTANTE: MetaTrader 5 debe estar ABIERTO
echo.
echo ======================================================================
echo.

REM Ejecutar Python con flags adicionales para forzar unbuffered
REM Usar -u y también redirigir para forzar flush
python -u -W ignore live\mt5_trading.py

REM Si llegamos aqui, el bot se detuvo
echo.
echo ======================================================================
echo Bot detenido
echo ======================================================================
pause




