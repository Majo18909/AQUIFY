# AQUIFY - Guía de Deployment en la Nube

## Opción 1: Render (RECOMENDADO - Gratis y Fácil)

### Pasos:

1. **Crear cuenta en Render**
   - Ve a https://render.com
   - Regístrate gratis con GitHub, GitLab o email

2. **Subir código a GitHub**
   ```bash
   git init
   git add .
   git commit -m "AQUIFY web app"
   git remote add origin https://github.com/TU-USUARIO/aquify.git
   git push -u origin main
   ```

3. **Crear Web Service en Render**
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Configuración:
     - Name: `aquify`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Click "Create Web Service"

4. **Acceder a tu app**
   - URL será: `https://aquify.onrender.com`
   - ¡Listo! Tu app está en la nube

### Notas Render:
- Plan gratuito disponible
- Se apaga después de 15 min de inactividad (se reactiva automáticamente)
- Límite de 750 horas/mes gratis

---

## Opción 2: Railway

### Pasos:

1. **Crear cuenta en Railway**
   - Ve a https://railway.app
   - Regístrate con GitHub

2. **Deploy desde GitHub**
   - Click "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Selecciona tu repositorio

3. **Configuración automática**
   - Railway detecta Flask automáticamente
   - Se despliega automáticamente

4. **Acceder**
   - Railway te da una URL pública
   - Ejemplo: `https://aquify.up.railway.app`

---

## Opción 3: Vercel (Solo Frontend estático)

Para Vercel necesitarías serverless functions (más complejo).

---

## Opción 4: Heroku

### Pasos:

1. **Crear cuenta**
   - https://heroku.com
   - Instalar Heroku CLI

2. **Deploy**
   ```bash
   heroku login
   heroku create aquify-app
   git push heroku main
   ```

3. **Acceder**
   - `https://aquify-app.herokuapp.com`

### Notas Heroku:
- Ya no tiene plan gratuito
- Mínimo $7/mes

---

## Opción 5: Google Cloud Run

### Pasos:

1. **Crear Dockerfile** (ya incluido en el proyecto)

2. **Configurar Google Cloud**
   ```bash
   gcloud init
   gcloud builds submit --tag gcr.io/PROJECT-ID/aquify
   gcloud run deploy --image gcr.io/PROJECT-ID/aquify --platform managed
   ```

---

## Opción 6: Azure Web Apps

1. Crear cuenta Azure
2. Crear Web App (Python)
3. Deploy desde GitHub o ZIP

---

## Configuraciones Importantes

### Variables de Entorno (si es necesario):
```
FLASK_ENV=production
MAX_CONTENT_LENGTH=52428800
```

### Archivos Necesarios para Deploy:
- ✅ `requirements.txt` - Dependencias Python
- ✅ `Procfile` - Comando para iniciar app
- ✅ `app.py` - Aplicación Flask
- ✅ `.gitignore` - Archivos a ignorar

---

## Recomendación Final

**Para principiantes: RENDER** ⭐
- Gratis
- Fácil de usar
- Conecta directo con GitHub
- No requiere tarjeta de crédito

### Pasos Rápidos con Render:

1. Sube tu código a GitHub
2. Conecta Render con GitHub
3. Click "Deploy"
4. ¡Listo!

---

## Limitaciones del Plan Gratuito

| Plataforma | Límite | Nota |
|------------|--------|------|
| Render | 750 hrs/mes | Se duerme después de inactividad |
| Railway | 500 hrs/mes | $5 crédito gratis inicial |
| Heroku | N/A | Ya no es gratis |
| Vercel | Funciones limitadas | Mejor para frontend |

---

## Próximos Pasos Después del Deploy

1. **Probar la aplicación**
   - Crear perfil
   - Subir música
   - Probar reproductor

2. **Compartir URL**
   - Comparte con amigos/familia
   - Funciona desde cualquier dispositivo

3. **Mejorar (opcional)**
   - Agregar dominio personalizado
   - Configurar HTTPS (automático en Render)
   - Agregar analytics

---

## Solución de Problemas

### Error: "Application Error"
- Verifica logs en la plataforma
- Revisa que todas las dependencias estén en `requirements.txt`

### Error: "Cannot upload files"
- Verifica límite de tamaño (50MB default)
- Algunas plataformas tienen filesystem read-only

### Música no se reproduce
- Verifica que la ruta `/musica/` esté accesible
- En producción, considera usar almacenamiento externo (S3, Cloudinary)

---

## Contacto

Si tienes problemas, revisa los logs de la plataforma elegida.
