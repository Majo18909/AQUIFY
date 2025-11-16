# -*- coding: utf-8 -*-
"""
Configuración específica para Vercel
Usa almacenamiento temporal para datos y música
"""

import os
import tempfile

# Sobrescribir directorios para usar /tmp en Vercel
def setup_vercel_storage():
    """Configura directorios en /tmp para Vercel (serverless)"""
    tmp_dir = tempfile.gettempdir()
    
    # Crear directorios en /tmp
    datos_dir = os.path.join(tmp_dir, 'aquify_datos')
    musica_dir = os.path.join(tmp_dir, 'aquify_musica')
    
    os.makedirs(datos_dir, exist_ok=True)
    os.makedirs(musica_dir, exist_ok=True)
    
    return datos_dir, musica_dir

# Detectar si estamos en Vercel
IS_VERCEL = os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL_ENV') is not None

if IS_VERCEL:
    print("🚀 Ejecutando en Vercel - Usando almacenamiento temporal")
    DATOS_FOLDER, UPLOAD_FOLDER = setup_vercel_storage()
else:
    print("💻 Ejecutando en local - Usando almacenamiento persistente")
    DATOS_FOLDER = os.path.join(os.getcwd(), 'datos')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'musica')
