# AQUIFY 🎵💧

Aplicación web y de terminal para gestionar música durante tus rutinas de baño.

## 🌐 Versión Web (RECOMENDADA)

### Instalación

```bash
# Clonar o descargar el proyecto
cd AQUIFFY

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar en Localhost

```bash
python app.py
```

Luego abre tu navegador en:
- **http://localhost:5000**
- **http://127.0.0.1:5000**

### Acceder desde otros dispositivos

Para acceder desde tu teléfono o tablet en la misma red WiFi:
1. Encuentra tu IP local (ejecuta `ipconfig` en Windows)
2. Abre `http://TU-IP-LOCAL:5000` en el otro dispositivo

## ☁️ Subir a la Nube

Lee la guía completa en **[DEPLOYMENT.md](DEPLOYMENT.md)**

### Opción Rápida: Render (Gratis)

1. Sube tu código a GitHub
2. Ve a https://render.com y crea cuenta
3. Conecta tu repositorio
4. Deploy automático
5. ¡Listo! Accesible desde cualquier parte del mundo

## 💻 Versión Terminal

También incluye una versión de terminal:

```bash
python main.py
```

## Características

- 👤 Creación de perfil de usuario (género, edad, tipo de piel)
- 🎵 Gestión de archivos de música (MP3, WAV, OGG, FLAC, M4A)
- 🤖 Chatbot asistente con rutinas personalizadas
- ⏱️ Temporizador y cronómetro
- 🎼 Reproductor de música con control de tiempo automático
- 🌈 Interfaz web moderna y colorida

## Requisitos

- Python 3.7+
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

## Colores de la aplicación

- Verde primario: #00CC57, #0A8A46
- Verde claro: #BFEFD6, #DFF7EA
- Azul claro: #B4E9FA, #C7EEFA
- Azul primario: #0077C8, #084A6F, #2EB7FF
- Azul muy claro: #E6F9FF
- Blanco/Neutros: #FFFFFF, #FBFCFE, #F3F9FF

## Estructura del Proyecto

```
AQUIFFY/
├── app.py                 # Servidor Flask (WEB)
├── main.py                # Aplicación terminal
├── requirements.txt       # Dependencias
├── Procfile              # Config para deployment
├── Dockerfile            # Config para Docker
├── DEPLOYMENT.md         # Guía de deployment
├── web/
│   ├── static/
│   │   ├── styles.css    # Estilos web
│   │   └── app.js        # JavaScript
│   └── templates/
│       └── index.html    # Página principal
├── src/                  # Módulos Python
├── datos/                # Datos de usuario
└── musica/               # Archivos de música
```

## Licencia

Proyecto educativo - Uso libre
