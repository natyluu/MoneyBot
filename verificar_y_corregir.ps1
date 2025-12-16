# Script para verificar y corregir los intervalos del bot en Windows
# Ejecuta: .\verificar_y_corregir.ps1

$file = "live\mt5_trading.py"

Write-Host "Verificando archivo..." -ForegroundColor Yellow

if (-not (Test-Path $file)) {
    Write-Host "❌ No se encontró $file" -ForegroundColor Red
    exit 1
}

$content = Get-Content $file -Raw -Encoding UTF8

# Verificar intervalos actuales
if ($content -match "run_auto_trading_loop\(analysis_interval=(\d+), update_interval=(\d+)\)") {
    $current_analysis = $matches[1]
    $current_update = $matches[2]
    Write-Host "Intervalos actuales:" -ForegroundColor Cyan
    Write-Host "  Análisis: ${current_analysis}s" -ForegroundColor Gray
    Write-Host "  Actualización: ${current_update}s" -ForegroundColor Gray
    
    if ($current_analysis -eq "180" -and $current_update -eq "30") {
        Write-Host "✅ Los intervalos ya están correctos (180s y 30s)" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Los intervalos necesitan actualizarse" -ForegroundColor Yellow
        Write-Host "  Cambiando a: 180s (análisis) y 30s (actualización)" -ForegroundColor Cyan
        
        # Crear backup
        Copy-Item $file "$file.backup"
        
        # Reemplazar intervalos
        $content = $content -replace "run_auto_trading_loop\(analysis_interval=\d+, update_interval=\d+\)", "run_auto_trading_loop(analysis_interval=180, update_interval=30)"
        
        # Guardar
        [System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
        
        Write-Host "✅ Archivo actualizado" -ForegroundColor Green
        Write-Host "   Backup guardado en: $file.backup" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠️ No se encontró la línea run_auto_trading_loop()" -ForegroundColor Yellow
    Write-Host "   El archivo puede tener un formato diferente" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Para aplicar los cambios, reinicia el bot" -ForegroundColor Cyan




