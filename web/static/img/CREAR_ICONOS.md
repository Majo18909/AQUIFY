# Iconos para PWA - AQUIFY

Para que AQUIFY funcione como PWA y puedas subirla a Play Store, necesitas crear 2 iconos:

## Iconos requeridos:

### 1. icon-192.png (192x192 píxeles)
- Usa el logo de AQUIFY
- Fondo del mismo color teal: #205462
- Nombre del archivo: `icon-192.png`

### 2. icon-512.png (512x512 píxeles)
- Misma imagen pero en tamaño más grande
- Fondo del mismo color teal: #205462
- Nombre del archivo: `icon-512.png`

## Cómo crearlos:

### Opción 1 - Online (MÁS FÁCIL):
1. Ve a: https://www.pwabuilder.com/imageGenerator
2. Sube tu logo `aquify-header.png`
3. Descarga los iconos generados
4. Renombra a `icon-192.png` e `icon-512.png`
5. Guárdalos en esta carpeta

### Opción 2 - Photoshop/GIMP/Canva:
1. Crea un documento de 512x512px
2. Fondo color #205462
3. Pega tu logo centrado
4. Exporta como PNG: `icon-512.png`
5. Reduce a 192x192px y exporta: `icon-192.png`

### Opción 3 - Usar imagen existente:
Si tu `aquify-header.png` tiene buena calidad:
1. Redimensiónala a 512x512px (cuadrada)
2. Guárdala como `icon-512.png`
3. Redimensiona a 192x192px
4. Guárdala como `icon-192.png`

## Una vez que tengas los iconos:
Guárdalos en: `c:\Users\Erika\AQUIFFY\web\static\img\`

Luego ejecuta:
```
git add web/static/img/icon-192.png web/static/img/icon-512.png
git commit -m "Add: Iconos PWA para Play Store"
git push
```
