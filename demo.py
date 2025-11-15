# -*- coding: utf-8 -*-
"""
Script de demostración de AQUIFY
Este script muestra las capacidades de la aplicación sin necesidad de interacción
"""

from src.colores import Colores

def mostrar_demo():
    """Muestra información sobre AQUIFY"""
    
    print(f"{Colores.AZUL_PRIMARIO}{'='*70}")
    print(f"{Colores.VERDE_PRIMARIO}")
    print(r"        █████╗  ██████╗ ██╗   ██╗██╗███████╗██╗   ██╗")
    print(r"       ██╔══██╗██╔═══██╗██║   ██║██║██╔════╝╚██╗ ██╔╝")
    print(r"       ███████║██║   ██║██║   ██║██║█████╗   ╚████╔╝ ")
    print(r"       ██╔══██║██║▄▄ ██║██║   ██║██║██╔══╝    ╚██╔╝  ")
    print(r"       ██║  ██║╚██████╔╝╚██████╔╝██║██║        ██║   ")
    print(r"       ╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝╚═╝        ╚═╝   ")
    print(f"{Colores.AZUL_CLARO}")
    print(f"{'🎵 Tu Compañero Musical para el Baño 💧':^70}")
    print(f"{Colores.AZUL_PRIMARIO}{'='*70}{Colores.RESET}\n")
    
    print(f"{Colores.TITULO}BIENVENIDO A AQUIFY{Colores.RESET}\n")
    
    print(f"{Colores.SUBTITULO}📋 FUNCIONALIDADES PRINCIPALES:{Colores.RESET}\n")
    
    funciones = [
        ("👤 PERFIL DE USUARIO", [
            "Selecciona tu género (con opción personalizada y pronombres)",
            "Ingresa tu edad",
            "Define tu tipo de piel (Normal, Seca, Mixta, Grasa, Sensible)"
        ]),
        ("🎵 GESTIÓN DE MÚSICA", [
            "Sube archivos MP3, WAV, OGG, FLAC, M4A",
            "Organiza tu playlist personal",
            "Elimina canciones que ya no uses"
        ]),
        ("🤖 CHATBOT ASISTENTE", [
            "Consulta rutinas de baño especializadas según tu tipo de piel",
            "Crea rutinas personalizadas paso a paso",
            "Recibe recomendaciones de música relajante",
            "Obtén consejos para el cuidado de tu piel"
        ]),
        ("▶️ REPRODUCTOR INTELIGENTE", [
            "Reproduce música con temporizador automático",
            "La música se pausa cuando termina tu rutina",
            "Modo de reproducción libre disponible"
        ]),
        ("⏱️ TEMPORIZADOR Y CRONÓMETRO", [
            "Temporizador personalizable en minutos",
            "Cronómetro para medir actividades específicas",
            "Integración perfecta con el reproductor"
        ])
    ]
    
    for titulo, items in funciones:
        print(f"{Colores.VERDE_PRIMARIO}{titulo}{Colores.RESET}")
        for item in items:
            print(f"  {Colores.AZUL_CLARO}•{Colores.RESET} {item}")
        print()
    
    print(f"{Colores.TITULO}⏱️ TIEMPOS DE RUTINA SUGERIDOS:{Colores.RESET}\n")
    
    tiempos = [
        ("Piel Normal", "7 minutos"),
        ("Piel Seca", "9 minutos"),
        ("Piel Mixta", "8 minutos"),
        ("Piel Grasa", "7 minutos"),
        ("Piel Sensible", "8 minutos")
    ]
    
    for tipo, tiempo in tiempos:
        print(f"  {Colores.VERDE_CLARO}•{Colores.RESET} {tipo}: {Colores.INFO}{tiempo}{Colores.RESET}")
    
    print(f"\n{Colores.TITULO}🎨 PALETA DE COLORES:{Colores.RESET}\n")
    print(f"  Verde: #00CC57 #0A8A46 #BFEFD6 #DFF7EA")
    print(f"  Azul: #B4E9FA #C7EEFA #0077C8 #084A6F #2EB7FF #E6F9FF")
    print(f"  Neutros: #FFFFFF #FBFCFE #F3F9FF")
    
    print(f"\n{Colores.TITULO}🚀 CÓMO EMPEZAR:{Colores.RESET}\n")
    print(f"  {Colores.OPCION}1.{Colores.RESET} Ejecuta: {Colores.INFO}python main.py{Colores.RESET}")
    print(f"  {Colores.OPCION}2.{Colores.RESET} Crea tu perfil de usuario")
    print(f"  {Colores.OPCION}3.{Colores.RESET} Agrega tus canciones favoritas")
    print(f"  {Colores.OPCION}4.{Colores.RESET} Consulta el chatbot para tu rutina ideal")
    print(f"  {Colores.OPCION}5.{Colores.RESET} ¡Disfruta de tu baño con música perfectamente sincronizada!")
    
    print(f"\n{Colores.EXITO}✓ La aplicación está lista para usar{Colores.RESET}")
    print(f"{Colores.INFO}📖 Lee GUIA_USO.md para más detalles{Colores.RESET}\n")
    
    print(f"{Colores.AZUL_PRIMARIO}{'='*70}{Colores.RESET}\n")

if __name__ == "__main__":
    mostrar_demo()
