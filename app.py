# -*- coding: utf-8 -*-
"""
Aplicación web Flask para AQUIFY
Servidor principal con API REST
"""

from flask import Flask, render_template, request, jsonify, send_from_directory, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from pathlib import Path
import secrets
import re
import requests
from urllib.parse import quote_plus

app = Flask(__name__, 
            template_folder='web/templates',
            static_folder='web/static')
CORS(app, supports_credentials=True)

# Clave secreta para sesiones
app.secret_key = secrets.token_hex(32)

# Configuración - Detectar si estamos en Vercel
IS_VERCEL = os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL_ENV') is not None

if IS_VERCEL:
    # En Vercel, usar almacenamiento temporal
    import tempfile
    tmp_dir = tempfile.gettempdir()
    app.config['UPLOAD_FOLDER'] = os.path.join(tmp_dir, 'aquify_musica')
    app.config['DATOS_FOLDER'] = os.path.join(tmp_dir, 'aquify_datos')
else:
    # En local, usar carpetas normales
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'musica')
    app.config['DATOS_FOLDER'] = os.path.join(os.getcwd(), 'datos')

# Configuración general
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}

# Asegurar que existen los directorios
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DATOS_FOLDER'], exist_ok=True)

def get_user_id():
    """Obtiene o crea un ID único para cada usuario"""
    if 'user_id' not in session:
        session['user_id'] = secrets.token_hex(16)
    return session['user_id']

def get_user_file(filename):
    """Obtiene la ruta del archivo específico del usuario"""
    user_id = get_user_id()
    user_dir = os.path.join(app.config['DATOS_FOLDER'], user_id)
    os.makedirs(user_dir, exist_ok=True)
    return os.path.join(user_dir, filename)

def get_user_music_dir():
    """Obtiene el directorio de música del usuario"""
    user_id = get_user_id()
    music_dir = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    os.makedirs(music_dir, exist_ok=True)
    return music_dir

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
        # Asegurar que el directorio existe
        directorio = os.path.dirname(archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error al guardar JSON {archivo}: {str(e)}")
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
    usuario_file = get_user_file('usuario.json')
    usuario = cargar_json(usuario_file, None)
    if usuario:
        return jsonify({'success': True, 'usuario': usuario})
    return jsonify({'success': False, 'message': 'No hay perfil creado'})

@app.route('/api/usuario', methods=['POST'])
def crear_usuario():
    """Crea o actualiza el perfil del usuario"""
    try:
        data = request.json
        
        # Asegurar que exista el directorio del usuario
        user_id = get_user_id()
        usuario_file = get_user_file('usuario.json')
        
        usuario = {
            'genero': data.get('genero'),
            'genero_personalizado': data.get('genero_personalizado'),
            'pronombres': data.get('pronombres'),
            'edad': data.get('edad'),
            'tipo_piel': data.get('tipo_piel'),
            'fecha_creacion': datetime.now().isoformat(),
            'user_id': user_id
        }
        
        # Guardar perfil
        if guardar_json(usuario_file, usuario):
            return jsonify({
                'success': True, 
                'message': 'Perfil creado exitosamente', 
                'usuario': usuario
            })
        else:
            return jsonify({
                'success': False, 
                'message': 'Error al escribir el archivo'
            })
            
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error al guardar perfil: {str(e)}'
        })

# ============ API - MÚSICA ============

@app.route('/api/canciones', methods=['GET'])
def obtener_canciones():
    """Obtiene la lista de canciones"""
    playlist_file = get_user_file('playlist.json')
    playlist = cargar_json(playlist_file, [])
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
        user_music_dir = get_user_music_dir()
        filepath = os.path.join(user_music_dir, filename)
        
        # Guardar archivo
        archivo.save(filepath)
        
        # Actualizar playlist
        playlist_file = get_user_file('playlist.json')
        playlist = cargar_json(playlist_file, [])
        
        cancion = {
            'id': len(playlist) + 1,
            'nombre': Path(filename).stem,
            'archivo': filename,
            'ruta': filepath,
            'fecha_agregada': datetime.now().isoformat()
        }
        
        playlist.append(cancion)
        guardar_json(playlist_file, playlist)
        
        return jsonify({'success': True, 'message': 'Canción agregada exitosamente', 'cancion': cancion})
    
    return jsonify({'success': False, 'message': 'Formato de archivo no permitido'})

