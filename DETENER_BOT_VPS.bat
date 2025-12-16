@echo off
REM ========================================
REM   DETENER BOT DE TRADING
REM ========================================
chcp 65001 >nul 2>&1
echo.
echo ========================================
echo   DETENIENDO BOT DE TRADING
echo ========================================
echo.

REM Buscar procesos Python relacionados con el bot
echo Buscando procesos del bot...
tasklist | findstr /i python >nul
if errorlevel 1 (
    echo No se encontraron procesos Python activos.
    echo El bot probablemente ya está detenido.
    pause
    exit /b 0
)

echo Procesos Python encontrados:
tasklist | findstr /i python
echo.

REM Preguntar confirmación
echo ¿Deseas detener todos los procesos Python? (S/N)
set /p confirmar=
if /i not "%confirmar%"=="S" (
    echo Operación cancelada.
    pause
    exit /b 0
)

REM Detener procesos Python
echo.
echo Deteniendo procesos...
taskkill /F /IM python.exe
if errorlevel 1 (
    echo No se pudieron detener los procesos.
    echo Puede que necesites permisos de administrador.
) else (
    echo Procesos detenidos correctamente.
)

echo.
echo ========================================
pause

