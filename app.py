# -*- coding: utf-8 -*-
"""
Aplicación web Flask para AQUIFY
Servidor principal con API REST
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__, 
            template_folder='web/templates',
            static_folder='web/static')
CORS(app)

# Configuración
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'musica')
app.config['DATOS_FOLDER'] = os.path.join(os.getcwd(), 'datos')
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}

# Asegurar que existen los directorios
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DATOS_FOLDER'], exist_ok=True)

# Archivos de datos
USUARIO_FILE = os.path.join(app.config['DATOS_FOLDER'], 'usuario.json')
PLAYLIST_FILE = os.path.join(app.config['DATOS_FOLDER'], 'playlist.json')

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cargar_json(archivo, default=None):
    """Carga un archivo JSON"""
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default if default is not None else {}
    return default if default is not None else {}

def guardar_json(archivo, datos):
    """Guarda datos en un archivo JSON"""
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

# Datos de rutinas por tipo de piel
RUTINAS_PIEL = {
    'Normal': {
        'rutina': [
            "Enjuaga tu cuerpo con agua tibia (1 min)",
            "Aplica gel de baño suave con movimientos circulares (2-3 min)",
            "Enjuaga completamente (1 min)",
            "Hidrata la piel después del baño (2 min)"
        ],
        'tiempo_total': 7,
        'consejos': [
            "Usa agua tibia, no muy caliente",
            "Seca con palmaditas, no frotes",
            "Aplica crema hidratante mientras la piel está húmeda"
        ]
    },
    'Seca': {
        'rutina': [
            "Enjuaga con agua tibia (1 min)",
            "Usa gel de baño hidratante con aceites naturales (3-4 min)",
            "Enjuaga suavemente (1 min)",
            "Aplica aceite corporal o crema muy hidratante (3 min)"
        ],
        'tiempo_total': 9,
        'consejos': [
            "Evita agua muy caliente que reseca la piel",
            "Usa productos con glicerina, aceite de coco o manteca de karité",
            "Hidrata inmediatamente después del baño"
        ]
    },
    'Mixta': {
        'rutina': [
            "Enjuaga con agua tibia (1 min)",
            "Aplica gel balanceador en todo el cuerpo (2-3 min)",
            "Usa exfoliante suave en zonas grasas 2 veces por semana (2 min)",
            "Enjuaga completamente (1 min)",
            "Hidratante ligero en zonas secas (2 min)"
        ],
        'tiempo_total': 8,
        'consejos': [
            "Balancea productos según la zona del cuerpo",
            "No uses productos muy pesados"
        ]
    },
    'Grasa': {
        'rutina': [
            "Enjuaga con agua tibia-fresca (1 min)",
            "Usa gel purificante o con ácido salicílico (2-3 min)",
            "Exfolia suavemente 2-3 veces por semana (2 min)",
            "Enjuaga con agua fresca (1 min)",
            "Aplica loción oil-free ligera (1-2 min)"
        ],
        'tiempo_total': 7,
        'consejos': [
            "Usa productos libres de aceite (oil-free)",
            "No exfolies en exceso",
            "El agua fría ayuda a cerrar los poros"
        ]
    },
    'Sensible': {
        'rutina': [
            "Enjuaga con agua tibia (no caliente) (1 min)",
            "Usa gel hipoalergénico sin fragancias (2-3 min)",
            "Enjuaga muy bien para eliminar residuos (2 min)",
            "Seca con palmaditas suaves (1 min)",
            "Aplica crema calmante hipoalergénica (2 min)"
        ],
        'tiempo_total': 8,
        'consejos': [
            "Evita productos con fragancias o colorantes",
            "No uses esponjas ásperas",
            "Busca productos con aloe vera o caléndula"
        ]
    },
    'No sé': {
        'rutina': [
            "Enjuaga con agua tibia (1 min)",
            "Aplica gel de baño suave (2-3 min)",
            "Enjuaga bien (1 min)",
            "Hidrata después del baño (2 min)"
        ],
        'tiempo_total': 7,
        'consejos': [
            "Observa cómo reacciona tu piel",
            "Consulta a un dermatólogo para identificar tu tipo"
        ]
    }
}

# ============ RUTAS WEB ============

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

# ============ API - USUARIO ============

@app.route('/api/usuario', methods=['GET'])
def obtener_usuario():
    """Obtiene el perfil del usuario"""
    usuario = cargar_json(USUARIO_FILE, None)
    if usuario:
        return jsonify({'success': True, 'usuario': usuario})
    return jsonify({'success': False, 'message': 'No hay perfil creado'})

@app.route('/api/usuario', methods=['POST'])
def crear_usuario():
    """Crea o actualiza el perfil del usuario"""
    data = request.json
    
    usuario = {
        'genero': data.get('genero'),
        'genero_personalizado': data.get('genero_personalizado'),
        'pronombres': data.get('pronombres'),
        'edad': data.get('edad'),
        'tipo_piel': data.get('tipo_piel'),
        'fecha_creacion': datetime.now().isoformat()
    }
    
    if guardar_json(USUARIO_FILE, usuario):
        return jsonify({'success': True, 'message': 'Perfil creado exitosamente'})
    return jsonify({'success': False, 'message': 'Error al guardar perfil'})

# ============ API - MÚSICA ============

@app.route('/api/canciones', methods=['GET'])
def obtener_canciones():
    """Obtiene la lista de canciones"""
    playlist = cargar_json(PLAYLIST_FILE, [])
    return jsonify({'success': True, 'canciones': playlist})

@app.route('/api/canciones/subir', methods=['POST'])
def subir_cancion():
    """Sube un archivo de música"""
    if 'archivo' not in request.files:
        return jsonify({'success': False, 'message': 'No se envió archivo'})
    
    archivo = request.files['archivo']
    
    if archivo.filename == '':
        return jsonify({'success': False, 'message': 'No se seleccionó archivo'})
    
    if archivo and allowed_file(archivo.filename):
        filename = secure_filename(archivo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Guardar archivo
        archivo.save(filepath)
        
        # Actualizar playlist
        playlist = cargar_json(PLAYLIST_FILE, [])
        
        cancion = {
            'id': len(playlist) + 1,
            'nombre': Path(filename).stem,
            'archivo': filename,
            'ruta': filepath,
            'fecha_agregada': datetime.now().isoformat()
        }
        
        playlist.append(cancion)
        guardar_json(PLAYLIST_FILE, playlist)
        
        return jsonify({'success': True, 'message': 'Canción agregada exitosamente', 'cancion': cancion})
    
    return jsonify({'success': False, 'message': 'Formato de archivo no permitido'})

@app.route('/api/canciones/<int:id>', methods=['DELETE'])
def eliminar_cancion(id):
    """Elimina una canción"""
    playlist = cargar_json(PLAYLIST_FILE, [])
    
    cancion_encontrada = None
    for i, cancion in enumerate(playlist):
        if cancion.get('id') == id:
            cancion_encontrada = playlist.pop(i)
            break
    
    if cancion_encontrada:
        # Eliminar archivo
        if os.path.exists(cancion_encontrada['ruta']):
            os.remove(cancion_encontrada['ruta'])
        
        guardar_json(PLAYLIST_FILE, playlist)
        return jsonify({'success': True, 'message': 'Canción eliminada'})
    
    return jsonify({'success': False, 'message': 'Canción no encontrada'})

@app.route('/musica/<filename>')
def servir_musica(filename):
    """Sirve archivos de música"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ============ API - CHATBOT ============

