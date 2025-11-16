# 🚀 Guía de Despliegue de AQUIFY en Netlify

## ⚠️ Importante: Limitaciones de Netlify

Netlify está diseñado principalmente para sitios estáticos. Tu aplicación AQUIFY usa Flask (Python) como backend, lo cual **NO es directamente compatible** con Netlify.

## 📋 Opciones de Despliegue

### Opción 1: Mantener en Render (RECOMENDADO) ✅

**Ventajas:**
- ✅ Soporte nativo para Flask/Python
- ✅ Base de datos y almacenamiento de archivos
- ✅ Despliegue automático desde GitHub
- ✅ SSL gratuito
- ✅ Ya está configurado y funcionando

**Desventajas:**
- ❌ Servicio gratuito se "duerme" después de 15 minutos de inactividad
- ❌ Arranque más lento en la primera petición

**Cómo mantenerlo activo:**
1. Usa un servicio como UptimeRobot (gratuito) para hacer ping cada 10 minutos
2. URL a monitorear: https://aquify.onrender.com

---

### Opción 2: Netlify + Backend Externo (HÍBRIDO)

Desplegar el frontend en Netlify y mantener el backend en Render.

**Pasos:**

1. **Frontend en Netlify:**
   - Sube solo la carpeta `web/` a Netlify
   - Configura las peticiones API para apuntar a Render

2. **Backend en Render:**
   - Mantén el backend Flask en Render
   - Configura CORS para aceptar peticiones desde Netlify

**Configuración necesaria:**
- Modificar `app.js` para usar la URL de Render como backend
- Actualizar CORS en `app.py`

---

### Opción 3: Alternativas Mejor Compatibles con Python

**Vercel** (RECOMENDADO como alternativa):
- ✅ Soporte para Python con Serverless Functions
- ✅ Despliegue gratuito
- ✅ No se "duerme"
- ✅ Muy rápido

**Railway:**
- ✅ Similar a Render
- ✅ Plan gratuito disponible
- ✅ Muy fácil de usar

**PythonAnywhere:**
- ✅ Especializado en Python
- ✅ Plan gratuito permanente
- ✅ Ideal para Flask

---

## 🔧 Si Decides Usar Netlify (Opción 2 - Híbrido)

### Archivos Necesarios:

#### 1. `netlify.toml` (crear en la raíz)

```toml
[build]
  publish = "web"
  command = "echo 'Frontend only'"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"
```

#### 2. Modificar `web/static/app.js`

Cambia todas las URLs de API de relativas a absolutas:

```javascript
// Antes:
const response = await fetch('/api/usuario', {

// Después:
const API_URL = 'https://aquify.onrender.com';
const response = await fetch(`${API_URL}/api/usuario`, {
```

#### 3. Actualizar CORS en `app.py`

```python
# Permitir peticiones desde Netlify
CORS(app, supports_credentials=True, origins=[
    'https://tu-app.netlify.app',
    'http://localhost:5000',
    'https://aquify.onrender.com'
])
```

### Pasos para Desplegar en Netlify:

1. **Crear cuenta en Netlify:** https://netlify.com
2. **Conectar con GitHub:**
   - Click en "Add new site"
   - Seleccionar "Import from Git"
   - Conectar tu cuenta de GitHub
   - Seleccionar el repositorio AQUIFY

3. **Configuración de Build:**
   - Build command: `echo 'Static site'`
   - Publish directory: `web`

4. **Variables de Entorno (si necesitas):**
   - Settings → Environment variables
   - Agregar `BACKEND_URL = https://aquify.onrender.com`

5. **Deploy:**
   - Click "Deploy site"

---

## 🎯 Mi Recomendación

**Para AQUIFY, te recomiendo:**

### Opción A: Vercel (Mejor alternativa a Netlify)
- Soporta Python Serverless
- No requiere separar frontend/backend
- Más rápido que Render
- No se duerme

### Opción B: Mantener Render + UptimeRobot
- Configuración actual funciona perfectamente
- Solo agregar monitoreo para mantenerlo activo
- Cero cambios de código necesarios

---

## 📱 Configuración de UptimeRobot (Mantener Render Activo)

1. Ir a: https://uptimerobot.com
2. Crear cuenta gratuita
3. Add New Monitor:
   - Monitor Type: HTTP(s)
   - Friendly Name: AQUIFY
   - URL: https://aquify.onrender.com
   - Monitoring Interval: 5 minutes
4. Save

Esto hará ping cada 5 minutos y mantendrá tu app despierta.

---

## 🚀 Guía Rápida para Vercel (SI DECIDES CAMBIAR)

### Archivos Necesarios:

#### 1. `vercel.json` (crear en la raíz)

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

#### 2. `requirements.txt` (ya lo tienes)

Ya está listo.

#### 3. Modificar `app.py`

Agregar al final:

```python
# Para Vercel
app = app
```

### Pasos en Vercel:

1. Ir a: https://vercel.com
2. Sign up con GitHub
3. Import Project → tu repositorio AQUIFY
4. Vercel detectará automáticamente Python
5. Deploy

---

## ❓ ¿Qué Opción Elegir?

| Plataforma | Costo | Velocidad | Facilidad | Python Backend |
|------------|-------|-----------|-----------|----------------|
| **Render** | Gratis* | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Excelente |
| **Netlify** | Gratis | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ Solo frontend |
| **Vercel** | Gratis | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Serverless |
| **Railway** | Gratis** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Excelente |
| **PythonAnywhere** | Gratis | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Excelente |

*Se duerme después de 15 min de inactividad
**Plan gratuito limitado

---

## 💡 Conclusión

**Mi recomendación:**
1. **Primera opción:** Mantener Render + configurar UptimeRobot (5 minutos de trabajo)
2. **Segunda opción:** Migrar a Vercel (mejor rendimiento, no se duerme)
3. **Tercera opción:** Netlify solo si separas frontend/backend (más complejo)

¿Qué opción prefieres que configure para ti?
