# -*- coding: utf-8 -*-
"""
Sistema de usuario para AQUIFY
"""

import json
import os
from datetime import datetime
from .colores import Colores

class Usuario:
    """Clase para gestionar el perfil del usuario"""
    
    GENEROS = {
        '1': 'Hombre',
        '2': 'Mujer',
        '3': 'Personalizado',
        '4': 'Prefiero no decirlo'
    }
    
    TIPOS_PIEL = {
        '1': 'Normal',
        '2': 'Seca',
        '3': 'Mixta',
        '4': 'Grasa',
        '5': 'Sensible',
        '6': 'No sé'
    }
    
    def __init__(self):
        self.datos_dir = 'datos'
        self.usuario_file = os.path.join(self.datos_dir, 'usuario.json')
        self.perfil = None
        self._cargar_perfil()
    
    def _cargar_perfil(self):
        """Carga el perfil del usuario desde archivo"""
        if not os.path.exists(self.datos_dir):
            os.makedirs(self.datos_dir)
        
        if os.path.exists(self.usuario_file):
            try:
                with open(self.usuario_file, 'r', encoding='utf-8') as f:
                    self.perfil = json.load(f)
            except Exception as e:
                print(f"{Colores.ERROR}Error al cargar perfil: {e}{Colores.RESET}")
                self.perfil = None
    
    def _guardar_perfil(self):
        """Guarda el perfil del usuario en archivo"""
        try:
            with open(self.usuario_file, 'w', encoding='utf-8') as f:
                json.dump(self.perfil, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"{Colores.ERROR}Error al guardar perfil: {e}{Colores.RESET}")
            return False
    
    def existe_perfil(self):
        """Verifica si existe un perfil de usuario"""
        return self.perfil is not None
    
    def crear_perfil(self):
        """Crea un nuevo perfil de usuario"""
        print(f"\n{Colores.TITULO}{'='*50}")
        print(f"{'CREAR PERFIL DE USUARIO':^50}")
        print(f"{'='*50}{Colores.RESET}\n")
        
        # Selección de género
        print(f"{Colores.SUBTITULO}Selecciona tu género:{Colores.RESET}")
        for key, value in self.GENEROS.items():
            print(f"{Colores.OPCION}{key}.{Colores.RESET} {value}")
        
        genero_key = input(f"\n{Colores.MENU}Opción: {Colores.RESET}").strip()
        
        if genero_key not in self.GENEROS:
            print(f"{Colores.ERROR}Opción inválida{Colores.RESET}")
            return False
        
        genero = self.GENEROS[genero_key]
        genero_personalizado = None
        pronombres = None
        
        if genero_key == '3':  # Personalizado
            genero_personalizado = input(f"{Colores.MENU}Especifica tu género: {Colores.RESET}").strip()
            pronombres = input(f"{Colores.MENU}Pronombres preferidos: {Colores.RESET}").strip()
        
        # Edad
        print(f"\n{Colores.SUBTITULO}Edad:{Colores.RESET}")
        edad_str = input(f"{Colores.MENU}Ingresa tu edad: {Colores.RESET}").strip()
        
        try:
            edad = int(edad_str)
            if edad < 1 or edad > 120:
                print(f"{Colores.ERROR}Edad inválida{Colores.RESET}")
                return False
        except ValueError:
            print(f"{Colores.ERROR}Por favor ingresa un número válido{Colores.RESET}")
            return False
        
        # Tipo de piel
        print(f"\n{Colores.SUBTITULO}Selecciona tu tipo de piel:{Colores.RESET}")
        for key, value in self.TIPOS_PIEL.items():
            print(f"{Colores.OPCION}{key}.{Colores.RESET} {value}")
        
        piel_key = input(f"\n{Colores.MENU}Opción: {Colores.RESET}").strip()
        
        if piel_key not in self.TIPOS_PIEL:
            print(f"{Colores.ERROR}Opción inválida{Colores.RESET}")
            return False
        
        tipo_piel = self.TIPOS_PIEL[piel_key]
        
        # Crear perfil
        self.perfil = {
            'genero': genero,
            'genero_personalizado': genero_personalizado,
            'pronombres': pronombres,
            'edad': edad,
            'tipo_piel': tipo_piel,
            'fecha_creacion': datetime.now().isoformat()
        }
        
        if self._guardar_perfil():
            print(f"\n{Colores.EXITO}✓ Perfil creado exitosamente{Colores.RESET}")
            return True
        
        return False
    
    def mostrar_perfil(self):
        """Muestra el perfil del usuario"""
        if not self.perfil:
            print(f"{Colores.ADVERTENCIA}No hay perfil creado{Colores.RESET}")
            return
        
        print(f"\n{Colores.TITULO}{'='*50}")
        print(f"{'TU PERFIL':^50}")
        print(f"{'='*50}{Colores.RESET}\n")
        
        genero_display = self.perfil['genero']
        if self.perfil.get('genero_personalizado'):
            genero_display = self.perfil['genero_personalizado']
        
        print(f"{Colores.SUBTITULO}Género:{Colores.RESET} {genero_display}")
        
        if self.perfil.get('pronombres'):
            print(f"{Colores.SUBTITULO}Pronombres:{Colores.RESET} {self.perfil['pronombres']}")
        
        print(f"{Colores.SUBTITULO}Edad:{Colores.RESET} {self.perfil['edad']} años")
        print(f"{Colores.SUBTITULO}Tipo de piel:{Colores.RESET} {self.perfil['tipo_piel']}")
        
        fecha = datetime.fromisoformat(self.perfil['fecha_creacion'])
        print(f"\n{Colores.INFO}Perfil creado el: {fecha.strftime('%d/%m/%Y')}{Colores.RESET}")
    
    def obtener_tipo_piel(self):
        """Retorna el tipo de piel del usuario"""
        if self.perfil:
            return self.perfil.get('tipo_piel', 'No especificado')
        return 'No especificado'
    
    def obtener_edad(self):
        """Retorna la edad del usuario"""
        if self.perfil:
            return self.perfil.get('edad', 0)
        return 0
