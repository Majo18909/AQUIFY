# ⏰ Configurar UptimeRobot para AQUIFY en Render

## ¿Qué hace UptimeRobot?

UptimeRobot hace "ping" a tu app cada 5 minutos para:
- ✅ **Mantener tu app activa** (evita que Render la hiberne)
- ✅ **Monitorear disponibilidad** (te avisa si la app se cae)
- ✅ **100% gratis** (hasta 50 monitores)

---

## 🚀 Guía paso a paso

### Paso 1: Crear cuenta en UptimeRobot

1. Ve a: **https://uptimerobot.com**
2. Haz clic en **"Free Sign Up"**
3. Completa el formulario:
   - **Email**: Tu correo electrónico
   - **Password**: Una contraseña segura
4. Haz clic en **"Sign Up"**
5. **Verifica tu email** (revisa tu bandeja de entrada)
6. Haz clic en el enlace de verificación

---

### Paso 2: Crear un Monitor

1. **Inicia sesión** en https://uptimerobot.com
2. Serás redirigido al **Dashboard**
3. Haz clic en **"+ Add New Monitor"** (botón verde)

---

### Paso 3: Configurar el Monitor

Completa el formulario con estos valores:

#### Monitor Type:
- Selecciona: **HTTP(s)**

#### Friendly Name:
```
AQUIFY - Render
```

#### URL (or IP):
```
https://aquify.onrender.com
```
⚠️ **Importante**: Usa la URL exacta que te dio Render cuando desplegaste

#### Monitoring Interval:
- Selecciona: **5 minutes** (opción gratuita)

#### Monitor Timeout:
- Deja el valor por defecto: **30 seconds**

#### Alert Contacts To Notify:
- Selecciona tu email (ya debería estar ahí)
- Opcional: Puedes agregar más contactos después

---

### Paso 4: Crear el Monitor

1. Revisa que la configuración sea correcta
2. Haz clic en **"Create Monitor"** (botón verde abajo)
3. ✅ ¡Monitor creado!

---

## ✅ Verificar que funciona

### En el Dashboard verás:

```
┌─────────────────────────────────────────┐
│ AQUIFY - Render                         │
│ Status: ● Up                            │
│ Uptime: 100%                            │
│ Last Check: hace 2 minutos              │
└─────────────────────────────────────────┘
```

### Interpretación de estados:

- **🟢 Up**: Tu app está funcionando correctamente
- **🔴 Down**: Tu app no responde (recibirás un email)
- **🟡 Paused**: Monitor pausado temporalmente

---

## 📊 Ver estadísticas

1. En el Dashboard, haz clic en el nombre del monitor: **"AQUIFY - Render"**
2. Verás gráficas con:
   - **Uptime %**: Porcentaje de disponibilidad
   - **Response Time**: Tiempo de respuesta
   - **Logs**: Historial de checks

---

## 📧 Configurar alertas

### Recibir notificaciones por email:

Ya está configurado por defecto. Recibirás un email cuando:
- ❌ La app se caiga
- ✅ La app se recupere

### Agregar más métodos de notificación:

1. Dashboard → **"My Settings"**
2. **"Alert Contacts"**
3. Puedes agregar:
   - Slack
   - Discord
   - Telegram
   - SMS (planes de pago)
   - Webhooks

---

## ⚙️ Configuración avanzada (Opcional)

### Cambiar el intervalo de monitoreo:

**Plan gratuito**: 5 minutos (mínimo)
**Plan Pro**: 1 minuto ($7/mes)

Para cambiar:
1. Dashboard → Haz clic en tu monitor
2. **"Edit"** → **"Monitoring Interval"**
3. Selecciona el nuevo intervalo
4. **"Save Changes"**

### Pausar el monitor temporalmente:

1. Dashboard → Haz clic en tu monitor
2. **"Pause"**
3. Para reanudar: **"Resume"**

---

## 🎯 Cómo funciona con Render

