# Configuración para Vercel Serverless
import sys
import os

# Agregar el directorio raíz al path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Importar la app Flask desde el directorio raíz
from app import app

# Exportar para Vercel (WSGI handler)
def handler(environ, start_response):
    return app(environ, start_response)

# También exportar la app directamente
app = app
