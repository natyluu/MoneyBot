@echo off
chcp 65001 >nul 2>&1
echo =====================================================================
echo VERIFICACION FINAL Y INICIO DEL BOT
echo =====================================================================
echo.

REM Cambiar al directorio del proyecto
cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
if errorlevel 1 (
    echo ERROR: No se puede acceder al directorio del proyecto
    pause
    exit /b 1
)

echo Directorio: %CD%
echo.

echo [1] Verificando archivos CRITICOS...
echo.

if exist "live\mt5_trading.py" (
    echo    [OK] live\mt5_trading.py
) else (
    echo    [ERROR] live\mt5_trading.py NO existe
    pause
    exit /b 1
)

if exist "config.py" (
    echo    [OK] config.py
) else (
    echo    [ERROR] config.py NO existe
    pause
    exit /b 1
)

if exist "strategy\ict_hybrid_strategy.py" (
    echo    [OK] strategy\ict_hybrid_strategy.py
) else (
    echo    [ERROR] strategy\ict_hybrid_strategy.py NO existe
    pause
    exit /b 1
)

if exist ".env" (
    echo    [OK] .env existe
) else (
    echo    [ADVERTENCIA] .env NO existe - Verifica que tenga tus credenciales
)

echo.
echo [2] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo    [ERROR] Python no encontrado
    pause
    exit /b 1
) else (
    python --version
    echo    [OK] Python instalado
)

echo.
echo [3] Verificando modulo MetaTrader5...
python -c "import MetaTrader5; print('    [OK] MetaTrader5 instalado')" 2>nul
if errorlevel 1 (
    echo    [ERROR] MetaTrader5 NO instalado
    echo    Ejecuta: pip install MetaTrader5
    pause
    exit /b 1
)

echo.
echo [4] Verificando que MT5 este ejecutandose...
tasklist | findstr /i "terminal64.exe" >nul 2>&1
if errorlevel 1 (
    echo    [ADVERTENCIA] MetaTrader 5 no parece estar ejecutandose
    echo    Abre MT5 antes de continuar
    echo.
    pause
) else (
    echo    [OK] MetaTrader 5 esta ejecutandose
)

echo.
echo =====================================================================
echo VERIFICACION COMPLETADA
echo =====================================================================
echo.
echo Presiona cualquier tecla para INICIAR EL BOT...
echo O presiona Ctrl+C para cancelar
echo.
pause >nul

echo.
echo =====================================================================
echo INICIANDO BOT DE TRADING
echo =====================================================================
echo.

REM Configurar variables de entorno para output sin buffer
set PYTHONUNBUFFERED=1

REM Iniciar el bot
python -u live\mt5_trading.py

echo.
echo =====================================================================
echo BOT DETENIDO
echo =====================================================================
echo.
pause