@app.route('/api/canciones/<int:id>', methods=['DELETE'])
def eliminar_cancion(id):
    """Elimina una canción"""
    playlist_file = get_user_file('playlist.json')
    playlist = cargar_json(playlist_file, [])
    
    cancion_encontrada = None
    for i, cancion in enumerate(playlist):
        if cancion.get('id') == id:
            cancion_encontrada = playlist.pop(i)
            break
    
    if cancion_encontrada:
        # Eliminar archivo
        if os.path.exists(cancion_encontrada['ruta']):
            os.remove(cancion_encontrada['ruta'])
        
        guardar_json(playlist_file, playlist)
        return jsonify({'success': True, 'message': 'Canción eliminada'})
    
    return jsonify({'success': False, 'message': 'Canción no encontrada'})

@app.route('/musica/<filename>')
def servir_musica(filename):
    """Sirve archivos de música"""
    user_music_dir = get_user_music_dir()
    return send_from_directory(user_music_dir, filename)

# ============ API - CHATBOT ============

@app.route('/api/chatbot/rutina', methods=['GET'])
def obtener_rutina():
    """Obtiene la rutina según el tipo de piel del usuario"""
    usuario_file = get_user_file('usuario.json')
    usuario = cargar_json(usuario_file, None)
    
    if not usuario:
        return jsonify({'success': False, 'message': 'Debes crear un perfil primero'})
    
    tipo_piel = usuario.get('tipo_piel', 'Normal')
    rutina = RUTINAS_PIEL.get(tipo_piel, RUTINAS_PIEL['Normal'])
    
    return jsonify({'success': True, 'rutina': rutina, 'tipo_piel': tipo_piel})

@app.route('/api/chatbot/consejos', methods=['GET'])
def obtener_consejos():
    """Obtiene consejos según el tipo de piel"""
    usuario_file = get_user_file('usuario.json')
    usuario = cargar_json(usuario_file, None)
    
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

# ============ API - CHATBOT INTERACTIVO ============

# Base de conocimiento del chatbot
CONOCIMIENTO_BASE = {
    'saludos': {
        'patrones': ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'hey', 'saludos', 'qué tal', 'cómo estás'],
        'respuestas': [
            '¡Hola! 👋 Soy el asistente de AQUIFY. ¿En qué puedo ayudarte hoy?',
            '¡Hola! 💧 ¿Necesitas ayuda con tu rutina de ducha o productos para el cuidado de la piel?',
            '¡Buenos días! 🎵 Estoy aquí para ayudarte con rutinas, productos y música para tu ducha.'
        ]
    },
    'funciones': {
        'patrones': ['qué puedes hacer', 'funciones', 'ayuda', 'cómo funciona', 'para qué sirves', 'características'],
        'respuesta': '''¡Puedo ayudarte con muchas cosas! 🌟

📋 **Funcionalidades de AQUIFY:**
• Ver tu rutina de ducha personalizada según tu tipo de piel
• Obtener consejos de cuidado de la piel
• Recomendarte productos adecuados para tu perfil
• Sugerirte rutinas de famosos y celebridades
• Ayudarte a editar y personalizar tu rutina
• Recomendar música perfecta para tu ducha
• Buscar canciones de artistas específicos para tu rutina
• Responder preguntas sobre cuidado de la piel basadas en fuentes confiables

¿Qué te gustaría hacer?'''
    },
    'despedida': {
        'patrones': ['adiós', 'chao', 'hasta luego', 'bye', 'nos vemos', 'gracias'],
        'respuestas': [
            '¡Hasta luego! 👋 ¡Que disfrutes tu ducha! 💧',
            '¡Adiós! 🎵 Vuelve cuando necesites ayuda con tu rutina.',
            '¡Nos vemos! ✨ ¡Cuida tu piel!'
        ]
    }
}

