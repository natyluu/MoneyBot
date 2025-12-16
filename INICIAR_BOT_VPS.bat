@echo off
REM ========================================
REM   INICIAR BOT DE TRADING EN VPS
REM ========================================
chcp 65001 >nul 2>&1
echo.
echo ========================================
echo   INICIANDO BOT DE TRADING EN VPS
echo ========================================
echo.

REM Cambiar al directorio del proyecto
cd /d "C:\BOT\trading-bot"
if errorlevel 1 (
    echo ERROR: No se pudo cambiar al directorio del proyecto
    echo Verifica que la ruta C:\BOT\trading-bot existe
    pause
    exit /b 1
)

REM Configurar unbuffered output
set PYTHONUNBUFFERED=1

REM Verificar que MT5 esté abierto
tasklist | findstr /i terminal64 >nul
if errorlevel 1 (
    echo.
    echo ========================================
    echo   ADVERTENCIA: MetaTrader 5 NO está abierto
    echo ========================================
    echo.
    echo El bot necesita MT5 abierto y conectado.
    echo ¿Deseas continuar de todas formas? (S/N)
    set /p continuar=
    if /i not "%continuar%"=="S" (
        echo Bot cancelado.
        pause
        exit /b 1
    )
)

REM Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en PATH
    pause
    exit /b 1
)

REM Verificar que el archivo existe
if not exist "live\mt5_trading.py" (
    echo ERROR: No se encontró live\mt5_trading.py
    echo Verifica que estás en el directorio correcto
    pause
    exit /b 1
)

echo.
echo Iniciando bot...
echo Presiona Ctrl+C para detener
echo.
echo ========================================
echo.

REM Ejecutar el bot
python -u live\mt5_trading.py

REM Si el bot se detiene, mostrar mensaje
echo.
echo ========================================
echo   BOT DETENIDO
echo ========================================
echo.
pause

