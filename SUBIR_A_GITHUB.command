#!/bin/bash
# Script para subir cambios a GitHub automáticamente

cd "$(dirname "$0")"

echo "🚀 Ejecutando sincronización con GitHub..."
echo ""

python3 SINCRONIZAR_VPS.py

# Mantener la ventana abierta para ver el resultado
echo ""
echo "Presiona Enter para cerrar..."
read





