@echo off
REM ACTUALIZAR_BOT_VPS.bat - Actualiza el bot desde GitHub
REM Ejecuta este script en el VPS para actualizar el bot a la última versión

echo ========================================
echo ACTUALIZANDO BOT DESDE GITHUB
echo ========================================
echo.

REM Cambiar al directorio del bot (ajusta la ruta según tu configuración)
REM cd /d "C:\ruta\al\bot"
REM Si el script está en la raíz del proyecto, no necesitas cambiar de directorio

echo 1. Verificando cambios en GitHub...
git fetch origin
if errorlevel 1 (
    echo ERROR: No se pudo conectar a GitHub
    pause
    exit /b 1
)

echo.
echo 2. Descargando última versión...
git pull origin main
if errorlevel 1 (
    echo ERROR: No se pudo actualizar desde GitHub
    pause
    exit /b 1
)

echo.
echo 3. Versiones disponibles (últimas 5):
git tag --sort=-version:refname | findstr /R "^v" | more +1 | head -5
if errorlevel 1 (
    echo    (No hay tags disponibles)
)

echo.
echo 4. Verificando estado...
git status

echo.
echo ========================================
echo ACTUALIZACION COMPLETADA
echo ========================================
echo.
echo Para usar una versión específica:
echo   git checkout v1.2.3
echo.
echo Para ver todas las versiones:
echo   git tag --sort=-version:refname
echo.
pause






