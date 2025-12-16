# 🔍 Encontrar la Carpeta del Proyecto

## ❌ Problema

La ruta con comillas simples puede causar problemas. Vamos a encontrar la carpeta correcta.

---

## Paso 1: Ver Qué Hay en C:\

En PowerShell, ejecuta:

```powershell
cd C:\
dir
```

Esto mostrará todas las carpetas en C:\

---

## Paso 2: Buscar la Carpeta del Proyecto

Busca en la lista una de estas carpetas:
- `trading-bot-windows-20251210 on 'Mac'`
- `bot de trader on 'Mac'`
- O cualquier otra carpeta que contenga el proyecto

---

## Paso 3: Acceder a la Carpeta

**Opción A: Usar Tab para Autocompletar**

1. Escribe: `cd C:\` y presiona **Tab** varias veces
2. PowerShell mostrará las carpetas disponibles
3. Cuando veas la carpeta del proyecto, presiona Enter

**Opción B: Copiar el Nombre Exacto**

1. En el Explorador de Windows, ve a `C:\`
2. Clic derecho en la carpeta del proyecto → **"Copiar ruta de acceso"** (Copy path)
3. En PowerShell, escribe: `cd ` y luego pega la ruta (Ctrl+V)

**Opción C: Usar Comillas Simples**

Intenta con comillas simples en lugar de dobles:

```powershell
cd 'C:\trading-bot-windows-20251210 on ''Mac'''
```

O escapa las comillas:

```powershell
cd "C:\trading-bot-windows-20251210 on 'Mac'"
```

---

## Paso 4: Verificar Contenido

Una vez dentro de la carpeta:

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
- etc.

---

## 💡 Solución Rápida: Renombrar la Carpeta

Si sigue habiendo problemas, renombra la carpeta:

1. En el Explorador de Windows, ve a `C:\`
2. Clic derecho en la carpeta → **"Cambiar nombre"** (Rename)
3. Escribe: `trading-bot` (sin espacios ni comillas)
4. Presiona Enter
5. En PowerShell: `cd C:\trading-bot`

---

¡Primero ejecuta `cd C:\` y luego `dir` para ver qué carpetas hay! 🚀