# Rutinas de famosos/celebridades (basadas en rutinas reales compartidas públicamente)
RUTINAS_FAMOSOS = {
    'miranda kerr': {
        'nombre': 'Miranda Kerr',
        'profesion': 'Modelo',
        'tipo_piel': ['Normal', 'Seca'],
        'rutina': [
            'Agua tibia para abrir los poros',
            'Limpiador suave con aceite de rosa mosqueta',
            'Exfoliación ligera 2 veces por semana',
            'Masaje facial con aceite de coco',
            'Enjuague con agua fría para cerrar poros'
        ],
        'productos': ['Aceite de rosa mosqueta', 'Aceite de coco orgánico', 'Limpiador natural'],
        'tiempo': 10,
        'filosofia': 'Enfoque en ingredientes naturales y orgánicos'
    },
    'hailey bieber': {
        'nombre': 'Hailey Bieber',
        'profesion': 'Modelo',
        'tipo_piel': ['Normal', 'Mixta'],
        'rutina': [
            'Doble limpieza (aceite + gel)',
            'Agua tibia constante',
            'Sérum de ácido hialurónico en piel húmeda',
            'Hidratación intensiva',
            'Protector solar si es de día'
        ],
        'productos': ['Limpiador con aceite', 'Gel limpiador', 'Ácido hialurónico', 'Crema hidratante'],
        'tiempo': 8,
        'filosofia': 'Glazed donut skin - hidratación profunda'
    },
    'jennie kim': {
        'nombre': 'Jennie Kim (BLACKPINK)',
        'profesion': 'Artista K-Pop',
        'tipo_piel': ['Normal', 'Sensible'],
        'rutina': [
            'Limpieza con espuma suave',
            'Tónico hidratante',
            'Esencia facial',
            'Crema hidratante ligera',
            'Mascarilla de hidrogel 2 veces por semana'
        ],
        'productos': ['Limpiador de espuma', 'Tónico coreano', 'Esencia', 'Crema gel'],
        'tiempo': 12,
        'filosofia': 'Rutina coreana de 10 pasos - hidratación en capas'
    },
    'zendaya': {
        'nombre': 'Zendaya',
        'profesion': 'Actriz',
        'tipo_piel': ['Normal', 'Mixta'],
        'rutina': [
            'Limpieza suave sin sulfatos',
            'Exfoliación química semanal',
            'Hidratación profunda',
            'Aceites naturales para el cuerpo',
            'Agua fría al final'
        ],
        'productos': ['Limpiador sin sulfatos', 'Exfoliante AHA/BHA', 'Manteca de karité', 'Aceite de jojoba'],
        'tiempo': 9,
        'filosofia': 'Productos limpios y naturales'
    },
    'rihanna': {
        'nombre': 'Rihanna',
        'profesion': 'Empresaria/Artista',
        'tipo_piel': ['Normal', 'Grasa'],
        'rutina': [
            'Limpieza profunda mañana y noche',
            'Tónico balanceador',
            'Sérum de vitamina C',
            'Hidratante ligero oil-free',
            'SPF 50 religiosamente'
        ],
        'productos': ['Fenty Skin cleanser', 'Tónico con niacinamida', 'Vitamina C', 'Hidratante gel'],
        'tiempo': 7,
        'filosofia': 'Piel saludable = mejor maquillaje'
    },
    'gwyneth paltrow': {
        'nombre': 'Gwyneth Paltrow',
        'profesion': 'Actriz/Empresaria',
        'tipo_piel': ['Seca', 'Sensible'],
        'rutina': [
            'Limpieza con aceite limpiador',
            'Agua termal como tónico',
            'Sérum antioxidante',
            'Crema rica en péptidos',
            'Aceite facial de noche'
        ],
        'productos': ['Aceite limpiador', 'Agua termal', 'Sérum con vitamina E', 'Crema de péptidos'],
        'tiempo': 11,
        'filosofia': 'Clean beauty - ingredientes puros y sostenibles'
    },
    'pharrell williams': {
        'nombre': 'Pharrell Williams',
        'profesion': 'Músico/Empresario',
        'tipo_piel': ['Normal', 'Grasa'],
        'rutina': [
            'Limpiador exfoliante diario',
            'Tónico con ácido salicílico',
            'Sérum de retinol por la noche',
            'Hidratante con SPF de día',
            'Agua muy fría al finalizar'
        ],
        'productos': ['Limpiador exfoliante', 'Ácido salicílico', 'Retinol', 'Humanrace skincare'],
        'tiempo': 8,
        'filosofia': 'Cuidado preventivo y anti-edad'
    },
    'kim kardashian': {
        'nombre': 'Kim Kardashian',
        'profesion': 'Empresaria',
        'tipo_piel': ['Grasa', 'Mixta'],
        'rutina': [
            'Doble limpieza profunda',
            'Exfoliación 3 veces por semana',
            'Tónico equilibrante',
            'Suero hidratante',
            'Crema con SPF siempre'
        ],
        'productos': ['Aceite limpiador', 'Exfoliante enzimático', 'Tónico', 'Ácido hialurónico'],
        'tiempo': 10,
        'filosofia': 'Consistencia y protección solar extrema'
    },
    'rosie huntington whiteley': {
        'nombre': 'Rosie Huntington-Whiteley',
        'profesion': 'Modelo/Empresaria',
        'tipo_piel': ['Seca', 'Normal'],
        'rutina': [
            'Limpieza con bálsamo desmaquillante',
            'Segunda limpieza con espuma suave',
            'Esencia hidratante',
            'Sérum facial',
            'Crema rica en la noche'
        ],
        'productos': ['Bálsamo limpiador', 'Espuma suave', 'Esencia', 'Sérum con ácidos'],
        'tiempo': 12,
        'filosofia': 'Hidratación en capas - skin first'
    },
    'priyanka chopra': {
        'nombre': 'Priyanka Chopra',
        'profesion': 'Actriz',
        'tipo_piel': ['Normal', 'Mixta'],
        'rutina': [
            'Limpieza con ingredientes naturales',
            'Tónico de agua de rosas',
            'Aceite de coco en el cuerpo',
            'Hidratante con cúrcuma',
            'Mascarillas semanales con miel'
        ],
        'productos': ['Limpiador ayurvédico', 'Agua de rosas', 'Aceite de coco', 'Cúrcuma'],
        'tiempo': 9,
        'filosofia': 'Remedios tradicionales indios y naturales'
    },
    'david beckham': {
        'nombre': 'David Beckham',
        'profesion': 'Deportista/Empresario',
        'tipo_piel': ['Normal', 'Grasa'],
        'rutina': [
            'Limpiador facial energizante',
            'Exfoliación 2 veces por semana',
            'Tónico refrescante',
            'Hidratante ligero con SPF',
            'Contorno de ojos'
        ],
        'productos': ['Limpiador energizante', 'Exfoliante físico', 'Tónico', 'House 99 products'],
        'tiempo': 6,
        'filosofia': 'Rutina simple pero efectiva para hombres'
    },
    'victoria beckham': {
        'nombre': 'Victoria Beckham',
        'profesion': 'Diseñadora',
        'tipo_piel': ['Seca', 'Sensible'],
        'rutina': [
            'Limpieza ultra suave',
            'Sérum de ácido hialurónico',
            'Crema de células madre',
            'Aceites faciales premium',
            'SPF alto todos los días'
        ],
        'productos': ['Limpiador suave', 'Ácido hialurónico', 'Crema de lujo', 'Aceite facial'],
        'tiempo': 15,
        'filosofia': 'Productos de alta gama y tratamientos profesionales'
    },
    'chrissy teigen': {
        'nombre': 'Chrissy Teigen',
        'profesion': 'Modelo',
        'tipo_piel': ['Normal', 'Mixta'],
        'rutina': [
            'Limpieza doble siempre',
            'Tónico calmante',
            'Mascarilla de arcilla 1 vez/semana',
            'Hidratante ligera',
            'Parches de hidrogel para ojos'
        ],
        'productos': ['Aceite limpiador', 'Gel limpiador', 'Tónico', 'Mascarilla de arcilla'],
        'tiempo': 10,
        'filosofia': 'Cuidado accesible pero efectivo'
    },
    'selena gomez': {
        'nombre': 'Selena Gomez',
        'profesion': 'Artista/Empresaria',
        'tipo_piel': ['Sensible', 'Mixta'],
        'rutina': [
            'Limpiador suave sin fragancia',
            'Tónico calmante',
            'Sérum con niacinamida',
            'Hidratante para piel sensible',
            'Rare Beauty skincare'
        ],
        'productos': ['Limpiador gentil', 'Tónico sin alcohol', 'Niacinamida', 'Crema calmante'],
        'tiempo': 8,
        'filosofia': 'Autoaceptación y cuidado gentil'
    },
    'harry styles': {
        'nombre': 'Harry Styles',
        'profesion': 'Músico/Actor',
        'tipo_piel': ['Normal'],
        'rutina': [
            'Limpiador facial suave',
            'Agua fría para refrescar',
            'Hidratante ligero',
            'Bálsamo labial siempre',
            'SPF cuando está de gira'
        ],
        'productos': ['Limpiador suave', 'Hidratante Aesop', 'Bálsamo labial', 'SPF'],
        'tiempo': 5,
        'filosofia': 'Natural y relajado - menos es más'
    }
}

