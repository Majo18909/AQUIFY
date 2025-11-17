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

# Clave secreta para sesiones - usar variable de entorno en producción o generar una fija
app.secret_key = os.environ.get('SECRET_KEY', 'aquify-secret-key-2024-vercel-deployment')

# Configuración - Detectar si estamos en Vercel
IS_VERCEL = os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL_ENV') is not None

if IS_VERCEL:
    # En Vercel, usar almacenamiento temporal y límite de tamaño reducido
    import tempfile
    tmp_dir = tempfile.gettempdir()
    app.config['UPLOAD_FOLDER'] = os.path.join(tmp_dir, 'aquify_musica')
    app.config['DATOS_FOLDER'] = os.path.join(tmp_dir, 'aquify_datos')
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB max en Vercel (límite de payload)
    # Usar cookies más persistentes en Vercel
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = True
    print("🚀 Ejecutando en VERCEL - Límite de archivos: 4MB (límite de Vercel), almacenamiento temporal")
else:
    # En local, usar carpetas normales
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'musica')
    app.config['DATOS_FOLDER'] = os.path.join(os.getcwd(), 'datos')
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max en local
    print("💻 Ejecutando en LOCAL - Límite de archivos: 50MB")

# Configuración general
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}

# CORS debe ir después de la configuración
CORS(app, supports_credentials=True)

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
    try:
        print("\n=== INICIO SUBIDA DE CANCIÓN ===")
        print(f"Request files: {list(request.files.keys())}")
        
        if 'archivo' not in request.files:
            print("ERROR: No se encontró 'archivo' en request.files")
            return jsonify({'success': False, 'message': 'No se envió archivo'})
        
        archivo = request.files['archivo']
        print(f"Archivo recibido: {archivo.filename}")
        
        if archivo.filename == '':
            print("ERROR: Nombre de archivo vacío")
            return jsonify({'success': False, 'message': 'No se seleccionó archivo'})
        
        if archivo and allowed_file(archivo.filename):
            filename = secure_filename(archivo.filename)
            print(f"Filename seguro: {filename}")
            
            user_music_dir = get_user_music_dir()
            print(f"Directorio de música: {user_music_dir}")
            
            # Asegurar que el directorio existe
            os.makedirs(user_music_dir, exist_ok=True)
            
            filepath = os.path.join(user_music_dir, filename)
            print(f"Ruta completa: {filepath}")
            
            # Guardar archivo
            print("Guardando archivo...")
            archivo.save(filepath)
            print(f"✓ Archivo guardado: {os.path.exists(filepath)}")
            
            # Actualizar playlist
            playlist_file = get_user_file('playlist.json')
            playlist = cargar_json(playlist_file, [])
            print(f"Playlist actual tiene {len(playlist)} canciones")
            
            cancion = {
                'id': len(playlist) + 1,
                'nombre': Path(filename).stem,
                'archivo': filename,
                'ruta': filepath,
                'fecha_agregada': datetime.now().isoformat()
            }
            
            playlist.append(cancion)
            print(f"Nueva canción: {cancion['nombre']}")
            
            if guardar_json(playlist_file, playlist):
                print("✓ Playlist guardada exitosamente")
                print("=== FIN SUBIDA DE CANCIÓN ===\n")
                return jsonify({'success': True, 'message': 'Canción agregada exitosamente', 'cancion': cancion})
            else:
                print("ERROR: No se pudo guardar la playlist")
                return jsonify({'success': False, 'message': 'Error al guardar la playlist'})
        
        print(f"ERROR: Formato no permitido: {archivo.filename}")
        return jsonify({'success': False, 'message': 'Formato de archivo no permitido. Usa: MP3, WAV, OGG, FLAC o M4A'})
    
    except Exception as e:
        import traceback
        print(f"\n!!! ERROR CRÍTICO !!!")
        print(f"Error: {str(e)}")
        print(f"Traceback:\n{traceback.format_exc()}")
        print("=== FIN CON ERROR ===\n")
        return jsonify({'success': False, 'message': f'Error al subir archivo: {str(e)}'})

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

