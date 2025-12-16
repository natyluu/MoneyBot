@echo off
REM Script simple y directo para iniciar el bot
chcp 65001 >nul 2>&1

REM Cambiar al directorio
cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

REM Verificar que el archivo existe
if not exist "live\mt5_trading.py" (
    echo.
    echo ERROR: No se encontro live\mt5_trading.py
    echo.
    echo Verifica que estas en el directorio correcto
    echo Directorio actual: %CD%
    echo.
    dir live
    echo.
    pause
    exit /b 1
)

REM Configurar variables
set PYTHONUNBUFFERED=1

REM Iniciar el bot
echo.
echo Iniciando bot...
echo.
python -u live\mt5_trading.py

pause




