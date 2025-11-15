# -*- coding: utf-8 -*-
"""
Configuración de colores para AQUIFY
"""

from colorama import Fore, Back, Style, init

# Inicializar colorama para Windows
init(autoreset=True)

class Colores:
    """Colores de la aplicación AQUIFY"""
    
    # Mapeo aproximado de los colores hex a colores ANSI disponibles
    VERDE_PRIMARIO = Fore.GREEN + Style.BRIGHT  # #00CC57
    VERDE_OSCURO = Fore.GREEN  # #0A8A46
    VERDE_CLARO = Fore.LIGHTGREEN_EX  # #BFEFD6, #DFF7EA
    
    AZUL_CLARO = Fore.LIGHTCYAN_EX  # #B4E9FA, #C7EEFA
    AZUL_PRIMARIO = Fore.CYAN + Style.BRIGHT  # #0077C8
    AZUL_OSCURO = Fore.BLUE  # #084A6F
    AZUL_BRILLANTE = Fore.LIGHTBLUE_EX  # #2EB7FF
    
    BLANCO = Fore.WHITE + Style.BRIGHT  # #FFFFFF
    GRIS_CLARO = Fore.LIGHTWHITE_EX  # #FBFCFE, #F3F9FF
    
    RESET = Style.RESET_ALL
    NEGRITA = Style.BRIGHT
    
    # Colores para estados
    ERROR = Fore.RED + Style.BRIGHT
    ADVERTENCIA = Fore.YELLOW + Style.BRIGHT
    EXITO = Fore.GREEN + Style.BRIGHT
    INFO = Fore.CYAN
    
    # Colores para secciones
    TITULO = AZUL_PRIMARIO + Style.BRIGHT
    SUBTITULO = VERDE_PRIMARIO
    MENU = BLANCO
    OPCION = AZUL_CLARO
    TEXTO = GRIS_CLARO

def limpiar_pantalla():
    """Limpia la pantalla de la terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

import os
