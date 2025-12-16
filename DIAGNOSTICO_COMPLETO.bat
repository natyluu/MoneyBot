@echo off
chcp 65001 >nul 2>&1
echo =====================================================================
echo DIAGNOSTICO COMPLETO DEL BOT
echo =====================================================================
echo.

echo [1] Verificando directorio actual...
echo Directorio: %CD%
echo.

echo [2] Verificando archivos del proyecto...
if exist "live\mt5_trading.py" (
    echo    OK: live\mt5_trading.py existe
) else (
    echo    ERROR: live\mt5_trading.py NO existe
    echo    Buscando archivos en el directorio actual...
    dir /b
    echo.
    echo    Buscando en subdirectorios...
    dir /s /b mt5_trading.py 2>nul
)
echo.

echo [3] Verificando Python...
python --version 2>nul
if errorlevel 1 (
    echo    ERROR: Python no encontrado
) else (
    echo    OK: Python instalado
)
echo.

echo [4] Verificando modulo MetaTrader5...
python -c "import MetaTrader5; print('    OK: MetaTrader5 instalado')" 2>nul
if errorlevel 1 (
    echo    ERROR: MetaTrader5 NO instalado
    echo    Ejecuta: pip install MetaTrader5
)
echo.

echo [5] Verificando archivo .env...
if exist ".env" (
    echo    OK: .env existe
    echo    Contenido (sin mostrar contraseña):
    findstr /V "PASSWORD" .env 2>nul
) else (
    echo    ERROR: .env NO existe
)
echo.

echo [6] Verificando MT5...
tasklist | findstr /i "terminal64.exe" >nul 2>nul
if errorlevel 1 (
    echo    ADVERTENCIA: MetaTrader 5 no parece estar ejecutandose
    echo    Abre MT5 antes de iniciar el bot
) else (
    echo    OK: MetaTrader 5 esta ejecutandose
)
echo.

echo =====================================================================
echo DIAGNOSTICO COMPLETADO
echo =====================================================================
echo.
echo Si hay errores, corrigelos antes de iniciar el bot.
echo.
pause




