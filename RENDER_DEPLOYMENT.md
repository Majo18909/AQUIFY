# 🚀 Desplegar AQUIFY en Render.com

## ¿Por qué Render?

- ✅ **Archivos grandes**: Hasta 100MB (vs 4MB en Vercel)
- ✅ **Almacenamiento persistente**: Los archivos NO se borran
- ✅ **Plan gratuito**: 750 horas/mes gratis
- ✅ **Siempre activo**: Opción de mantener el servidor despierto

---

## 📋 Paso 1: Preparar el repositorio

Tu repositorio ya está listo en:
```
https://github.com/Majo18909/AQUIFY.git
```

Los archivos necesarios ya están incluidos:
- ✅ `requirements.txt`
- ✅ `app.py`
- ✅ `Procfile` (para Render)

---

## 🌐 Paso 2: Crear cuenta en Render

1. Ve a: **https://render.com**
2. Haz clic en **"Get Started"** o **"Sign Up"**
3. Selecciona **"Sign up with GitHub"**
4. Autoriza a Render para acceder a tu GitHub

---

## ⚙️ Paso 3: Crear Web Service

1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio:
   - Haz clic en **"Connect a repository"**
   - Busca **"AQUIFY"**
   - Haz clic en **"Connect"**

---

## 🔧 Paso 4: Configurar el servicio

Completa el formulario con estos valores:

### Configuración básica:
- **Name**: `aquify` (o el nombre que prefieras)
- **Region**: `Oregon (US West)` (o el más cercano a ti)
- **Branch**: `main`
- **Root Directory**: (dejar vacío)

### Build & Deploy:
- **Runtime**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  gunicorn app:app
  ```

### Plan:
- Selecciona **"Free"** (750 horas/mes gratis)

---

## 🎯 Paso 5: Variables de entorno (Opcional)

Si quieres, puedes agregar:

1. Haz clic en **"Advanced"**
2. Agrega estas variables de entorno:

| Variable | Valor |
|----------|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `SECRET_KEY` | `aquify-render-2024-secret-key` |

---

## 🚀 Paso 6: Deploy

1. Haz clic en **"Create Web Service"**
2. Render automáticamente:
   - ✅ Clonará tu repositorio
   - ✅ Instalará las dependencias
   - ✅ Iniciará el servidor
3. **Espera 3-5 minutos** para el primer deploy

---

## ✅ Paso 7: Verificar el deployment

1. Cuando termine, verás: **"Live"** con un ✅ verde
2. Tu URL será algo como:
   ```
   https://aquify.onrender.com
   ```
3. **Haz clic en el enlace** para abrir tu app

---

## 🎵 Paso 8: Probar subida de música

1. Abre tu app en Render
2. Crea tu perfil
3. Ve a la pestaña **"Música"**
4. **Sube tu archivo** In_The_Morning.mp3 (7.1 MB)
5. ✅ ¡Debería funcionar sin problemas!

---

## 🔄 Auto-deployment (Actualización automática)

**Render auto-deploya automáticamente** cuando haces `git push`:

```bash
# Hacer cambios en tu código
git add .
git commit -m "Descripción de cambios"
git push

# Render detecta el push y redespliega automáticamente (1-2 min)
```

---

## ⚙️ Mantener el servicio activo

El plan gratuito de Render **hiberna después de 15 minutos** sin actividad.

### Opción 1: UptimeRobot (Recomendado)

1. Ve a: **https://uptimerobot.com**
2. Crea cuenta gratuita
3. Agrega un nuevo monitor:
   - **Type**: HTTP(s)
   - **URL**: `https://aquify.onrender.com`
   - **Monitoring Interval**: 5 minutes
4. ✅ Esto hará ping cada 5 min y mantendrá el servidor activo

### Opción 2: Upgrade a plan de pago

- **$7/mes**: Sin hibernación, siempre activo

---

## 📊 Comparación: Render vs Vercel

| Feature | Render | Vercel |
|---------|--------|--------|
| **Tamaño máximo** | 100MB | 4MB |
| **Almacenamiento** | Persistente | Temporal |
| **Hibernación** | Sí (15 min) | No |
| **Auto-deploy** | ✅ Sí | ✅ Sí |
| **Plan gratuito** | 750h/mes | Ilimitado |
| **Mejor para** | Archivos grandes | Demos rápidas |

---

## 🆘 Solución de problemas

### El build falla

**Error**: `ModuleNotFoundError`
- **Solución**: Verifica que `requirements.txt` tenga todas las dependencias
- Ejecuta: `pip freeze > requirements.txt`

### La app no inicia

**Error**: `Application failed to respond`
- **Solución**: Verifica el **Start Command**
- Debe ser: `gunicorn app:app`

### Errores en los logs

1. Ve a tu servicio en Render
2. Haz clic en **"Logs"**
3. Busca errores en rojo
4. Copia el error y búscalo en Google

---

## 🎉 ¡Listo!

Ahora tienes AQUIFY funcionando en Render con:
- ✅ Archivos de hasta 100MB
- ✅ Almacenamiento persistente
- ✅ Auto-deployment desde GitHub
- ✅ URL pública para compartir

**URL de tu app**: `https://aquify.onrender.com` (o el nombre que elegiste)

---

## 📝 Notas adicionales

### Actualizar la app:

```bash
# 1. Hacer cambios en tu código
# 2. Subir a GitHub
git add .
git commit -m "Nuevas funcionalidades"
git push

# 3. Render auto-despliega en 1-2 minutos
```

### Ver logs en tiempo real:

1. Dashboard de Render
2. Tu servicio → **"Logs"**
3. Verás todos los requests y errores

### Borrar el servicio:

1. Dashboard → Tu servicio
2. **"Settings"** → Scroll hasta abajo
3. **"Delete Web Service"**

---

**¿Necesitas ayuda?** Revisa la documentación oficial:
- https://render.com/docs/web-services
- https://render.com/docs/deploy-flask

🎵 ¡Disfruta tu app AQUIFY! 💧
