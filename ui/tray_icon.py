# ui/tray_icon.py
import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item

class TrayIcon:
    """Gestiona el icono en la bandeja del sistema"""
    
    def __init__(self, autocorrect_engine):
        self.engine = autocorrect_engine
        self.icon = None
        self.is_running = False
        
        # Callbacks
        self.on_show_callback = None
        self.on_quit_callback = None
    
    def create_icon_image(self, active=False):
        """
        Crea una imagen para el icono de la bandeja
        active: si está activo (verde) o inactivo (rojo)
        """
        # Crear imagen 64x64
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Color según estado
        color = '#27ae60' if active else '#e74c3c'
        
        # Dibujar una tilde estilizada
        draw.ellipse([10, 10, 54, 54], outline=color, width=4)
        
        # Dibujar símbolo de tilde (´)
        draw.line([25, 35, 35, 25], fill=color, width=5)
        draw.line([35, 25, 40, 30], fill=color, width=5)
        
        return image
    
    def update_icon(self):
        """Actualiza el icono según el estado del motor"""
        if self.icon:
            self.icon.icon = self.create_icon_image(self.engine.is_active)
            self.icon.title = f"Autocorrector - {'Activo' if self.engine.is_active else 'Inactivo'}"
    
    def set_callbacks(self, on_show, on_quit):
        """Establece los callbacks para las acciones del menú"""
        self.on_show_callback = on_show
        self.on_quit_callback = on_quit
    
    def toggle_autocorrect(self, icon, item):
        """Toggle del autocorrector desde el menú"""
        self.engine.toggle()
        self.update_icon()
    
    def show_window(self, icon, item):
        """Muestra la ventana principal"""
        if self.on_show_callback:
            self.on_show_callback()
    
    def quit_app(self, icon, item):
        """Cierra la aplicación"""
        self.stop()
        if self.on_quit_callback:
            self.on_quit_callback()
    
    def create_menu(self):
        """Crea el menú contextual del icono"""
        return pystray.Menu(
            item(
                'Activar/Desactivar',
                self.toggle_autocorrect,
                default=True
            ),
            item(
                'Mostrar Ventana',
                self.show_window
            ),
            pystray.Menu.SEPARATOR,
            item(
                'Salir',
                self.quit_app
            )
        )
    
    def start(self):
        """Inicia el icono de bandeja"""
        if self.is_running:
            return
        
        # Crear icono
        self.icon = pystray.Icon(
            'autocorrector_tildes',
            self.create_icon_image(self.engine.is_active),
            'Autocorrector de Tildes',
            self.create_menu()
        )
        
        self.is_running = True
        
        # Ejecutar en thread separado
        self.icon.run_detached()
    
    def stop(self):
        """Detiene el icono de bandeja"""
        if self.icon and self.is_running:
            self.icon.stop()
            self.is_running = False