### Antes de UptimeRobot:
```
Usuario visita → App despierta (30 seg) → App responde
     ↓
15 min sin uso → Render hiberna la app
     ↓
Usuario visita → App despierta (30 seg) → App responde
```

### Con UptimeRobot:
```
UptimeRobot hace ping cada 5 min
     ↓
Render mantiene la app activa
     ↓
Usuario visita → App responde INMEDIATAMENTE ✅
```

---

## 📱 App Móvil (Opcional)

UptimeRobot tiene apps móviles:

- **iOS**: https://apps.apple.com/app/uptimerobot/id1104878581
- **Android**: https://play.google.com/store/apps/details?id=com.uptimerobot

Con la app puedes:
- Ver el estado de tus monitores
- Recibir notificaciones push
- Ver estadísticas en tiempo real

---

## 🆘 Solución de problemas

### El monitor muestra "Down"

**Posibles causas**:

1. **Tu app de Render está caída**
   - Revisa los logs en Render
   - Verifica que el deployment haya sido exitoso

2. **URL incorrecta**
   - Verifica que la URL sea exactamente: `https://aquify.onrender.com`
   - No pongas `www.` ni `/` al final

3. **Render está reiniciando**
   - Espera 2-3 minutos
   - El monitor debería volver a "Up"

### No recibo emails de alerta

1. **Revisa spam/promociones**
   - Los emails de UptimeRobot a veces van ahí

2. **Verifica tu email**
   - Dashboard → **"My Settings"** → **"Alert Contacts"**
   - Confirma que tu email está verificado

3. **Prueba el monitor**
   - Edita el monitor temporalmente con una URL falsa
   - Deberías recibir un email de "Down"
   - Vuelve a poner la URL correcta

---

## 💡 Consejos

### Mejores prácticas:

1. **Mantén el intervalo en 5 minutos**
   - Es suficiente para evitar hibernación
   - No sobrecarga tu app

2. **Revisa las estadísticas cada semana**
   - Te ayuda a identificar problemas
   - Puedes ver tendencias de disponibilidad

3. **Configura alertas en Slack/Discord**
   - Si trabajas en equipo
   - Respuesta más rápida que email

### Para múltiples ambientes:

Si tienes versiones de desarrollo y producción:

```
Monitor 1: AQUIFY - Producción (Render)
Monitor 2: AQUIFY - Desarrollo (localhost con ngrok)
Monitor 3: AQUIFY - Testing (Vercel)
```

---

## 📊 Dashboard personalizado

### Widget público:

1. Dashboard → Tu monitor → **"Get Widget"**
2. Copia el código HTML
3. Puedes ponerlo en tu README.md:

```markdown
[![Uptime Robot status](https://img.shields.io/uptimerobot/status/m123456789-abc123def456?label=AQUIFY)](https://aquify.onrender.com)
```

---

## 🎉 ¡Listo!

Ahora tienes:
- ✅ **App siempre activa** (sin esperas de 30 seg)
- ✅ **Monitoreo 24/7** de tu app
- ✅ **Alertas automáticas** si algo falla
- ✅ **Estadísticas** de disponibilidad

---

## 📝 Checklist final

- [ ] Cuenta creada en UptimeRobot
- [ ] Email verificado
- [ ] Monitor creado con URL de Render
- [ ] Intervalo configurado a 5 minutos
- [ ] Email de alerta configurado
- [ ] Monitor mostrando status "Up" 🟢
- [ ] Primera alerta de prueba recibida (opcional)

---

## 🔗 Enlaces útiles

- **UptimeRobot Dashboard**: https://uptimerobot.com/dashboard
- **Documentación**: https://uptimerobot.com/help
- **Status Page**: https://stats.uptimerobot.com
- **API Docs**: https://uptimerobot.com/api

---

**¿Preguntas?** Revisa la documentación oficial de UptimeRobot o busca en su centro de ayuda.

🎵 ¡Tu AQUIFY ahora está siempre lista! 💧
