# 🚀 Iniciar el Bot - Guía Rápida

## Opción 1: Desde PowerShell (Más Simple)

Ya estás en el directorio correcto. Solo ejecuta:

```powershell
python live\mt5_trading.py
```

O si usas Python 3.12:

```powershell
py -3.12 live\mt5_trading.py
```

---

## Opción 2: Verificar Primero la Conexión

Antes de iniciar el bot, puedes probar la conexión:

```powershell
python test_mt5_connection.py
```

O:

```powershell
py -3.12 test_mt5_connection.py
```

---

## ⚠️ IMPORTANTE: Antes de Ejecutar

1. **Abre MetaTrader 5** en Windows
2. **Conéctate a tu cuenta** Zeven (LIVE en tu caso)
3. **Verifica que el símbolo XAUUSD.vip esté visible** en Market Watch

---

## ✅ Qué Deberías Ver

Cuando el bot inicia correctamente:

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

🔍 Análisis multi-temporal...
```

---

## 🛑 Para Detener el Bot

Presiona `Ctrl + C` en la ventana de PowerShell.




