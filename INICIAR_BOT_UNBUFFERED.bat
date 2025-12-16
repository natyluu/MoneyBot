@echo off
REM Script para iniciar el bot con output unbuffered forzado
chcp 65001 >nul
cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

REM Forzar variables de entorno para unbuffered
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

REM Iniciar Python con flags adicionales para forzar unbuffered
python -u -W ignore live\mt5_trading.py

pause




