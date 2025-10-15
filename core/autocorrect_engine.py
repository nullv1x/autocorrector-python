# core/autocorrect_engine.py
import re
import time
import pyautogui
import pyperclip
from typing import Optional

class AutocorrectEngine:
    """Motor de autocorrección de palabras"""
    
    def __init__(self, dictionary_manager):
        self.dict_manager = dictionary_manager
        self.is_active = False
        self.last_word = ""
        self.correction_in_progress = False
        
        # Configuración de pyautogui
        pyautogui.PAUSE = 0.01  # Reducir delay entre acciones
        pyautogui.FAILSAFE = False
    
    def activate(self):
        """Activa el motor de corrección"""
        self.is_active = True
    
    def deactivate(self):
        """Desactiva el motor de corrección"""
        self.is_active = False
    
    def toggle(self) -> bool:
        """Alterna el estado del motor. Retorna el nuevo estado"""
        self.is_active = not self.is_active
        return self.is_active
    
    def get_last_word_from_clipboard(self) -> Optional[str]:
        """
        Intenta obtener la última palabra usando el portapapeles
        """
        try:
            # Guardar contenido actual del portapapeles
            original_clipboard = pyperclip.paste()
            
            # Seleccionar palabra anterior (Ctrl+Shift+Left)
            pyautogui.hotkey('ctrl', 'shift', 'left')
            time.sleep(0.05)
            
            # Copiar al portapapeles
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.05)
            
            # Obtener palabra
            word = pyperclip.paste()
            
            # Restaurar portapapeles original
            pyperclip.copy(original_clipboard)
            
            # Limpiar palabra
            word = word.strip()
            
            # Verificar que sea una palabra válida
            if word and re.match(r'^[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]+$', word):
                return word
            
            return None
            
        except Exception as e:
            print(f"[Error] Obteniendo palabra: {e}")
            return None
    
    def correct_word(self, word: str) -> bool:
        """
        Corrige una palabra si encuentra coincidencia en el diccionario
        Returns: True si se hizo corrección, False si no
        """
        if not word or self.correction_in_progress:
            return False
        
        corrected = self.dict_manager.get_corrected_word(word)
        
        # Si no hay cambio, no hacer nada
        if corrected == word:
            return False
        
        try:
            self.correction_in_progress = True
            
            # Seleccionar la palabra nuevamente
            pyautogui.hotkey('ctrl', 'shift', 'left')
            time.sleep(0.03)
            
            # Escribir palabra corregida
            pyautogui.write(corrected, interval=0.01)
            
            self.correction_in_progress = False
            return True
            
        except Exception as e:
            print(f"[Error] Corrigiendo palabra: {e}")
            self.correction_in_progress = False
            return False
    
    def process_trigger(self, event=None):
        """
        Procesa un trigger (espacio, enter, puntuación)
        Intenta corregir la última palabra escrita
        """
        if not self.is_active or self.correction_in_progress:
            return
        
        try:
            word = self.get_last_word_from_clipboard()
            
            if word:
                corrected = self.correct_word(word)
                if corrected:
                    print(f"Corregido: {word} → {self.dict_manager.get_corrected_word(word)}")
            
        except Exception as e:
            print(f"[Error] En process_trigger: {e}")
    
    def manual_correct_selection(self):
        """
        Corrige la selección actual manualmente
        Útil para corregir texto ya escrito
        """
        if self.correction_in_progress:
            return
        
        try:
            self.correction_in_progress = True
            
            # Guardar clipboard original
            original_clipboard = pyperclip.paste()
            
            # Copiar selección
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.05)
            
            selected_text = pyperclip.paste()
            if not selected_text:
                self.correction_in_progress = False
                return
            
            words = re.findall(r'[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]+', selected_text)
            corrected_text = selected_text
            
            for word in words:
                corrected = self.dict_manager.get_corrected_word(word)
                if corrected != word:
                    corrected_text = corrected_text.replace(word, corrected)
            
            # Si hubo cambios, reemplazar
            if corrected_text != selected_text:
                pyautogui.write(corrected_text, interval=0.01)
            
            # Restaurar clipboard
            pyperclip.copy(original_clipboard)
            
            self.correction_in_progress = False
            
        except Exception as e:
            print(f"[Error] En corrección manual: {e}")
            self.correction_in_progress = False
