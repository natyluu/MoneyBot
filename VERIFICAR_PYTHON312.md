# ✅ Verificar Python 3.12 - Paso a Paso

## Paso 1: Cerrar el Instalador

1. Haz clic en **"Close"** en la ventana del instalador
2. El instalador se cerrará

---

## Paso 2: Abrir Nueva PowerShell

**IMPORTANTE:** Abre una **NUEVA** ventana de PowerShell (no uses una que ya estaba abierta).

### Opción A: Desde el Escritorio
1. Clic derecho en el escritorio de Windows
2. Selecciona **"Abrir PowerShell aquí"** o **"Open PowerShell here"**

### Opción B: Desde el Menú Inicio
1. Presiona la tecla **Windows**
2. Escribe **"PowerShell"**
3. Clic en **"Windows PowerShell"** o **"PowerShell"**

---

## Paso 3: Verificar Todas las Versiones de Python

En la nueva PowerShell, ejecuta:

```powershell
py --list
```

**Deberías ver algo como:**
```
-V:3.14 Python 3.14.2
-V:3.12 Python 3.12.10
```

Esto confirma que tienes **ambas versiones** instaladas.

---

## Paso 4: Verificar Python 3.12 Específicamente

Ejecuta:

```powershell
py -3.12 --version
```

**Deberías ver:**
```
Python 3.12.10
```

---

## Paso 5: Verificar pip de Python 3.12

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
- Cierra PowerShell completamente
- Abre una nueva PowerShell
- Prueba de nuevo: `py --list`
- Si sigue sin funcionar, reinicia Windows

### Problema: "py -3.12" no funciona

**Solución:**
- Verifica que Python 3.12 se instaló: `py --list`
- Si no aparece, reinstala Python 3.12 y marca "Add python.exe to PATH"

---

## 🎯 Comandos Rápidos (Copia y Pega)

```powershell
# Ver todas las versiones
py --list

# Verificar Python 3.12
py -3.12 --version

# Verificar pip de Python 3.12
py -3.12 -m pip --version
```

---

¡Sigue estos pasos y avísame qué resultado obtienes! 🚀







