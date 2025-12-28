@echo off
REM SUBIR_A_GITHUB.bat - Sube cambios a GitHub automáticamente

echo ========================================
echo SUBIENDO CAMBIOS A GITHUB
echo ========================================
echo.

cd /d "%~dp0"

echo 1. Verificando si Git está inicializado...
if not exist ".git" (
    echo ERROR: No hay repositorio Git en este directorio
    echo.
    echo Ejecuta primero: git init
    echo O clona el repositorio desde GitHub
    pause
    exit /b 1
)
echo ✅ Repositorio Git encontrado
echo.

echo 2. Verificando estado de Git...
git status --short
echo.

echo 3. Agregando TODOS los cambios (incluyendo nuevos archivos)...
git add -A
if errorlevel 1 (
    echo ERROR: No se pudieron agregar cambios
    pause
    exit /b 1
)
echo ✅ Archivos agregados
echo.

echo 4. Verificando qué se va a commitear...
git status --short
set /a files_count=0
for /f %%i in ('git status --short ^| find /c /v ""') do set files_count=%%i
if %files_count%==0 (
    echo.
    echo ⚠️ No hay cambios para commitear
    echo.
    echo Posibles razones:
    echo - Todos los archivos ya están commiteados
    echo - Los archivos están en .gitignore
    echo - No hay cambios nuevos desde el último commit
    echo.
    echo Verificando si hay commits sin push...
    git log origin/main..HEAD --oneline 2>nul
    if errorlevel 1 (
        git log origin/master..HEAD --oneline 2>nul
        if errorlevel 1 (
            echo No hay commits sin push
            pause
            exit /b 0
        )
    )
    echo Hay commits sin push, continuando...
    goto :push
)

echo.
echo 5. Haciendo commit...
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set mydate=%%c-%%a-%%b
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a:%%b
set commit_msg=Mejoras News Risk Gate: SafeNewsProvider, bloqueo eventos HIGH, file locking seguro - %mydate% %mytime%

git commit -m "%commit_msg%"
if errorlevel 1 (
    echo ERROR: No se pudo hacer commit
    echo Puede que no haya cambios para commitear
    pause
    exit /b 1
)
echo ✅ Commit realizado
:push

echo.
echo 6. Subiendo a GitHub...
git push origin main
if errorlevel 1 (
    echo Intentando con master...
    git push origin master
    if errorlevel 1 (
        echo Intentando push simple...
        git push
        if errorlevel 1 (
            echo ERROR: No se pudo subir a GitHub
            pause
            exit /b 1
        )
    )
)

echo.
echo ========================================
echo CAMBIOS SUBIDOS A GITHUB EXITOSAMENTE
echo ========================================
echo.
echo Proximo paso: En el VPS, ejecuta ACTUALIZAR_BOT_VPS.bat
echo.
pause





