# ui/main_window.py
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QTableWidget, 
    QTableWidgetItem, QMessageBox, QGroupBox, QComboBox,
    QCheckBox, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    close_signal = pyqtSignal()
    
    def __init__(self, dict_manager, autocorrect_engine, keyboard_listener, config_manager):
        super().__init__()
        self.dict_manager = dict_manager
        self.engine = autocorrect_engine
        self.listener = keyboard_listener
        self.config = config_manager
        
        self.init_ui()
        self.load_settings()
        self.populate_table()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("Autocorrector de Tildes")
        self.setMinimumSize(800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # === SECCIÓN: Control Principal ===
        control_group = self.create_control_section()
        main_layout.addWidget(control_group)
        
        # === SECCIÓN: Agregar Palabra ===
        add_word_group = self.create_add_word_section()
        main_layout.addWidget(add_word_group)
        
        # === SECCIÓN: Diccionario ===
        dict_group = self.create_dictionary_section()
        main_layout.addWidget(dict_group)
        
        # === SECCIÓN: Configuración ===
        config_group = self.create_config_section()
        main_layout.addWidget(config_group)
        
        # Aplicar estilos
        self.apply_styles()
    
    def create_control_section(self):
        """Crea la sección de control ON/OFF"""
        group = QGroupBox("Control Principal")
        layout = QHBoxLayout()
        
        # Botón ON/OFF
        self.toggle_btn = QPushButton("ACTIVAR")
        self.toggle_btn.setMinimumHeight(60)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.clicked.connect(self.toggle_autocorrector)
        
        # Indicador de estado
        self.status_label = QLabel("● INACTIVO")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_font = QFont()
        status_font.setPointSize(14)
        status_font.setBold(True)
        self.status_label.setFont(status_font)
        
        layout.addWidget(self.toggle_btn, 2)
        layout.addWidget(self.status_label, 1)
        
        group.setLayout(layout)
        return group
    
    def create_add_word_section(self):
        """Crea la sección para agregar palabras"""
        group = QGroupBox("Agregar Nueva Palabra")
        layout = QVBoxLayout()
        
        # Campos de entrada
        input_layout = QHBoxLayout()
        
        self.word_without_input = QLineEdit()
        self.word_without_input.setPlaceholderText("Palabra sin tilde (ej: camion)")
        
        self.word_with_input = QLineEdit()
        self.word_with_input.setPlaceholderText("Palabra con tilde (ej: camión)")
        
        self.add_btn = QPushButton("Agregar")
        self.add_btn.clicked.connect(self.add_word)
        self.add_btn.setMinimumWidth(120)
        
        input_layout.addWidget(QLabel("Sin tilde:"))
        input_layout.addWidget(self.word_without_input)
        input_layout.addWidget(QLabel("Con tilde:"))
        input_layout.addWidget(self.word_with_input)
        input_layout.addWidget(self.add_btn)
        
        layout.addLayout(input_layout)
        group.setLayout(layout)
        return group
    
    def create_dictionary_section(self):
        """Crea la sección del diccionario"""
        group = QGroupBox("Diccionario de Palabras")
        layout = QVBoxLayout()
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar palabra...")
        self.search_input.textChanged.connect(self.filter_table)
        
        self.delete_btn = QPushButton("Eliminar Seleccionada")
        self.delete_btn.clicked.connect(self.delete_word)
        
        search_layout.addWidget(QLabel("Buscar:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.delete_btn)
        
        # Tabla de palabras
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Sin Tilde", "Con Tilde", "Origen"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        
        # Contador de palabras
        self.word_count_label = QLabel()
        layout.addWidget(self.word_count_label)
        
        group.setLayout(layout)
        return group
    
    def create_config_section(self):
        """Crea la sección de configuración"""
        group = QGroupBox("Configuración")
        layout = QVBoxLayout()
        
        # Hotkey
        hotkey_layout = QHBoxLayout()
        hotkey_layout.addWidget(QLabel("Atajo de teclado:"))
        
        self.hotkey_combo = QComboBox()
        self.hotkey_combo.addItems([
            "ctrl+shift+a",
            "ctrl+shift+t",
            "ctrl+alt+a",
            "alt+shift+a",
            "ctrl+shift+z"
        ])
        self.hotkey_combo.currentTextChanged.connect(self.change_hotkey)
        
        hotkey_layout.addWidget(self.hotkey_combo)
        hotkey_layout.addStretch()
        
        # Checkbox: Iniciar con Windows
        self.startup_check = QCheckBox("Iniciar automáticamente con Windows")
        self.startup_check.stateChanged.connect(self.toggle_startup)
        
        # Checkbox: Ejecutar en segundo plano
        self.background_check = QCheckBox("Ejecutar en segundo plano al iniciar")
        self.background_check.stateChanged.connect(self.toggle_background)
        
        layout.addLayout(hotkey_layout)
        layout.addWidget(self.startup_check)
        layout.addWidget(self.background_check)
        
        group.setLayout(layout)
        return group
    
    def apply_styles(self):
        """Aplica estilos CSS a la interfaz"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2a5f8f;
            }
            QPushButton:checked {
                background-color: #27ae60;
            }
            QPushButton:checked:hover {
                background-color: #229954;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
            QTableWidget::item:selected {
                background-color: #4a90e2;
                color: white;
            }
            QHeaderView::section {
                background-color: #e8e8e8;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
    
    def toggle_autocorrector(self, checked):
        """Toggle del autocorrector"""
        if checked:
            self.engine.activate()
            self.toggle_btn.setText("DESACTIVAR")
            self.status_label.setText("● ACTIVO")
            self.status_label.setStyleSheet("color: #27ae60;")
        else:
            self.engine.deactivate()
            self.toggle_btn.setText("ACTIVAR")
            self.status_label.setText("● INACTIVO")
            self.status_label.setStyleSheet("color: #e74c3c;")
    
    def add_word(self):
        """Agrega una nueva palabra al diccionario"""
        word_without = self.word_without_input.text().strip()
        word_with = self.word_with_input.text().strip()
        
        if not word_without or not word_with:
            QMessageBox.warning(self, "Error", "Por favor completa ambos campos")
            return
        
        success, message = self.dict_manager.add_word(word_without, word_with)
        
        if success:
            QMessageBox.information(self, "Éxito", message)
            self.word_without_input.clear()
            self.word_with_input.clear()
            self.populate_table()
        else:
            QMessageBox.warning(self, "Error", message)
    
    def delete_word(self):
        """Elimina la palabra seleccionada"""
        current_row = self.table.currentRow()
        
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Por favor selecciona una palabra")
            return
        
        word_without = self.table.item(current_row, 0).text()
        origin = self.table.item(current_row, 2).text()
        
        if origin == "Sistema":
            QMessageBox.warning(self, "Error", 
                "No puedes eliminar palabras del diccionario base")
            return
        
        reply = QMessageBox.question(self, "Confirmar", 
            f"¿Eliminar la palabra '{word_without}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.dict_manager.remove_word(word_without)
            
            if success:
                self.populate_table()
                QMessageBox.information(self, "Éxito", message)
            else:
                QMessageBox.warning(self, "Error", message)
    
    def populate_table(self):
        """Llena la tabla con todas las palabras del diccionario"""
        words = self.dict_manager.get_all_words()
        
        self.table.setRowCount(0)
        self.table.setRowCount(len(words))
        
        for i, (word_without, (word_with, is_user)) in enumerate(sorted(words.items())):
            # Columna 1: Palabra sin tilde
            item_without = QTableWidgetItem(word_without)
            self.table.setItem(i, 0, item_without)
            
            # Columna 2: Palabra con tilde
            item_with = QTableWidgetItem(word_with)
            self.table.setItem(i, 1, item_with)
            
            # Columna 3: Origen
            origin = "Usuario" if is_user else "Sistema"
            item_origin = QTableWidgetItem(origin)
            
            if is_user:
                item_origin.setForeground(QColor("#27ae60"))
            else:
                item_origin.setForeground(QColor("#7f8c8d"))
            
            self.table.setItem(i, 2, item_origin)
        
        self.update_word_count()
    
    def filter_table(self, text):
        """Filtra la tabla según el texto de búsqueda"""
        for i in range(self.table.rowCount()):
            word_without = self.table.item(i, 0).text()
            word_with = self.table.item(i, 1).text()
            
            match = text.lower() in word_without.lower() or text.lower() in word_with.lower()
            self.table.setRowHidden(i, not match)
    
    def update_word_count(self):
        """Actualiza el contador de palabras"""
        total = self.table.rowCount()
        user_count = sum(1 for i in range(total) 
                        if self.table.item(i, 2).text() == "Usuario")
        
        self.word_count_label.setText(
            f"Total: {total} palabras ({user_count} personalizadas, "
            f"{total - user_count} del sistema)"
        )
    
    def change_hotkey(self, hotkey):
        """Cambia el atajo de teclado"""
        if self.listener.is_valid_hotkey(hotkey):
            self.listener.set_hotkey(hotkey)
            self.config.set_setting('hotkey', hotkey)
            self.config.save()
    
    def toggle_startup(self, state):
        """Activa/desactiva inicio automático con Windows"""
        enabled = state == Qt.CheckState.Checked.value
        self.config.set_setting('start_with_windows', enabled)
        self.config.save()
        self.config.set_startup(enabled)
    
    def toggle_background(self, state):
        """Activa/desactiva ejecución en segundo plano"""
        enabled = state == Qt.CheckState.Checked.value
        self.config.set_setting('run_in_background', enabled)
        self.config.save()
    
    def load_settings(self):
        """Carga la configuración guardada"""
        hotkey = self.config.get_setting('hotkey', 'ctrl+shift+a')
        index = self.hotkey_combo.findText(hotkey)
        if index >= 0:
            self.hotkey_combo.setCurrentIndex(index)
        
        self.startup_check.setChecked(
            self.config.get_setting('start_with_windows', False)
        )
        
        self.background_check.setChecked(
            self.config.get_setting('run_in_background', True)
        )
    
    def closeEvent(self, event):
        """Evento al cerrar la ventana"""
        self.close_signal.emit()
        event.accept()