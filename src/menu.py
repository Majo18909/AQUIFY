# -*- coding: utf-8 -*-
"""
Menú principal de AQUIFY
"""

import sys
from .colores import Colores, limpiar_pantalla
from .usuario import Usuario
from .gestor_musica import GestorMusica
from .chatbot import Chatbot
from .temporizador import InterfazTemporizador
from .reproductor import ReproductorMusica

class MenuPrincipal:
    """Menú principal de la aplicación AQUIFY"""
    
    def __init__(self):
        self.usuario = Usuario()
        self.gestor_musica = GestorMusica()
        self.chatbot = Chatbot(self.usuario)
        self.temporizadores = InterfazTemporizador()
        self.reproductor = ReproductorMusica(self.gestor_musica)
    
    def mostrar_banner(self):
        """Muestra el banner de AQUIFY"""
        print(f"\n{Colores.AZUL_PRIMARIO}{'='*60}")
        print(f"{Colores.VERDE_PRIMARIO}")
        print(r"     █████╗  ██████╗ ██╗   ██╗██╗███████╗██╗   ██╗")
        print(r"    ██╔══██╗██╔═══██╗██║   ██║██║██╔════╝╚██╗ ██╔╝")
        print(r"    ███████║██║   ██║██║   ██║██║█████╗   ╚████╔╝ ")
        print(r"    ██╔══██║██║▄▄ ██║██║   ██║██║██╔══╝    ╚██╔╝  ")
        print(r"    ██║  ██║╚██████╔╝╚██████╔╝██║██║        ██║   ")
        print(r"    ╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝╚═╝        ╚═╝   ")
        print(f"{Colores.AZUL_CLARO}")
        print(f"{'🎵 Tu Compañero Musical para el Baño 💧':^60}")
        print(f"{Colores.AZUL_PRIMARIO}{'='*60}{Colores.RESET}\n")
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        print(f"\n{Colores.TITULO}╔{'═'*58}╗")
        print(f"║{' MENÚ PRINCIPAL ':^58}║")
        print(f"╚{'═'*58}╝{Colores.RESET}\n")
        
        # Estado del perfil
        if self.usuario.existe_perfil():
            print(f"{Colores.EXITO}✓ Perfil creado{Colores.RESET}")
        else:
            print(f"{Colores.ADVERTENCIA}⚠ Sin perfil (crea uno para acceder a todas las funciones){Colores.RESET}")
        
        print()
        
        # Opciones del menú
        opciones = [
            ("👤 Perfil de Usuario", "1"),
            ("🎵 Gestión de Música", "2"),
            ("🤖 Asistente Chatbot", "3"),
            ("▶️ Reproducir con Rutina", "4"),
            ("🎼 Reproducir Música", "5"),
            ("⏱️ Temporizador", "6"),
            ("⏲️ Cronómetro", "7"),
            ("❌ Salir", "0")
        ]
        
        for texto, numero in opciones:
            print(f"{Colores.OPCION}{numero}.{Colores.RESET} {texto}")
    
    def menu_perfil(self):
        """Submenú de perfil de usuario"""
        while True:
            print(f"\n{Colores.TITULO}{'='*50}")
            print(f"{'👤 PERFIL DE USUARIO':^50}")
            print(f"{'='*50}{Colores.RESET}\n")
            
            if self.usuario.existe_perfil():
                print(f"{Colores.OPCION}1.{Colores.RESET} Ver perfil")
                print(f"{Colores.OPCION}2.{Colores.RESET} Crear nuevo perfil")
                print(f"{Colores.OPCION}0.{Colores.RESET} Volver")
                
                opcion = input(f"\n{Colores.MENU}Selecciona una opción: {Colores.RESET}").strip()
                
                if opcion == '1':
                    self.usuario.mostrar_perfil()
                    input(f"\n{Colores.INFO}Presiona Enter para continuar...{Colores.RESET}")
                elif opcion == '2':
                    confirmar = input(f"{Colores.ADVERTENCIA}¿Sobrescribir perfil actual? (s/n): {Colores.RESET}").strip().lower()
                    if confirmar == 's':
                        self.usuario.crear_perfil()
                        input(f"\n{Colores.INFO}Presiona Enter para continuar...{Colores.RESET}")
                elif opcion == '0':
                    break
            else:
                print(f"{Colores.INFO}No tienes un perfil creado aún{Colores.RESET}\n")
                print(f"{Colores.OPCION}1.{Colores.RESET} Crear perfil")
                print(f"{Colores.OPCION}0.{Colores.RESET} Volver")
                
                opcion = input(f"\n{Colores.MENU}Selecciona una opción: {Colores.RESET}").strip()
                
                if opcion == '1':
                    self.usuario.crear_perfil()
                    input(f"\n{Colores.INFO}Presiona Enter para continuar...{Colores.RESET}")
                elif opcion == '0':
                    break
    
    def menu_musica(self):
        """Submenú de gestión de música"""
        while True:
            print(f"\n{Colores.TITULO}{'='*50}")
            print(f"{'🎵 GESTIÓN DE MÚSICA':^50}")
            print(f"{'='*50}{Colores.RESET}\n")
            
            print(f"{Colores.OPCION}1.{Colores.RESET} Agregar canción")
            print(f"{Colores.OPCION}2.{Colores.RESET} Ver playlist")
            print(f"{Colores.OPCION}3.{Colores.RESET} Eliminar canción")
            print(f"{Colores.OPCION}0.{Colores.RESET} Volver")
            
            opcion = input(f"\n{Colores.MENU}Selecciona una opción: {Colores.RESET}").strip()
            
            if opcion == '1':
                self.gestor_musica.agregar_cancion()
                input(f"\n{Colores.INFO}Presiona Enter para continuar...{Colores.RESET}")
            elif opcion == '2':
                self.gestor_musica.listar_canciones()
                input(f"\n{Colores.INFO}Presiona Enter para continuar...{Colores.RESET}")
            elif opcion == '3':
                self.gestor_musica.eliminar_cancion()
                input(f"\n{Colores.INFO}Presiona Enter para continuar...{Colores.RESET}")
            elif opcion == '0':
                break
    
    def ejecutar(self):
        """Ejecuta el menú principal"""
        while True:
            limpiar_pantalla()
            self.mostrar_banner()
            self.mostrar_menu()
            
            opcion = input(f"\n{Colores.MENU}Selecciona una opción: {Colores.RESET}").strip()
            
            if opcion == '1':
                self.menu_perfil()
            elif opcion == '2':
                self.menu_musica()
            elif opcion == '3':
                self.chatbot.ejecutar()
            elif opcion == '4':
                self.reproductor.reproducir_con_rutina(self.usuario, self.chatbot)
                input(f"\n{Colores.INFO}Presiona Enter para continuar...{Colores.RESET}")
            elif opcion == '5':
                self.reproductor.reproducir_simple()
                input(f"\n{Colores.INFO}Presiona Enter para continuar...{Colores.RESET}")
            elif opcion == '6':
                self.temporizadores.menu_temporizador()
                input(f"\n{Colores.INFO}Presiona Enter para continuar...{Colores.RESET}")
            elif opcion == '7':
                self.temporizadores.menu_cronometro()
                input(f"\n{Colores.INFO}Presiona Enter para continuar...{Colores.RESET}")
            elif opcion == '0':
                print(f"\n{Colores.VERDE_PRIMARIO}¡Gracias por usar AQUIFY! 🎵💧{Colores.RESET}\n")
                sys.exit(0)
            else:
                print(f"{Colores.ERROR}Opción inválida{Colores.RESET}")
                input(f"{Colores.INFO}Presiona Enter para continuar...{Colores.RESET}")
