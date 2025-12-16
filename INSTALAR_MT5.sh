#!/bin/bash
# Script para instalar dependencias de MT5

echo "🔧 Instalando dependencias para MT5..."

# Actualiza pip
python3 -m pip install --upgrade pip

# Instala dependencias básicas
python3 -m pip install python-dotenv pandas numpy

# Intenta instalar MetaTrader5
echo "📦 Instalando MetaTrader5..."
python3 -m pip install MetaTrader5

# Si falla, muestra instrucciones alternativas
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️ No se pudo instalar MetaTrader5 automáticamente"
    echo ""
    echo "Opciones alternativas:"
    echo "1. Instala desde PyPI con: pip3 install MetaTrader5"
    echo "2. Verifica que tengas Python 3.7+"
    echo "3. En macOS, puede necesitar: xcode-select --install"
    echo ""
    echo "O visita: https://pypi.org/project/MetaTrader5/"
fi

echo ""
echo "✅ Instalación completada"
