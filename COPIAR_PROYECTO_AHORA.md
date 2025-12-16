# 📁 Copiar Proyecto a Windows - Guía Paso a Paso

## ✅ Verificación Completada

- [x] MetaTrader5 instalado y funcionando ✅

---

## 📋 Pasos para Copiar el Proyecto

### Paso 1: Habilitar Compartir en Parallels

1. En Parallels, haz clic en el menú **"Acciones"** (o **"Actions"** en inglés)
2. Selecciona **"Configuración"** (⚙️) o **"Settings"**
3. En la ventana de configuración, ve a **"Opciones"** (o **"Options"**)
4. Selecciona **"Compartir"** (o **"Sharing"**)
5. Marca ✅ **"Compartir Mac"** (o **"Share Mac"**)
6. Cierra la ventana de configuración

---

### Paso 2: Acceder al Proyecto desde Windows

1. En Windows, abre **Explorador de archivos** (icono de carpeta en la barra de tareas)
2. En la barra lateral izquierda, busca **"Red"** o **"Network"**
3. Expande **"Red"** y busca tu Mac (puede aparecer como "Mac" o el nombre de tu Mac)
4. Haz clic en tu Mac para ver las carpetas compartidas
5. Navega hasta la carpeta del proyecto: `bot de trader`
   - Ruta completa: `Red > Mac > bot de trader`

---

### Paso 3: Copiar el Proyecto

**Opción A: Copiar y Pegar**

1. Selecciona toda la carpeta `bot de trader`
2. Clic derecho → **"Copiar"** (o **"Copy"**)
3. Ve a `C:\` (disco local C:)
4. Clic derecho → **"Pegar"** (o **"Paste"**)
5. Si Windows pregunta si quieres renombrar, puedes renombrarla a `trading-bot` o dejarla como está

**Opción B: Arrastrar**

1. Abre otra ventana del Explorador
2. Ve a `C:\`
3. Arrastra la carpeta `bot de trader` desde la red a `C:\`
4. Puedes renombrarla a `trading-bot` si quieres

---

### Paso 4: Verificar que el Proyecto Está Correcto

En PowerShell, ejecuta:

```powershell
cd C:\trading-bot
```

O si la dejaste con el nombre original:

```powershell
cd "C:\bot de trader"
```

Luego verifica la estructura:

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

## ❌ Si No Puedes Ver la Carpeta Compartida

### Solución 1: Verificar Compartir

1. En Parallels: Configuración → Opciones → Compartir
2. Asegúrate de que **"Compartir Mac"** esté marcado ✅
3. Reinicia Windows si es necesario

### Solución 2: Usar Ruta Directa

En el Explorador de Windows, en la barra de direcciones, escribe:

```
\\Mac\bot de trader
```

O busca en:

```
\\Mac\Users\nataliaturizo\bot de trader
```

### Solución 3: Copiar Manualmente

1. En Mac, comprime la carpeta del proyecto (clic derecho → Comprimir)
2. Copia el ZIP a Windows (USB, Dropbox, etc.)
3. En Windows, descomprime en `C:\trading-bot`

---

## ✅ Si Todo Está Bien

El proyecto está listo. Siguiente paso: Instalar MetaTrader 5 (la aplicación)

---

## 🎯 Comandos Rápidos (Después de Copiar)

```powershell
# Ir al proyecto
cd C:\trading-bot

# Ver estructura
dir

# Ver archivos principales
dir *.py
```

---

¡Sigue estos pasos y avísame cuando el proyecto esté copiado! 🚀







