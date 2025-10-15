# config/config_manager.py
import json
import os
import sys
import winreg
from pathlib import Path

class ConfigManager:
    """Gestiona la configuración de la aplicación"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.config_dir = self.base_dir / "config"
        self.config_file = self.config_dir / "settings.json"
        
        self.settings = {}
        self.default_settings = {
            'hotkey': 'ctrl+shift+a',
            'start_with_windows': False,
            'run_in_background': True,
            'first_run': True,
            'ask_background_on_startup': True
        }
        
        self._ensure_config_file()
        self.load()
    
    def _ensure_config_file(self):
        """Crea el archivo de configuración si no existe"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.config_file.exists():
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.default_settings, f, ensure_ascii=False, indent=2)
    
    def load(self):
        """Carga la configuración desde el archivo"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
            
            # Asegurar que todas las claves por defecto existan
            for key, value in self.default_settings.items():
                if key not in self.settings:
                    self.settings[key] = value
            
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            self.settings = self.default_settings.copy()
    
    def save(self):
        """Guarda la configuración en el archivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            return False
    
    def get_setting(self, key, default=None):
        """Obtiene un valor de configuración"""
        return self.settings.get(key, default)
    
    def set_setting(self, key, value):
        """Establece un valor de configuración"""
        self.settings[key] = value
    
    def is_first_run(self):
        """Verifica si es la primera ejecución"""
        return self.get_setting('first_run', True)
    
    def mark_first_run_complete(self):
        """Marca que la primera ejecución se completó"""
        self.set_setting('first_run', False)
        self.save()
    
    def set_startup(self, enable=True):
        """
        Configura el inicio automático con Windows
        """
        app_name = "AutocorrectorTildes"
        
        try:
            # Obtener ruta del ejecutable
            if getattr(sys, 'frozen', False):
                # Si está compilado con PyInstaller
                exe_path = sys.executable
            else:
                # Si se ejecuta desde Python
                exe_path = os.path.abspath(sys.argv[0])
            
            # Acceder al registro de Windows
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0,
                winreg.KEY_SET_VALUE
            )
            
            if enable:
                # Agregar entrada al registro
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{exe_path}" --minimized')
            else:
                # Eliminar entrada del registro
                try:
                    winreg.DeleteValue(key, app_name)
                except FileNotFoundError:
                    pass  # La entrada no existe
            
            winreg.CloseKey(key)
            return True
            
        except Exception as e:
            print(f"Error configurando inicio automático: {e}")
            return False
    
    def is_startup_enabled(self):
        """
        Verifica si el inicio automático está habilitado
        """
        app_name = "AutocorrectorTildes"
        
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0,
                winreg.KEY_READ
            )
            
            try:
                value, _ = winreg.QueryValueEx(key, app_name)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
                
        except Exception as e:
            print(f"Error verificando inicio automático: {e}")
            return False