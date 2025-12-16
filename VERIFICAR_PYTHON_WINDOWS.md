# ✅ Verificar que Python Funciona en Windows

## Paso 1: Abrir PowerShell

**IMPORTANTE:** Abre una **NUEVA** ventana de PowerShell (no uses la terminal donde instalaste Python).

### Opción A: Desde el Escritorio
1. Clic derecho en el escritorio de Windows
2. Selecciona **"Abrir PowerShell aquí"** o **"Open PowerShell here"**

### Opción B: Desde el Menú Inicio
1. Presiona la tecla **Windows** (o clic en el menú inicio)
2. Escribe **"PowerShell"**
3. Clic en **"Windows PowerShell"** o **"PowerShell"**

---

## Paso 2: Verificar Python

En la nueva ventana de PowerShell, ejecuta:

```powershell
python --version
```

### ✅ Si Funciona Correctamente:
Verás algo como:
```
Python 3.14.0
```
o
```
Python 3.12.5
```

### ❌ Si NO Funciona:
Verás un error como:
```
python : no se reconoce como comando...
```

**Solución:**
- Cierra y abre una nueva PowerShell
- O reinicia Windows
- Si sigue sin funcionar, reinstala Python y marca "Add Python to PATH"

---

## Paso 3: Verificar pip

En la misma ventana de PowerShell, ejecuta:

```powershell
pip --version
```

### ✅ Si Funciona Correctamente:
Verás algo como:
```
pip 24.2.0 from C:\Users\nataliaturizo\AppData\Local\Python\...
```

### ❌ Si NO Funciona:
Verás un error.

**Solución:**
```powershell
python -m ensurepip --upgrade
```

---

## Paso 4: Probar que Python Ejecuta Código

Ejecuta este comando para verificar que Python puede ejecutar código:

```powershell
python -c "print('✅ Python funciona correctamente!')"
```

### ✅ Si Funciona:
Verás:
```
✅ Python funciona correctamente!
```

---

## ✅ Checklist de Verificación

Marca cada paso cuando funcione:

- [ ] PowerShell abierto (nueva ventana)
- [ ] `python --version` muestra una versión (ej: Python 3.14.0)
- [ ] `pip --version` muestra una versión (ej: pip 24.2.0)
- [ ] `python -c "print('✅ Python funciona!')"` muestra el mensaje

---

## 🎯 Si Todo Funciona

¡Python está instalado correctamente! 

**Siguiente paso:** Copiar el proyecto a Windows (ver `COPIAR_PROYECTO_WINDOWS.md`)

---

## ❌ Si Hay Problemas

### Problema: "python no se reconoce como comando"

**Causa:** Python no está en el PATH o necesitas reiniciar la terminal.

**Solución:**
1. Cierra PowerShell completamente
2. Abre una nueva PowerShell
3. Prueba de nuevo: `python --version`
4. Si sigue sin funcionar:
   - Reinstala Python
   - Durante la instalación, marca ✅ **"Add Python to PATH"**
   - Reinicia Windows después de instalar

### Problema: "pip no se reconoce"

**Solución:**
```powershell
python -m ensurepip --upgrade
pip --version
```

### Problema: Python funciona pero pip no

**Solución:**
```powershell
python -m pip install --upgrade pip
```

---

## 📝 Comandos Rápidos (Copia y Pega)

```powershell
# Verificar Python
python --version

# Verificar pip
pip --version

# Probar Python
python -c "print('✅ Python funciona!')"
```

---

¡Sigue estos pasos y avísame qué resultado obtienes! 🚀







