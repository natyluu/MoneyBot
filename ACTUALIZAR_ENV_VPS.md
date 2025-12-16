# 📝 Actualizar archivo .env en el VPS

## Credenciales completas para el archivo `.env`

Copia este contenido completo al archivo `.env` en tu VPS:

```
MT5_LOGIN=94342
MT5_PASSWORD=Santos2025!
MT5_SERVER=ZevenGlobal-Live
MT5_SYMBOL=XAUUSD.vip
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=1.5
TELEGRAM_BOT_TOKEN=8447919749:AAEM0_pIrfA6h8c7PoQST4_Pd1FJ_cp8cNA
TELEGRAM_CHAT_ID=-1003607928345
```

---

## Pasos para actualizar en el VPS

### 1. Navega a la carpeta del bot:

```cmd
cd "C:\Users\Administrator\Downloads\bot de trader"
```

### 2. Abre el archivo `.env`:

```cmd
notepad .env
```

### 3. Reemplaza todo el contenido con el texto de arriba

### 4. Guarda el archivo (Ctrl+S)

### 5. Verifica que se guardó:

```cmd
type .env
```

Deberías ver las 9 líneas con todas las credenciales.

---

## Verificación rápida

El archivo debe tener exactamente estas líneas:

- ✅ MT5_LOGIN=94342
- ✅ MT5_PASSWORD=Santos2025!
- ✅ MT5_SERVER=ZevenGlobal-Live
- ✅ MT5_SYMBOL=XAUUSD.vip
- ✅ RISK_PER_TRADE=0.01
- ✅ MAX_CONCURRENT_TRADES=3
- ✅ MIN_RR=1.5
- ✅ TELEGRAM_BOT_TOKEN=8447919749:AAEM0_pIrfA6h8c7PoQST4_Pd1FJ_cp8cNA
- ✅ TELEGRAM_CHAT_ID=-1003607928345

---

## Después de actualizar

Ejecuta el bot:

```cmd
python -u live\mt5_trading.py
```

Ahora debería conectarse correctamente a MT5 y Telegram.

