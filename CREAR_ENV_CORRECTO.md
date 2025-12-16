# ✅ Crear .env Correctamente

## 🔧 Comando Corregido

Ejecuta este comando **completo** en PowerShell (copia y pega todo de una vez):

```powershell
$content = @"
# Configuración MetaTrader 5 (Zeven)
MT5_LOGIN=94338
MT5_PASSWORD=Santos2025!
MT5_SERVER=ZevenGlobal-Live
MT5_SYMBOL=XAUUSD.vip

# Configuración de riesgo
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=2.0
"@
$content | Out-File -FilePath .env -Encoding utf8
```

---

## ✅ Verificar que se creó

```powershell
dir .env
```

Deberías ver el archivo `.env`.

---

## ✅ Ver contenido (opcional)

```powershell
type .env
```

---

## 🎯 Alternativa: Crear línea por línea

Si el comando anterior no funciona, puedes crear el archivo manualmente:

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

## ✅ Verificar

```powershell
dir .env
type .env
```