@app.route('/api/chatbot/rutina', methods=['GET'])
def obtener_rutina():
    """Obtiene la rutina según el tipo de piel del usuario"""
    usuario = cargar_json(USUARIO_FILE, None)
    
    if not usuario:
        return jsonify({'success': False, 'message': 'Debes crear un perfil primero'})
    
    tipo_piel = usuario.get('tipo_piel', 'Normal')
    rutina = RUTINAS_PIEL.get(tipo_piel, RUTINAS_PIEL['Normal'])
    
    return jsonify({'success': True, 'rutina': rutina, 'tipo_piel': tipo_piel})

@app.route('/api/chatbot/consejos', methods=['GET'])
def obtener_consejos():
    """Obtiene consejos según el tipo de piel"""
    usuario = cargar_json(USUARIO_FILE, None)
    
    if not usuario:
        return jsonify({'success': False, 'message': 'Debes crear un perfil primero'})
    
    tipo_piel = usuario.get('tipo_piel', 'Normal')
    rutina = RUTINAS_PIEL.get(tipo_piel, RUTINAS_PIEL['Normal'])
    
    return jsonify({
        'success': True, 
        'consejos': rutina['consejos'],
        'tipo_piel': tipo_piel
    })

@app.route('/api/chatbot/recomendaciones-musica', methods=['GET'])
def obtener_recomendaciones_musica():
    """Obtiene recomendaciones de música"""
    recomendaciones = [
        "Música relajante instrumental",
        "Lo-fi hip hop para estudiar/relajarse",
        "Sonidos de la naturaleza (lluvia, olas)",
        "Música clásica suave (Debussy, Chopin)",
        "Chill pop acústico",
        "Jazz suave",
        "Música ambient/atmospheric",
        "Indie folk tranquilo"
    ]
    
    return jsonify({'success': True, 'recomendaciones': recomendaciones})

# ============ EJECUTAR SERVIDOR ============

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎵 AQUIFY - Servidor Web Iniciado 💧")
    print("="*60)
    print("\n📍 Accede a la aplicación en:")
    print("   http://localhost:5000")
    print("   http://127.0.0.1:5000")
    print("\n🌐 Para acceder desde otros dispositivos en tu red:")
    print("   http://<tu-ip-local>:5000")
    print("\n⏹️  Presiona Ctrl+C para detener el servidor")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
