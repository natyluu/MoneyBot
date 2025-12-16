# 🔍 Cómo Encontrar el Proyecto en Windows

## ✅ Paso 1: Buscar en tu carpeta de usuario

Ejecuta en PowerShell:

```powershell
dir
```

Esto muestra lo que hay en `C:\Users\nataliaturizo\`

---

## ✅ Paso 2: Buscar en C:\

Si no está en tu carpeta de usuario, busca en C:\:

```powershell
cd C:\
dir
```

Busca carpetas que contengan:
- `trading`
- `bot`
- `windows-20251210`

---

## ✅ Paso 3: Buscar en toda la unidad C

Si no aparece, busca todas las carpetas que contengan "trading" o "bot":

```powershell
Get-ChildItem -Path C:\ -Recurse -Directory -Filter "*trading*" -ErrorAction SilentlyContinue -Depth 2 | Select-Object FullName
```

O:

```powershell
Get-ChildItem -Path C:\ -Recurse -Directory -Filter "*bot*" -ErrorAction SilentlyContinue -Depth 2 | Select-Object FullName
```

---

## ✅ Paso 4: Si NO encuentras el proyecto

### Opción A: Copiar desde el Explorador de Windows

1. Abre el **Explorador de Windows** (Win + E)
2. En el panel izquierdo, busca **"Red"** o **"Network"**
3. Busca **"Mac"** o el nombre de tu Mac
4. Navega hasta encontrar la carpeta del proyecto
5. **Copia** la carpeta completa
6. **Pega** en `C:\trading-bot`

### Opción B: Usar el Explorador de Archivos de Parallels

1. En Windows, abre el **Explorador de archivos**
2. En el panel izquierdo, busca **"PSF"** o **"Parallels Shared Folders"**
3. Navega hasta encontrar la carpeta del proyecto
4. **Copia** la carpeta completa
5. **Pega** en `C:\trading-bot`

### Opción C: Crear el proyecto desde cero en Windows

Si no encuentras el proyecto, puedo ayudarte a copiarlo directamente desde Mac a Windows usando otra método.

---

## ✅ Paso 5: Verificar que el proyecto está completo

Una vez que encuentres o copies el proyecto a `C:\trading-bot`, verifica:

```powershell
cd C:\trading-bot
dir
```

Deberías ver:
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

## 🎯 Siguiente Paso

Ejecuta `dir` en PowerShell (ya lo tienes escrito) y presiona Enter. Luego dime qué ves.





