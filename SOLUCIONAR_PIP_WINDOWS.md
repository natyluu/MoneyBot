# 🔧 Solucionar Problema con pip en Windows

## Problema
Python funciona (`python --version` ✅) pero `pip` no se reconoce.

## Solución Rápida

En PowerShell, ejecuta estos comandos **uno por uno**:

### Paso 1: Instalar pip usando Python

```powershell
python -m ensurepip --upgrade
```

Esto instalará pip usando el módulo integrado de Python.

### Paso 2: Verificar que pip funciona

```powershell
python -m pip --version
```

Deberías ver algo como: `pip 24.x.x from ...`

### Paso 3: Actualizar pip (opcional pero recomendado)

```powershell
python -m pip install --upgrade pip
```

### Paso 4: Probar pip directamente

Después de los pasos anteriores, intenta:

```powershell
pip --version
```

Si aún no funciona, usa siempre: `python -m pip` en lugar de solo `pip`

---

## Alternativa: Usar `python -m pip` siempre

Si `pip` directamente no funciona, puedes usar siempre:

```powershell
python -m pip install MetaTrader5
```

En lugar de:

```powershell
pip install MetaTrader5
```

Ambos hacen lo mismo, solo que `python -m pip` siempre funciona.

---

## Verificación Final

Ejecuta:

```powershell
python -m pip --version
```

Si muestra una versión de pip, ¡está funcionando! Puedes continuar con la instalación de dependencias.

---

## Siguiente Paso

Una vez que `python -m pip --version` funcione, puedes instalar las dependencias:

```powershell
python -m pip install MetaTrader5 python-dotenv pandas numpy
```







