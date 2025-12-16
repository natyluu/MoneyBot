# 📦 Instalar Dependencias con Python 3.12

## ✅ Python 3.12 Verificado

Tienes ambas versiones instaladas:
- Python 3.14.2 ✅
- Python 3.12.10 ✅

---

## Paso 1: Verificar Python 3.12 Específicamente

En PowerShell, ejecuta:

```powershell
py -3.12 --version
```

**Deberías ver:** `Python 3.12.10`

---

## Paso 2: Verificar pip de Python 3.12

```powershell
py -3.12 -m pip --version
```

**Deberías ver algo como:** `pip 24.x.x from ...`

---

## Paso 3: Instalar Paquetes Básicos (con Python 3.14)

Primero instala los paquetes que sí funcionan con Python 3.14:

```powershell
python -m pip install python-dotenv pandas numpy
```

Esto instalará:
- `python-dotenv` - Para leer archivos .env
- `pandas` - Para manejar datos
- `numpy` - Para cálculos numéricos

Espera a que termine (2-5 minutos).

---

## Paso 4: Instalar MetaTrader5 (con Python 3.12)

Ahora instala MetaTrader5 usando Python 3.12:

```powershell
py -3.12 -m pip install MetaTrader5
```

Espera a que termine (1-2 minutos).

---

## Paso 5: Verificar que MetaTrader5 Funciona

```powershell
py -3.12 -c "import MetaTrader5; print('✅ MetaTrader5 OK')"
```

**Deberías ver:** `✅ MetaTrader5 OK`

---

## ✅ Si Todo Funciona

¡Todas las dependencias están instaladas!

**Siguiente paso:** Copiar el proyecto a Windows

---

## ❌ Si Hay Problemas

### Problema: "py -3.12" no funciona

**Solución:**
- Cierra y abre una nueva PowerShell
- O reinicia Windows
- Prueba de nuevo: `py -3.12 --version`

### Problema: MetaTrader5 no se instala

**Solución:**
- Verifica que estás usando Python 3.12: `py -3.12 --version`
- Intenta de nuevo: `py -3.12 -m pip install MetaTrader5`
- Si sigue sin funcionar, actualiza pip: `py -3.12 -m pip install --upgrade pip`

---

## 🎯 Comandos Rápidos (Ejecuta en Orden)

```powershell
# 1. Verificar Python 3.12
py -3.12 --version

# 2. Instalar paquetes básicos
python -m pip install python-dotenv pandas numpy

# 3. Instalar MetaTrader5
py -3.12 -m pip install MetaTrader5

# 4. Verificar MetaTrader5
py -3.12 -c "import MetaTrader5; print('✅ MetaTrader5 OK')"
```

---

¡Sigue estos pasos y avísame cuando termines! 🚀