# Productos recomendados por tipo de piel# Productos recomendados por tipo de piel
PRODUCTOS_RECOMENDADOS = {
    'Normal': {
        'limpiadores': ['CeraVe Hydrating Cleanser', 'Neutrogena Hydro Boost', 'La Roche-Posay Toleriane'],
        'hidratantes': ['Cetaphil Daily Hydrating Lotion', 'Eucerin Original Healing Cream', 'Aveeno Daily Moisturizing'],
        'especiales': ['The Ordinary Niacinamide', 'Paula\'s Choice BHA']
    },
    'Seca': {
        'limpiadores': ['CeraVe Cream-to-Foam Cleanser', 'Dove Beauty Bar', 'Eucerin Advanced Cleansing Body'],
        'hidratantes': ['La Roche-Posay Lipikar Balm', 'Eucerin Advanced Repair', 'Aveeno Eczema Therapy'],
        'especiales': ['Aceite de jojoba', 'Manteca de karité', 'Ácido hialurónico']
    },
    'Grasa': {
        'limpiadores': ['CeraVe Foaming Facial Cleanser', 'Neutrogena Oil-Free Acne Wash', 'La Roche-Posay Effaclar'],
        'hidratantes': ['Neutrogena Hydro Boost Water Gel', 'CeraVe PM Facial Moisturizing Lotion', 'La Roche-Posay Effaclar Mat'],
        'especiales': ['Ácido salicílico', 'Niacinamida', 'Té verde']
    },
    'Mixta': {
        'limpiadores': ['CeraVe Foaming Facial Cleanser', 'Neutrogena Deep Clean', 'Bioderma Sensibio'],
        'hidratantes': ['Neutrogena Hydro Boost Gel', 'The Ordinary Natural Moisturizing Factors', 'Clinique Dramatically Different Gel'],
        'especiales': ['Niacinamida', 'Ácido hialurónico', 'Té verde']
    },
    'Sensible': {
        'limpiadores': ['La Roche-Posay Toleriane', 'CeraVe Hydrating Cleanser', 'Vanicream Gentle Cleanser'],
        'hidratantes': ['CeraVe Moisturizing Cream', 'La Roche-Posay Cicaplast Baume', 'Eucerin Sensitive Skin'],
        'especiales': ['Centella asiática', 'Avena coloidal', 'Aloe vera']
    }
}

