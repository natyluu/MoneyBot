# 📁 Copiar Proyecto a Windows

Hay dos formas de copiar el proyecto desde Mac a Windows dentro de Parallels.

## Método 1: Carpeta Compartida (Más Fácil) ⭐ RECOMENDADO

### Paso 1: Habilitar Compartir en Parallels

1. En Parallels, ve a: **Configuración** (⚙️) → **Opciones** → **Compartir**
2. Marca ✅ **"Compartir Mac"**
3. Cierra la ventana de configuración

### Paso 2: Acceder desde Windows

1. En Windows, abre **Explorador de archivos**
2. En la barra lateral izquierda, busca **"Red"** o **"Network"**
3. Expande **"Mac"** o busca tu Mac
4. Navega hasta la carpeta del proyecto:
   - Ruta en Mac: `/Users/nataliaturizo/bot de trader`
   - En Windows aparecerá como: `\\Mac\bot de trader` o similar

### Paso 3: Copiar Proyecto

1. Selecciona toda la carpeta del proyecto
2. Copia (Ctrl+C)
3. Pega en `C:\trading-bot` (Crea la carpeta si no existe)

**O directamente:**
- Arrastra la carpeta desde la red a `C:\trading-bot`

---

## Método 2: Usar el ZIP

### Paso 1: En Mac

El archivo ZIP ya está creado: `trading-bot-windows-20251210.zip`

### Paso 2: Copiar ZIP a Windows

**Opción A: Carpeta Compartida**
1. Habilitar compartir (ver Método 1, Paso 1)
2. Copiar el ZIP desde la red a Windows
3. Descomprimir en `C:\trading-bot`

**Opción B: USB o Dropbox/Google Drive**
1. Copia el ZIP a USB o sube a la nube
2. En Windows, descarga/copia el ZIP
3. Descomprimir en `C:\trading-bot`

### Paso 3: Descomprimir

1. Clic derecho en el ZIP → **"Extraer todo"** o **"Extract All"**
2. Selecciona destino: `C:\trading-bot`
3. Espera a que termine

---

## Verificar que el Proyecto Esté Correcto

Abre PowerShell en Windows y ejecuta:

```powershell
cd C:\trading-bot
dir
```

Deberías ver:
```
backtest/
live/
strategy/
utils/
config.py
setup_mt5.py
test_mt5_connection.py
.env.example
requirements.txt
... (otros archivos)
```

---

## ✅ Si Todo Está Bien

El proyecto está listo. Siguiente paso: Instalar dependencias

---

## ❌ Si Hay Problemas

### No puedo ver la carpeta compartida

**Solución:**
1. Verifica que "Compartir Mac" esté habilitado en Parallels
2. Reinicia Windows
3. O usa el método del ZIP

### El proyecto no tiene todos los archivos

**Solución:**
1. Verifica que copiaste toda la carpeta
2. O usa el ZIP que tiene todo incluido

---

## 🎯 Siguiente Paso

Una vez que el proyecto esté en `C:\trading-bot`, avísame y te guío para instalar las dependencias.







