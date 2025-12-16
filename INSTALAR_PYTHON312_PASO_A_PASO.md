# 🐍 Instalar Python 3.12 - Paso a Paso

## Paso 1: Abrir Navegador en Windows

1. En Windows (dentro de Parallels), abre **Microsoft Edge** o **Chrome**
2. Ve a esta URL exacta:
   ```
   https://www.python.org/downloads/release/python-3128/
   ```

---

## Paso 2: Descargar Python 3.12

En la página que se abrió:

1. Busca la sección **"Files"** (Archivos)
2. Busca **"Windows installer (64-bit)"**
3. Clic en el enlace para descargar
4. El archivo se llamará algo como: `python-3.12.8-amd64.exe`
5. Espera a que termine la descarga (tamaño: ~25 MB)

---

## Paso 3: Ejecutar el Instalador

1. Ve a la carpeta **Descargas** en Windows
2. Busca el archivo `python-3.12.8-amd64.exe` (o similar)
3. **Doble clic** para ejecutarlo
4. Si Windows pregunta permisos, clic en **"Sí"** o **"Yes"**

---

## Paso 4: Instalar Python 3.12

**⚠️ MUY IMPORTANTE:** Durante la instalación:

1. En la **primera pantalla** del instalador:
   - **Marca ✅ "Add Python 3.12 to PATH"** (abajo en la ventana)
   - Esta opción es CRÍTICA

2. Clic en **"Install Now"** (o "Instalar ahora")

3. Espera a que termine la instalación (2-5 minutos)
   - Verás una barra de progreso
   - No cierres la ventana

4. Cuando termine, verás **"Setup was successful"**
   - Clic en **"Close"** o **"Cerrar"**

---

## Paso 5: Verificar Instalación

1. **Cierra cualquier PowerShell abierto** (importante: nueva ventana)

2. Abre una **nueva PowerShell**:
   - Clic derecho en escritorio → "Abrir PowerShell aquí"
   - O busca "PowerShell" en el menú inicio

3. Ejecuta este comando para ver todas las versiones de Python:

```powershell
py --list
```

**Deberías ver algo como:**
```
-V:3.14 Python 3.14.2
-V:3.12 Python 3.12.8
```

Esto confirma que tienes Python 3.14 Y Python 3.12 instalados.

---

## Paso 6: Verificar Python 3.12 Específicamente

Ejecuta:

```powershell
py -3.12 --version
```

**Deberías ver:**
```
Python 3.12.8
```

---

## Paso 7: Verificar pip de Python 3.12

Ejecuta:

```powershell
py -3.12 -m pip --version
```

**Deberías ver algo como:**
```
pip 24.x.x from ...
```

---

## ✅ Si Todo Funciona

¡Python 3.12 está instalado correctamente!

**Siguiente paso:** Instalar las dependencias con Python 3.12

---

## ❌ Si Hay Problemas

### Problema: "py --list" no muestra Python 3.12

**Solución:**
- Reinicia Windows
- O reinstala Python 3.12 y marca "Add Python to PATH"

### Problema: "py -3.12" no funciona

**Solución:**
- Verifica que Python 3.12 se instaló correctamente
- Prueba: `py -3.12 --version`
- Si no funciona, reinstala Python 3.12

---

## 🎯 Comandos Rápidos (Después de Instalar)

```powershell
# Ver todas las versiones
py --list

# Verificar Python 3.12
py -3.12 --version

# Verificar pip de Python 3.12
py -3.12 -m pip --version
```

---

¡Sigue estos pasos y avísame cuando termines! 🚀