# Géneros musicales por tipo de rutina
MUSICA_POR_RUTINA = {
    'relajante': ['Lo-fi', 'Ambient', 'Jazz suave', 'Bossa nova', 'Música clásica'],
    'energizante': ['Pop', 'Indie pop', 'Electrónica chill', 'R&B moderno'],
    'rapida': ['Indie rock', 'Pop rock', 'Electrónica upbeat'],
    'larga': ['Playlists ambient', 'Música instrumental', 'Soundtracks']
}

def clasificar_intencion(mensaje):
    """Clasifica la intención del usuario"""
    mensaje = mensaje.lower().strip()
    
    # Saludos
    if any(patron in mensaje for patron in CONOCIMIENTO_BASE['saludos']['patrones']):
        return 'saludo'
    
    # Despedidas
    if any(patron in mensaje for patron in CONOCIMIENTO_BASE['despedida']['patrones']):
        return 'despedida'
    
    # Funciones de la app
    if any(patron in mensaje for patron in CONOCIMIENTO_BASE['funciones']['patrones']):
        return 'funciones'
    
    # Rutinas de famosos recomendadas para mi perfil (debe ir ANTES de rutina_famoso general)
    if any(palabra in mensaje for palabra in ['recomiendas según', 'para mi perfil', 'para mí según', 'me sirven según', 'adecuados para mí', 'según mi piel', 'me convienen']):
        return 'rutina_famoso_recomendada'
    
    if 'qué famosos' in mensaje and ('mi' in mensaje or 'perfil' in mensaje or 'piel' in mensaje):
        return 'rutina_famoso_recomendada'
    
    if 'cuáles famosos' in mensaje and ('mi' in mensaje or 'perfil' in mensaje or 'piel' in mensaje):
        return 'rutina_famoso_recomendada'
    
    # Rutinas de famosos (general)
    if any(palabra in mensaje for palabra in ['famoso', 'celebridad', 'celebrity', 'estrella', 'artista famoso']):
        return 'rutina_famoso'
    
    # Rutina personalizada
    if any(palabra in mensaje for palabra in ['mi rutina', 'rutina', 'pasos', 'qué debo hacer']):
        return 'rutina'
    
    # Editar rutina
    if any(palabra in mensaje for palabra in ['editar', 'modificar', 'cambiar', 'personalizar']) and 'rutina' in mensaje:
        return 'editar_rutina'
    
    # Productos
    if any(palabra in mensaje for palabra in ['producto', 'crema', 'limpiador', 'hidratante', 'recomienda', 'recomendación']):
        return 'productos'
    
    # Música
    if any(palabra in mensaje for palabra in ['música', 'canción', 'canciones', 'playlist', 'artista', 'cantante']):
        return 'musica'
    
    # Búsqueda general (temas de piel y cuidado)
    if any(palabra in mensaje for palabra in ['piel', 'cuidado', 'acné', 'arrugas', 'manchas', 'dermatitis', 'eczema', 'psoriasis', 'rosácea']):
        return 'busqueda_salud'
    
    return 'desconocido'

