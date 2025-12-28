# 📦 Sistema de Versionado del Bot

## 🎯 Propósito

Este sistema permite mantener un historial organizado de todas las mejoras del bot, facilitando:
- ✅ Sincronización automática entre Mac y VPS
- ✅ Historial completo de versiones
- ✅ Rollback a versiones anteriores si es necesario
- ✅ Documentación de cada mejora

---

## 🚀 Uso Rápido

### Para cambios menores (sincronización rápida):

```bash
python3 SINCRONIZAR_VPS.py
```

Esto:
1. Detecta cambios
2. Crea commit
3. Sube a GitHub
4. En el VPS ejecutas `ACTUALIZAR_BOT_VPS.bat`

### Para mejoras importantes (crear versión):

```bash
python3 CREAR_VERSION.py
```

Esto:
1. Detecta cambios
2. Crea commit con descripción
3. Crea tag de versión (ej: v1.2.3)
4. Sube todo a GitHub
5. En el VPS ejecutas `ACTUALIZAR_BOT_VPS.bat`

---

## 📋 Flujo de Trabajo Completo

### En Mac (después de hacer cambios conmigo):

#### Opción 1: Sincronización rápida
```bash
python3 SINCRONIZAR_VPS.py
```
- Útil para cambios menores
- No crea versión formal
- Solo sincroniza cambios

#### Opción 2: Crear versión formal
```bash
python3 CREAR_VERSION.py
```
- Describe la mejora
- Crea versión numerada (v1.2.3)
- Historial completo

### En VPS (para actualizar):

```batch
ACTUALIZAR_BOT_VPS.bat
```

O manualmente:
```bash
git pull
```

Para usar una versión específica:
```bash
git checkout v1.2.3
```

---

## 📊 Ver Historial de Versiones

```bash
# Ver todas las versiones
git tag --sort=-version:refname

# Ver detalles de una versión
git show v1.2.3

# Ver cambios entre versiones
git diff v1.2.2 v1.2.3

# Ver log de commits
git log --oneline --graph
```

---

## 🔄 Sincronización Automática

### Mac → GitHub → VPS

1. **Mac**: Haces cambios conmigo
2. **Mac**: Ejecutas `CREAR_VERSION.py` o `SINCRONIZAR_VPS.py`
3. **GitHub**: Recibe los cambios automáticamente
4. **VPS**: Ejecutas `ACTUALIZAR_BOT_VPS.bat` para descargar

---

## 📝 Convención de Versiones

Usamos **Semantic Versioning** (SemVer):
- **v1.2.3**
  - `1` = Major (cambios grandes que rompen compatibilidad)
  - `2` = Minor (nuevas funcionalidades, compatible)
  - `3` = Patch (correcciones, compatible)

Ejemplos:
- `v1.0.0` - Primera versión estable
- `v1.1.0` - Agregar News Risk Gate
- `v1.1.1` - Corregir bug en News Gate
- `v2.0.0` - Refactorización mayor

---

## ⚠️ Notas Importantes

1. **Siempre sincroniza después de cambios**: No dejes cambios sin subir
2. **Usa versiones para mejoras importantes**: Facilita el rollback
3. **Describe bien las mejoras**: Ayuda a entender el historial
4. **En VPS, siempre pull antes de ejecutar**: Asegura tener la última versión

---

## 🐛 Solución de Problemas

### Error: "No se pudo conectar a GitHub"
- Verifica tu conexión a internet
- Verifica que tengas acceso al repositorio
- Revisa credenciales de Git

### Error: "Cambios locales serían sobrescritos"
- En VPS, haz commit de cambios locales primero
- O usa `git stash` para guardar cambios temporalmente

### Quiero volver a una versión anterior
```bash
git checkout v1.2.0
```

### Quiero ver qué cambió en una versión
```bash
git show v1.2.3
```

---

## 📁 Archivos del Sistema

- `CREAR_VERSION.py` - Crea versiones formales con tags
- `SINCRONIZAR_VPS.py` - Sincronización rápida sin versión
- `ACTUALIZAR_BOT_VPS.bat` - Script para actualizar en VPS
- `README_VERSIONADO.md` - Esta documentación

---

**Última actualización**: 2025-01-17






