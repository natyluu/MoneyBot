# ========================================
#   CREAR ARCHIVO .env EN VPS (PowerShell)
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   CREANDO ARCHIVO .env EN VPS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Verificar si .env ya existe
if (Test-Path ".env") {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "   ADVERTENCIA: El archivo .env ya existe" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    $sobrescribir = Read-Host "¿Deseas sobrescribirlo? (S/N)"
    if ($sobrescribir -ne "S" -and $sobrescribir -ne "s") {
        Write-Host "Operación cancelada." -ForegroundColor Red
        exit
    }
}

# Crear el archivo .env
Write-Host "Creando archivo .env..." -ForegroundColor Green

$envContent = @"
MT5_LOGIN=94342
MT5_PASSWORD=Santos2025!
MT5_SERVER=ZevenGlobal-Live
MT5_SYMBOL=XAUUSD.vip
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=1.5
TELEGRAM_BOT_TOKEN=8447919749:AAEM0_pIrfA6h8c7PoQST4_Pd1FJ_cp8cNA
TELEGRAM_CHAT_ID=-1003607928345
"@

try {
    $envContent | Out-File -FilePath ".env" -Encoding UTF8 -NoNewline
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   ARCHIVO .env CREADO EXITOSAMENTE" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "El archivo .env ha sido creado con todas las credenciales." -ForegroundColor Green
    Write-Host ""
    Write-Host "Verificando contenido..." -ForegroundColor Cyan
    Get-Content .env
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
} catch {
    Write-Host "ERROR: No se pudo crear el archivo .env" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}







