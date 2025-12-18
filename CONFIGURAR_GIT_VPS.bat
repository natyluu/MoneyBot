@echo off
REM CONFIGURAR_GIT_VPS.bat - Configura Git en el VPS para conectar con GitHub
REM Ejecuta este script UNA VEZ para configurar Git en el VPS

echo ========================================
echo CONFIGURAR GIT EN VPS PARA GITHUB
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

REM Configurar usuario de Git (si no está configurado)
echo 1. Configurando usuario de Git...
echo.
set /p GIT_USER="   Nombre de usuario de Git (o Enter para usar 'Bot Trader'): "
if "%GIT_USER%"=="" set GIT_USER=Bot Trader

set /p GIT_EMAIL="   Email de Git (o Enter para usar 'bot@trader.local'): "
if "%GIT_EMAIL%"=="" set GIT_EMAIL=bot@trader.local

git config --global user.name "%GIT_USER%"
git config --global user.email "%GIT_EMAIL%"

echo.
echo ✅ Usuario configurado: %GIT_USER% ^<%GIT_EMAIL%^>
echo.

REM Verificar si ya existe un repositorio Git
if exist ".git" (
    echo 2. Repositorio Git encontrado
    echo.
    echo Verificando configuración del remoto...
    git remote -v
    echo.
    
    REM Verificar si ya tiene origin configurado
    git remote get-url origin >nul 2>&1
    if errorlevel 1 (
        echo ⚠️ No hay remoto 'origin' configurado
        goto :config_remote
    ) else (
        echo ✅ Remoto 'origin' ya está configurado
        git remote get-url origin
        echo.
        set /p RECONFIG="   ¿Deseas reconfigurar el remoto? (s/n): "
        if /i "%RECONFIG%"=="s" goto :config_remote
        goto :clone_check
    )
) else (
    echo 2. No hay repositorio Git en este directorio
    echo.
    set /p CLONE="   ¿Deseas clonar el repositorio desde GitHub? (s/n): "
    if /i "%CLONE%"=="s" goto :clone_repo
    goto :end
)

:config_remote
echo.
echo Configurando remoto de GitHub...
echo.
echo Opciones:
echo   1. HTTPS (más fácil, requiere token)
echo   2. SSH (más seguro, requiere configuración de llaves)
echo.
set /p REMOTE_TYPE="   Elige opción (1 o 2): "

if "%REMOTE_TYPE%"=="1" goto :config_https
if "%REMOTE_TYPE%"=="2" goto :config_ssh
goto :config_remote

:config_https
echo.
echo Configurando HTTPS...
set /p GITHUB_URL="   URL del repositorio (ej: https://github.com/natyluu/MoneyBot.git): "
if "%GITHUB_URL%"=="" (
    echo ERROR: URL requerida
    pause
    exit /b 1
)

REM Si ya existe origin, actualizarlo
git remote get-url origin >nul 2>&1
if not errorlevel 1 (
    git remote set-url origin "%GITHUB_URL%"
    echo ✅ Remoto actualizado
) else (
    git remote add origin "%GITHUB_URL%"
    echo ✅ Remoto agregado
)

echo.
echo ⚠️ IMPORTANTE: Para HTTPS necesitarás un Personal Access Token
echo    Crea uno en: https://github.com/settings/tokens
echo    Permisos necesarios: repo (acceso completo a repositorios)
echo.
goto :clone_check

:config_ssh
echo.
echo Configurando SSH...
set /p GITHUB_SSH="   URL SSH del repositorio (ej: git@github.com:natyluu/MoneyBot.git): "
if "%GITHUB_SSH%"=="" (
    echo ERROR: URL SSH requerida
    pause
    exit /b 1
)

REM Si ya existe origin, actualizarlo
git remote get-url origin >nul 2>&1
if not errorlevel 1 (
    git remote set-url origin "%GITHUB_SSH%"
    echo ✅ Remoto actualizado
) else (
    git remote add origin "%GITHUB_SSH%"
    echo ✅ Remoto agregado
)

echo.
echo ⚠️ IMPORTANTE: Para SSH necesitas configurar llaves SSH
echo    Guía: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
echo.
goto :clone_check

:clone_repo
echo.
echo Clonando repositorio desde GitHub...
set /p REPO_URL="   URL del repositorio (HTTPS o SSH): "
if "%REPO_URL%"=="" (
    echo ERROR: URL requerida
    pause
    exit /b 1
)

set /p CLONE_DIR="   Directorio donde clonar (Enter para usar actual): "
if "%CLONE_DIR%"=="" (
    git clone "%REPO_URL%" .
) else (
    git clone "%REPO_URL%" "%CLONE_DIR%"
)

if errorlevel 1 (
    echo ERROR: No se pudo clonar el repositorio
    echo Verifica la URL y tus credenciales
    pause
    exit /b 1
)

echo.
echo ✅ Repositorio clonado exitosamente
goto :end

:clone_check
echo.
echo 3. Verificando conexión con GitHub...
git fetch origin
if errorlevel 1 (
    echo.
    echo ❌ ERROR: No se pudo conectar a GitHub
    echo.
    echo Posibles causas:
    echo   - Credenciales incorrectas (HTTPS)
    echo   - Llaves SSH no configuradas (SSH)
    echo   - URL del repositorio incorrecta
    echo   - Sin conexión a internet
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Conexión con GitHub exitosa
echo.

:end
echo ========================================
echo CONFIGURACION COMPLETADA
echo ========================================
echo.
echo Resumen:
git config --global --get user.name >nul 2>&1
if not errorlevel 1 (
    echo   Usuario: 
    git config --global --get user.name
    echo   Email: 
    git config --global --get user.email
)
echo.
if exist ".git" (
    echo   Remoto configurado:
    git remote -v
    echo.
    echo   Rama actual:
    git branch --show-current
)
echo.
echo Próximos pasos:
echo   1. Ejecuta ACTUALIZAR_BOT_VPS.bat para actualizar
echo   2. O manualmente: git pull
echo.
pause

