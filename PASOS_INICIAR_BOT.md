# 🚀 Pasos para Iniciar el Bot - Guía Completa

## ✅ PASO 1: Abrir PowerShell en Windows

1. En Windows (dentro de Parallels), presiona `Win + X`
2. Selecciona **"Windows PowerShell"** o **"Terminal"**

---

## ✅ PASO 2: Ir al Directorio del Proyecto

Copia y pega este comando (presiona Enter después):

```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
```

**Verifica que funcionó:** Deberías ver:
```
PS C:\BOT\trading-bot-windows-20251210 on 'Mac'>
```

---

## ✅ PASO 3: Verificar que los Archivos Existen

Ejecuta estos comandos uno por uno para verificar:

```powershell
dir config.py
```

**Deberías ver:** El archivo `config.py` listado

```powershell
dir live\mt5_trading.py
```

**Deberías ver:** El archivo `mt5_trading.py` listado

```powershell
dir strategy
```

**Deberías ver:** La carpeta `strategy` listada

---

## ✅ PASO 4: Abrir MetaTrader 5

**IMPORTANTE:** El bot necesita MT5 abierto y conectado.

1. Abre **MetaTrader 5** en Windows
2. **Conéctate** a tu cuenta Zeven (LIVE en tu caso)
3. Verifica que el símbolo **XAUUSD.vip** esté visible en **Market Watch**

---

## ✅ PASO 5: Iniciar el Bot

Ejecuta este comando:

```powershell
python live\mt5_trading.py
```

O si usas Python 3.12 específicamente:

```powershell
py -3.12 live\mt5_trading.py
```

---

## ✅ PASO 6: Verificar que Funciona

**Deberías ver algo como esto:**

```
======================================================================
🚀 INICIANDO BOT DE TRADING AUTOMÁTICO
======================================================================

🔌 Inicializando conexión con MetaTrader 5...
✓ MT5 inicializado
✓ Conectado a cuenta 94338 en servidor ZevenGlobal-Live
✓ Símbolo XAUUSD.vip activado y disponible

📊 Información de la cuenta:
   Balance: $...
   Equity: $...
   ...

🔍 Análisis multi-temporal (14:20:00)...
```

---

## ⚠️ Si Hay Errores

### Error: "No module named 'config'"

**Solución:**
1. Verifica que estás en el directorio correcto:
   ```powershell
   pwd
   ```
   Debería mostrar: `C:\BOT\trading-bot-windows-20251210 on 'Mac'`

2. Verifica que config.py existe:
   ```powershell
   dir config.py
   ```

### Error: "No se pudo inicializar MT5"

**Solución:**
1. Abre MetaTrader 5
2. Conéctate a tu cuenta
3. Verifica que XAUUSD.vip esté visible

### Error: "can't open file"

**Solución:**
1. Verifica que estás en el directorio correcto (Paso 2)
2. Verifica que los archivos existen (Paso 3)

---

## 🛑 Para Detener el Bot

Presiona `Ctrl + C` en la ventana de PowerShell donde está corriendo el bot.

---

## 📝 Resumen Rápido (Copia y Pega)

```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
python live\mt5_trading.py
```

**¡Eso es todo!** 🎉




