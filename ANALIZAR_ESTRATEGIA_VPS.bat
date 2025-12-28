@echo off
REM ANALIZAR_ESTRATEGIA_VPS.bat - Ejecuta análisis completo de señales y trades en VPS
REM Este script analiza todas las entradas del bot y sugiere mejoras

echo ========================================
echo   ANALISIS COMPLETO DE ESTRATEGIA
echo ========================================
echo.

REM Cambia al directorio del bot
cd /d "%~dp0"

REM Verifica que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado
    echo Por favor instala Python 3.10 o superior
    pause
    exit /b 1
)

echo Ejecutando analisis...
echo.

REM Ejecuta el script de análisis
python -u analizar_estrategia.py

echo.
echo ========================================
echo   ANALISIS COMPLETADO
echo ========================================
echo.
pause

