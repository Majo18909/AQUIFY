# Configuración para Vercel Serverless
import sys
import os

# Agregar el directorio raíz al path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Importar la app Flask desde el directorio raíz
from app import app as application

# Exportar para Vercel
app = application
