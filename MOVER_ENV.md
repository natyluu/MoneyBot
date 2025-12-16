# 📁 Mover .env a la Carpeta del Proyecto

## ⚠️ Problema

El archivo `.env` se creó en `C:\Users\nataliaturizo`, pero debe estar en la carpeta del proyecto:
`C:\BOT\trading-bot-windows-20251210 on 'Mac'`

---

## ✅ Solución 1: Mover el archivo

Ejecuta estos comandos:

```powershell
# 1. Ir a la carpeta del proyecto
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

# 2. Copiar el .env desde tu carpeta de usuario
copy "C:\Users\nataliaturizo\.env" .env

# 3. Verificar que se copió
dir .env
```

---

## ✅ Solución 2: Crear .env directamente en la carpeta del proyecto

Ejecuta estos comandos:

```powershell
# 1. Ir a la carpeta del proyecto
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

# 2. Crear el .env línea por línea
echo "# Configuración MetaTrader 5 (Zeven)" > .env
echo "MT5_LOGIN=94338" >> .env
echo "MT5_PASSWORD=Santos2025!" >> .env
echo "MT5_SERVER=ZevenGlobal-Live" >> .env
echo "MT5_SYMBOL=XAUUSD.vip" >> .env
echo "" >> .env
echo "# Configuración de riesgo" >> .env
echo "RISK_PER_TRADE=0.01" >> .env
echo "MAX_CONCURRENT_TRADES=3" >> .env
echo "MIN_RR=2.0" >> .env

# 3. Verificar
dir .env
type .env
```

---

## ✅ Verificar que está en el lugar correcto

```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
dir .env
```

Deberías ver el archivo `.env` en esta carpeta.

---

## 🎯 Siguiente Paso

Una vez que el `.env` esté en la carpeta correcta, prueba la conexión:

```powershell
python test_mt5_connection.py
```





