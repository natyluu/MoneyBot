#!/bin/bash
# configurar_parallels.sh - Guía interactiva para configurar Parallels

echo "═══════════════════════════════════════════════════════════════"
echo "  CONFIGURACIÓN DE PARALLELS DESKTOP"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Verifica si Parallels está instalado
if [ -d "/Applications/Parallels Desktop.app" ]; then
    echo "✅ Parallels Desktop está instalado"
    echo ""
    echo "¿Quieres abrir Parallels ahora? (s/n)"
    read -r respuesta
    if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
        open "/Applications/Parallels Desktop.app"
        echo ""
        echo "✅ Parallels abierto. Sigue las instrucciones en pantalla."
    fi
else
    echo "❌ Parallels Desktop no está instalado"
    echo ""
    echo "OPCIONES PARA INSTALAR:"
    echo ""
    echo "1. Mac App Store (Recomendado - Prueba 14 días gratis)"
    echo "   - Abre Mac App Store"
    echo "   - Busca 'Parallels Desktop'"
    echo "   - Descarga e instala"
    echo ""
    echo "2. Descarga Directa"
    echo "   - Ve a: https://www.parallels.com/products/desktop/"
    echo "   - Descarga la versión para Mac"
    echo ""
    echo "¿Quieres abrir Mac App Store ahora? (s/n)"
    read -r respuesta
    if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
        open "macappstore://apps.apple.com/app/parallels-desktop/id1085114709"
        echo ""
        echo "✅ Mac App Store abierto. Busca 'Parallels Desktop' e instala."
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  PRÓXIMOS PASOS DESPUÉS DE INSTALAR PARALLELS"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "1. Abre Parallels Desktop"
echo "2. Clic en 'Instalar Windows'"
echo "3. Parallels descargará Windows 11 automáticamente"
echo "4. Espera 30-60 minutos para la instalación"
echo "5. Configura Windows (cuenta Microsoft, etc.)"
echo ""
echo "📖 Para más detalles, lee: GUIA_PARALLELS_COMPLETA.md"
echo ""








