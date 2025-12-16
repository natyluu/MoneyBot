# 🔧 SOLUCIÓN INMEDIATA: Bot no muestra mensajes

## 🚨 PROBLEMA
El bot está ejecutándose pero no muestra mensajes en tiempo real (problema de buffering).

## ✅ SOLUCIÓN 1: Usar CMD en lugar de PowerShell (MÁS RÁPIDO)

### Paso 1: Abrir CMD
1. Presiona `Win + R`
2. Escribe: `cmd`
3. Presiona Enter

### Paso 2: Ejecutar comandos en CMD
```cmd
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
python -u live\mt5_trading.py
```

**CMD muestra los mensajes mejor que PowerShell.**

---

## ✅ SOLUCIÓN 2: Ver mensajes en archivo (FUNCIONA SIEMPRE)

### En PowerShell, ejecuta:
```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
python -u live\mt5_trading.py > bot_output.txt 2>&1
```

Luego, en otra ventana de PowerShell:
```powershell
Get-Content bot_output.txt -Wait
```

Esto mostrará los mensajes en tiempo real.

---

## ✅ SOLUCIÓN 3: Verificar que el bot está corriendo

### En otra ventana de PowerShell:
```powershell
tasklist | findstr python
```

Si ves `python.exe`, el bot está corriendo.

---

## ✅ SOLUCIÓN 4: Detener y ver mensajes

1. En la ventana donde ejecutaste el bot, presiona `Ctrl + C`
2. Deberías ver todos los mensajes acumulados

---

## 🎯 RECOMENDACIÓN: Usar CMD

**CMD funciona mejor para mostrar mensajes en tiempo real.**

1. Abre CMD (Win + R → `cmd`)
2. Ejecuta:
```cmd
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
python -u live\mt5_trading.py
```

---

## 📋 RESUMEN RÁPIDO

**Opción A: CMD (Recomendado)**
- Abre CMD
- Ejecuta los comandos
- Verás mensajes en tiempo real

**Opción B: Ver en archivo**
- Ejecuta con `> bot_output.txt`
- Abre el archivo para ver mensajes

**Opción C: Detener y ver**
- Presiona Ctrl+C
- Verás todos los mensajes acumulados




