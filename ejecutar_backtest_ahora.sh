#!/bin/bash
# ejecutar_backtest_ahora.sh - Ejecuta el backtest en macOS

echo "🚀 Ejecutando Backtest de Estrategia ICT"
echo "=========================================="
echo ""

cd "/Users/nataliaturizo/bot de trader"

# Verifica que Python esté disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado"
    exit 1
fi

# Verifica datos
if [ ! -d "data" ] || [ -z "$(ls -A data/*.csv 2>/dev/null)" ]; then
    echo "⚠️ No hay datos históricos"
    echo "Generando datos de ejemplo..."
    python3 utils/generate_sample_data.py
fi

# Ejecuta backtest
echo ""
echo "Ejecutando backtest..."
echo ""

PYTHONPATH="/Users/nataliaturizo/bot de trader:$PYTHONPATH" python3 backtest/backtest.py









