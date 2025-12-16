@echo off
REM Script de prueba para verificar que todo funciona
chcp 65001 >nul 2>&1

echo ======================================================================
echo TEST DEL BOT - VERIFICACION COMPLETA
echo ======================================================================
echo.

REM Cambiar al directorio
cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'" 2>nul
if errorlevel 1 (
    echo [ERROR] No se pudo cambiar al directorio
    pause
    exit /b 1
)

echo [OK] Directorio: %CD%
echo.

REM Verificar archivos
if exist "config.py" (
    echo [OK] config.py existe
) else (
    echo [ERROR] config.py NO existe
)

if exist ".env" (
    echo [OK] .env existe
) else (
    echo [ERROR] .env NO existe
)

if exist "live\mt5_trading.py" (
    echo [OK] live\mt5_trading.py existe
) else (
    echo [ERROR] live\mt5_trading.py NO existe
)

if exist "strategy\ict_hybrid_strategy.py" (
    echo [OK] strategy\ict_hybrid_strategy.py existe
) else (
    echo [ERROR] strategy\ict_hybrid_strategy.py NO existe
)

echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python NO esta instalado
) else (
    echo [OK] Python esta instalado:
    python --version
)

echo.

REM Verificar modulos
echo Verificando modulos Python...
python -c "import MetaTrader5; print('[OK] MetaTrader5 instalado')" 2>nul || echo [ERROR] MetaTrader5 NO instalado
python -c "import pandas; print('[OK] pandas instalado')" 2>nul || echo [ERROR] pandas NO instalado
python -c "import numpy; print('[OK] numpy instalado')" 2>nul || echo [ERROR] numpy NO instalado

echo.

REM Verificar MT5
tasklist /FI "IMAGENAME eq terminal64.exe" 2>NUL | find /I /N "terminal64.exe">NUL
if errorlevel 1 (
    echo [ADVERTENCIA] MetaTrader 5 NO esta abierto
) else (
    echo [OK] MetaTrader 5 esta abierto
)

echo.
echo ======================================================================
echo TEST COMPLETADO
echo ======================================================================
echo.
pause




