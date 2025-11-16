# 📦 Instrucciones de Despliegue - AQUIFY

## 🎯 Opción Recomendada: Vercel

### Paso 1: Preparar el Repositorio

Todos los archivos ya están listos:
- ✅ `vercel.json` - Configuración de Vercel
- ✅ `requirements.txt` - Dependencias Python
- ✅ `app.py` - Backend Flask
- ✅ `web/` - Frontend

### Paso 2: Desplegar en Vercel

1. **Ir a Vercel:**
   - https://vercel.com/signup
   - Sign up con GitHub

2. **Importar Proyecto:**
   - Click "Add New" → "Project"
   - Seleccionar tu repositorio `AQUIFY`
   - Vercel detectará automáticamente Python

3. **Configurar:**
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Build Command: (dejar vacío)
   - Output Directory: (dejar vacío)

4. **Deploy:**
   - Click "Deploy"
   - Esperar 2-3 minutos

5. **Verificar:**
   - Se te dará una URL como: `https://aquify.vercel.app`
   - Prueba todas las funcionalidades

### Paso 3: Configurar Dominio Personalizado (Opcional)

1. En Vercel, ir a Settings → Domains
2. Agregar tu dominio personalizado

---

## 🔄 Opción 2: Mantener Render + UptimeRobot

### Paso 1: Configurar UptimeRobot

1. **Crear cuenta:**
   - https://uptimerobot.com/signUp
   - Sign up (gratis)

2. **Agregar Monitor:**
   - Dashboard → Add New Monitor
   - Monitor Type: `HTTP(s)`
   - Friendly Name: `AQUIFY`
   - URL: `https://aquify.onrender.com`
   - Monitoring Interval: `5 minutes`
   - Monitor Timeout: `30 seconds`

3. **Configurar Alertas:**
   - Alert Contacts → Add Email
   - Te notificará si la app cae

4. **Guardar:**
   - Click "Create Monitor"

### Resultado:
- ✅ Tu app nunca se dormirá
- ✅ Gratis para siempre
- ✅ Monitoreo incluido

---

## 🌐 Opción 3: Netlify (Solo Frontend) + Render (Backend)

### Archivos ya creados:
- ✅ `netlify.toml`

### Paso 1: Modificar app.js para usar backend remoto

Editar `web/static/app.js`, agregar al inicio:

```javascript
// Configuración del backend
const API_URL = 'https://aquify.onrender.com';

// Luego en cada fetch, cambiar de:
fetch('/api/usuario', ...)

// A:
fetch(`${API_URL}/api/usuario`, ...)
```

### Paso 2: Actualizar CORS en app.py

```python
# En app.py, línea ~18, cambiar:
CORS(app, supports_credentials=True)

# A:
CORS(app, supports_credentials=True, origins=[
    'https://tu-app.netlify.app',  # Tu URL de Netlify
    'http://localhost:5000',
    'https://aquify.onrender.com'
])
```

### Paso 3: Desplegar en Netlify

1. **Ir a Netlify:**
   - https://app.netlify.com/signup
   - Sign up con GitHub

2. **Importar Proyecto:**
   - Sites → Add new site → Import from Git
   - Conectar GitHub
   - Seleccionar repositorio AQUIFY

3. **Configurar Build:**
   - Base directory: (vacío)
   - Build command: `echo 'Static site'`
   - Publish directory: `web`

4. **Deploy:**
   - Click "Deploy site"

5. **Configurar Variables:**
   - Site settings → Environment variables
   - Agregar: `BACKEND_URL` = `https://aquify.onrender.com`

---

## 📊 Comparación de Opciones

### ⭐ Vercel (RECOMENDADO)
**Pros:**
- ✅ Todo en un solo lugar (frontend + backend)
- ✅ No se duerme
- ✅ Muy rápido (CDN global)
- ✅ SSL automático
- ✅ Despliegue automático desde GitHub

**Contras:**
- ❌ Límite de 100GB bandwidth/mes (suficiente para empezar)

### 🔵 Render + UptimeRobot
**Pros:**
- ✅ Ya está funcionando
- ✅ Cero cambios de código
- ✅ Gratis para siempre
- ✅ Fácil de mantener

**Contras:**
- ❌ Arranque lento en primera petición (10-15 seg)

### 🟢 Netlify + Render
**Pros:**
- ✅ Frontend ultra rápido en Netlify
- ✅ Backend estable en Render

**Contras:**
- ❌ Más complejo de configurar
- ❌ Dos plataformas que mantener
- ❌ Requiere modificar código

---

## 🚀 Pasos Rápidos Según tu Elección

### Si eliges Vercel:
```bash
# Ya está todo listo, solo:
1. Ir a vercel.com
2. Importar repositorio de GitHub
3. Deploy
```

### Si eliges Mantener Render:
```bash
# Solo configurar UptimeRobot (5 minutos)
1. uptimerobot.com
2. Agregar monitor
3. URL: https://aquify.onrender.com
```

### Si eliges Netlify:
```bash
# Modificar código primero
1. Editar web/static/app.js (agregar API_URL)
2. Editar app.py (actualizar CORS)
3. Commit y push
4. Ir a netlify.com
5. Importar repositorio
```

---

## 💡 Mi Recomendación Final

Para AQUIFY, **Vercel es la mejor opción** porque:

1. ✅ Soporta Python nativamente
2. ✅ No requiere separar frontend/backend
3. ✅ No se duerme (siempre rápido)
4. ✅ Gratis y sin límites molestos
5. ✅ Zero configuration needed (archivos ya listos)

**Tiempo estimado:** 5 minutos para desplegar

---

## 🆘 Si Necesitas Ayuda

1. **Vercel:** https://vercel.com/docs
2. **Netlify:** https://docs.netlify.com
3. **Render:** https://render.com/docs
4. **UptimeRobot:** https://uptimerobot.com/faq

---

## ✅ Checklist de Despliegue

- [ ] Elegir plataforma (Vercel recomendado)
- [ ] Crear cuenta en la plataforma
- [ ] Conectar con GitHub
- [ ] Importar repositorio AQUIFY
- [ ] Configurar build settings (si aplica)
- [ ] Deploy
- [ ] Probar URL generada
- [ ] Configurar dominio personalizado (opcional)
- [ ] Agregar monitoreo (si usas Render)

---

**¿Cuál opción prefieres? Te ayudo a configurarla paso a paso.**