# Canciones recomendadas por artista (para ducha/rutinas)
CANCIONES_POR_ARTISTA = {
    'sabrina carpenter': {
        'nombre': 'Sabrina Carpenter',
        'canciones_relajantes': [
            'Skin',
            'Vicious',
            'exhale',
            'decode',
            'opposite'
        ],
        'canciones_energizantes': [
            'Espresso',
            'Feather',
            'Nonsense',
            'Fast Times',
            'because i liked a boy'
        ],
        'genero': 'Pop'
    },
    'billie eilish': {
        'nombre': 'Billie Eilish',
        'canciones_relajantes': [
            'when the party\'s over',
            'idontwannabeyouanymore',
            'ocean eyes',
            'lovely',
            'What Was I Made For?'
        ],
        'canciones_energizantes': [
            'bad guy',
            'Therefore I Am',
            'you should see me in a crown',
            'Happier Than Ever',
            'LUNCH'
        ],
        'genero': 'Alt-Pop'
    },
    'taylor swift': {
        'nombre': 'Taylor Swift',
        'canciones_relajantes': [
            'Lover',
            'Cardigan',
            'Champagne Problems',
            'Snow On The Beach',
            'Sweet Nothing'
        ],
        'canciones_energizantes': [
            'Shake It Off',
            'Anti-Hero',
            'Cruel Summer',
            'ME!',
            'Look What You Made Me Do'
        ],
        'genero': 'Pop'
    },
    'olivia rodrigo': {
        'nombre': 'Olivia Rodrigo',
        'canciones_relajantes': [
            'drivers license',
            'traitor',
            'happier',
            'logical',
            'making the bed'
        ],
        'canciones_energizantes': [
            'good 4 u',
            'brutal',
            'deja vu',
            'bad idea right?',
            'get him back!'
        ],
        'genero': 'Pop Rock'
    },
    'ariana grande': {
        'nombre': 'Ariana Grande',
        'canciones_relajantes': [
            'breathin',
            'just like magic',
            'ghostin',
            'R.E.M',
            'moonlight'
        ],
        'canciones_energizantes': [
            '7 rings',
            'thank u, next',
            'positions',
            'yes, and?',
            'Side To Side'
        ],
        'genero': 'Pop/R&B'
    },
    'gracie abrams': {
        'nombre': 'Gracie Abrams',
        'canciones_relajantes': [
            'I miss you, I\'m sorry',
            'Where do we go now?',
            'Difficult',
            'The blue',
            'Block me out'
        ],
        'canciones_energizantes': [
            'Risk',
            'Close To You',
            'That\'s So True',
            'I Love You, I\'m Sorry',
            'Feel Like Shit'
        ],
        'genero': 'Indie Pop'
    },
    'lana del rey': {
        'nombre': 'Lana Del Rey',
        'canciones_relajantes': [
            'Video Games',
            'Young and Beautiful',
            'Summertime Sadness',
            'Love',
            'hope is a dangerous thing'
        ],
        'canciones_energizantes': [
            'Born To Die',
            'Ride',
            'West Coast',
            'High By The Beach',
            'A&W'
        ],
        'genero': 'Alt-Pop/Indie'
    },
    'the weeknd': {
        'nombre': 'The Weeknd',
        'canciones_relajantes': [
            'Die For You',
            'Earned It',
            'Call Out My Name',
            'Wicked Games',
            'Save Your Tears'
        ],
        'canciones_energizantes': [
            'Blinding Lights',
            'Starboy',
            'Can\'t Feel My Face',
            'The Hills',
            'Popular'
        ],
        'genero': 'R&B/Pop'
    },
    'bad bunny': {
        'nombre': 'Bad Bunny',
        'canciones_relajantes': [
            'Callaíta',
            'La Noche de Anoche',
            'Neverita',
            'Un x100to',
            'Andrea'
        ],
        'canciones_energizantes': [
            'Tití Me Preguntó',
            'Moscow Mule',
            'Yo Perreo Sola',
            'Dakiti',
            'MONACO'
        ],
        'genero': 'Reggaetón/Urbano'
    },
    'sza': {
        'nombre': 'SZA',
        'canciones_relajantes': [
            'The Weekend',
            'Good Days',
            'Drew Barrymore',
            'Snooze',
            'Special'
        ],
        'canciones_energizantes': [
            'Kill Bill',
            'I Hate U',
            'All The Stars',
            'Shirt',
            'Low'
        ],
        'genero': 'R&B/Soul'
    },
    'harry styles': {
        'nombre': 'Harry Styles',
        'canciones_relajantes': [
            'Falling',
            'Matilda',
            'Fine Line',
            'Cherry',
            'Little Freak'
        ],
        'canciones_energizantes': [
            'As It Was',
            'Watermelon Sugar',
            'Adore You',
            'Late Night Talking',
            'Music For a Sushi Restaurant'
        ],
        'genero': 'Pop Rock'
    },
    'bruno mars': {
        'nombre': 'Bruno Mars',
        'canciones_relajantes': [
            'When I Was Your Man',
            'Talking to the Moon',
            'It Will Rain',
            'Versace on the Floor',
            'Leave The Door Open'
        ],
        'canciones_energizantes': [
            'Uptown Funk',
            '24K Magic',
            'Treasure',
            'Locked Out Of Heaven',
            'That\'s What I Like'
        ],
        'genero': 'Pop/R&B/Funk'
    }
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

def extraer_artista(mensaje):
    """Extrae el nombre del artista del mensaje"""
    mensaje = mensaje.lower()
    
    # Primero buscar coincidencias exactas en nuestro diccionario
    for artista_key in CANCIONES_POR_ARTISTA.keys():
        if artista_key in mensaje:
            return artista_key
    
    # Patrones comunes para extraer nombre de artista
    patrones = [
        r'canciones de (.+?)(?:\?|$|para|que)',
        r'música de (.+?)(?:\?|$|para|que)',
        r'sugiere(?:me)? canciones de (.+?)(?:\?|$|para|que)',
        r'recomienda(?:me)? canciones de (.+?)(?:\?|$|para|que)',
        r'artista (.+?)(?:\?|$|para|que)',
        r'cantante (.+?)(?:\?|$|para|que)',
    ]
    
    for patron in patrones:
        match = re.search(patron, mensaje)
        if match:
            artista_extraido = match.group(1).strip()
            # Buscar coincidencia parcial en el diccionario
            for artista_key, data in CANCIONES_POR_ARTISTA.items():
                if artista_key in artista_extraido or artista_extraido in artista_key:
                    return artista_key
            return artista_extraido
    
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
        
        if artista and artista in CANCIONES_POR_ARTISTA:
            # Tenemos canciones específicas de este artista
            artista_info = CANCIONES_POR_ARTISTA[artista]
            
            # Determinar si el usuario quiere música relajante o energizante
            es_relajante = any(palabra in mensaje for palabra in ['relaj', 'calm', 'suave', 'tranquil', 'spa'])
            es_energizante = any(palabra in mensaje for palabra in ['energi', 'activ', 'rápid', 'upbeat', 'mover'])
            
            respuesta = f'''🎵 **Canciones de {artista_info["nombre"]} perfectas para tu ducha:**\n\n'''
            
            # Si no especificaron tipo, mostrar ambas categorías
            if not es_relajante and not es_energizante:
                respuesta += f'**💧 Para rutina relajante/spa (7-10 min):**\n'
                for cancion in artista_info['canciones_relajantes']:
                    respuesta += f'• {cancion}\n'
                
                respuesta += f'\n**⚡ Para rutina energizante/rápida (5-7 min):**\n'
                for cancion in artista_info['canciones_energizantes']:
                    respuesta += f'• {cancion}\n'
            elif es_relajante:
                respuesta += f'**💧 Canciones relajantes perfectas para una rutina spa:**\n'
                for cancion in artista_info['canciones_relajantes']:
                    respuesta += f'• {cancion}\n'
            else:
                respuesta += f'**⚡ Canciones energizantes para empezar el día:**\n'
                for cancion in artista_info['canciones_energizantes']:
                    respuesta += f'• {cancion}\n'
            
            respuesta += f'\n**🎸 Género:** {artista_info["genero"]}\n'
            respuesta += f'\n💡 **Tip:** Puedes subir estas canciones en la pestaña "Música" y crear tu playlist personalizada.'
            
            datos_extra['artista'] = artista_info
        
        elif artista:
            # Artista mencionado pero no está en nuestro diccionario
            respuesta = f'''🎵 **Canciones de {artista.title()}:**

No tengo recomendaciones específicas de este artista en mi base de datos, pero puedes:

1. 🔍 **Buscar en Spotify/YouTube:** "{artista} chill songs" o "{artista} upbeat songs"
2. 📱 **Ir a la pestaña "Música":** Sube tus canciones favoritas
3. 🎧 **Crear tu playlist:** Personalízala para tu rutina

**Artistas similares que tengo:**
• Sabrina Carpenter • Billie Eilish • Taylor Swift
• Olivia Rodrigo • Ariana Grande • The Weeknd
• Harry Styles • SZA • Lana Del Rey

¿Quieres que te sugiera canciones de alguno de estos?'''
        
        else:
            # No mencionaron artista específico
            respuesta = '''🎵 **Recomendaciones de música para tu ducha:**

**Por tipo de rutina:**
• **Relajante:** Lo-fi, Ambient, Jazz suave
• **Energizante:** Pop, Indie pop, R&B moderno
• **Rápida:** Indie rock, Pop rock
• **Larga/Spa:** Playlists ambient, Instrumental

**Artistas disponibles con recomendaciones:**
• 🎤 Sabrina Carpenter • Billie Eilish • Taylor Swift
• 🎵 Olivia Rodrigo • Ariana Grande • Gracie Abrams
• 🎸 Harry Styles • The Weeknd • Lana Del Rey
• 🎹 SZA • Bad Bunny • Bruno Mars

💡 **Pregúntame:** "Canciones de [artista] para mi ducha" 
**Ejemplo:** "Sugiéreme canciones de Sabrina Carpenter"

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
