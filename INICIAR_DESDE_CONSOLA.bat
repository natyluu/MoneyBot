@echo off
REM Script para abrir la consola y ejecutar comandos automáticamente
chcp 65001 >nul 2>&1

echo ======================================================================
echo ABRIENDO CONSOLA PARA INICIAR EL BOT
echo ======================================================================
echo.
echo Este script abrira una nueva ventana de consola
echo con los comandos listos para ejecutar.
echo.
pause

REM Abrir nueva ventana de CMD con los comandos
start cmd /k "cd /d \"C:\BOT\trading-bot-windows-20251210 on 'Mac'\" && echo ====================================================================== && echo BOT DE TRADING - LISTO PARA INICIAR && echo ====================================================================== && echo. && echo Directorio: && cd && echo. && echo IMPORTANTE: Asegurate de que MetaTrader 5 este ABIERTO && echo. && echo Para iniciar el bot, ejecuta: && echo python -u live\mt5_trading.py && echo. && echo ====================================================================== && cmd /k"




