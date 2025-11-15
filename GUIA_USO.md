# Guía de Uso de AQUIFY

## Instalación

1. Asegúrate de tener Python 3.7+ instalado
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Para iniciar AQUIFY, ejecuta:
```bash
python main.py
```

## Funcionalidades

### 1. Perfil de Usuario
- Crea tu perfil seleccionando género, edad y tipo de piel
- El género puede ser: Hombre, Mujer, Personalizado (con pronombres), o Prefiero no decirlo
- Tipos de piel: Normal, Seca, Mixta, Grasa, Sensible, No sé

### 2. Gestión de Música
- Agrega canciones desde tu computadora
- Formatos soportados: MP3, WAV, OGG, FLAC, M4A
- Visualiza tu playlist
- Elimina canciones que ya no quieras

### 3. Chatbot Asistente
El chatbot te puede ayudar con:
- Información sobre las funciones de la app
- Rutinas de baño especializadas según tu tipo de piel
- Crear rutinas personalizadas paso a paso
- Recomendaciones de géneros musicales
- Consejos específicos para tu tipo de piel

### 4. Reproducir con Rutina
- Selecciona una canción de tu playlist
- El sistema sugiere un tiempo basado en tu tipo de piel
- La música se reproduce en loop
- Se pausa automáticamente cuando el tiempo de rutina termina
- Perfecto para seguir tu rutina de baño sin preocuparte

### 5. Reproducir Música
- Reproduce canciones sin temporizador
- Modo libre para escuchar música mientras te bañas

### 6. Temporizador
- Configura un temporizador en minutos
- Útil para controlar el tiempo de tu baño

### 7. Cronómetro
- Mide el tiempo de actividades específicas
- Se detiene con Ctrl+C

## Tiempos de Rutina por Tipo de Piel

- **Normal**: 7 minutos
- **Seca**: 9 minutos
- **Mixta**: 8 minutos
- **Grasa**: 7 minutos
- **Sensible**: 8 minutos
- **No sé**: 7 minutos

## Consejos de Uso

1. **Prepara tu música**: Antes de entrar al baño, agrega tus canciones favoritas
2. **Crea tu perfil**: Esto permite rutinas personalizadas
3. **Consulta al chatbot**: Obtén la rutina ideal para tu tipo de piel
4. **Usa "Reproducir con Rutina"**: La música se ajustará automáticamente al tiempo recomendado
5. **Mantén archivos organizados**: Los archivos de música se copian a la carpeta `musica/`

## Estructura de Directorios

```
AQUIFFY/
├── main.py              # Punto de entrada
├── requirements.txt     # Dependencias
├── src/                 # Código fuente
│   ├── usuario.py       # Sistema de perfiles
│   ├── gestor_musica.py # Gestión de playlist
│   ├── chatbot.py       # Asistente inteligente
│   ├── temporizador.py  # Temporizador y cronómetro
│   ├── reproductor.py   # Reproductor de música
│   ├── menu.py          # Menú principal
│   └── colores.py       # Sistema de colores
├── datos/               # Datos del usuario (creado automáticamente)
│   ├── usuario.json     # Perfil del usuario
│   └── playlist.json    # Lista de canciones
└── musica/              # Archivos de música (creado automáticamente)
```

## Colores de la Aplicación

AQUIFY usa una paleta de colores cuidadosamente seleccionada:
- Verde primario: #00CC57, #0A8A46
- Verde claro: #BFEFD6, #DFF7EA
- Azul claro: #B4E9FA, #C7EEFA
- Azul primario: #0077C8, #084A6F, #2EB7FF
- Azul muy claro: #E6F9FF
- Blancos/Neutros: #FFFFFF, #FBFCFE, #F3F9FF

## Solución de Problemas

### La música no se reproduce
- Verifica que pygame esté instalado: `pip install pygame`
- Asegúrate de que el archivo de música existe y está en un formato soportado

### Error al crear perfil
- Verifica que tengas permisos de escritura en el directorio
- La carpeta `datos/` se crea automáticamente

### El temporizador no funciona
- Asegúrate de ingresar un número válido de minutos
- No cierres la aplicación mientras el temporizador está activo

## Controles

- **Ctrl+C**: Detiene la reproducción de música o el cronómetro
- **Enter**: Continúa después de mostrar información
- **0**: Volver al menú anterior en la mayoría de los submenús

¡Disfruta de AQUIFY! 🎵💧
