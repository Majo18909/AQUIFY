# -*- coding: utf-8 -*-
"""
Chatbot asistente para AQUIFY
"""

import random
from .colores import Colores

class Chatbot:
    """Chatbot asistente con información sobre rutinas y la app"""
    
    def __init__(self, usuario=None):
        self.usuario = usuario
        self.rutinas_piel = {
            'Normal': {
                'rutina': [
                    "1. Enjuaga tu cuerpo con agua tibia (1 min)",
                    "2. Aplica gel de baño suave con movimientos circulares (2-3 min)",
                    "3. Enjuaga completamente (1 min)",
                    "4. Hidrata la piel después del baño (2 min)"
                ],
                'tiempo_total': 7,
                'consejos': [
                    "Usa agua tibia, no muy caliente",
                    "Seca con palmaditas, no frotes",
                    "Aplica crema hidratante mientras la piel está húmeda"
                ]
            },
            'Seca': {
                'rutina': [
                    "1. Enjuaga con agua tibia (1 min)",
                    "2. Usa gel de baño hidratante con aceites naturales (3-4 min)",
                    "3. Enjuaga suavemente (1 min)",
                    "4. Aplica aceite corporal o crema muy hidratante (3 min)"
                ],
                'tiempo_total': 9,
                'consejos': [
                    "Evita agua muy caliente que reseca la piel",
                    "Usa productos con glicerina, aceite de coco o manteca de karité",
                    "Hidrata inmediatamente después del baño",
                    "Considera usar un humidificador"
                ]
            },
            'Mixta': {
                'rutina': [
                    "1. Enjuaga con agua tibia (1 min)",
                    "2. Aplica gel balanceador en todo el cuerpo (2-3 min)",
                    "3. Usa exfoliante suave en zonas grasas 2 veces por semana (2 min)",
                    "4. Enjuaga completamente (1 min)",
                    "5. Hidratante ligero en zonas secas, tónico en zonas grasas (2 min)"
                ],
                'tiempo_total': 8,
                'consejos': [
                    "Balancea productos según la zona del cuerpo",
                    "No uses productos muy pesados",
                    "Presta atención a cómo reacciona cada área"
                ]
            },
            'Grasa': {
                'rutina': [
                    "1. Enjuaga con agua tibia-fresca (1 min)",
                    "2. Usa gel purificante o con ácido salicílico (2-3 min)",
                    "3. Exfolia suavemente 2-3 veces por semana (2 min)",
                    "4. Enjuaga con agua fresca (1 min)",
                    "5. Aplica loción oil-free ligera (1-2 min)"
                ],
                'tiempo_total': 7,
                'consejos': [
                    "Usa productos libres de aceite (oil-free)",
                    "No exfolies en exceso, puede producir más grasa",
                    "El agua fría ayuda a cerrar los poros",
                    "Lava tu toalla frecuentemente"
                ]
            },
            'Sensible': {
                'rutina': [
                    "1. Enjuaga con agua tibia (no caliente) (1 min)",
                    "2. Usa gel hipoalergénico sin fragancias (2-3 min)",
                    "3. Enjuaga muy bien para eliminar residuos (2 min)",
                    "4. Seca con palmaditas suaves (1 min)",
                    "5. Aplica crema calmante hipoalergénica (2 min)"
                ],
                'tiempo_total': 8,
                'consejos': [
                    "Evita productos con fragancias o colorantes",
                    "No uses esponjas ásperas",
                    "Prueba nuevos productos en pequeñas áreas primero",
                    "Busca productos con aloe vera o caléndula"
                ]
            },
            'No sé': {
                'rutina': [
                    "1. Enjuaga con agua tibia (1 min)",
                    "2. Aplica gel de baño suave (2-3 min)",
                    "3. Enjuaga bien (1 min)",
                    "4. Hidrata después del baño (2 min)"
                ],
                'tiempo_total': 7,
                'consejos': [
                    "Observa cómo reacciona tu piel",
                    "Si se siente tirante, puede ser seca",
                    "Si brilla mucho, puede ser grasa",
                    "Consulta a un dermatólogo para identificar tu tipo"
                ]
            }
        }
        
        self.canciones_recomendadas = [
            "Música relajante instrumental",
            "Lo-fi hip hop para estudiar/relajarse",
            "Sonidos de la naturaleza (lluvia, olas)",
            "Música clásica suave (Debussy, Chopin)",
            "Chill pop acústico",
            "Jazz suave",
            "Música ambient/atmospheric",
            "Indie folk tranquilo"
        ]
        
        self.funciones_app = {
            'perfil': "Crea y personaliza tu perfil con género, edad y tipo de piel",
            'musica': "Sube y gestiona tus canciones favoritas para el baño",
            'rutinas': "Obtén rutinas de baño personalizadas según tu tipo de piel",
            'temporizador': "Usa el temporizador para seguir tu rutina paso a paso",
            'cronometro': "Mide el tiempo de actividades específicas",
            'reproductor': "Escucha música que se ajusta automáticamente a tu rutina"
        }
    
    def ejecutar(self):
        """Interfaz principal del chatbot"""
        while True:
            print(f"\n{Colores.TITULO}{'='*50}")
            print(f"{'🤖 ASISTENTE AQUIFY':^50}")
            print(f"{'='*50}{Colores.RESET}\n")
            
            print(f"{Colores.SUBTITULO}¿En qué puedo ayudarte?{Colores.RESET}\n")
            print(f"{Colores.OPCION}1.{Colores.RESET} Ver funciones de la app")
            print(f"{Colores.OPCION}2.{Colores.RESET} Rutina de baño especializada")
            print(f"{Colores.OPCION}3.{Colores.RESET} Rutina personalizada")
            print(f"{Colores.OPCION}4.{Colores.RESET} Recomendaciones de música")
            print(f"{Colores.OPCION}5.{Colores.RESET} Consejos para tu tipo de piel")
            print(f"{Colores.OPCION}0.{Colores.RESET} Volver")
            
            opcion = input(f"\n{Colores.MENU}Selecciona una opción: {Colores.RESET}").strip()
            
            if opcion == '1':
                self._mostrar_funciones()
            elif opcion == '2':
                self._mostrar_rutina_especializada()
            elif opcion == '3':
                self._crear_rutina_personalizada()
            elif opcion == '4':
                self._recomendar_musica()
            elif opcion == '5':
                self._mostrar_consejos()
            elif opcion == '0':
                break
            else:
                print(f"{Colores.ERROR}Opción inválida{Colores.RESET}")
            
            input(f"\n{Colores.INFO}Presiona Enter para continuar...{Colores.RESET}")
    
    def _mostrar_funciones(self):
        """Muestra las funciones de la aplicación"""
        print(f"\n{Colores.TITULO}{'='*50}")
        print(f"{'FUNCIONES DE AQUIFY':^50}")
        print(f"{'='*50}{Colores.RESET}\n")
        
        for nombre, descripcion in self.funciones_app.items():
            print(f"{Colores.VERDE_PRIMARIO}• {nombre.upper()}{Colores.RESET}")
            print(f"  {Colores.TEXTO}{descripcion}{Colores.RESET}\n")
    
    def _mostrar_rutina_especializada(self):
        """Muestra rutina basada en el perfil del usuario"""
        if not self.usuario or not self.usuario.existe_perfil():
            print(f"\n{Colores.ADVERTENCIA}Primero debes crear un perfil de usuario{Colores.RESET}")
            return
        
        tipo_piel = self.usuario.obtener_tipo_piel()
        rutina = self.rutinas_piel.get(tipo_piel)
        
        if not rutina:
            print(f"\n{Colores.ERROR}No se encontró rutina para tu tipo de piel{Colores.RESET}")
            return
        
        print(f"\n{Colores.TITULO}{'='*50}")
        print(f"{'RUTINA PARA PIEL ' + tipo_piel.upper():^50}")
        print(f"{'='*50}{Colores.RESET}\n")
        
        print(f"{Colores.SUBTITULO}Pasos de la rutina:{Colores.RESET}\n")
        for paso in rutina['rutina']:
            print(f"{Colores.BLANCO}{paso}{Colores.RESET}")
        
        print(f"\n{Colores.INFO}⏱️ Tiempo total aproximado: {rutina['tiempo_total']} minutos{Colores.RESET}\n")
        
        print(f"{Colores.SUBTITULO}Consejos adicionales:{Colores.RESET}\n")
        for consejo in rutina['consejos']:
            print(f"{Colores.VERDE_CLARO}✓ {consejo}{Colores.RESET}")
    
    def _crear_rutina_personalizada(self):
        """Crea una rutina personalizada"""
        print(f"\n{Colores.TITULO}{'='*50}")
        print(f"{'CREAR RUTINA PERSONALIZADA':^50}")
        print(f"{'='*50}{Colores.RESET}\n")
        
        print(f"{Colores.INFO}Vamos a crear una rutina paso a paso{Colores.RESET}\n")
        
        pasos = []
        tiempo_total = 0
        
        while True:
            print(f"\n{Colores.SUBTITULO}Paso {len(pasos) + 1}:{Colores.RESET}")
            descripcion = input(f"{Colores.MENU}Descripción del paso (Enter para terminar): {Colores.RESET}").strip()
            
            if not descripcion:
                break
            
            tiempo_str = input(f"{Colores.MENU}Tiempo en minutos: {Colores.RESET}").strip()
            
            try:
                tiempo = int(tiempo_str)
                pasos.append({'descripcion': descripcion, 'tiempo': tiempo})
                tiempo_total += tiempo
                print(f"{Colores.EXITO}✓ Paso agregado{Colores.RESET}")
            except ValueError:
                print(f"{Colores.ERROR}Tiempo inválido, paso no agregado{Colores.RESET}")
        
        if pasos:
            print(f"\n{Colores.TITULO}{'='*50}")
            print(f"{'TU RUTINA PERSONALIZADA':^50}")
            print(f"{'='*50}{Colores.RESET}\n")
            
            for i, paso in enumerate(pasos, 1):
                print(f"{Colores.BLANCO}{i}. {paso['descripcion']} ({paso['tiempo']} min){Colores.RESET}")
            
            print(f"\n{Colores.INFO}⏱️ Tiempo total: {tiempo_total} minutos{Colores.RESET}")
    
    def _recomendar_musica(self):
        """Recomienda géneros de música"""
        print(f"\n{Colores.TITULO}{'='*50}")
        print(f"{'🎵 RECOMENDACIONES DE MÚSICA':^50}")
        print(f"{'='*50}{Colores.RESET}\n")
        
        print(f"{Colores.SUBTITULO}Géneros recomendados para tu baño:{Colores.RESET}\n")
        
        for i, genero in enumerate(self.canciones_recomendadas, 1):
            print(f"{Colores.AZUL_CLARO}{i}. {genero}{Colores.RESET}")
        
        print(f"\n{Colores.INFO}💡 Tip: La música relajante ayuda a crear un ambiente tranquilo")
        print(f"{Colores.INFO}   y puede mejorar tu experiencia de baño.{Colores.RESET}")
    
    def _mostrar_consejos(self):
        """Muestra consejos para el tipo de piel del usuario"""
        if not self.usuario or not self.usuario.existe_perfil():
            print(f"\n{Colores.ADVERTENCIA}Primero debes crear un perfil de usuario{Colores.RESET}")
            return
        
        tipo_piel = self.usuario.obtener_tipo_piel()
        rutina = self.rutinas_piel.get(tipo_piel)
        
        if not rutina:
            print(f"\n{Colores.ERROR}No se encontraron consejos para tu tipo de piel{Colores.RESET}")
            return
        
        print(f"\n{Colores.TITULO}{'='*50}")
        print(f"{'CONSEJOS PARA PIEL ' + tipo_piel.upper():^50}")
        print(f"{'='*50}{Colores.RESET}\n")
        
        for consejo in rutina['consejos']:
            print(f"{Colores.VERDE_CLARO}✓ {consejo}{Colores.RESET}")
    
    def obtener_tiempo_rutina(self, tipo_piel):
        """Obtiene el tiempo total de rutina para un tipo de piel"""
        rutina = self.rutinas_piel.get(tipo_piel)
        if rutina:
            return rutina['tiempo_total']
        return 7  # Tiempo por defecto
