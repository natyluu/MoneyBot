# 📁 Acceder a la Carpeta del Proyecto

## ✅ Carpetas Encontradas

Tienes dos carpetas en `C:\`:
1. `bot de trader on 'Mac'`
2. `trading-bot-windows-20251210 on 'Mac'` ⭐ (Usa esta)

---

## Paso 1: Acceder a la Carpeta

**Opción A: Usar Comillas Dobles (Recomendado)**

En PowerShell, ejecuta:

```powershell
cd "C:\trading-bot-windows-20251210 on 'Mac'"
dir
```

**Opción B: Usar Tab para Autocompletar**

1. Escribe: `cd "C:\trading-bot` y presiona **Tab**
2. PowerShell completará automáticamente el nombre
3. Presiona Enter

**Opción C: Renombrar la Carpeta (Más Fácil)**

1. En el Explorador de Windows, ve a `C:\`
2. Clic derecho en `trading-bot-windows-20251210 on 'Mac'`
3. Selecciona **"Cambiar nombre"** (Rename)
4. Escribe: `trading-bot`
5. Presiona Enter

Luego en PowerShell:

```powershell
cd C:\trading-bot
dir
```

---

## Paso 2: Verificar Contenido

Una vez dentro de la carpeta, ejecuta:

```powershell
dir
```

**Deberías ver:**
- `backtest/`
- `live/`
- `strategy/`
- `utils/`
- `config.py`
- `setup_mt5.py`
- `test_mt5_connection.py`
- `requirements.txt`
- etc.

---

## ✅ Si Todo Está Correcto

El proyecto está listo. Siguiente paso: **Instalar MetaTrader 5 (la aplicación)**

---

## 💡 Recomendación

**Renombra la carpeta a `trading-bot`** para evitar problemas con las comillas en el futuro.

---

¡Intenta acceder a la carpeta y verifica el contenido! 🚀







