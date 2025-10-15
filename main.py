# main.py
"""
AUTOCORRECTOR GLOBAL DE TILDES
Aplicación de escritorio para corrección automática de tildes en Windows

Autor: [Tu Nombre]
Versión: 1.0.0
"""

import sys
import os
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

# Importar módulos del proyecto
from core.dictionary_manager import DictionaryManager
from core.autocorrect_engine import AutocorrectEngine
from core.keyboard_listener import KeyboardListener
from ui.main_window import MainWindow
from ui.tray_icon import TrayIcon
from config.config_manager import ConfigManager


class AutocorrectorApp:
    """Clase principal de la aplicación"""
    
    def __init__(self):
        # Inicializar QApplication
        self.qt_app = QApplication(sys.argv)
        self.qt_app.setApplicationName("Autocorrector de Tildes")
        
        # Inicializar componentes
        self.config = ConfigManager()
        self.dict_manager = DictionaryManager()
        self.engine = AutocorrectEngine(self.dict_manager)
        self.listener = KeyboardListener(self.engine)
        
        # Configurar listener callback
        self.listener.set_toggle_callback(self.on_toggle_from_hotkey)
        
        # Interfaz gráfica
        self.main_window = MainWindow(
            self.dict_manager,
            self.engine,
            self.listener,
            self.config
        )
        
        # Icono de bandeja
        self.tray_icon = TrayIcon(self.engine)
        self.tray_icon.set_callbacks(
            on_show=self.show_window,
            on_quit=self.quit_app
        )
        
        # Conectar señal de cierre de ventana
        self.main_window.close_signal.connect(self.on_window_close)
        
        # Estado
        self.window_visible = False
        self.minimized_mode = False
    
    def show_first_run_dialog(self):
        """Muestra diálogo informativo en primera ejecución"""
        msg = QMessageBox()
        msg.setWindowTitle("Bienvenido al Autocorrector de Tildes")
        msg.setIcon(QMessageBox.Icon.Information)
        
        text = """
        <h3>¡Bienvenido!</h3>
        <p>Este programa te ayudará a escribir más rápido corrigiendo 
        automáticamente las palabras sin tilde.</p>
        
        <p><b>¿Cómo funciona?</b></p>
        <ul>
            <li>Escribe normalmente sin tildes</li>
            <li>El programa detecta las palabras y las corrige automáticamente</li>
            <li>Funciona en cualquier aplicación de Windows</li>
        </ul>
        
        <p><b>Privacidad:</b></p>
        <p>El programa necesita leer las teclas que presionas para poder 
        corregir las palabras, pero NO almacena ni transmite ningún dato. 
        Todo el procesamiento es local en tu computadora.</p>
        
        <p><b>Atajo rápido:</b> Usa <b>Ctrl+Shift+A</b> para activar/desactivar 
        el corrector en cualquier momento.</p>
        """
        
        msg.setText(text)
        msg.exec()
        
        self.config.mark_first_run_complete()
    
    def ask_background_mode(self):
        """Pregunta si desea ejecutar en segundo plano"""
        if not self.config.get_setting('ask_background_on_startup', True):
            return self.config.get_setting('run_in_background', True)
        
        msg = QMessageBox()
        msg.setWindowTitle("Modo de Ejecución")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText(
            "¿Deseas ejecutar el autocorrector en segundo plano?\n\n"
            "Si eliges SÍ, el programa se ejecutará minimizado en la bandeja "
            "del sistema. Podrás acceder a él haciendo clic en el icono."
        )
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | 
            QMessageBox.StandardButton.No
        )
        msg.setDefaultButton(QMessageBox.StandardButton.Yes)
        
        result = msg.exec()
        return result == QMessageBox.StandardButton.Yes
    
    def start(self):
        """Inicia la aplicación"""
        # Verificar si es primera ejecución
        if self.config.is_first_run():
            self.show_first_run_dialog()
        
        # Iniciar listener de teclado
        self.listener.start()
        
        # Iniciar icono de bandeja
        self.tray_icon.start()
        
        # Decidir si mostrar ventana o minimizar
        if '--minimized' in sys.argv or self.ask_background_mode():
            self.minimized_mode = True
            self.engine.activate()
            self.tray_icon.update_icon()
        else:
            self.show_window()
        
        # Ejecutar aplicación
        sys.exit(self.qt_app.exec())
    
    def show_window(self):
        """Muestra la ventana principal"""
        if not self.window_visible:
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()
            self.window_visible = True
    
    def hide_window(self):
        """Oculta la ventana principal"""
        if self.window_visible:
            self.main_window.hide()
            self.window_visible = False
    
    def on_window_close(self):
        """Callback cuando se cierra la ventana"""
        # En lugar de cerrar, minimizar a bandeja
        self.hide_window()
        
        # Mostrar notificación
        if self.tray_icon.icon:
            self.tray_icon.icon.notify(
                "Autocorrector de Tildes",
                "La aplicación sigue ejecutándose en segundo plano"
            )
    
    def on_toggle_from_hotkey(self, new_state):
        """Callback cuando se usa el hotkey para toggle"""
        # Actualizar icono de bandeja
        self.tray_icon.update_icon()
        
        # Actualizar UI si está visible
        if self.window_visible:
            self.main_window.toggle_btn.setChecked(new_state)
            if new_state:
                self.main_window.status_label.setText("● ACTIVO")
                self.main_window.status_label.setStyleSheet("color: #27ae60;")
            else:
                self.main_window.status_label.setText("● INACTIVO")
                self.main_window.status_label.setStyleSheet("color: #e74c3c;")
        
        # Notificación
        if self.tray_icon.icon:
            status = "activado" if new_state else "desactivado"
            self.tray_icon.icon.notify(
                "Autocorrector",
                f"Corrector {status}"
            )
    
    def quit_app(self):
        """Cierra completamente la aplicación"""
        # Detener listener
        self.listener.stop()
        
        # Cerrar ventana
        self.main_window.close()
        
        # Salir de Qt
        self.qt_app.quit()


def main():
    """Punto de entrada principal"""
    try:
        # Verificar que se ejecuta en Windows
        if sys.platform != 'win32':
            print("Error: Esta aplicación solo funciona en Windows")
            sys.exit(1)
        
        # Crear y ejecutar aplicación
        app = AutocorrectorApp()
        app.start()
        
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()