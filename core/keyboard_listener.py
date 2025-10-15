# core/keyboard_listener.py

import keyboard
import threading
from typing import Callable, Optional

class KeyboardListener:
    """Escucha eventos del teclado globalmente y ejecuta acciones según teclas configuradas."""
    
    def __init__(self, autocorrect_engine):
        self.engine = autocorrect_engine
        self.is_listening = False
        self.toggle_callback: Optional[Callable] = None
        self.hotkey = "ctrl+shift+a"
        self.trigger_handlers = []  # Para almacenar los manejadores de teclas

        # Teclas que activan la corrección
        self.trigger_keys = [
            'space', 'enter',
            '.', ',', ';', ':',
            '!', '?', ')', ']', '}',
            'tab'
        ]
    
    # -------------------------------
    # Configuración de callbacks
    # -------------------------------
    
    def set_toggle_callback(self, callback: Callable):
        """Establece el callback para cuando se active/desactive el autocorrector."""
        self.toggle_callback = callback
    
    def set_hotkey(self, hotkey: str):
        """
        Cambia la combinación de teclas para activar/desactivar el autocorrector.
        Formato: 'ctrl+shift+a', 'alt+t', etc.
        """
        if self.is_listening:
            # Eliminar el hotkey anterior si ya estaba escuchando
            try:
                keyboard.remove_hotkey(self.hotkey)
            except Exception as e:
                print(f"Advertencia al eliminar hotkey anterior: {e}")
        
        self.hotkey = hotkey.lower()
        
        if self.is_listening:
            # Registrar el nuevo hotkey
            keyboard.add_hotkey(self.hotkey, self._on_toggle_hotkey)
    
    # -------------------------------
    # Control del listener
    # -------------------------------
    
    def start(self):
        """Inicia la escucha del teclado."""
        if self.is_listening:
            return
        
        try:
            # Registrar hotkey para toggle
            keyboard.add_hotkey(self.hotkey, self._on_toggle_hotkey)
            
            # Registrar triggers de corrección y guardar los handlers
            for key in self.trigger_keys:
                handler = keyboard.on_press_key(key, self._on_trigger_key, suppress=False)
                self.trigger_handlers.append(handler)
            
            self.is_listening = True
            print(f"✓ Listener iniciado. Hotkey: {self.hotkey}")
            
        except Exception as e:
            print(f"Error iniciando listener: {e}")
    
    def stop(self):
        """Detiene la escucha del teclado."""
        if not self.is_listening:
            return
        
        try:
            # Desregistrar hotkey
            try:
                keyboard.remove_hotkey(self.hotkey)
            except Exception as e:
                print(f"Advertencia al eliminar hotkey: {e}")
            
            # Desregistrar triggers
            for handler in self.trigger_handlers:
                try:
                    keyboard.unhook(handler)
                except Exception as e:
                    print(f"Advertencia al desregistrar handler: {e}")
            
            self.trigger_handlers.clear()
            self.is_listening = False
            print("✓ Listener detenido")
            
        except Exception as e:
            print(f"Error deteniendo listener: {e}")
    
    # -------------------------------
    # Callbacks de eventos
    # -------------------------------
    
    def _on_toggle_hotkey(self):
        """Callback cuando se presiona el hotkey de toggle."""
        try:
            new_state = self.engine.toggle()
            
            if self.toggle_callback:
                self.toggle_callback(new_state)
            
            print(f"Autocorrector: {'ACTIVADO' if new_state else 'DESACTIVADO'}")
        except Exception as e:
            print(f"Error en toggle hotkey: {e}")
    
    def _on_trigger_key(self, event):
        """
        Callback cuando se presiona una tecla trigger.
        Se ejecuta en un hilo separado para no bloquear la escritura.
        """
        if not getattr(self.engine, "is_active", False):
            return
        
        try:
            # Lanzar la corrección en un thread separado
            thread = threading.Thread(
                target=self.engine.process_trigger,
                args=(event,),  # Se pasa el evento por si se usa
                daemon=True
            )
            thread.start()
        except Exception as e:
            print(f"Error ejecutando trigger: {e}")
    
    # -------------------------------
    # Utilidades
    # -------------------------------
    
    def is_valid_hotkey(self, hotkey: str) -> bool:
        """Valida si una combinación de teclas es válida."""
        try:
            keyboard.parse_hotkey(hotkey)
            return True
        except Exception:
            return False
