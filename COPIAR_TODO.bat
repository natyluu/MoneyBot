@echo off
chcp 65001 >nul 2>&1
echo =====================================================================
echo COPIAR TODOS LOS ARCHIVOS DESDE MAC
echo =====================================================================
echo.

REM Verificar acceso a carpeta compartida
if not exist "\\Mac\Home\bot de trader" (
    echo.
    echo ERROR: No se puede acceder a \\Mac\Home\bot de trader
    echo.
    echo SOLUCIONES:
    echo   1. Abre Parallels Desktop en Mac
    echo   2. Ve a Configuracion -^> Opciones -^> Compartir
    echo   3. Activa "Compartir Mac"
    echo   4. Reinicia Windows
    echo   5. Intenta de nuevo
    echo.
    pause
    exit /b 1
)

echo [OK] Carpeta compartida encontrada
echo.

REM Crear directorio si no existe
if not exist "C:\BOT\trading-bot-windows-20251210 on 'Mac'" (
    echo Creando directorio...
    mkdir "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
)

echo Copiando archivos...
echo.

REM Copiar scripts .bat
echo [1/6] Copiando scripts .bat...
xcopy "\\Mac\Home\bot de trader\*.bat" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\" /Y /Q
if errorlevel 1 (
    echo    [ADVERTENCIA] Algunos .bat no se copiaron
) else (
    echo    [OK] Scripts .bat copiados
)

REM Copiar scripts .ps1
echo [2/6] Copiando scripts .ps1...
xcopy "\\Mac\Home\bot de trader\*.ps1" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\" /Y /Q
if errorlevel 1 (
    echo    [ADVERTENCIA] Algunos .ps1 no se copiaron
) else (
    echo    [OK] Scripts .ps1 copiados
)

REM Copiar carpeta live
echo [3/6] Copiando carpeta live...
xcopy "\\Mac\Home\bot de trader\live\*" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\live\" /E /I /Y /Q
if errorlevel 1 (
    echo    [ERROR] No se pudo copiar carpeta live
) else (
    echo    [OK] Carpeta live copiada
)

REM Copiar carpeta strategy
echo [4/6] Copiando carpeta strategy...
xcopy "\\Mac\Home\bot de trader\strategy\*" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\strategy\" /E /I /Y /Q
if errorlevel 1 (
    echo    [ERROR] No se pudo copiar carpeta strategy
) else (
    echo    [OK] Carpeta strategy copiada
)

REM Copiar archivos individuales
echo [5/6] Copiando archivos individuales...
copy "\\Mac\Home\bot de trader\config.py" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\" /Y >nul 2>&1
if exist "C:\BOT\trading-bot-windows-20251210 on 'Mac'\config.py" (
    echo    [OK] config.py copiado
) else (
    echo    [ERROR] config.py NO copiado
)

copy "\\Mac\Home\bot de trader\.env" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\" /Y >nul 2>&1
if exist "C:\BOT\trading-bot-windows-20251210 on 'Mac'\.env" (
    echo    [OK] .env copiado
) else (
    echo    [ADVERTENCIA] .env NO copiado (puede estar oculto)
)

copy "\\Mac\Home\bot de trader\requirements.txt" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\" /Y >nul 2>&1
if exist "C:\BOT\trading-bot-windows-20251210 on 'Mac'\requirements.txt" (
    echo    [OK] requirements.txt copiado
)

REM Copiar documentación
echo [6/6] Copiando documentacion...
xcopy "\\Mac\Home\bot de trader\*.md" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\" /Y /Q >nul 2>&1
xcopy "\\Mac\Home\bot de trader\*.txt" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\" /Y /Q >nul 2>&1

echo.
echo =====================================================================
echo VERIFICACION DE ARCHIVOS CRITICOS
echo =====================================================================
echo.

cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

if exist "live\mt5_trading.py" (
    echo [OK] live\mt5_trading.py
) else (
    echo [ERROR] live\mt5_trading.py NO existe
)

if exist "config.py" (
    echo [OK] config.py
) else (
    echo [ERROR] config.py NO existe
)

if exist "strategy\ict_hybrid_strategy.py" (
    echo [OK] strategy\ict_hybrid_strategy.py
) else (
    echo [ERROR] strategy\ict_hybrid_strategy.py NO existe
)

if exist ".env" (
    echo [OK] .env
) else (
    echo [ADVERTENCIA] .env NO existe
)

if exist "INICIAR_BOT_FACIL.bat" (
    echo [OK] INICIAR_BOT_FACIL.bat
) else (
    echo [FALTA] INICIAR_BOT_FACIL.bat
)

if exist "DIAGNOSTICO_COMPLETO.bat" (
    echo [OK] DIAGNOSTICO_COMPLETO.bat
) else (
    echo [FALTA] DIAGNOSTICO_COMPLETO.bat
)

echo.
echo =====================================================================
echo COPIA COMPLETADA
echo =====================================================================
echo.
echo Si todos los archivos estan OK, puedes iniciar el bot con:
echo    python -u live\mt5_trading.py
echo.
echo O usa el script:
echo    INICIAR_BOT_FACIL.bat
echo.
pause




