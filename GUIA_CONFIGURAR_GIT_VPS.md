# 🔧 Guía: Configurar Git en VPS para GitHub

## 📋 Pasos para Conectar el VPS con GitHub

### Paso 1: Verificar que Git está Instalado

En PowerShell o CMD del VPS:

```cmd
git --version
```

**Si NO está instalado:**
1. Descarga Git desde: https://git-scm.com/download/win
2. Instala con opciones por defecto
3. Reinicia el terminal

---

### Paso 2: Ejecutar Script de Configuración

1. Copia `CONFIGURAR_GIT_VPS.bat` al VPS
2. Ejecuta el script:

```cmd
CONFIGURAR_GIT_VPS.bat
```

El script te guiará paso a paso.

---

### Paso 3: Elegir Método de Autenticación

Tienes dos opciones:

#### Opción A: HTTPS (Más Fácil) ⭐ RECOMENDADO

**Ventajas:**
- Más fácil de configurar
- No requiere llaves SSH

**Desventajas:**
- Necesitas un Personal Access Token (PAT)

**Pasos:**
1. Crea un PAT en GitHub:
   - Ve a: https://github.com/settings/tokens
   - Click en "Generate new token (classic)"
   - Nombre: "VPS Bot Trader"
   - Permisos: Marca `repo` (acceso completo)
   - Genera y copia el token

2. Cuando Git te pida credenciales:
   - Usuario: tu usuario de GitHub
   - Contraseña: pega el PAT (no tu contraseña real)

#### Opción B: SSH (Más Seguro)

**Ventajas:**
- Más seguro
- No necesitas ingresar credenciales cada vez

**Desventajas:**
- Requiere configurar llaves SSH

**Pasos:**
1. Genera llave SSH en el VPS:
```cmd
ssh-keygen -t ed25519 -C "bot@vps"
```
2. Copia la llave pública:
```cmd
type %USERPROFILE%\.ssh\id_ed25519.pub
```
3. Agrega la llave a GitHub:
   - Ve a: https://github.com/settings/keys
   - Click "New SSH key"
   - Pega la llave pública

---

### Paso 4: Configurar el Repositorio

#### Si el bot YA está en el VPS (sin Git):

1. Ve al directorio del bot:
```cmd
cd C:\ruta\al\bot
```

2. Inicializa Git:
```cmd
git init
```

3. Agrega el remoto:
```cmd
git remote add origin https://github.com/natyluu/MoneyBot.git
```

4. Haz pull:
```cmd
git pull origin main
```

#### Si el bot NO está en el VPS:

1. Clona el repositorio:
```cmd
git clone https://github.com/natyluu/MoneyBot.git C:\ruta\al\bot
```

---

### Paso 5: Verificar Conexión

```cmd
cd C:\ruta\al\bot
git fetch origin
```

Si funciona, verás:
```
✅ Conexión exitosa
```

---

## 🔄 Actualizar el Bot (Después de Configurar)

### Método 1: Script Automático

```cmd
ACTUALIZAR_BOT_VPS.bat
```

### Método 2: Manual

```cmd
cd C:\ruta\al\bot
git pull origin main
```

---

## ⚠️ Solución de Problemas

### Error: "fatal: could not read Username"

**Solución:**
- Usa HTTPS con Personal Access Token
- O configura SSH

### Error: "Permission denied (publickey)"

**Solución:**
- Configura llaves SSH (ver Opción B arriba)

### Error: "repository not found"

**Solución:**
- Verifica que la URL del repositorio sea correcta
- Verifica que tengas acceso al repositorio

### Error: "fatal: not a git repository"

**Solución:**
- Ejecuta `git init` en el directorio del bot
- O clona el repositorio desde cero

---

## 📝 Comandos Útiles

```cmd
# Ver configuración actual
git config --list

# Ver remotos configurados
git remote -v

# Cambiar URL del remoto
git remote set-url origin https://github.com/natyluu/MoneyBot.git

# Verificar conexión
git fetch origin

# Actualizar desde GitHub
git pull origin main

# Ver estado
git status
```

---

## ✅ Checklist de Configuración

- [ ] Git instalado en VPS
- [ ] Usuario de Git configurado
- [ ] Repositorio clonado o inicializado
- [ ] Remoto 'origin' configurado
- [ ] Conexión con GitHub verificada
- [ ] `ACTUALIZAR_BOT_VPS.bat` funciona

---

**Una vez configurado, podrás actualizar el bot fácilmente desde GitHub!** 🚀






