# -*- coding: utf-8 -*-
"""
Temporizador y cronómetro para AQUIFY
"""

import time
import threading
from datetime import datetime, timedelta
from .colores import Colores

class Temporizador:
    """Clase para temporizador con cuenta regresiva"""
    
    def __init__(self):
        self.activo = False
        self.pausado = False
        self.tiempo_restante = 0
        self.thread = None
        self.callback_fin = None
    
    def iniciar(self, minutos, callback_fin=None):
        """Inicia el temporizador con duración en minutos"""
        if self.activo:
            print(f"{Colores.ADVERTENCIA}El temporizador ya está activo{Colores.RESET}")
            return False
        
        self.tiempo_restante = minutos * 60
        self.activo = True
        self.pausado = False
        self.callback_fin = callback_fin
        
        self.thread = threading.Thread(target=self._ejecutar, daemon=True)
        self.thread.start()
        
        return True
    
    def _ejecutar(self):
        """Ejecuta la cuenta regresiva"""
        while self.tiempo_restante > 0 and self.activo:
            if not self.pausado:
                time.sleep(1)
                self.tiempo_restante -= 1
            else:
                time.sleep(0.1)
        
        if self.activo and self.tiempo_restante <= 0:
            self.activo = False
            if self.callback_fin:
                self.callback_fin()
    
    def pausar(self):
        """Pausa el temporizador"""
        if self.activo and not self.pausado:
            self.pausado = True
            return True
        return False
    
    def reanudar(self):
        """Reanuda el temporizador"""
        if self.activo and self.pausado:
            self.pausado = False
            return True
        return False
    
    def detener(self):
        """Detiene el temporizador"""
        if self.activo:
            self.activo = False
            self.pausado = False
            self.tiempo_restante = 0
            return True
        return False
    
    def obtener_tiempo_restante(self):
        """Obtiene el tiempo restante en formato mm:ss"""
        minutos = self.tiempo_restante // 60
        segundos = self.tiempo_restante % 60
        return f"{minutos:02d}:{segundos:02d}"
    
    def esta_activo(self):
        """Verifica si el temporizador está activo"""
        return self.activo
    
    def esta_pausado(self):
        """Verifica si el temporizador está pausado"""
        return self.pausado


class Cronometro:
    """Clase para cronómetro con cuenta progresiva"""
    
    def __init__(self):
        self.activo = False
        self.pausado = False
        self.tiempo_transcurrido = 0
        self.tiempo_inicio = None
        self.tiempo_pausa = 0
        self.thread = None
    
    def iniciar(self):
        """Inicia el cronómetro"""
        if self.activo:
            print(f"{Colores.ADVERTENCIA}El cronómetro ya está activo{Colores.RESET}")
            return False
        
        self.tiempo_transcurrido = 0
        self.tiempo_pausa = 0
        self.tiempo_inicio = time.time()
        self.activo = True
        self.pausado = False
        
        self.thread = threading.Thread(target=self._ejecutar, daemon=True)
        self.thread.start()
        
        return True
    
    def _ejecutar(self):
        """Ejecuta la cuenta progresiva"""
        while self.activo:
            if not self.pausado:
                time.sleep(0.1)
            else:
                time.sleep(0.1)
    
    def pausar(self):
        """Pausa el cronómetro"""
        if self.activo and not self.pausado:
            self.pausado = True
            self.tiempo_pausa = time.time()
            return True
        return False
    
    def reanudar(self):
        """Reanuda el cronómetro"""
        if self.activo and self.pausado:
            pausa_duracion = time.time() - self.tiempo_pausa
            self.tiempo_inicio += pausa_duracion
            self.pausado = False
            return True
        return False
    
    def detener(self):
        """Detiene el cronómetro"""
        if self.activo:
            self.activo = False
            self.pausado = False
            return True
        return False
    
    def obtener_tiempo_transcurrido(self):
        """Obtiene el tiempo transcurrido en formato hh:mm:ss"""
        if not self.activo:
            return "00:00:00"
        
        if self.pausado:
            tiempo_actual = self.tiempo_pausa
        else:
            tiempo_actual = time.time()
        
        transcurrido = int(tiempo_actual - self.tiempo_inicio)
        horas = transcurrido // 3600
        minutos = (transcurrido % 3600) // 60
        segundos = transcurrido % 60
        
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    
    def esta_activo(self):
        """Verifica si el cronómetro está activo"""
        return self.activo
    
    def esta_pausado(self):
        """Verifica si el cronómetro está pausado"""
        return self.pausado


class InterfazTemporizador:
    """Interfaz de usuario para temporizador y cronómetro"""
    
    def __init__(self):
        self.temporizador = Temporizador()
        self.cronometro = Cronometro()
    
    def menu_temporizador(self):
        """Menú para el temporizador"""
        print(f"\n{Colores.TITULO}{'='*50}")
        print(f"{'⏱️ TEMPORIZADOR':^50}")
        print(f"{'='*50}{Colores.RESET}\n")
        
        minutos_str = input(f"{Colores.MENU}Tiempo en minutos: {Colores.RESET}").strip()
        
        try:
            minutos = int(minutos_str)
            if minutos <= 0:
                print(f"{Colores.ERROR}El tiempo debe ser mayor a 0{Colores.RESET}")
                return
            
            print(f"\n{Colores.EXITO}⏱️ Temporizador iniciado por {minutos} minuto(s){Colores.RESET}")
            
            def callback_fin():
                print(f"\n{Colores.ADVERTENCIA}⏰ ¡TIEMPO TERMINADO!{Colores.RESET}")
            
            self.temporizador.iniciar(minutos, callback_fin)
            
            # Interfaz de control
            while self.temporizador.esta_activo():
                print(f"\r{Colores.INFO}Tiempo restante: {self.temporizador.obtener_tiempo_restante()}{Colores.RESET}", end='', flush=True)
                
                time.sleep(0.5)
            
            print()  # Nueva línea después de terminar
            
        except ValueError:
            print(f"{Colores.ERROR}Por favor ingresa un número válido{Colores.RESET}")
    
    def menu_cronometro(self):
        """Menú para el cronómetro"""
        print(f"\n{Colores.TITULO}{'='*50}")
        print(f"{'⏱️ CRONÓMETRO':^50}")
        print(f"{'='*50}{Colores.RESET}\n")
        
        print(f"{Colores.EXITO}⏱️ Cronómetro iniciado{Colores.RESET}")
        print(f"{Colores.INFO}Presiona Ctrl+C para detener{Colores.RESET}\n")
        
        self.cronometro.iniciar()
        
        try:
            while self.cronometro.esta_activo():
                print(f"\r{Colores.INFO}Tiempo: {self.cronometro.obtener_tiempo_transcurrido()}{Colores.RESET}", end='', flush=True)
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.cronometro.detener()
            print(f"\n\n{Colores.EXITO}⏱️ Cronómetro detenido: {self.cronometro.obtener_tiempo_transcurrido()}{Colores.RESET}")
    
    def obtener_temporizador(self):
        """Retorna la instancia del temporizador"""
        return self.temporizador
    
    def obtener_cronometro(self):
        """Retorna la instancia del cronómetro"""
        return self.cronometro
