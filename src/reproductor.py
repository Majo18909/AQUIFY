# -*- coding: utf-8 -*-
"""
Reproductor de música para AQUIFY
"""

import os
import sys
import time
import threading
try:
    import pygame
    PYGAME_DISPONIBLE = True
except ImportError:
    PYGAME_DISPONIBLE = False

from .colores import Colores
from .temporizador import Temporizador

class ReproductorMusica:
    """Reproductor de música integrado con temporizador"""
    
    def __init__(self, gestor_musica):
        self.gestor_musica = gestor_musica
        self.cancion_actual = None
        self.reproduciendo = False
        self.pausado = False
        self.temporizador = Temporizador()
        
        if PYGAME_DISPONIBLE:
            pygame.mixer.init()
        else:
            print(f"{Colores.ADVERTENCIA}⚠️ pygame no está instalado. El reproductor tendrá funcionalidad limitada.{Colores.RESET}")
            print(f"{Colores.INFO}Para usar el reproductor, instala pygame: pip install pygame{Colores.RESET}")
    
    def reproducir_con_rutina(self, usuario, chatbot):
        """Reproduce música con temporizador basado en la rutina del usuario"""
        if not PYGAME_DISPONIBLE:
            print(f"\n{Colores.ERROR}El reproductor requiere pygame instalado{Colores.RESET}")
            return
        
        if not self.gestor_musica.tiene_canciones():
            print(f"\n{Colores.ADVERTENCIA}No hay canciones en la playlist{Colores.RESET}")
            return
        
        if not usuario.existe_perfil():
            print(f"\n{Colores.ADVERTENCIA}Primero debes crear un perfil de usuario{Colores.RESET}")
            return
        
        # Seleccionar canción
        self.gestor_musica.listar_canciones()
        
        try:
            opcion = input(f"\n{Colores.MENU}Selecciona una canción: {Colores.RESET}").strip()
            indice = int(opcion) - 1
            
            cancion = self.gestor_musica.obtener_cancion(indice)
            if not cancion:
                print(f"{Colores.ERROR}Opción inválida{Colores.RESET}")
                return
            
            # Obtener tiempo de rutina
            tipo_piel = usuario.obtener_tipo_piel()
            tiempo_rutina = chatbot.obtener_tiempo_rutina(tipo_piel)
            
            print(f"\n{Colores.INFO}Tiempo de rutina sugerido: {tiempo_rutina} minutos{Colores.RESET}")
            personalizar = input(f"{Colores.MENU}¿Usar este tiempo? (s/n): {Colores.RESET}").strip().lower()
            
            if personalizar == 'n':
                tiempo_str = input(f"{Colores.MENU}Tiempo en minutos: {Colores.RESET}").strip()
                try:
                    tiempo_rutina = int(tiempo_str)
                except ValueError:
                    print(f"{Colores.ERROR}Tiempo inválido, usando tiempo sugerido{Colores.RESET}")
            
            # Reproducir
            self._reproducir_cancion(cancion, tiempo_rutina)
            
        except ValueError:
            print(f"{Colores.ERROR}Por favor ingresa un número válido{Colores.RESET}")
        except KeyboardInterrupt:
            self.detener()
            print(f"\n{Colores.INFO}Reproducción detenida{Colores.RESET}")
    
    def _reproducir_cancion(self, cancion, tiempo_minutos):
        """Reproduce una canción con temporizador"""
        try:
            pygame.mixer.music.load(cancion['ruta'])
            self.cancion_actual = cancion
            self.reproduciendo = True
            self.pausado = False
            
            print(f"\n{Colores.EXITO}🎵 Reproduciendo: {cancion['nombre']}{Colores.RESET}")
            print(f"{Colores.INFO}⏱️ Tiempo de rutina: {tiempo_minutos} minutos{Colores.RESET}")
            print(f"{Colores.INFO}La música se detendrá automáticamente al finalizar el tiempo{Colores.RESET}\n")
            print(f"{Colores.ADVERTENCIA}Presiona Ctrl+C para detener{Colores.RESET}\n")
            
            # Iniciar reproducción en loop
            pygame.mixer.music.play(-1)  # -1 para loop infinito
            
            # Iniciar temporizador
            def callback_fin():
                self._pausar_por_temporizador()
            
            self.temporizador.iniciar(tiempo_minutos, callback_fin)
            
            # Monitorear reproducción
            try:
                while self.temporizador.esta_activo() and self.reproduciendo:
                    tiempo_restante = self.temporizador.obtener_tiempo_restante()
                    estado = "⏸️ PAUSADO" if self.pausado else "▶️ REPRODUCIENDO"
                    
                    print(f"\r{Colores.VERDE_PRIMARIO}{estado}{Colores.RESET} | "
                          f"{Colores.INFO}Tiempo restante: {tiempo_restante}{Colores.RESET}  ", 
                          end='', flush=True)
                    
                    time.sleep(0.5)
                
                print()  # Nueva línea
                
            except KeyboardInterrupt:
                self.detener()
                print(f"\n\n{Colores.INFO}Reproducción detenida manualmente{Colores.RESET}")
            
        except Exception as e:
            print(f"\n{Colores.ERROR}Error al reproducir: {e}{Colores.RESET}")
            self.reproduciendo = False
    
    def _pausar_por_temporizador(self):
        """Pausa la música cuando el temporizador termina"""
        if self.reproduciendo and PYGAME_DISPONIBLE:
            pygame.mixer.music.pause()
            self.pausado = True
            print(f"\n\n{Colores.ADVERTENCIA}⏰ ¡TIEMPO DE RUTINA COMPLETADO!{Colores.RESET}")
            print(f"{Colores.EXITO}La música se ha pausado automáticamente{Colores.RESET}")
    
    def reproducir_simple(self):
        """Reproduce una canción sin temporizador"""
        if not PYGAME_DISPONIBLE:
            print(f"\n{Colores.ERROR}El reproductor requiere pygame instalado{Colores.RESET}")
            return
        
        if not self.gestor_musica.tiene_canciones():
            print(f"\n{Colores.ADVERTENCIA}No hay canciones en la playlist{Colores.RESET}")
            return
        
        self.gestor_musica.listar_canciones()
        
        try:
            opcion = input(f"\n{Colores.MENU}Selecciona una canción: {Colores.RESET}").strip()
            indice = int(opcion) - 1
            
            cancion = self.gestor_musica.obtener_cancion(indice)
            if not cancion:
                print(f"{Colores.ERROR}Opción inválida{Colores.RESET}")
                return
            
            pygame.mixer.music.load(cancion['ruta'])
            self.cancion_actual = cancion
            self.reproduciendo = True
            self.pausado = False
            
            print(f"\n{Colores.EXITO}🎵 Reproduciendo: {cancion['nombre']}{Colores.RESET}")
            print(f"{Colores.ADVERTENCIA}Presiona Ctrl+C para detener{Colores.RESET}\n")
            
            pygame.mixer.music.play(-1)
            
            try:
                while pygame.mixer.music.get_busy() or self.pausado:
                    estado = "⏸️ PAUSADO" if self.pausado else "▶️ REPRODUCIENDO"
                    print(f"\r{Colores.VERDE_PRIMARIO}{estado}{Colores.RESET}  ", end='', flush=True)
                    time.sleep(0.5)
            except KeyboardInterrupt:
                self.detener()
                print(f"\n\n{Colores.INFO}Reproducción detenida{Colores.RESET}")
            
        except ValueError:
            print(f"{Colores.ERROR}Por favor ingresa un número válido{Colores.RESET}")
        except Exception as e:
            print(f"\n{Colores.ERROR}Error al reproducir: {e}{Colores.RESET}")
    
    def pausar(self):
        """Pausa la reproducción"""
        if PYGAME_DISPONIBLE and self.reproduciendo and not self.pausado:
            pygame.mixer.music.pause()
            self.pausado = True
            return True
        return False
    
    def reanudar(self):
        """Reanuda la reproducción"""
        if PYGAME_DISPONIBLE and self.reproduciendo and self.pausado:
            pygame.mixer.music.unpause()
            self.pausado = False
            return True
        return False
    
    def detener(self):
        """Detiene la reproducción"""
        if PYGAME_DISPONIBLE and self.reproduciendo:
            pygame.mixer.music.stop()
            self.reproduciendo = False
            self.pausado = False
            self.cancion_actual = None
            self.temporizador.detener()
            return True
        return False