def recomendar_famosos_por_perfil(tipo_piel):
    """Recomienda rutinas de famosos basándose en el tipo de piel del usuario"""
    recomendaciones = []
    
    for key, famoso in RUTINAS_FAMOSOS.items():
        if tipo_piel in famoso['tipo_piel']:
            recomendaciones.append(famoso)
    
    return recomendaciones

def extraer_nombre_famoso(mensaje):
    """Extrae el nombre del famoso del mensaje"""
    mensaje = mensaje.lower()
    for nombre in RUTINAS_FAMOSOS.keys():
        if nombre in mensaje:
            return nombre
    return None

def extraer_artista(mensaje):
    """Extrae el nombre del artista del mensaje"""
    # Patrones comunes
    patrones = [
        r'canciones de (.+)',
        r'música de (.+)',
        r'artista (.+)',
        r'cantante (.+)',
        r'de (.+)',
    ]
    
    for patron in patrones:
        match = re.search(patron, mensaje.lower())
        if match:
            return match.group(1).strip()
    return None

def buscar_en_google(query):
    """Busca información en Google (simulado - solo devuelve fuentes confiables)"""
    # Fuentes confiables autorizadas
    fuentes_confiables = [
        'mayoclinic.org',
        'aad.org',  # American Academy of Dermatology
        'who.int',  # World Health Organization
        'nih.gov',  # National Institutes of Health
        'healthline.com',
        'webmd.com',
        'medlineplus.gov',
        'cdc.gov'
    ]
    
    # Nota: En producción, usarías una API real de búsqueda
    # Por ahora, devolvemos información educativa general
    respuesta = f'''He encontrado información sobre "{query}" de fuentes confiables:

📚 **Recomendaciones generales:**
• Consulta siempre con un dermatólogo para problemas específicos
• Usa productos adecuados para tu tipo de piel
• Mantén una rutina consistente de limpieza e hidratación
• Protege tu piel del sol diariamente

🔍 **Fuentes confiables recomendadas:**
• American Academy of Dermatology (aad.org)
• Mayo Clinic (mayoclinic.org)
• National Institutes of Health (nih.gov)

Para información más específica sobre tu consulta, te recomiendo visitar estos sitios oficiales.'''
    
    return respuesta

