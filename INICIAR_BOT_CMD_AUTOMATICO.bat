@echo off
REM Script que abre CMD automáticamente y ejecuta el bot
REM CMD muestra los mensajes mejor que PowerShell

REM Abrir nueva ventana de CMD con los comandos listos
start cmd /k "cd /d \"C:\BOT\trading-bot-windows-20251210 on 'Mac'\" && echo ====================================================================== && echo INICIANDO BOT DE TRADING && echo ====================================================================== && echo. && echo IMPORTANTE: MetaTrader 5 debe estar ABIERTO && echo. && echo Presiona Ctrl+C para detener el bot && echo. && echo ====================================================================== && echo. && set PYTHONUNBUFFERED=1 && python -u live\mt5_trading.py && echo. && echo ====================================================================== && echo Bot detenido && echo ====================================================================== && pause"




