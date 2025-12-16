@echo off
REM Script para iniciar el bot - Abre CMD automáticamente
chcp 65001 >nul 2>&1

REM Abrir nueva ventana de CMD con los comandos listos
start cmd /k "cd /d \"C:\BOT\trading-bot-windows-20251210 on 'Mac'\" && echo ====================================================================== && echo INICIANDO BOT DE TRADING && echo ====================================================================== && echo. && echo IMPORTANTE: MetaTrader 5 debe estar ABIERTO && echo. && set PYTHONUNBUFFERED=1 && python -u live\mt5_trading.py && pause"




