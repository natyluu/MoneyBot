"""
SINCRONIZAR_VPS.py - Sincroniza cambios desde Mac a GitHub

Script simplificado para sincronizar cambios rápidamente sin crear versión.
Útil para cambios menores o pruebas.
"""

import subprocess
import sys
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

def main():
    print("=" * 70)
    print("🚀 SINCRONIZACIÓN MAC → GITHUB → VPS")
    print("=" * 70)
    
    # 1. Verificar estado de Git
    print("\n1️⃣ Verificando estado de Git...")
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True, cwd=project_root)
    
    if not result.stdout.strip():
        print("   ✅ No hay cambios pendientes")
        print("   💡 Ejecutando git pull para asegurar que estás actualizado...")
        run_command("git pull", "Actualizando desde GitHub")
        return
    
    print("   📝 Cambios detectados:")
    print(result.stdout)
    
    # 2. Agregar todos los cambios
    if not run_command("git add -A", "Agregando cambios"):
        return
    
    # 3. Commit
    from datetime import datetime
    commit_message = input("\n📝 Mensaje del commit (o Enter para 'Actualización automática'): ").strip()
    if not commit_message:
        commit_message = f"Actualización automática: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    if not run_command(f'git commit -m "{commit_message}"', "Haciendo commit"):
        return
    
    # 4. Push a GitHub
    if not run_command("git push", "Subiendo a GitHub"):
        return
    
    print("\n" + "=" * 70)
    print("✅ Sincronización completada: Mac → GitHub")
    print("=" * 70)
    print("\n📋 Próximo paso: En el VPS, ejecuta:")
    print("   ACTUALIZAR_BOT_VPS.bat")
    print("\n   O manualmente:")
    print("   git pull")
    print("\n💡 Para crear una versión formal, usa: python3 CREAR_VERSION.py")

if __name__ == "__main__":
    main()

