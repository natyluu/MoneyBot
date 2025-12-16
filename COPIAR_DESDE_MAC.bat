@echo off
chcp 65001 >nul 2>&1
echo =====================================================================
echo COPIAR ARCHIVOS DESDE MAC A WINDOWS
echo =====================================================================
echo.

REM Verificar si existe la carpeta compartida
if not exist "\\Mac\Home\bot de trader" (
    echo ERROR: No se puede acceder a la carpeta compartida de Mac
    echo.
    echo Rutas alternativas a probar:
    echo   1. \\Mac\Home\bot de trader
    echo   2. \\Mac\Home\Documents\bot de trader
    echo   3. Busca en el Explorador: Mac o Parallels Shared Folders
    echo.
    pause
    exit /b 1
)

echo [OK] Carpeta compartida encontrada: \\Mac\Home\bot de trader
echo.

REM Crear directorio destino si no existe
if not exist "C:\BOT\trading-bot-windows-20251210 on 'Mac'" (
    echo Creando directorio destino...
    mkdir "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
)

echo Copiando archivos...
echo.

REM Copiar carpetas
echo [1] Copiando carpeta live...
if exist "\\Mac\Home\bot de trader\live" (
    xcopy "\\Mac\Home\bot de trader\live\*" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\live\" /E /I /Y /Q
    echo    [OK] Carpeta live copiada
) else (
    echo    [ERROR] Carpeta live no encontrada en Mac
)

echo [2] Copiando carpeta strategy...
if exist "\\Mac\Home\bot de trader\strategy" (
    xcopy "\\Mac\Home\bot de trader\strategy\*" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\strategy\" /E /I /Y /Q
    echo    [OK] Carpeta strategy copiada
) else (
    echo    [ERROR] Carpeta strategy no encontrada en Mac
)

echo [3] Copiando archivos individuales...
if exist "\\Mac\Home\bot de trader\config.py" (
    copy "\\Mac\Home\bot de trader\config.py" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\" /Y >nul
    echo    [OK] config.py copiado
) else (
    echo    [ERROR] config.py no encontrado
)

if exist "\\Mac\Home\bot de trader\.env" (
    copy "\\Mac\Home\bot de trader\.env" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\" /Y >nul
    echo    [OK] .env copiado
) else (
    echo    [ADVERTENCIA] .env no encontrado (puede estar oculto)
)

if exist "\\Mac\Home\bot de trader\requirements.txt" (
    copy "\\Mac\Home\bot de trader\requirements.txt" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\" /Y >nul
    echo    [OK] requirements.txt copiado
) else (
    echo    [ADVERTENCIA] requirements.txt no encontrado
)

echo [4] Copiando scripts .bat...
if exist "\\Mac\Home\bot de trader\*.bat" (
    copy "\\Mac\Home\bot de trader\*.bat" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\" /Y >nul
    echo    [OK] Scripts .bat copiados
)

echo [5] Copiando scripts .ps1...
if exist "\\Mac\Home\bot de trader\*.ps1" (
    copy "\\Mac\Home\bot de trader\*.ps1" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\" /Y >nul
    echo    [OK] Scripts .ps1 copiados
)

echo.
echo =====================================================================
echo COPIA COMPLETADA
echo =====================================================================
echo.
echo Verificando archivos copiados...
echo.

cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

if exist "live\mt5_trading.py" (
    echo [OK] live\mt5_trading.py existe
) else (
    echo [ERROR] live\mt5_trading.py NO existe
)

if exist "config.py" (
    echo [OK] config.py existe
) else (
    echo [ERROR] config.py NO existe
)

if exist "strategy\ict_hybrid_strategy.py" (
    echo [OK] strategy\ict_hybrid_strategy.py existe
) else (
    echo [ERROR] strategy\ict_hybrid_strategy.py NO existe
)

if exist ".env" (
    echo [OK] .env existe
) else (
    echo [ADVERTENCIA] .env NO existe (puede estar oculto)
)

echo.
echo =====================================================================
echo Si todos los archivos estan OK, puedes iniciar el bot con:
echo    python -u live\mt5_trading.py
echo =====================================================================
echo.
pause




