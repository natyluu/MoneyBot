# 🔧 Corregir Intervalos del Bot en Windows

El bot está mostrando intervalos antiguos (300s y 60s) en lugar de los nuevos (180s y 30s).

## ✅ Solución Rápida

### Opción 1: Usar el Script (Recomendado)

Ejecuta en PowerShell:

```powershell
.\verificar_y_corregir.ps1
```

Este script:
- Verifica los intervalos actuales
- Los corrige automáticamente si están mal
- Crea un backup del archivo

---

### Opción 2: Editar Manualmente

1. Abre el archivo:
```powershell
notepad live\mt5_trading.py
```

2. Busca esta línea (al final del archivo, alrededor de la línea 712):
```python
run_auto_trading_loop()
```

3. Cámbiala por:
```python
run_auto_trading_loop(analysis_interval=180, update_interval=30)
```

4. Guarda el archivo (`Ctrl + S`)

---

## ✅ Después de Corregir

Reinicia el bot:

```powershell
python -c "import sys; sys.path.insert(0, '.'); exec(open('live/mt5_trading.py', encoding='utf-8').read())"
```

Deberías ver:
```
   Análisis cada: 180s    ← 3 minutos
   Actualización cada: 30s  ← 30 segundos
```

---

## 📝 Nota sobre la Información Detallada

La información detallada del precio (cuando no hay confirmaciones) también requiere que el archivo `strategy/ict_hybrid_strategy.py` esté actualizado en Windows. Si no aparece, puede ser un problema de sincronización de archivos entre macOS y Windows.




