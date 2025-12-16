# 🔧 Solucionar Problema con MetaTrader5

## Problema
`MetaTrader5` no se puede instalar porque Python 3.14 es muy nuevo y el paquete aún no lo soporta.

## Solución: Instalar Python 3.12

MetaTrader5 funciona mejor con Python 3.11 o 3.12. Vamos a instalar Python 3.12 además de tu Python 3.14.

### Opción 1: Instalar Python 3.12 (Recomendado)

1. Ve a: https://www.python.org/downloads/release/python-3128/
2. Descarga "Windows installer (64-bit)"
3. Instala Python 3.12
4. **IMPORTANTE:** Marca "Add Python to PATH"
5. Después de instalar, usa Python 3.12 para el proyecto:

```powershell
py -3.12 -m pip install MetaTrader5 python-dotenv pandas numpy
```

### Opción 2: Intentar con Python 3.14 (Puede no funcionar)

Primero instala los otros paquetes:

```powershell
python -m pip install python-dotenv pandas numpy
```

Luego intenta MetaTrader5:

```powershell
python -m pip install MetaTrader5
```

Si sigue sin funcionar, necesitarás Python 3.12.

---

## Verificar Versión de Python

Para ver qué versiones tienes instaladas:

```powershell
py --list
```

Esto mostrará todas las versiones de Python instaladas.

---

## Usar Python 3.12 Específicamente

Si instalas Python 3.12, puedes usarlo así:

```powershell
# Instalar dependencias con Python 3.12
py -3.12 -m pip install MetaTrader5 python-dotenv pandas numpy

# Ejecutar scripts con Python 3.12
py -3.12 setup_mt5.py
py -3.12 test_mt5_connection.py
py -3.12 live/mt5_trading.py
```

---

## Solución Rápida: Instalar Solo los que Funcionan

Por ahora, instala los paquetes que sí funcionan:

```powershell
python -m pip install python-dotenv pandas numpy
```

Luego instalaremos MetaTrader5 con Python 3.12.







