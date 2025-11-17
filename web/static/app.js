// Variables globales
let currentUser = null;
let playlist = [];
let audioPlayer = null;
let timerInterval = null;
let timerSeconds = 0;
let rutinaSeconds = 0;
let isVercel = window.location.hostname.includes('vercel.app');
let deviceUserId = null;

// ============ FUNCIONES DE USUARIO ============

function getDeviceUserId() {
    // Obtiene o crea un ID único para este dispositivo
    if (!deviceUserId) {
        deviceUserId = localStorage.getItem('aquify_device_id');
        if (!deviceUserId) {
            // Generar un ID único para este dispositivo
            deviceUserId = 'device_' + Math.random().toString(36).substring(2) + Date.now().toString(36);
            localStorage.setItem('aquify_device_id', deviceUserId);
            console.log('✓ Nuevo ID de dispositivo creado:', deviceUserId);
        } else {
            console.log('✓ ID de dispositivo recuperado:', deviceUserId);
        }
    }
    return deviceUserId;
}

function getFetchHeaders(additionalHeaders = {}) {
    // Devuelve headers estándar con el ID de dispositivo
    return {
        'X-User-ID': getDeviceUserId(),
        ...additionalHeaders
    };
}

// ============ INICIALIZACIÓN ============

document.addEventListener('DOMContentLoaded', function () {
    // Inicializar ID de dispositivo
    getDeviceUserId();

    cargarPerfil();
    cargarCanciones();

    // Mostrar aviso si estamos en Vercel
    if (isVercel) {
        const warning = document.getElementById('vercel-warning');
        if (warning) {
            warning.style.display = 'block';
        }
        const uploadInfo = document.getElementById('upload-info');
        if (uploadInfo) {
            uploadInfo.textContent = 'Formatos: MP3, WAV, OGG, FLAC, M4A (Máx. 4MB en Vercel - Almacenamiento temporal)';
        }
    }

    // Setup drag and drop para archivos
    const uploadArea = document.getElementById('upload-area');
    if (uploadArea) {
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                document.getElementById('file-input').files = files;
                subirCancion();
            }
        });
    }
});

// ============ UTILIDADES ============

function switchTab(tabName) {
    // Ocultar todos los contenidos
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));

    // Desactivar todos los botones
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => button.classList.remove('active'));

    // Activar el tab seleccionado
    document.getElementById(`tab-${tabName}`).classList.add('active');
    event.target.classList.add('active');

    // Cargar datos específicos si es necesario
    if (tabName === 'musica') {
        cargarCanciones();
    } else if (tabName === 'reproductor') {
        cargarCancionesEnSelector();
    }
}

