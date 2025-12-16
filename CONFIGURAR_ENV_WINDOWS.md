# ⚙️ Configurar .env en Windows

## ✅ Opción 1: Crear .env directamente con PowerShell (RÁPIDO)

Ejecuta estos comandos en PowerShell (estando en la carpeta del proyecto):

```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

@"
# Configuración MetaTrader 5 (Zeven)
MT5_LOGIN=94338
MT5_PASSWORD=Santos2025!
MT5_SERVER=ZevenGlobal-Live
MT5_SYMBOL=XAUUSD.vip

# Configuración de riesgo
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=2.0
"@ | Out-File -FilePath .env -Encoding utf8

dir .env
```

---

## ✅ Opción 2: Usar el script configurar_env_windows.py

1. Copia el archivo `configurar_env_windows.py` a Windows (si no está ya)
2. Ejecuta:

```powershell
python configurar_env_windows.py
```

---

## ✅ Opción 3: Usar setup_mt5.py (interactivo)

Ejecuta:

```powershell
python setup_mt5.py
```

Y responde:
- **Número de cuenta:** `94338`
- **Contraseña:** `Santos2025!`
- **Tipo de cuenta:** `2` (Real)
- **Símbolo:** `XAUUSD.vip`
- **Riesgo:** `1` (o Enter para 1%)
- **Máximo de operaciones:** `3` (o Enter)
- **RR mínimo:** `2.0` (o Enter)

---

## ✅ Verificar que se creó correctamente

```powershell
dir .env
type .env
```

Deberías ver el archivo `.env` con tus credenciales.

---

## 🎯 Siguiente Paso

Una vez creado el `.env`, prueba la conexión:

```powershell
python test_mt5_connection.py
```





