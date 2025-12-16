"""
Script para corregir live/mt5_trading.py y agregar el path correcto
"""

import os
import shutil

file_path = 'live/mt5_trading.py'

if not os.path.exists(file_path):
    print(f"❌ No se encontró {file_path}")
    exit(1)

# Leer el archivo
with open(file_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

# Verificar si ya tiene la corrección
if 'sys.path.insert(0, project_root)' in contenido:
    print("✅ El archivo ya está corregido")
    exit(0)

# Buscar la línea de imports
inicio_imports = contenido.find('import MetaTrader5 as mt5')
if inicio_imports == -1:
    print("❌ No se encontró la sección de imports")
    exit(1)

# Código a insertar antes de los imports
codigo_a_insertar = '''import sys
import os

# Agregar el directorio raíz al path para que Python encuentre los módulos
# Esto permite importar config y otros módulos desde cualquier ubicación
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

'''

# Crear backup
shutil.copy(file_path, file_path + '.backup')

# Insertar el código
contenido_corregido = contenido[:inicio_imports] + codigo_a_insertar + contenido[inicio_imports:]

# Guardar
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(contenido_corregido)

print("✅ live/mt5_trading.py corregido exitosamente!")
print("   Se creó un backup: live/mt5_trading.py.backup")





