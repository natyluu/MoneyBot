# ⚡ Inicio Rápido: Parallels + Windows

## 🎯 Objetivo

Configurar Parallels Desktop para ejecutar tu bot de trading en Windows.

## 📦 Lo que Ya Está Listo

✅ **Paquete preparado:** `../trading-bot-windows-20251210`
✅ **Código completo** listo para Windows
✅ **Scripts de instalación** incluidos
✅ **Instrucciones detalladas** en `GUIA_PARALLELS_COMPLETA.md`

## 🚀 Pasos Rápidos

### 1. Instalar Parallels (Si No Lo Tienes)

```bash
# Opción A: Mac App Store
open "macappstore://apps.apple.com/app/parallels-desktop/id1085114709"

# Opción B: Descarga directa
# Ve a: https://www.parallels.com/products/desktop/
```

### 2. Crear Windows en Parallels

1. Abre Parallels Desktop
2. Clic "Instalar Windows"
3. Espera a que se instale (30-60 min)

### 3. En Windows: Instalar Python

```powershell
# Descarga Python desde python.org
# IMPORTANTE: Marca "Add Python to PATH"
```

### 4. Copiar Proyecto a Windows

**Método fácil:**
1. Parallels → Configuración → Compartir → Marca "Compartir Mac"
2. En Windows: Red → Mac → Copia la carpeta del proyecto

### 5. En Windows: Instalar y Configurar

```powershell
cd C:\trading-bot

# Instalar
pip install MetaTrader5 python-dotenv pandas numpy

# Configurar
python setup_mt5.py

# Probar (con MT5 abierto)
python test_mt5_connection.py

# Ejecutar
python live/mt5_trading.py
```

## 📋 Checklist

- [ ] Parallels Desktop instalado
- [ ] Windows instalado en Parallels
- [ ] Python instalado en Windows (con PATH)
- [ ] Proyecto copiado a Windows
- [ ] Dependencias instaladas
- [ ] MT5 instalado en Windows
- [ ] Credenciales configuradas
- [ ] Prueba de conexión exitosa

## 🆘 ¿Necesitas Ayuda?

- **Guía completa:** `GUIA_PARALLELS_COMPLETA.md`
- **Pasos detallados:** `PASOS_PARALLELS.md`
- **Instrucciones Windows:** `INSTRUCCIONES_WINDOWS.txt`

## 💡 Tip

Usa **modo Coherencia** de Parallels para tener MT5 visible mientras trabajas en Mac.









