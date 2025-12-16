# 🔧 Solucionar Error al Leer .env

## ⚠️ Problema

El error indica que `python-dotenv` no puede leer el archivo `.env` correctamente. Esto puede deberse a:
- Encoding incorrecto
- Formato del archivo
- Caracteres especiales

---

## ✅ Solución: Recrear .env con Formato Correcto

Ejecuta estos comandos en PowerShell:

```powershell
# 1. Eliminar el .env actual (si existe)
del .env -ErrorAction SilentlyContinue

# 2. Crear el .env con formato correcto usando Notepad
notepad .env
```

Cuando se abra Notepad, pega exactamente esto (sin espacios extra):

```
MT5_LOGIN=94338
MT5_PASSWORD=Santos2025!
MT5_SERVER=ZevenGlobal-Live
MT5_SYMBOL=XAUUSD.vip
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=2.0
```

**IMPORTANTE:**
- Guarda el archivo (Ctrl+S)
- Cierra Notepad

---

## ✅ Alternativa: Usar PowerShell con Encoding Correcto

Si prefieres usar PowerShell, ejecuta esto:

```powershell
# Eliminar .env anterior
del .env -ErrorAction SilentlyContinue

# Crear nuevo .env
$lines = @(
    "MT5_LOGIN=94338",
    "MT5_PASSWORD=Santos2025!",
    "MT5_SERVER=ZevenGlobal-Live",
    "MT5_SYMBOL=XAUUSD.vip",
    "RISK_PER_TRADE=0.01",
    "MAX_CONCURRENT_TRADES=3",
    "MIN_RR=2.0"
)
$lines | Out-File -FilePath .env -Encoding ASCII -NoNewline
```

---

## ✅ Verificar

```powershell
type .env
```

Deberías ver todas las líneas sin caracteres extraños.

---

## ✅ Probar de Nuevo

```powershell
python test_mt5_connection.py
```

---

## 🎯 Si Aún Falla

Si el error persiste, podemos modificar el script para que no use `load_dotenv()` y cargue las variables directamente.





