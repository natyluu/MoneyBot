#!/bin/bash
# instalar_windows_parallels.sh - Abre Parallels para instalar Windows

echo "═══════════════════════════════════════════════════════════════"
echo "  INSTALAR WINDOWS EN PARALLELS"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Verifica si Parallels está instalado
if [ -d "/Applications/Parallels Desktop.app" ]; then
    echo "✅ Parallels Desktop está instalado"
    echo ""
    echo "Abriendo Parallels Desktop..."
    open "/Applications/Parallels Desktop.app"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  INSTRUCCIONES PARA INSTALAR WINDOWS"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "1. En la ventana de Parallels que se abrió:"
    echo "   - Clic en 'Instalar Windows' o 'Install Windows'"
    echo "   - O ve a: Archivo → Nuevo → Instalar Windows"
    echo ""
    echo "2. Parallels te preguntará qué versión de Windows:"
    echo "   - Selecciona 'Windows 11' (recomendado)"
    echo "   - O 'Windows 10' si prefieres"
    echo ""
    echo "3. Parallels descargará Windows automáticamente:"
    echo "   - Tamaño: ~5-6 GB"
    echo "   - Tiempo: 30-60 minutos (depende de tu internet)"
    echo ""
    echo "4. Durante la instalación:"
    echo "   - NO necesitas una clave de producto"
    echo "   - Puedes usar Windows sin activar (con algunas limitaciones)"
    echo "   - La instalación es automática"
    echo ""
    echo "5. Cuando termine, Windows se abrirá automáticamente"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  ⏳ ESPERA A QUE TERMINE LA INSTALACIÓN"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "Una vez que Windows esté instalado y funcionando,"
    echo "avísame y te guío para configurar el bot."
    echo ""
    echo "📖 Mientras tanto, puedes leer: PASO_A_PASO_PARALLELS.md"
    echo ""

else
    echo "❌ Parallels Desktop no está instalado"
    echo ""
    echo "Por favor, instala Parallels Desktop primero desde Mac App Store"
    exit 1
fi







