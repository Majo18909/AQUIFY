#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AQUIFY - Aplicación de música para rutinas de baño
"""

import os
import sys
from src.menu import MenuPrincipal

def main():
    """Punto de entrada de la aplicación AQUIFY"""
    try:
        menu = MenuPrincipal()
        menu.ejecutar()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
