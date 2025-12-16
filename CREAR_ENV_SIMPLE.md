# ✅ Crear .env de Forma Simple

## 🔧 Método Línea por Línea (MÁS CONFIABLE)

Ejecuta estos comandos **uno por uno** en PowerShell:

```powershell
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
```

---

## ✅ Verificar que se creó

```powershell
dir .env
```

Deberías ver el archivo `.env`.

---

## ✅ Ver contenido

```powershell
type .env
```

Deberías ver todas las líneas que creaste.

---

## 🎯 Siguiente Paso

Una vez creado el `.env`, prueba la conexión:

```powershell
python test_mt5_connection.py
```





