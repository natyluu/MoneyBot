# 🐍 Instalar Python en Windows (Dentro de Parallels)

## Paso 1: Abrir Navegador en Windows

1. En Windows (dentro de Parallels), abre **Microsoft Edge** o **Chrome**
2. Ve a: https://www.python.org/downloads/

## Paso 2: Descargar Python

1. Clic en el botón grande **"Download Python 3.12.x"** (o la versión más reciente)
2. El archivo `.exe` se descargará automáticamente
3. Ve a la carpeta **Descargas** y ejecuta el instalador

## Paso 3: Instalar Python

⚠️ **MUY IMPORTANTE:** Durante la instalación:

1. En la primera pantalla, marca ✅ **"Add Python to PATH"**
   - Esta opción está en la parte inferior de la ventana
   - Es CRÍTICA para que Python funcione desde PowerShell

2. Clic en **"Install Now"**

3. Espera a que termine la instalación (2-5 minutos)

4. Cuando termine, verás "Setup was successful"
5. Clic en **"Close"**

## Paso 4: Verificar Instalación

1. Abre **PowerShell** en Windows:
   - Clic derecho en el escritorio → "Abrir PowerShell aquí"
   - O busca "PowerShell" en el menú inicio

2. Ejecuta estos comandos:

```powershell
python --version
```

Deberías ver algo como: `Python 3.12.x`

```powershell
pip --version
```

Deberías ver algo como: `pip 24.x.x`

## ✅ Si Funciona

Si ambos comandos muestran versiones, Python está instalado correctamente.

**Siguiente paso:** Copiar el proyecto a Windows

## ❌ Si No Funciona

### Error: "python no se reconoce como comando"

**Solución:**
1. Reinstala Python
2. Durante la instalación, marca ✅ **"Add Python to PATH"**
3. Reinicia PowerShell después de instalar

### Error: "pip no se reconoce"

**Solución:**
1. Verifica que Python esté instalado: `python --version`
2. Si Python funciona pero pip no, ejecuta:
   ```powershell
   python -m ensurepip --upgrade
   ```

---

## 🎯 Siguiente Paso

Una vez que Python esté instalado y funcionando, avísame y te guío para:
1. Copiar el proyecto a Windows
2. Instalar dependencias
3. Configurar el bot







