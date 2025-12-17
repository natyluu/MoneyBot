@echo off
REM ========================================
REM   CREAR ARCHIVO .env EN VPS
REM ========================================
chcp 65001 >nul 2>&1
echo.
echo ========================================
echo   CREANDO ARCHIVO .env EN VPS
echo ========================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"
if errorlevel 1 (
    echo ERROR: No se pudo cambiar al directorio del proyecto
    pause
    exit /b 1
)

REM Verificar si .env ya existe
if exist .env (
    echo.
    echo ========================================
    echo   ADVERTENCIA: El archivo .env ya existe
    echo ========================================
    echo.
    echo ¿Deseas sobrescribirlo? (S/N)
    set /p sobrescribir=
    if /i not "%sobrescribir%"=="S" (
        echo Operación cancelada.
        pause
        exit /b 0
    )
)

REM Crear el archivo .env con las credenciales
echo Creando archivo .env...
(
echo MT5_LOGIN=94342
echo MT5_PASSWORD=Santos2025!
echo MT5_SERVER=ZevenGlobal-Live
echo MT5_SYMBOL=XAUUSD.vip
echo RISK_PER_TRADE=0.01
echo MAX_CONCURRENT_TRADES=3
echo MIN_RR=1.5
echo TELEGRAM_BOT_TOKEN=8447919749:AAEM0_pIrfA6h8c7PoQST4_Pd1FJ_cp8cNA
echo TELEGRAM_CHAT_ID=-1003607928345
) > .env

if errorlevel 1 (
    echo ERROR: No se pudo crear el archivo .env
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ARCHIVO .env CREADO EXITOSAMENTE
echo ========================================
echo.
echo El archivo .env ha sido creado con todas las credenciales.
echo.
echo Verificando contenido...
type .env
echo.
echo ========================================
pause


