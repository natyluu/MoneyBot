# 🔄 Guía Completa: Reiniciar el Bot desde Cero

Esta guía te ayudará a reiniciar el bot de trading paso a paso en Windows (Parallels).

## 📋 Checklist Pre-Inicio

Antes de empezar, verifica:

- [ ] MetaTrader 5 está **abierto y conectado** a tu cuenta Zeven
- [ ] El archivo `.env` existe y tiene tus credenciales correctas
- [ ] Python 3.12 está instalado y funciona
- [ ] Las dependencias están instaladas (`MetaTrader5`, `pandas`, etc.)

---

## 🚀 Opción 1: Reinicio Automático (Recomendado)

### Paso 1: Abrir PowerShell en Windows

1. En Windows (dentro de Parallels), presiona `Win + X`
2. Selecciona **"Windows PowerShell"** o **"Terminal"**

### Paso 2: Navegar al Proyecto

```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
```

### Paso 3: Ejecutar el Script de Reinicio

```powershell
.\REINICIAR_BOT.ps1
```

Este script:
- ✅ Detiene procesos anteriores del bot
- ✅ Verifica que MT5 esté abierto
- ✅ Verifica que el archivo `.env` exista
- ✅ Prueba la conexión con MT5
- ✅ Inicia el bot automáticamente

---

## 🔧 Opción 2: Reinicio Manual Paso a Paso

### Paso 1: Detener Procesos Anteriores

Si el bot está corriendo en otra ventana:

1. Abre PowerShell
2. Ejecuta:
```powershell
Get-Process python* | Where-Object { $_.Path -like "*python*" } | Stop-Process -Force
```

O simplemente:
- Ve a la ventana donde está corriendo el bot
- Presiona `Ctrl + C` para detenerlo

### Paso 2: Verificar MetaTrader 5

**IMPORTANTE:** El bot necesita MT5 abierto y conectado.

1. Abre MetaTrader 5
2. Conéctate a tu cuenta Zeven (Demo o Real)
3. Verifica que el símbolo **XAUUSD** esté visible en Market Watch

### Paso 3: Verificar Archivo .env

Verifica que el archivo `.env` existe y tiene tus credenciales:

```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
type .env
```

Deberías ver algo como:
```
MT5_LOGIN=1234567
MT5_PASSWORD=tu_password
MT5_SERVER=ZevenGlobal-Demo
MT5_SYMBOL=XAUUSD
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=2.0
```

**Si el archivo no existe o está mal:**
```powershell
python setup_mt5.py
```

### Paso 4: Probar Conexión (Opcional pero Recomendado)

```powershell
python test_mt5_connection.py
```

O si usas Python 3.12:
```powershell
py -3.12 test_mt5_connection.py
```

Deberías ver:
```
✓ MT5 inicializado
✓ Conectado a cuenta...
✓ Símbolo XAUUSD activado
```

### Paso 5: Iniciar el Bot

```powershell
python live/mt5_trading.py
```

O si usas Python 3.12:
```powershell
py -3.12 live/mt5_trading.py
```

---

## ✅ Qué Deberías Ver

Cuando el bot inicia correctamente, verás:

```
======================================================================
🚀 INICIANDO BOT DE TRADING AUTOMÁTICO
======================================================================

🔌 Inicializando conexión con MetaTrader 5...
✓ MT5 inicializado
✓ Conectado a cuenta 1234567 en servidor ZevenGlobal-Demo
✓ Símbolo XAUUSD activado y disponible

📊 Información de la cuenta:
   Balance: $10,000.00
   Equity: $10,000.00
   Margen libre: $10,000.00
   Leverage: 1:500

⚙️ Configuración:
   Símbolo: XAUUSD
   Riesgo por operación: 1.0%
   Máximo de operaciones simultáneas: 3
   Risk:Reward mínimo: 1:2.0
   Análisis cada: 300s
   Actualización cada: 60s

⚠️ Presiona Ctrl+C para detener el bot
======================================================================

🔍 Análisis multi-temporal (14:20:00)...
📊 Obteniendo datos multi-temporales para XAUUSD...
   ✓ D1: 100 velas
   ✓ H4: 200 velas
   ✓ H1: 300 velas
   ✓ M15: 500 velas
   ✓ M5: 500 velas
   ✓ M3: 500 velas
   ✓ M1: 500 velas
✓ Contexto construido con 7 timeframes

[... análisis completo ...]

⏳ Bot activo - Próximo análisis en 4m 30s (14:20:30)
```

---

## ⚠️ Problemas Comunes

### Error: "No se pudo inicializar MT5"

**Solución:**
1. Verifica que MetaTrader 5 esté **abierto y funcionando**
2. Verifica que estés **conectado** a tu cuenta Zeven
3. Cierra y vuelve a abrir MT5

### Error: "ModuleNotFoundError: No module named 'config'"

**Solución:**
```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
python live/mt5_trading.py
```

Asegúrate de estar en el directorio correcto.

### Error: "Error al conectar a MT5"

**Solución:**
1. Verifica tus credenciales en `.env`
2. Verifica que el servidor sea correcto (ej: `ZevenGlobal-Demo`)
3. Prueba la conexión manualmente en MT5 primero

### El Bot se Detiene Inmediatamente

**Solución:**
1. Verifica que MT5 esté abierto
2. Ejecuta `python test_mt5_connection.py` para ver el error específico
3. Revisa los mensajes de error en la consola

---

## 📊 Monitoreo del Bot

Una vez que el bot está corriendo:

- **Cada 30 segundos:** Verás un mensaje indicando que está activo
- **Cada 5 minutos:** Verás un análisis completo multi-temporal
- **Cuando hay señal:** Verás información detallada de la operación

### Para Detener el Bot

Presiona `Ctrl + C` en la ventana de PowerShell donde está corriendo.

---

## 🔄 Reiniciar Después de Cambios

Si hiciste cambios en el código:

1. Detén el bot (`Ctrl + C`)
2. Ejecuta de nuevo:
```powershell
python live/mt5_trading.py
```

---

## 📝 Notas Importantes

- ⚠️ **Siempre usa cuenta DEMO primero** para probar
- ⚠️ **Nunca dejes el bot corriendo sin supervisión** al principio
- ⚠️ **Verifica que el bot esté funcionando correctamente** antes de confiar en él
- ✅ El bot muestra mensajes cada 30 segundos para confirmar que está activo
- ✅ El bot hace análisis completos cada 5 minutos

---

## 🆘 Si Necesitas Ayuda

Si algo no funciona:

1. Ejecuta `python test_mt5_connection.py` para diagnosticar
2. Revisa los mensajes de error en la consola
3. Verifica que todos los pasos del checklist estén completos




