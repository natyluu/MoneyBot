@echo off
REM CONFIGURAR_GIT_VPS_COPIADO.bat
REM Configura Git cuando ya copiaste la carpeta del bot al VPS

echo ========================================
echo CONFIGURAR GIT EN VPS (CARPETA COPIADA)
echo ========================================
echo.

REM Verificar si Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git no está instalado
    echo.
    echo Por favor instala Git desde: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo Git está instalado: 
git --version
echo.

REM Verificar si estamos en un directorio con archivos del bot
if not exist "live\mt5_trading.py" (
    echo ERROR: No se encontraron archivos del bot
    echo.
    echo Asegúrate de ejecutar este script desde la carpeta del bot
    echo Ejemplo: cd C:\ruta\al\bot
    echo.
    pause
    exit /b 1
)

echo ✅ Archivos del bot encontrados
echo.

REM Verificar si ya tiene .git
if exist ".git" (
    echo ⚠️ Ya existe un repositorio Git en este directorio
    echo.
    set /p CONTINUAR="   ¿Deseas reconfigurarlo? (s/n): "
    if /i not "%CONTINUAR%"=="s" (
        echo Cancelado
        pause
        exit /b 0
    )
    echo.
    echo Eliminando configuración Git anterior...
    rmdir /s /q .git
    echo ✅ Configuración anterior eliminada
    echo.
)

REM 1. Inicializar repositorio Git
echo 1. Inicializando repositorio Git...
git init
if errorlevel 1 (
    echo ERROR: No se pudo inicializar Git
    pause
    exit /b 1
)
echo ✅ Repositorio inicializado
echo.

REM 2. Configurar usuario de Git
echo 2. Configurando usuario de Git...
echo.
set /p GIT_USER="   Nombre de usuario (o Enter para 'Bot Trader'): "
if "%GIT_USER%"=="" set GIT_USER=Bot Trader

set /p GIT_EMAIL="   Email (o Enter para 'bot@trader.local'): "
if "%GIT_EMAIL%"=="" set GIT_EMAIL=bot@trader.local

git config user.name "%GIT_USER%"
git config user.email "%GIT_EMAIL%"

echo.
echo ✅ Usuario configurado: %GIT_USER% ^<%GIT_EMAIL%^>
echo.

REM 3. Agregar todos los archivos
echo 3. Agregando archivos al repositorio...
git add -A
if errorlevel 1 (
    echo ERROR: No se pudieron agregar archivos
    pause
    exit /b 1
)
echo ✅ Archivos agregados
echo.

REM 4. Hacer commit inicial
echo 4. Creando commit inicial...
git commit -m "Estado inicial del bot copiado"
if errorlevel 1 (
    echo ⚠️ No se pudo crear commit (puede que no haya cambios)
)
echo.

REM 5. Configurar remoto de GitHub
echo 5. Configurando conexión con GitHub...
echo.
echo URL del repositorio: https://github.com/natyluu/MoneyBot.git
echo.
set /p CONFIG_REMOTE="   ¿Configurar este repositorio? (s/n): "
if /i "%CONFIG_REMOTE%"=="s" (
    git remote add origin https://github.com/natyluu/MoneyBot.git
    if errorlevel 1 (
        REM Intentar actualizar si ya existe
        git remote set-url origin https://github.com/natyluu/MoneyBot.git
    )
    echo ✅ Remoto configurado
    echo.
    
    REM 6. Verificar conexión
    echo 6. Verificando conexión con GitHub...
    echo.
    echo ⚠️ IMPORTANTE: Necesitarás un Personal Access Token
    echo    Crea uno en: https://github.com/settings/tokens
    echo    Permisos: repo (acceso completo)
    echo.
    set /p TEST_CONNECTION="   ¿Probar conexión ahora? (s/n): "
    if /i "%TEST_CONNECTION%"=="s" (
        git fetch origin
        if errorlevel 1 (
            echo.
            echo ❌ ERROR: No se pudo conectar a GitHub
            echo.
            echo Posibles causas:
            echo   - No tienes Personal Access Token configurado
            echo   - Token incorrecto o expirado
            echo   - Sin conexión a internet
            echo.
            echo Puedes configurar el token después ejecutando:
            echo   git pull origin main
            echo.
        ) else (
            echo.
            echo ✅ Conexión exitosa con GitHub
            echo.
            echo 7. Sincronizando con GitHub...
            echo.
            set /p SYNC="   ¿Descargar última versión desde GitHub? (s/n): "
            if /i "%SYNC%"=="s" (
                git pull origin main --allow-unrelated-histories
                if errorlevel 1 (
                    echo ⚠️ Hubo conflictos al sincronizar
                    echo Puedes resolverlos manualmente después
                ) else (
                    echo ✅ Sincronización completada
                )
            )
        )
    )
) else (
    echo ⚠️ Remoto no configurado. Puedes configurarlo después con:
    echo    git remote add origin https://github.com/natyluu/MoneyBot.git
)

echo.
echo ========================================
echo CONFIGURACION COMPLETADA
echo ========================================
echo.
echo Resumen:
echo   Repositorio: Inicializado
echo   Usuario: %GIT_USER%
echo   Email: %GIT_EMAIL%
if exist ".git\config" (
    echo   Remoto: 
    git remote -v 2>nul
)
echo.
echo Próximos pasos:
echo   1. Si no configuraste el remoto, ejecuta:
echo      git remote add origin https://github.com/natyluu/MoneyBot.git
echo.
echo   2. Para actualizar desde GitHub:
echo      git pull origin main
echo.
echo   3. O usa el script: ACTUALIZAR_BOT_VPS.bat
echo.
pause