@app.route('/api/chatbot/mensaje', methods=['POST'])
def procesar_mensaje_chatbot():
    """Procesa mensajes del chatbot interactivo"""
    data = request.json
    mensaje = data.get('mensaje', '').strip()
    
    if not mensaje:
        return jsonify({'success': False, 'message': 'Mensaje vacío'})
    
    # Obtener perfil del usuario
    usuario_file = get_user_file('usuario.json')
    usuario = cargar_json(usuario_file, None)
    
    # Clasificar intención
    intencion = clasificar_intencion(mensaje)
    
    respuesta = ''
    datos_extra = {}
    
    if intencion == 'saludo':
        import random
        respuesta = random.choice(CONOCIMIENTO_BASE['saludos']['respuestas'])
    
    elif intencion == 'despedida':
        import random
        respuesta = random.choice(CONOCIMIENTO_BASE['despedida']['respuestas'])
    
    elif intencion == 'funciones':
        respuesta = CONOCIMIENTO_BASE['funciones']['respuesta']
    
    elif intencion == 'rutina':
        if not usuario:
            respuesta = 'Primero necesitas crear tu perfil en la pestaña "Perfil" para que pueda darte una rutina personalizada. 😊'
        else:
            tipo_piel = usuario.get('tipo_piel', 'Normal')
            rutina_info = RUTINAS_PIEL.get(tipo_piel, RUTINAS_PIEL['Normal'])
            
            respuesta = f'''Tu rutina personalizada para piel **{tipo_piel}**: 💧

**Pasos:**
'''
            for i, paso in enumerate(rutina_info['rutina'], 1):
                respuesta += f'{i}. {paso}\n'
            
            respuesta += f'\n⏱️ **Tiempo total:** {rutina_info["tiempo_total"]} minutos\n\n'
            respuesta += '**💡 Consejos:**\n'
            for consejo in rutina_info['consejos']:
                respuesta += f'• {consejo}\n'
            
            datos_extra['rutina'] = rutina_info
    
    elif intencion == 'rutina_famoso_recomendada':
        if not usuario:
            respuesta = '''Primero necesitas crear tu perfil para poder recomendarte rutinas de famosos adecuadas para ti. 😊
            
Ve a la pestaña "Perfil" y completa tu información, especialmente tu tipo de piel.'''
        else:
            tipo_piel = usuario.get('tipo_piel', 'Normal')
            recomendaciones = recomendar_famosos_por_perfil(tipo_piel)
            
            if recomendaciones:
                respuesta = f'''**Rutinas de famosos perfectas para tu piel {tipo_piel}:** ⭐\n\n'''
                
                for famoso in recomendaciones[:5]:  # Máximo 5 recomendaciones
                    respuesta += f'''
**{famoso["nombre"]}** ({famoso["profesion"]})
• Filosofía: {famoso["filosofia"]}
• Tiempo: {famoso["tiempo"]} minutos
• Productos clave: {", ".join(famoso["productos"][:3])}

'''
                
                respuesta += '\n💡 **Tip:** Pregúntame por cualquiera de estos famosos para ver su rutina completa.'
                datos_extra['recomendaciones'] = recomendaciones
            else:
                respuesta = f'No encontré rutinas específicas para piel {tipo_piel}, pero puedo mostrarte todas las rutinas disponibles. ¿Te gustaría verlas?'
    
    elif intencion == 'rutina_famoso':
        nombre_famoso = extraer_nombre_famoso(mensaje)
        
        if nombre_famoso:
            rutina = RUTINAS_FAMOSOS[nombre_famoso]
            respuesta = f'''**Rutina de {rutina["nombre"]}** ({rutina["profesion"]}) ✨

**Filosofía:** {rutina["filosofia"]}
**Tipos de piel recomendados:** {", ".join(rutina["tipo_piel"])}

**Pasos de la rutina:**
'''
            for i, paso in enumerate(rutina['rutina'], 1):
                respuesta += f'{i}. {paso}\n'
            
            respuesta += f'\n⏱️ **Tiempo:** {rutina["tiempo"]} minutos\n\n'
            respuesta += '**Productos que usa:**\n'
            for prod in rutina['productos']:
                respuesta += f'• {prod}\n'
            
            datos_extra['rutina_famoso'] = rutina
        else:
            # Listar todos los famosos disponibles por categoría
            modelos = []
            artistas = []
            empresarios = []
            actores = []
            
            for key, famoso in RUTINAS_FAMOSOS.items():
                profesion = famoso.get('profesion', '')
                nombre = famoso.get('nombre', '')
                
                if 'Modelo' in profesion:
                    modelos.append(nombre)
                elif any(x in profesion for x in ['Artista', 'Músico', 'K-Pop']):
                    artistas.append(nombre)
                elif any(x in profesion for x in ['Empresario', 'Empresaria']):
                    empresarios.append(nombre)
                elif 'Actriz' in profesion or 'Actor' in profesion:
                    actores.append(nombre)
                else:
                    actores.append(nombre)
            
            respuesta = '**Rutinas de celebridades disponibles:** 🌟\n\n'
            
            if modelos:
                respuesta += '**👗 Modelos:**\n'
                for nombre in sorted(modelos):
                    respuesta += f'• {nombre}\n'
                respuesta += '\n'
            
            if artistas:
                respuesta += '**🎵 Artistas/Músicos:**\n'
                for nombre in sorted(artistas):
                    respuesta += f'• {nombre}\n'
                respuesta += '\n'
            
            if empresarios:
                respuesta += '**💼 Empresarios:**\n'
                for nombre in sorted(empresarios):
                    respuesta += f'• {nombre}\n'
                respuesta += '\n'
            
            if actores:
                respuesta += '**🎬 Actores/Otros:**\n'
                for nombre in sorted(actores):
                    respuesta += f'• {nombre}\n'
                respuesta += '\n'
            
            respuesta += '\n💡 **Pregúntame por alguna en específico, por ejemplo:**\n'
            respuesta += '• "¿Cuál es la rutina de Hailey Bieber?"\n'
            respuesta += '• "Rutina de Pharrell Williams"\n'
            respuesta += '• "Muéstrame la rutina de Rihanna"\n'
            respuesta += '• "¿Qué famosos me recomiendas según mi perfil?"\n\n'
            respuesta += f'**Total: {len(RUTINAS_FAMOSOS)} rutinas de celebridades disponibles**'
            
            datos_extra['total_famosos'] = len(RUTINAS_FAMOSOS)
            datos_extra['categorias'] = {
                'modelos': modelos,
                'artistas': artistas,
                'empresarios': empresarios,
                'actores': actores
            }
    
    elif intencion == 'editar_rutina':
        respuesta = '''Para editar tu rutina puedo ayudarte con: 🛠️

1. **Reducir tiempo:** Rutina rápida de 5 minutos
2. **Aumentar tiempo:** Rutina spa de 15+ minutos  
3. **Agregar pasos:** Exfoliación, mascarillas, etc.
4. **Cambiar productos:** Según tu presupuesto o preferencias

¿Qué te gustaría modificar?'''
    
    elif intencion == 'productos':
        if not usuario:
            tipo_piel = 'Normal'
            respuesta = 'Te doy recomendaciones generales. Para productos personalizados, crea tu perfil primero. 😊\n\n'
        else:
            tipo_piel = usuario.get('tipo_piel', 'Normal')
            respuesta = f'**Productos recomendados para piel {tipo_piel}:** 🧴\n\n'
        
        productos = PRODUCTOS_RECOMENDADOS.get(tipo_piel, PRODUCTOS_RECOMENDADOS['Normal'])
        
        respuesta += '**Limpiadores:**\n'
        for prod in productos['limpiadores']:
            respuesta += f'• {prod}\n'
        
        respuesta += '\n**Hidratantes:**\n'
        for prod in productos['hidratantes']:
            respuesta += f'• {prod}\n'
        
        respuesta += '\n**Ingredientes especiales:**\n'
        for prod in productos['especiales']:
            respuesta += f'• {prod}\n'
        
        respuesta += '\n💡 **Tip:** Estos productos están respaldados por dermatólogos y son de marcas confiables.'
        
        datos_extra['productos'] = productos
    
    elif intencion == 'musica':
        artista = extraer_artista(mensaje)
        
        if artista:
            respuesta = f'''🎵 **Canciones de {artista.title()} perfectas para tu ducha:**

Para encontrar canciones específicas de este artista, puedes:
1. Ir a la pestaña "Música"
2. Subir tus canciones favoritas de {artista.title()}
3. Crear tu playlist personalizada

💡 **Tip:** Las canciones relajantes y a tempo medio (60-90 BPM) son ideales para ducharte.'''
        else:
            respuesta = '''🎵 **Recomendaciones de música para tu ducha:**

**Por tipo de rutina:**
• **Relajante:** Lo-fi, Ambient, Jazz suave
• **Energizante:** Pop, Indie pop, R&B moderno
• **Rápida:** Indie rock, Pop rock
• **Larga/Spa:** Playlists ambient, Instrumental

**Artistas recomendados:**
• Billie Eilish (canciones suaves)
• Rex Orange County
• Conan Gray
• Clairo
• Keshi
• JVKE

¿Buscas canciones de algún artista en particular?'''
        
        datos_extra['musica'] = MUSICA_POR_RUTINA
    
    elif intencion == 'busqueda_salud':
        # Buscar información de fuentes confiables
        respuesta = buscar_en_google(mensaje)
        datos_extra['fuentes_confiables'] = True
    
    else:
        respuesta = '''No estoy seguro de cómo ayudarte con eso. 🤔

Puedo ayudarte con:
• Tu rutina de ducha personalizada
• Rutinas de famosos
• Recomendaciones de productos
• Sugerencias de música
• Información sobre cuidado de la piel

¿Qué te gustaría saber?'''
    
    return jsonify({
        'success': True,
        'respuesta': respuesta,
        'intencion': intencion,
        'datos_extra': datos_extra
    })

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
