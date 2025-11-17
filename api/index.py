# Configuración para Vercel Serverless
import sys
import os

# Agregar el directorio raíz al path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Configurar variable de entorno para Vercel
os.environ['VERCEL'] = '1'
os.environ['VERCEL_ENV'] = 'production'

# Importar la app Flask
from app import app

# Exportar la app para Vercel
# Vercel espera que exporte 'app' directamente
