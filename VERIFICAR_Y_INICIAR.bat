@echo off
REM Script que verifica TODO y luego inicia el bot
chcp 65001 >nul 2>&1

echo ======================================================================
echo VERIFICACION COMPLETA Y INICIO DEL BOT
echo ======================================================================
echo.

cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'" 2>nul
if errorlevel 1 (
    echo [ERROR] Directorio no encontrado
    pause
    exit /b 1
)

echo [1/5] Verificando archivos...
if exist "config.py" (echo   [OK] config.py) else (echo   [FALTA] config.py)
if exist ".env" (echo   [OK] .env) else (echo   [FALTA] .env - CRITICO)
if exist "live\mt5_trading.py" (echo   [OK] live\mt5_trading.py) else (echo   [FALTA] live\mt5_trading.py)
echo.

echo [2/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Python no encontrado
    pause
    exit /b 1
) else (
    echo   [OK] Python instalado
    python --version
)
echo.

echo [3/5] Verificando modulos...
python -c "import MetaTrader5" 2>nul && echo   [OK] MetaTrader5 || echo   [FALTA] MetaTrader5 - Ejecuta: pip install MetaTrader5
python -c "import pandas" 2>nul && echo   [OK] pandas || echo   [FALTA] pandas - Ejecuta: pip install pandas
python -c "import numpy" 2>nul && echo   [OK] numpy || echo   [FALTA] numpy - Ejecuta: pip install numpy
echo.

echo [4/5] Verificando MetaTrader 5...
tasklist /FI "IMAGENAME eq terminal64.exe" 2>NUL | find /I /N "terminal64.exe">NUL
if errorlevel 1 (
    echo   [ADVERTENCIA] MT5 no esta abierto
    echo.
    echo   IMPORTANTE: Abre MetaTrader 5 antes de continuar
    echo.
    timeout /t 5 /nobreak
) else (
    echo   [OK] MetaTrader 5 esta abierto
)
echo.

echo [5/5] Iniciando bot...
echo.
echo ======================================================================
echo INICIANDO BOT DE TRADING
echo ======================================================================
echo.
echo Presiona Ctrl+C para detener
echo.
echo ======================================================================
echo.

set PYTHONUNBUFFERED=1
python -u live\mt5_trading.py

echo.
echo Bot detenido
pause




