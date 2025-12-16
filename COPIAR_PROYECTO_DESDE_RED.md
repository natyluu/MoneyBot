# 📁 Copiar Proyecto desde la Red a Windows

## ✅ Carpetas Compartidas Configuradas

Ya tienes las carpetas compartidas:
- ✅ "bot de trader" (activada)
- ✅ "trading-bot-windows..." (activada)

---

## Paso 1: Cerrar la Configuración de Parallels

1. En la ventana de configuración de Parallels, haz clic en **"Aceptar"** (botón rosa/rojo)
2. La ventana se cerrará

---

## Paso 2: Acceder a las Carpetas Compartidas desde Windows

1. En Windows, abre **Explorador de archivos** (icono de carpeta en la barra de tareas)
2. En la barra lateral izquierda, busca **"Red"** (Network)
3. Haz clic en **"Red"**
4. Busca tu Mac (puede aparecer como "Mac" o el nombre de tu Mac)
5. Haz clic en tu Mac para ver las carpetas compartidas
6. Deberías ver la carpeta **"bot de trader"**

---

## Paso 3: Copiar el Proyecto

**Opción A: Copiar y Pegar**

1. Abre la carpeta **"bot de trader"** desde la red
2. Selecciona **todos los archivos y carpetas** dentro (Ctrl+A)
3. Clic derecho → **"Copiar"** (Copy)
4. Ve a `C:\` (disco local C:)
5. Clic derecho → **"Pegar"** (Paste)
6. Si Windows pregunta, acepta
7. Opcional: Renombra la carpeta a `trading-bot` si quieres

**Opción B: Arrastrar**

1. Abre otra ventana del Explorador
2. Ve a `C:\`
3. Arrastra la carpeta **"bot de trader"** desde la red a `C:\`
4. Puedes renombrarla a `trading-bot` si quieres

---

## Paso 4: Verificar que el Proyecto Está Correcto

En PowerShell:

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

## ✅ Si Todo Está Bien

El proyecto está listo. Siguiente paso: Instalar MetaTrader 5 (la aplicación)

---

## ❌ Si No Puedes Ver la Carpeta en la Red

**Solución 1:** Reinicia Windows

**Solución 2:** En el Explorador, en la barra de direcciones escribe:
```
\\Mac\bot de trader
```

**Solución 3:** Verifica que las carpetas estén activadas en la configuración de Parallels

---

¡Sigue estos pasos y avísame cuando el proyecto esté copiado! 🚀







