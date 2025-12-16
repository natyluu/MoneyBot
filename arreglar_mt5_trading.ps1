# Script para arreglar el archivo mt5_trading.py en Windows
# Ejecuta: .\arreglar_mt5_trading.ps1

$file = "live\mt5_trading.py"
$backup = "live\mt5_trading.py.backup"

Write-Host "Creando backup..." -ForegroundColor Yellow
Copy-Item $file $backup

Write-Host "Leyendo archivo..." -ForegroundColor Yellow
$content = Get-Content $file -Raw -Encoding UTF8

# Buscar la línea problemática y comentarla
$content = $content -replace "from config import \(", "# from config import ("
$content = $content -replace "from strategy.ict_hybrid_strategy import ICTHybridStrategy", "# from strategy.ict_hybrid_strategy import ICTHybridStrategy"

# Agregar código para cargar config antes de los imports
$insertCode = @"

# Cargar config.py manualmente
import importlib.util
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
config_path = os.path.join(project_root, "config.py")
if os.path.exists(config_path):
    spec = importlib.util.spec_from_file_location("config", config_path)
    config_module = importlib.util.module_from_spec(spec)
    sys.modules["config"] = config_module
    spec.loader.exec_module(config_module)
    MT5_LOGIN = config_module.MT5_LOGIN
    MT5_PASSWORD = config_module.MT5_PASSWORD
    MT5_SERVER = config_module.MT5_SERVER
    MT5_SYMBOL = config_module.MT5_SYMBOL
    RISK_PER_TRADE = config_module.RISK_PER_TRADE
    MAX_CONCURRENT_TRADES = config_module.MAX_CONCURRENT_TRADES
    MIN_RR = config_module.MIN_RR
else:
    print(f"ERROR: No se encontró config.py en {config_path}")
    sys.exit(1)

# Cargar strategy
strategy_path = os.path.join(project_root, "strategy", "ict_hybrid_strategy.py")
if os.path.exists(strategy_path):
    spec = importlib.util.spec_from_file_location("ict_hybrid_strategy", strategy_path)
    strategy_module = importlib.util.module_from_spec(spec)
    sys.modules["strategy.ict_hybrid_strategy"] = strategy_module
    spec.loader.exec_module(strategy_module)
    ICTHybridStrategy = strategy_module.ICTHybridStrategy
else:
    print(f"ERROR: No se encontró strategy/ict_hybrid_strategy.py")
    sys.exit(1)

"@

# Insertar después de la línea que agrega al path
$pattern = "if project_root not in sys.path:"
if ($content -match $pattern) {
    $content = $content -replace "($pattern[^\n]*\n[^\n]*\n)", "`$1$insertCode"
} else {
    # Si no encuentra el patrón, insertar después de los imports básicos
    $content = $content -replace "(import sys\nimport os\n)", "`$1$insertCode"
}

Write-Host "Guardando archivo..." -ForegroundColor Yellow
[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)

Write-Host "✓ Archivo arreglado!" -ForegroundColor Green
Write-Host "Backup guardado en: $backup" -ForegroundColor Gray




