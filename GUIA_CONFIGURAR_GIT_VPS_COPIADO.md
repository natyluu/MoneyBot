# 🔧 Guía: Configurar Git en VPS (Carpeta Copiada)

## 📋 Situación

Ya copiaste la carpeta completa del bot al VPS y ahora necesitas configurar Git para sincronizar con GitHub.

---

## 🚀 Pasos Rápidos

### Paso 1: Ir a la Carpeta del Bot

En PowerShell o CMD del VPS:

```cmd
cd C:\ruta\al\bot
```

**Ejemplo:**
```cmd
cd "C:\bot de trader"
```

---

### Paso 2: Ejecutar Script de Configuración

Si copiaste la carpeta completa, deberías tener el archivo `CONFIGURAR_GIT_VPS_COPIADO.bat`.

Ejecuta:

```cmd
CONFIGURAR_GIT_VPS_COPIADO.bat
```

El script te guiará paso a paso.

---

## 📝 Pasos Manuales (Si Prefieres)

### 1. Verificar que Git está Instalado

```cmd
git --version
```

**Si NO está instalado:**
- Descarga desde: https://git-scm.com/download/win
- Instala y reinicia el terminal

---

### 2. Ir al Directorio del Bot

```cmd
cd C:\ruta\al\bot
```

---

### 3. Inicializar Git

```cmd
git init
```

---

### 4. Configurar Usuario

```cmd
git config user.name "Bot Trader"
git config user.email "bot@trader.local"
```

---

### 5. Agregar Archivos

```cmd
git add -A
git commit -m "Estado inicial del bot copiado"
```

---

### 6. Conectar con GitHub

```cmd
git remote add origin https://github.com/natyluu/MoneyBot.git
```

---

### 7. Crear Personal Access Token (IMPORTANTE)

1. Ve a: https://github.com/settings/tokens
2. Click en **"Generate new token (classic)"**
3. Nombre: "VPS Bot Trader"
4. Permisos: Marca **`repo`** (acceso completo)
5. Click **"Generate token"**
6. **COPIA EL TOKEN** (solo se muestra una vez)

---

### 8. Sincronizar con GitHub

```cmd
git pull origin main --allow-unrelated-histories
```

Cuando te pida credenciales:
- **Username**: tu usuario de GitHub
- **Password**: pega el Personal Access Token (NO tu contraseña)

---

## ✅ Verificar que Funciona

```cmd
git fetch origin
git status
```

Si ves información sin errores, ¡está funcionando!

---

## 🔄 Actualizar el Bot (Después de Configurar)

### Opción 1: Script Automático

```cmd
ACTUALIZAR_BOT_VPS.bat
```

### Opción 2: Manual

```cmd
git pull origin main
```

---

## ⚠️ Solución de Problemas

### Error: "fatal: could not read Username"

**Solución:**
1. Crea un Personal Access Token (ver paso 7 arriba)
2. Cuando Git pida credenciales, usa el token como contraseña

### Error: "fatal: refusing to merge unrelated histories"

**Solución:**
```cmd
git pull origin main --allow-unrelated-histories
```

### Error: "remote origin already exists"

**Solución:**
```cmd
git remote remove origin
git remote add origin https://github.com/natyluu/MoneyBot.git
```

### Error: "Permission denied"

**Solución:**
- Verifica que el Personal Access Token tenga permisos `repo`
- Verifica que el token no haya expirado
- Crea un nuevo token si es necesario

---

## 📋 Checklist

- [ ] Git instalado en VPS
- [ ] En el directorio del bot
- [ ] Git inicializado (`git init`)
- [ ] Usuario configurado
- [ ] Archivos agregados y commit inicial
- [ ] Remoto configurado (`git remote add origin`)
- [ ] Personal Access Token creado
- [ ] Conexión verificada (`git fetch origin`)
- [ ] Sincronizado con GitHub (`git pull`)

---

## 🎯 Después de Configurar

Una vez configurado, podrás:

1. **Actualizar el bot** desde GitHub:
   ```cmd
   ACTUALIZAR_BOT_VPS.bat
   ```

2. **Ver el estado**:
   ```cmd
   git status
   ```

3. **Ver historial de versiones**:
   ```cmd
   git tag --sort=-version:refname
   ```

---

**¡Una vez configurado, la sincronización será automática!** 🚀






