# -*- coding: utf-8 -*-
"""
Gestor de música para AQUIFY
"""

import os
import json
import shutil
from pathlib import Path
from .colores import Colores

class GestorMusica:
    """Clase para gestionar archivos de música"""
    
    FORMATOS_PERMITIDOS = ['.mp3', '.wav', '.ogg', '.flac', '.m4a']
    
    def __init__(self):
        self.musica_dir = 'musica'
        self.playlist_file = os.path.join('datos', 'playlist.json')
        self.playlist = []
        self._inicializar()
    
    def _inicializar(self):
        """Inicializa directorios y carga playlist"""
        if not os.path.exists(self.musica_dir):
            os.makedirs(self.musica_dir)
        
        if not os.path.exists('datos'):
            os.makedirs('datos')
        
        self._cargar_playlist()
    
    def _cargar_playlist(self):
        """Carga la playlist desde archivo"""
        if os.path.exists(self.playlist_file):
            try:
                with open(self.playlist_file, 'r', encoding='utf-8') as f:
                    self.playlist = json.load(f)
            except Exception as e:
                print(f"{Colores.ERROR}Error al cargar playlist: {e}{Colores.RESET}")
                self.playlist = []
    
    def _guardar_playlist(self):
        """Guarda la playlist en archivo"""
        try:
            with open(self.playlist_file, 'w', encoding='utf-8') as f:
                json.dump(self.playlist, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"{Colores.ERROR}Error al guardar playlist: {e}{Colores.RESET}")
            return False
    
    def agregar_cancion(self):
        """Permite al usuario agregar una canción desde su sistema"""
        print(f"\n{Colores.TITULO}{'='*50}")
        print(f"{'AGREGAR CANCIÓN':^50}")
        print(f"{'='*50}{Colores.RESET}\n")
        
        ruta_archivo = input(f"{Colores.MENU}Ruta del archivo de música: {Colores.RESET}").strip()
        
        # Limpiar comillas si las hay
        ruta_archivo = ruta_archivo.strip('"').strip("'")
        
        if not os.path.exists(ruta_archivo):
            print(f"{Colores.ERROR}El archivo no existe{Colores.RESET}")
            return False
        
        # Verificar extensión
        extension = Path(ruta_archivo).suffix.lower()
        if extension not in self.FORMATOS_PERMITIDOS:
            print(f"{Colores.ERROR}Formato no permitido. Formatos aceptados: {', '.join(self.FORMATOS_PERMITIDOS)}{Colores.RESET}")
            return False
        
        # Nombre personalizado
        nombre_archivo = Path(ruta_archivo).name
        print(f"\n{Colores.INFO}Nombre actual: {nombre_archivo}{Colores.RESET}")
        nuevo_nombre = input(f"{Colores.MENU}Nuevo nombre (Enter para mantener): {Colores.RESET}").strip()
        
        if nuevo_nombre:
            if not nuevo_nombre.endswith(extension):
                nuevo_nombre += extension
            nombre_archivo = nuevo_nombre
        
        # Copiar archivo
        destino = os.path.join(self.musica_dir, nombre_archivo)
        
        try:
            shutil.copy2(ruta_archivo, destino)
            
            # Agregar a playlist
            cancion = {
                'nombre': Path(nombre_archivo).stem,
                'archivo': nombre_archivo,
                'ruta': destino,
                'duracion': 0  # Se puede calcular con librerías especializadas
            }
            
            self.playlist.append(cancion)
            self._guardar_playlist()
            
            print(f"\n{Colores.EXITO}✓ Canción agregada exitosamente{Colores.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colores.ERROR}Error al copiar archivo: {e}{Colores.RESET}")
            return False
    
    def listar_canciones(self):
        """Lista todas las canciones disponibles"""
        if not self.playlist:
            print(f"\n{Colores.ADVERTENCIA}No hay canciones en la playlist{Colores.RESET}")
            return
        
        print(f"\n{Colores.TITULO}{'='*50}")
        print(f"{'TU PLAYLIST':^50}")
        print(f"{'='*50}{Colores.RESET}\n")
        
        for i, cancion in enumerate(self.playlist, 1):
            print(f"{Colores.OPCION}{i}.{Colores.RESET} {Colores.BLANCO}{cancion['nombre']}{Colores.RESET}")
            print(f"   {Colores.INFO}Archivo: {cancion['archivo']}{Colores.RESET}")
    
    def eliminar_cancion(self):
        """Elimina una canción de la playlist"""
        if not self.playlist:
            print(f"\n{Colores.ADVERTENCIA}No hay canciones para eliminar{Colores.RESET}")
            return False
        
        self.listar_canciones()
        
        try:
            opcion = input(f"\n{Colores.MENU}Número de canción a eliminar (0 para cancelar): {Colores.RESET}").strip()
            indice = int(opcion) - 1
            
            if indice == -1:
                return False
            
            if 0 <= indice < len(self.playlist):
                cancion = self.playlist[indice]
                
                # Eliminar archivo
                if os.path.exists(cancion['ruta']):
                    os.remove(cancion['ruta'])
                
                # Eliminar de playlist
                self.playlist.pop(indice)
                self._guardar_playlist()
                
                print(f"\n{Colores.EXITO}✓ Canción eliminada{Colores.RESET}")
                return True
            else:
                print(f"{Colores.ERROR}Opción inválida{Colores.RESET}")
                return False
                
        except ValueError:
            print(f"{Colores.ERROR}Por favor ingresa un número válido{Colores.RESET}")
            return False
    
    def obtener_cancion(self, indice):
        """Obtiene una canción por índice"""
        if 0 <= indice < len(self.playlist):
            return self.playlist[indice]
        return None
    
    def tiene_canciones(self):
        """Verifica si hay canciones en la playlist"""
        return len(self.playlist) > 0
