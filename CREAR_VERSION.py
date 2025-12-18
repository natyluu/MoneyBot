"""
CREAR_VERSION.py - Crea una nueva versión del bot con tag de Git

Sistema de versionado automático que:
1. Detecta cambios
2. Crea commit con descripción
3. Crea tag de versión
4. Sube todo a GitHub
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

project_root = Path(__file__).parent

def run_command(cmd, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, cwd=project_root)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(e.stderr)
        return False

def get_next_version():
    """Obtiene la siguiente versión basada en los tags existentes"""
    result = subprocess.run("git tag", shell=True, capture_output=True, text=True, cwd=project_root)
    tags = [tag for tag in result.stdout.strip().split('\n') if tag and tag.startswith('v')]
    
    if not tags:
        return "v1.0.0"
    
    # Ordenar tags y obtener el mayor
    try:
        # Extraer números de versión
        versions = []
        for tag in tags:
            if tag.startswith('v'):
                try:
                    parts = tag[1:].split('.')
                    if len(parts) == 3:
                        versions.append((int(parts[0]), int(parts[1]), int(parts[2])))
                except:
                    continue
        
        if versions:
            versions.sort()
            last = versions[-1]
            # Incrementar patch version
            return f"v{last[0]}.{last[1]}.{last[2] + 1}"
    except Exception as e:
        print(f"⚠️ Error al calcular versión: {e}")
    
    return "v1.0.0"

def main():
    print("=" * 70)
    print("📦 CREAR NUEVA VERSIÓN DEL BOT")
    print("=" * 70)
    
    # 1. Verificar cambios
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True, cwd=project_root)
    has_changes = bool(result.stdout.strip())
    
    if has_changes:
        print("\n📝 Cambios detectados:")
        print(result.stdout)
    else:
        print("\n⚠️ No hay cambios para commitear")
        response = input("¿Deseas crear una versión de todos modos? (s/n): ").strip().lower()
        if response != 's':
            print("❌ Cancelado")
            return
    
    # 2. Agregar cambios si hay
    if has_changes:
        if not run_command("git add -A", "Agregando cambios"):
            return
    
    # 3. Commit
    print("\n" + "-" * 70)
    descripcion = input("📝 Descripción de la mejora (ej: 'Agregar News Risk Gate'): ").strip()
    if not descripcion:
        descripcion = f"Mejora: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    commit_message = f"{descripcion}"
    
    if has_changes:
        if not run_command(f'git commit -m "{commit_message}"', "Haciendo commit"):
            return
    
    # 4. Obtener versión
    next_version = get_next_version()
    print(f"\n📌 Versión sugerida: {next_version}")
    version = input(f"   Versión (Enter para {next_version} o escribe otra): ").strip()
    if not version:
        version = next_version
    if not version.startswith('v'):
        version = f"v{version}"
    
    # 5. Crear tag
    tag_message = f"{descripcion} - {datetime.now().strftime('%Y-%m-%d')}"
    if not run_command(f'git tag -a {version} -m "{tag_message}"', f"Creando tag {version}"):
        return
    
    # 6. Push a GitHub (commits y tags)
    if has_changes:
        if not run_command("git push", "Subiendo commits a GitHub"):
            return
    
    if not run_command("git push --tags", "Subiendo tags a GitHub"):
        return
    
    print("\n" + "=" * 70)
    print(f"✅ Versión {version} creada y subida a GitHub")
    print("=" * 70)
    print(f"\n📋 Próximo paso en el VPS:")
    print(f"   Ejecuta: ACTUALIZAR_BOT_VPS.bat")
    print(f"   O manualmente:")
    print(f"   git pull")
    print(f"   git checkout {version}  # (opcional, para usar esta versión específica)")
    print(f"\n💡 Para ver todas las versiones: git tag --sort=-version:refname")

if __name__ == "__main__":
    main()

