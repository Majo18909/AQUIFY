# 🚀 INICIO RÁPIDO - AQUIFY

## Para usar AQUIFY en tu PC (localhost)

### 1️⃣ Iniciar el servidor

Abre una terminal en la carpeta AQUIFFY y ejecuta:

```bash
python app.py
```

### 2️⃣ Abrir en tu navegador

Abre cualquiera de estas URLs:
- http://localhost:5000
- http://127.0.0.1:5000

### 3️⃣ Usar desde tu teléfono/tablet (misma red WiFi)

1. En la terminal verás algo como: `Running on http://192.168.0.101:5000`
2. Copia esa IP (será diferente en tu caso)
3. En tu teléfono/tablet, abre el navegador y ve a: `http://TU-IP:5000`

---

## 📱 Para usar AQUIFY desde cualquier lugar (Internet)

Lee la guía completa en **DEPLOYMENT.md**

### Opción más fácil: Render (Gratis)

1. **Sube a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Mi app AQUIFY"
   # Crea un repo en GitHub y sigue las instrucciones
   git remote add origin https://github.com/TU-USUARIO/aquify.git
   git push -u origin main
   ```

2. **Deploy en Render:**
   - Ve a https://render.com
   - Crea cuenta gratis
   - Click "New +" → "Web Service"
   - Conecta tu GitHub
   - Selecciona el repo "aquify"
   - Click "Create Web Service"
   - Espera 2-3 minutos

3. **¡Listo!**
   - Te darán una URL como: `https://aquify.onrender.com`
   - Compártela con quien quieras
   - Funciona desde cualquier dispositivo con internet

---

## 🎯 Primeros Pasos en la App

1. **Crear tu perfil**
   - Click en tab "👤 Perfil"
   - Completa tu información
   - Guarda

2. **Subir música**
   - Click en tab "🎵 Música"
   - Arrastra archivos MP3 o haz click para seleccionar
   - Sube tus canciones favoritas

3. **Consultar tu rutina**
   - Click en tab "🤖 Asistente"
   - Click en "Ver Mi Rutina"
   - Verás una rutina personalizada según tu tipo de piel

4. **Reproducir música con rutina**
   - Click en tab "▶️ Reproductor"
   - Selecciona una canción
   - Elige "Con Rutina"
   - Ajusta el tiempo si quieres
   - Click "▶️ Reproducir"
   - ¡La música se pausará automáticamente cuando termine tu tiempo!

---

## 🛑 Detener el servidor

En la terminal donde ejecutaste `python app.py`:
- Presiona `Ctrl+C`

---

## ❓ Solución de Problemas

### No puedo acceder desde mi teléfono
- Asegúrate de estar en la misma red WiFi
- Verifica que usas la IP correcta (la que aparece en la terminal)
- Algunos routers bloquean conexiones entre dispositivos (revisa configuración)

### Error al subir música
- Verifica que el archivo sea MP3, WAV, OGG, FLAC o M4A
- Máximo 50MB por archivo

### La página no carga
- Verifica que el servidor esté corriendo (debe decir "Running on...")
- Prueba cerrar y abrir el navegador
- Intenta con http://127.0.0.1:5000

---

## 💡 Consejos

- **Mejor experiencia:** Usa Chrome o Firefox
- **Privacidad:** Tus datos se guardan solo en tu computadora (o en tu servidor si lo subes a la nube)
- **Música:** Los archivos se guardan en la carpeta `musica/` de tu proyecto
- **Respaldo:** Para no perder tus datos, respalda las carpetas `datos/` y `musica/`

---

## 🌟 Próximos Pasos

1. ✅ Prueba todas las funciones
2. ✅ Sube tu música favorita
3. ✅ Crea tu rutina perfecta
4. 🚀 Súbelo a la nube con Render
5. 📱 Comparte con amigos/familia

---

¡Disfruta de AQUIFY! 🎵💧
