from PIL import Image
import os

# Ruta del logo original
logo_path = "web/static/img/aquify logo 3.png"
output_dir = "web/static/img"

# Cargar la imagen original
try:
    img = Image.open(logo_path)
    print(f"Imagen original cargada: {img.size}")
    
    # Tamaños necesarios para PWA
    sizes = [192, 512]
    
    for size in sizes:
        # Crear imagen cuadrada con fondo transparente
        icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # Redimensionar el logo manteniendo aspecto
        img_copy = img.copy()
        img_copy.thumbnail((size, size), Image.Resampling.LANCZOS)
        
        # Centrar el logo en el canvas cuadrado
        x = (size - img_copy.width) // 2
        y = (size - img_copy.height) // 2
        icon.paste(img_copy, (x, y), img_copy if img_copy.mode == 'RGBA' else None)
        
        # Guardar
        output_path = os.path.join(output_dir, f"icon-{size}x{size}.png")
        icon.save(output_path, "PNG")
        print(f"✓ Creado: {output_path}")
    
    print("\n¡Iconos creados exitosamente!")
    
except Exception as e:
    print(f"Error: {e}")