function showAlert(message, type = 'success') {
    const container = document.getElementById('alert-container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;

    container.appendChild(alert);

    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// ============ PERFIL DE USUARIO ============

async function cargarPerfil() {
    try {
        // Primero intentar cargar desde localStorage (persistencia en el dispositivo)
        const perfilLocal = localStorage.getItem('aquify_perfil');

        if (perfilLocal) {
            currentUser = JSON.parse(perfilLocal);
            console.log('✓ Perfil cargado desde localStorage (dispositivo)');
            mostrarPerfilDisplay();

            // También sincronizar con el servidor en segundo plano
            sincronizarPerfilConServidor(currentUser);
            return;
        }

        // Si no hay perfil local, intentar cargar desde el servidor
        const response = await fetch('/api/usuario', {
            credentials: 'include',
            headers: getFetchHeaders()
        });
        const data = await response.json();

        if (data.success) {
            currentUser = data.usuario;
            // Guardar en localStorage para la próxima vez
            localStorage.setItem('aquify_perfil', JSON.stringify(currentUser));
            console.log('✓ Perfil cargado desde servidor y guardado localmente');
            mostrarPerfilDisplay();
        } else {
            mostrarPerfilForm();
        }
    } catch (error) {
        console.error('Error al cargar perfil:', error);

        // Si hay error de red, intentar usar el perfil guardado localmente
        const perfilLocal = localStorage.getItem('aquify_perfil');
        if (perfilLocal) {
            currentUser = JSON.parse(perfilLocal);
            console.log('⚠️ Usando perfil local (sin conexión al servidor)');
            mostrarPerfilDisplay();
        } else {
            mostrarPerfilForm();
        }
    }
}

async function sincronizarPerfilConServidor(perfil) {
    try {
        await fetch('/api/usuario', {
            method: 'POST',
            headers: getFetchHeaders({
                'Content-Type': 'application/json'
            }),
            credentials: 'include',
            body: JSON.stringify(perfil)
        });
        console.log('✓ Perfil sincronizado con servidor');
    } catch (error) {
        console.log('⚠️ No se pudo sincronizar con servidor (modo offline)');
    }
}

function mostrarPerfilDisplay() {
    const display = document.getElementById('perfil-display');
    const form = document.getElementById('perfil-form');
    const info = document.getElementById('perfil-info');

    let genero = currentUser.genero;
    if (currentUser.genero_personalizado) {
        genero = currentUser.genero_personalizado;
    }

    let html = `
        <div class="profile-item">
            <span class="profile-label">Género:</span>
            <span>${genero}</span>
        </div>
    `;

    if (currentUser.pronombres) {
        html += `
            <div class="profile-item">
                <span class="profile-label">Pronombres:</span>
                <span>${currentUser.pronombres}</span>
            </div>
        `;
    }

    html += `
        <div class="profile-item">
            <span class="profile-label">Edad:</span>
            <span>${currentUser.edad} años</span>
        </div>
        <div class="profile-item">
            <span class="profile-label">Tipo de Piel:</span>
            <span>${currentUser.tipo_piel}</span>
        </div>
    `;

    info.innerHTML = html;
    display.style.display = 'block';
    form.style.display = 'none';
}

function mostrarPerfilForm() {
    const display = document.getElementById('perfil-display');
    const form = document.getElementById('perfil-form');

    display.style.display = 'none';
    form.style.display = 'block';
}

function editarPerfil() {
    // Cargar datos actuales en el formulario
    if (currentUser) {
        document.getElementById('genero').value = currentUser.genero;
        document.getElementById('edad').value = currentUser.edad;
        document.getElementById('tipo-piel').value = currentUser.tipo_piel;

        if (currentUser.genero === 'Personalizado') {
            document.getElementById('genero-custom').value = currentUser.genero_personalizado || '';
            document.getElementById('pronombres').value = currentUser.pronombres || '';
            toggleGeneroPersonalizado();
        }
    }

    mostrarPerfilForm();
}

function toggleGeneroPersonalizado() {
    const genero = document.getElementById('genero').value;
    const customDiv = document.getElementById('genero-personalizado');

    if (genero === 'Personalizado') {
        customDiv.classList.add('show');
    } else {
        customDiv.classList.remove('show');
    }
}

async function guardarPerfil() {
    const genero = document.getElementById('genero').value;
    const edad = parseInt(document.getElementById('edad').value);
    const tipoPiel = document.getElementById('tipo-piel').value;

    if (!edad || edad < 1 || edad > 120) {
        showAlert('Por favor ingresa una edad válida', 'error');
        return;
    }

    const perfil = {
        genero: genero,
        edad: edad,
        tipo_piel: tipoPiel
    };

    if (genero === 'Personalizado') {
        perfil.genero_personalizado = document.getElementById('genero-custom').value;
        perfil.pronombres = document.getElementById('pronombres').value;
    }

    try {
        // Guardar primero en localStorage (inmediato)
        localStorage.setItem('aquify_perfil', JSON.stringify(perfil));
        console.log('✓ Perfil guardado en dispositivo');

        // Luego intentar guardar en el servidor
        const response = await fetch('/api/usuario', {
            method: 'POST',
            headers: getFetchHeaders({
                'Content-Type': 'application/json'
            }),
            credentials: 'include',
            body: JSON.stringify(perfil)
        });

        const data = await response.json();

        if (data.success) {
            showAlert('✓ Perfil guardado exitosamente (dispositivo + servidor)', 'success');
            await cargarPerfil();
        } else {
            // Aunque falle el servidor, ya está guardado localmente
            showAlert('✓ Perfil guardado en dispositivo (servidor no disponible)', 'success');
            currentUser = perfil;
            mostrarPerfilDisplay();
        }
    } catch (error) {
        console.error('Error:', error);
        // El perfil ya está guardado en localStorage, así que aún funciona
        showAlert('✓ Perfil guardado en dispositivo (modo offline)', 'success');
        currentUser = perfil;
        mostrarPerfilDisplay();
    }
}

function limpiarPerfilLocal() {
    if (confirm('¿Estás seguro de borrar tu perfil de este dispositivo? Tendrás que crearlo nuevamente.')) {
        localStorage.removeItem('aquify_perfil');
        currentUser = null;
        showAlert('Perfil eliminado del dispositivo', 'success');
        mostrarPerfilForm();
    }
}

function limpiarCancionesLocales() {
    if (confirm('¿Estás seguro de borrar todas las canciones de este dispositivo? Solo se borrarán de este navegador.')) {
        localStorage.removeItem('aquify_canciones');
        playlist = [];
        mostrarCanciones();
        showAlert('Canciones eliminadas del dispositivo', 'success');
        const infoElement = document.getElementById('canciones-local-info');
        if (infoElement) {
            infoElement.style.display = 'none';
        }
    }
}

// ============ GESTIÓN DE MÚSICA ============

async function cargarCanciones() {
    try {
        // Primero intentar cargar desde localStorage
        const cancionesLocales = localStorage.getItem('aquify_canciones');

        if (cancionesLocales) {
            playlist = JSON.parse(cancionesLocales);
            console.log('✓ Canciones cargadas desde dispositivo:', playlist.length, 'canciones');
            mostrarCanciones();
        }

        // Luego intentar sincronizar con el servidor
        const response = await fetch('/api/canciones', {
            credentials: 'include',
            headers: getFetchHeaders()
        });
        const data = await response.json();

        if (data.success && data.canciones && data.canciones.length > 0) {
            // Solo actualizar si el servidor tiene canciones
            playlist = data.canciones;
            // Guardar en localStorage
            localStorage.setItem('aquify_canciones', JSON.stringify(playlist));
            console.log('✓ Canciones sincronizadas con servidor:', playlist.length, 'canciones');
            mostrarCanciones();
        } else if (playlist.length === 0) {
            // Si no hay canciones ni en servidor ni en localStorage
            console.log('ℹ No hay canciones guardadas');
            mostrarCanciones();
        }
    } catch (error) {
        console.error('Error al cargar canciones:', error);
        // Si ya teníamos canciones locales, seguimos con esas
        if (playlist.length > 0) {
            console.log('✓ Usando canciones guardadas localmente (modo offline)');
            mostrarCanciones();
        }
    }
}

function mostrarCanciones() {
    const list = document.getElementById('song-list');
    const infoElement = document.getElementById('canciones-local-info');

    if (playlist.length === 0) {
        list.innerHTML = '<li style="text-align: center; padding: 2rem; color: #666;">No hay canciones. ¡Sube tu primera canción!</li>';
        if (infoElement) {
            infoElement.style.display = 'none';
        }
        return;
    }

    // Mostrar mensaje de que hay canciones guardadas
    if (infoElement) {
        infoElement.style.display = 'block';
    }

    list.innerHTML = playlist.map(song => `
        <li class="song-item">
            <div class="song-info">
                <span class="song-icon">🎵</span>
                <div>
                    <strong>${song.nombre}</strong>
                    <br>
                    <small style="color: #666;">${song.archivo}</small>
                </div>
            </div>
            <div class="song-actions">
                <button class="btn btn-secondary" onclick="reproducirCancion(${song.id})">▶️ Reproducir</button>
                <button class="btn btn-danger" onclick="eliminarCancion(${song.id})">🗑️</button>
            </div>
        </li>
    `).join('');
}

async function subirCancion() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (!file) {
        showAlert('Por favor selecciona un archivo', 'error');
        return;
    }

    // Límites diferentes para Vercel vs Local
    // Vercel tiene límite de payload de 4.5MB, usamos 4MB para estar seguros
    const maxSize = isVercel ? 4 * 1024 * 1024 : 50 * 1024 * 1024; // 4MB en Vercel, 50MB en local
    const maxSizeMB = isVercel ? '4MB' : '50MB';

    if (file.size > maxSize) {
        showAlert(`El archivo es demasiado grande (máximo ${maxSizeMB})`, 'error');
        return;
    }

    // Verificar tipo de archivo
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const allowedExtensions = ['mp3', 'wav', 'ogg', 'flac', 'm4a'];

    if (!allowedExtensions.includes(fileExtension)) {
        showAlert('Formato no permitido. Usa: MP3, WAV, OGG, FLAC o M4A', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('archivo', file);

    try {
        console.log('Subiendo archivo:', file.name, 'Tamaño:', file.size, 'bytes', 'En Vercel:', isVercel);
        showAlert('Subiendo canción...', 'info');

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 segundos timeout

        const response = await fetch('/api/canciones/subir', {
            method: 'POST',
            credentials: 'include',
            headers: getFetchHeaders(),
            body: formData,
            signal: controller.signal
        });

        clearTimeout(timeoutId);
        console.log('Respuesta recibida:', response.status);

        // Manejar error 413 (Payload Too Large)
        if (response.status === 413) {
            showAlert(`El archivo es muy grande para Vercel. Máximo ${maxSizeMB}. Usa localhost para archivos más grandes.`, 'error');
            fileInput.value = '';
            return;
        }

        const data = await response.json();
        console.log('Datos:', data);

        if (data.success) {
            showAlert('✓ Canción agregada exitosamente', 'success');
            fileInput.value = '';
            await cargarCanciones();
            // Guardar en localStorage también
            localStorage.setItem('aquify_canciones', JSON.stringify(playlist));
        } else {
            showAlert(data.message || 'Error al subir canción', 'error');
        }
    } catch (error) {
        console.error('Error completo:', error);
        if (error.name === 'AbortError') {
            showAlert('Timeout: El archivo es muy grande o la conexión es lenta', 'error');
        } else {
            showAlert('Error al subir canción: ' + error.message, 'error');
        }
    }
}

async function eliminarCancion(id) {
    if (!confirm('¿Estás seguro de eliminar esta canción?')) {
        return;
    }

    try {
        const response = await fetch(`/api/canciones/${id}`, {
            method: 'DELETE',
            credentials: 'include',
            headers: getFetchHeaders()
        }); const data = await response.json();

        if (data.success) {
            showAlert('✓ Canción eliminada', 'success');
            await cargarCanciones();
            // Actualizar localStorage
            localStorage.setItem('aquify_canciones', JSON.stringify(playlist));
        } else {
            showAlert('Error al eliminar canción', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error al eliminar canción', 'error');
    }
}

// ============ CHATBOT ============

// Variables del chat
let chatHistory = [];

async function enviarMensaje() {
    const input = document.getElementById('chat-input');
    const mensaje = input.value.trim();

    if (!mensaje) return;

    // Agregar mensaje del usuario al chat
    agregarMensajeAlChat('user', mensaje);
    input.value = '';

    // Mostrar indicador de escritura
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'chat-message bot-message typing-indicator';
    typingIndicator.innerHTML = '<strong>AQUIFY:</strong><p>Escribiendo...</p>';
    typingIndicator.id = 'typing-indicator';
    chatMessages.appendChild(typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch('/api/chatbot/mensaje', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ mensaje })
        });

        const data = await response.json();

        // Eliminar indicador de escritura
        document.getElementById('typing-indicator')?.remove();

        if (data.success) {
            agregarMensajeAlChat('bot', data.respuesta);
        } else {
            agregarMensajeAlChat('bot', 'Lo siento, hubo un error al procesar tu mensaje. 😅');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('typing-indicator')?.remove();
        agregarMensajeAlChat('bot', 'Error de conexión. Por favor, intenta de nuevo.');
    }
}

function agregarMensajeAlChat(tipo, mensaje) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${tipo}-message`;

    if (tipo === 'user') {
        messageDiv.innerHTML = `<p>${mensaje}</p>`;
    } else {
        // Convertir markdown básico y saltos de línea
        let formattedMessage = mensaje
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');

        messageDiv.innerHTML = `<strong>AQUIFY:</strong><p>${formattedMessage}</p>`;
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Guardar en historial
    chatHistory.push({ tipo, mensaje, timestamp: new Date() });
}

async function mostrarRutina() {
    try {
        const response = await fetch('/api/chatbot/rutina', {
            credentials: 'include'
        });
        const data = await response.json();

        const container = document.getElementById('chatbot-response');

        if (!data.success) {
            container.innerHTML = `
                <div class="alert alert-error">
                    ${data.message}
                </div>
            `;
            return;
        }

        const rutina = data.rutina;

        let html = `
            <div class="card">
                <h3>Rutina para Piel ${data.tipo_piel}</h3>
                <p style="color: var(--azul-primario); font-weight: 600; margin-bottom: 1rem;">
                    ⏱️ Tiempo total: ${rutina.tiempo_total} minutos
                </p>
                <h4 style="color: var(--verde-primario); margin-top: 1.5rem;">Pasos de la Rutina:</h4>
                <ul class="routine-steps">
                    ${rutina.rutina.map(paso => `<li class="routine-step">${paso}</li>`).join('')}
                </ul>
                <h4 style="color: var(--verde-primario); margin-top: 1.5rem;">Consejos:</h4>
                <ul class="tips-list">
                    ${rutina.consejos.map(consejo => `<li class="tip-item">${consejo}</li>`).join('')}
                </ul>
            </div>
        `;

        container.innerHTML = html;
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error al obtener rutina', 'error');
    }
}

async function mostrarConsejos() {
    try {
        const response = await fetch('/api/chatbot/consejos', {
            credentials: 'include'
        });
        const data = await response.json();

        const container = document.getElementById('chatbot-response');

        if (!data.success) {
            container.innerHTML = `
                <div class="alert alert-error">
                    ${data.message}
                </div>
            `;
            return;
        }

        let html = `
            <div class="card">
                <h3>Consejos para Piel ${data.tipo_piel}</h3>
                <ul class="tips-list">
                    ${data.consejos.map(consejo => `<li class="tip-item">${consejo}</li>`).join('')}
                </ul>
            </div>
        `;

        container.innerHTML = html;
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error al obtener consejos', 'error');
    }
}

async function mostrarRecomendaciones() {
    try {
        const response = await fetch('/api/chatbot/recomendaciones-musica');
        const data = await response.json();

        const container = document.getElementById('chatbot-response');

        let html = `
            <div class="card">
                <h3>🎵 Recomendaciones Musicales</h3>
                <p style="margin-bottom: 1rem;">Géneros perfectos para tu baño relajante:</p>
                <ul class="tips-list">
                    ${data.recomendaciones.map(rec => `<li class="tip-item">${rec}</li>`).join('')}
                </ul>
            </div>
        `;

        container.innerHTML = html;
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error al obtener recomendaciones', 'error');
    }
}

// ============ REPRODUCTOR ============

function cargarCancionesEnSelector() {
    const selector = document.getElementById('cancion-seleccionada');

    selector.innerHTML = '<option value="">-- Selecciona una canción --</option>' +
        playlist.map(song => `<option value="${song.id}">${song.nombre}</option>`).join('');
}

function toggleTiempoRutina() {
    const modo = document.querySelector('input[name="modo"]:checked').value;
    const container = document.getElementById('tiempo-rutina-container');

    if (modo === 'rutina') {
        container.style.display = 'block';

        // Cargar tiempo sugerido basado en tipo de piel
        if (currentUser && currentUser.tipo_piel) {
            const tiemposSugeridos = {
                'Normal': 7,
                'Seca': 9,
                'Mixta': 8,
                'Grasa': 7,
                'Sensible': 8,
                'No sé': 7
            };
            document.getElementById('tiempo-rutina').value = tiemposSugeridos[currentUser.tipo_piel] || 7;
        }
    } else {
        container.style.display = 'none';
    }
}

function iniciarReproduccion() {
    const cancionId = parseInt(document.getElementById('cancion-seleccionada').value);

    if (!cancionId) {
        showAlert('Por favor selecciona una canción', 'error');
        return;
    }

    const cancion = playlist.find(s => s.id === cancionId);
    if (!cancion) {
        showAlert('Canción no encontrada', 'error');
        return;
    }

    const modo = document.querySelector('input[name="modo"]:checked').value;

    audioPlayer = document.getElementById('audio-player');
    audioPlayer.src = `/musica/${cancion.archivo}`;

    document.getElementById('player-song-name').textContent = cancion.nombre;

    if (modo === 'rutina') {
        const minutos = parseInt(document.getElementById('tiempo-rutina').value) || 7;
        rutinaSeconds = minutos * 60;
        document.getElementById('player-mode').textContent = `Modo Rutina - ${minutos} minutos`;

        audioPlayer.play();
        iniciarTimerRutina();
    } else {
        rutinaSeconds = 0;
        document.getElementById('player-mode').textContent = 'Modo Libre';
        audioPlayer.play();
    }

    document.getElementById('player-container').style.display = 'block';
    document.getElementById('btn-pause').style.display = 'inline-block';
    document.getElementById('btn-play').style.display = 'none';

    showAlert('▶️ Reproducción iniciada', 'success');
}

function iniciarTimerRutina() {
    timerSeconds = rutinaSeconds;

    if (timerInterval) {
        clearInterval(timerInterval);
    }

    actualizarDisplayTimer();

    timerInterval = setInterval(() => {
        timerSeconds--;
        actualizarDisplayTimer();

        if (timerSeconds <= 0) {
            clearInterval(timerInterval);
            audioPlayer.pause();
            showAlert('⏰ ¡Tiempo de rutina completado! La música se ha pausado.', 'info');
            document.getElementById('btn-pause').style.display = 'none';
            document.getElementById('btn-play').style.display = 'inline-block';
        }
    }, 1000);
}

function actualizarDisplayTimer() {
    const minutos = Math.floor(timerSeconds / 60);
    const segundos = timerSeconds % 60;
    document.getElementById('timer-display').textContent =
        `${minutos.toString().padStart(2, '0')}:${segundos.toString().padStart(2, '0')}`;

    if (rutinaSeconds > 0) {
        const progress = ((rutinaSeconds - timerSeconds) / rutinaSeconds) * 100;
        document.getElementById('progress-fill').style.width = `${progress}%`;
    }
}

function pausarReproduccion() {
    if (audioPlayer) {
        audioPlayer.pause();
        if (timerInterval) {
            clearInterval(timerInterval);
        }
        document.getElementById('btn-pause').style.display = 'none';
        document.getElementById('btn-play').style.display = 'inline-block';
    }
}

function reanudarReproduccion() {
    if (audioPlayer) {
        audioPlayer.play();
        if (rutinaSeconds > 0 && timerSeconds > 0) {
            iniciarTimerRutina();
        }
        document.getElementById('btn-pause').style.display = 'inline-block';
        document.getElementById('btn-play').style.display = 'none';
    }
}

function detenerReproduccion() {
    if (audioPlayer) {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
    }

    if (timerInterval) {
        clearInterval(timerInterval);
    }

    document.getElementById('player-container').style.display = 'none';
    document.getElementById('progress-fill').style.width = '0%';
    showAlert('⏹️ Reproducción detenida', 'info');
}

function reproducirCancion(id) {
    document.getElementById('cancion-seleccionada').value = id;
    switchTab('reproductor');

    // Esperar a que el tab cambie
    setTimeout(() => {
        const tabButton = Array.from(document.querySelectorAll('.tab-button'))
            .find(btn => btn.textContent.includes('Reproductor'));
        if (tabButton) {
            tabButton.click();
        }
    }, 100);
}

// ============ TEMPORIZADOR STANDALONE ============

let standaloneTimerInterval = null;
let standaloneSeconds = 0;

function iniciarTemporizador() {
    const minutos = parseInt(document.getElementById('timer-minutes').value);

    if (!minutos || minutos < 1) {
        showAlert('Por favor ingresa un tiempo válido', 'error');
        return;
    }

    standaloneSeconds = minutos * 60;

    document.getElementById('timer-active').style.display = 'block';
    actualizarStandaloneTimer();

    if (standaloneTimerInterval) {
        clearInterval(standaloneTimerInterval);
    }

    standaloneTimerInterval = setInterval(() => {
        standaloneSeconds--;
        actualizarStandaloneTimer();

        if (standaloneSeconds <= 0) {
            clearInterval(standaloneTimerInterval);
            showAlert('⏰ ¡Tiempo terminado!', 'info');
        }
    }, 1000);

    showAlert('⏱️ Temporizador iniciado', 'success');
}

function actualizarStandaloneTimer() {
    const minutos = Math.floor(standaloneSeconds / 60);
    const segundos = standaloneSeconds % 60;
    document.getElementById('standalone-timer').textContent =
        `${minutos.toString().padStart(2, '0')}:${segundos.toString().padStart(2, '0')}`;
}

function detenerTemporizador() {
    if (standaloneTimerInterval) {
        clearInterval(standaloneTimerInterval);
    }
    document.getElementById('timer-active').style.display = 'none';
    showAlert('⏹️ Temporizador detenido', 'info');
}
