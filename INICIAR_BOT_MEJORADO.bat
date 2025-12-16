@echo off
REM Script mejorado para iniciar el bot con diagnóstico y manejo de errores
chcp 65001 >nul
echo ======================================================================
echo INICIANDO BOT DE TRADING - VERSION MEJORADA
echo ======================================================================
echo.

REM Cambiar al directorio del proyecto
cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
if errorlevel 1 (
    echo ERROR: No se pudo cambiar al directorio del proyecto
    echo Verifica que la ruta existe: "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
    pause
    exit /b 1
)

echo Directorio actual: %CD%
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Instala Python 3.12 desde python.org
    pause
    exit /b 1
)

echo Python encontrado:
python --version
echo.

REM Verificar que el archivo existe
if not exist "live\mt5_trading.py" (
    echo ERROR: No se encontró live\mt5_trading.py
    echo Verifica que estás en el directorio correcto
    pause
    exit /b 1
)

echo Archivo encontrado: live\mt5_trading.py
echo.

REM Verificar que MT5 está abierto (opcional, solo advertencia)
tasklist /FI "IMAGENAME eq terminal64.exe" 2>NUL | find /I /N "terminal64.exe">NUL
if errorlevel 1 (
    echo ADVERTENCIA: MetaTrader 5 no parece estar abierto
    echo Asegúrate de abrir MT5 antes de iniciar el bot
    echo.
    timeout /t 3 /nobreak >nul
)

echo ======================================================================
echo INICIANDO BOT...
echo ======================================================================
echo.
echo Presiona Ctrl+C para detener el bot
echo.

REM Iniciar el bot con unbuffered output
set PYTHONUNBUFFERED=1
python -u live\mt5_trading.py

REM Si el bot se detiene, mostrar mensaje
echo.
echo ======================================================================
echo Bot detenido
echo ======================================================================
pause




