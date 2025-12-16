@echo off
chcp 65001 >nul 2>&1
echo =====================================================================
echo VERIFICACION DE ARCHIVOS EN WINDOWS
echo =====================================================================
echo.

REM Cambiar al directorio del proyecto
cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'" 2>nul
if errorlevel 1 (
    echo ERROR: No se puede acceder al directorio del proyecto
    echo.
    echo Directorios disponibles en C:\BOT:
    dir C:\BOT /b
    echo.
    echo Directorios disponibles en disco C:
    dir C:\ /b | findstr /i "bot"
    echo.
    pause
    exit /b 1
)

echo Directorio actual: %CD%
echo.

echo [1] Verificando archivos CRITICOS...
echo.

if exist "live\mt5_trading.py" (
    echo    [OK] live\mt5_trading.py existe
    for %%F in ("live\mt5_trading.py") do echo        Fecha: %%~tF
) else (
    echo    [ERROR] live\mt5_trading.py NO existe
)

if exist "config.py" (
    echo    [OK] config.py existe
    for %%F in ("config.py") do echo        Fecha: %%~tF
) else (
    echo    [ERROR] config.py NO existe
)

if exist "strategy\ict_hybrid_strategy.py" (
    echo    [OK] strategy\ict_hybrid_strategy.py existe
    for %%F in ("strategy\ict_hybrid_strategy.py") do echo        Fecha: %%~tF
) else (
    echo    [ERROR] strategy\ict_hybrid_strategy.py NO existe
)

if exist ".env" (
    echo    [OK] .env existe
    for %%F in (".env") do echo        Fecha: %%~tF
) else (
    echo    [ERROR] .env NO existe
)

echo.
echo [2] Verificando scripts de inicio...
echo.

if exist "INICIAR_BOT_FACIL.bat" (
    echo    [OK] INICIAR_BOT_FACIL.bat existe
) else (
    echo    [FALTA] INICIAR_BOT_FACIL.bat
)

if exist "DIAGNOSTICO_COMPLETO.bat" (
    echo    [OK] DIAGNOSTICO_COMPLETO.bat existe
) else (
    echo    [FALTA] DIAGNOSTICO_COMPLETO.bat
)

echo.
echo [3] Verificando estructura de carpetas...
echo.

if exist "live" (
    echo    [OK] Carpeta live existe
    echo    Archivos en live:
    dir live\*.py /b 2>nul
) else (
    echo    [ERROR] Carpeta live NO existe
)

if exist "strategy" (
    echo    [OK] Carpeta strategy existe
    echo    Archivos en strategy:
    dir strategy\*.py /b 2>nul
) else (
    echo    [ERROR] Carpeta strategy NO existe
)

echo.
echo [4] Verificando acceso a carpeta compartida de Mac...
echo.

if exist "\\Mac\Home\bot de trader" (
    echo    [OK] Carpeta compartida de Mac accesible
    echo    Ruta: \\Mac\Home\bot de trader
) else (
    echo    [ADVERTENCIA] No se puede acceder a \\Mac\Home\bot de trader
    echo    Verifica la configuracion de Parallels
)

echo.
echo =====================================================================
echo VERIFICACION COMPLETADA
echo =====================================================================
echo.
echo Si hay archivos faltantes, necesitas copiarlos desde Mac.
echo.
pause




