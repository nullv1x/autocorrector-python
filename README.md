# 🎯 Autocorrector Global de Tildes para Windows

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Aplicación de escritorio que corrige automáticamente palabras sin tilde en cualquier aplicación de Windows.**

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Configuración](#-configuración)
- [Compilar a EXE](#-compilar-a-exe)
- [Preguntas Frecuentes](#-preguntas-frecuentes)
- [Solución de Problemas](#-solución-de-problemas)

---

## ✨ Características

### 🔥 Funcionalidades Principales

- **Corrección Automática Global**: Funciona en cualquier aplicación de Windows (Word, navegadores, chat, etc.)
- **Diccionario Extensible**: Incluye cientos de palabras comunes y permite agregar palabras personalizadas
- **Interfaz Moderna**: GUI intuitiva y atractiva construida con PyQt6
- **Ejecución en Segundo Plano**: Se ejecuta minimizado en la bandeja del sistema
- **Atajos de Teclado**: Control rápido con hotkeys personalizables (por defecto: Ctrl+Shift+A)
- **Inicio Automático**: Opción para iniciar con Windows
- **Sin Conexión**: Todo el procesamiento es local, sin envío de datos a internet
- **Bajo Consumo**: Optimizado para funcionar eficientemente en segundo plano

### 🎨 Interfaz Gráfica

- Control ON/OFF con indicador visual
- Gestión completa del diccionario
- Búsqueda y filtrado de palabras
- Agregar/eliminar palabras personalizadas
- Configuración de atajos de teclado
- Icono en bandeja del sistema con menú contextual

---

## 💻 Requisitos

### Sistema Operativo
- Windows 10 o Windows 11
- Permisos de administrador (para interceptación de teclado global)

### Python
- Python 3.11 o superior

### Dependencias
Todas las dependencias están listadas en `requirements.txt`:

```
PyQt6>=6.6.0
keyboard>=0.13.5
pyautogui>=0.9.54
pystray>=0.19.5
Pillow>=10.1.0
pyperclip>=1.8.2
```

---

## 🚀 Instalación

### Opción 1: Instalación desde Código Fuente

#### Paso 1: Clonar o Descargar el Proyecto

```bash
# Si usas Git
git clone https://github.com/tuusuario/autocorrector-tildes.git
cd autocorrector-tildes

# O descarga el ZIP y extráelo
```

#### Paso 2: Crear la Estructura de Carpetas

Asegúrate de tener esta estructura:

```
autocorrector/
├── main.py
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── autocorrect_engine.py
│   ├── keyboard_listener.py
│   └── dictionary_manager.py
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   └── tray_icon.py
├── data/
│   ├── default_dictionary.json (se crea automáticamente)
│   └── user_dictionary.json (se crea automáticamente)
├── config/
│   ├── __init__.py
│   ├── config_manager.py
│   └── settings.json (se crea automáticamente)
└── README.md
```

#### Paso 3: Instalar Dependencias

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

#### Paso 4: Ejecutar la Aplicación

```bash
# Ejecutar con permisos de administrador (requerido)
python main.py
```

⚠️ **IMPORTANTE**: Debes ejecutar el programa como administrador para que pueda interceptar el teclado globalmente.

### Opción 2: Usar el Ejecutable (EXE)

Si ya tienes el archivo `.exe` compilado:

1. Descarga `AutocorrectorTildes.exe`
2. Ejecuta como administrador (clic derecho → "Ejecutar como administrador")
3. Sigue las instrucciones en pantalla

---

## 📖 Uso

### Primera Ejecución

1. Al ejecutar por primera vez, verás un diálogo de bienvenida explicando:
   - Cómo funciona el programa
   - Información de privacidad
   - Atajos de teclado

2. Se te preguntará si deseas ejecutar en segundo plano

### Uso Básico

#### Activar/Desactivar el Corrector

**Desde la interfaz:**
- Haz clic en el botón "ACTIVAR" / "DESACTIVAR"
- El indicador cambiará de color (verde = activo, rojo = inactivo)

**Desde el teclado:**
- Presiona `Ctrl+Shift+A` en cualquier momento
- Verás una notificación indicando el estado

**Desde la bandeja del sistema:**
- Clic derecho en el icono
- Selecciona "Activar/Desactivar"

#### Escribir con Corrección Automática

1. Activa el corrector
2. Escribe normalmente en cualquier aplicación
3. Las palabras se corrigen automáticamente al presionar:
   - Espacio
   - Enter
   - Signos de puntuación (. , ; : ! ?)

**Ejemplo:**
```
Escribes: "El camion paso por el arbol"
Resultado: "El camión paso por el árbol"
         (se corrige automáticamente)
```

### Gestión del Diccionario

#### Agregar Palabras Personalizadas

1. En la sección "Agregar Nueva Palabra":
   - Campo 1: Escribe la palabra SIN tilde (ej: `camion`)
   - Campo 2: Escribe la palabra CON tilde (ej: `camión`)
2. Haz clic en "Agregar"

El sistema validará automáticamente que:
- La palabra no esté duplicada
- La palabra con tilde realmente contenga una tilde

#### Eliminar Palabras

1. Busca la palabra en la tabla
2. Selecciona la fila
3. Haz clic en "Eliminar Seleccionada"

⚠️ Solo puedes eliminar palabras que hayas agregado (marcadas como "Usuario")

#### Buscar Palabras

Usa el campo de búsqueda para filtrar el diccionario en tiempo real.

### Configuración

#### Cambiar Atajo de Teclado

1. Ve a la sección "Configuración"
2. Selecciona un nuevo atajo del menú desplegable
3. Los cambios se aplican inmediatamente

Opciones disponibles:
- `ctrl+shift+a` (por defecto)
- `ctrl+shift+t`
- `ctrl+alt+a`
- `alt+shift+a`
- `ctrl+shift+z`

#### Inicio Automático con Windows

Marca la casilla "Iniciar automáticamente con Windows" para que el programa se ejecute al encender tu PC.

#### Ejecución en Segundo Plano

Marca "Ejecutar en segundo plano al iniciar" para que el programa se minimice a la bandeja del sistema al abrirse.

---

## 📁 Estructura del Proyecto

```
autocorrector/
│
├── main.py                          # Punto de entrada principal
├── requirements.txt                 # Dependencias Python
├── README.md                        # Esta documentación
│
├── core/                            # Lógica principal
│   ├── __init__.py
│   ├── autocorrect_engine.py       # Motor de corrección
│   ├── keyboard_listener.py        # Captura de teclado
│   └── dictionary_manager.py       # Gestión de diccionarios
│
├── ui/                              # Interfaz gráfica
│   ├── __init__.py
│   ├── main_window.py              # Ventana principal
│   └── tray_icon.py                # Icono de bandeja
│
├── config/                          # Configuración
│   ├── __init__.py
│   ├── config_manager.py           # Gestor de configuración
│   └── settings.json               # Configuración guardada
│
└── data/                            # Datos
    ├── default_dictionary.json     # Diccionario base
    └── user_dictionary.json        # Palabras personalizadas
```

### Descripción de Módulos

#### `core/autocorrect_engine.py`
Motor principal que:
- Detecta palabras sin tilde
- Busca coincidencias en el diccionario
- Reemplaza palabras automáticamente

#### `core/keyboard_listener.py`
Escucha eventos del teclado:
- Detecta teclas de activación (espacio, enter, puntuación)
- Maneja el hotkey de toggle
- Ejecuta correcciones en tiempo real

#### `core/dictionary_manager.py`
Gestiona los diccionarios:
- Carga/guarda palabras
- Valida entradas
- Fusiona diccionario base y de usuario

#### `ui/main_window.py`
Interfaz gráfica principal con:
- Control ON/OFF
- Gestión de palabras
- Configuración
- Tabla de diccionario

#### `ui/tray_icon.py`
Icono en bandeja del sistema:
- Menú contextual
- Indicador visual de estado
- Notificaciones

#### `config/config_manager.py`
Configuración persistente:
- Guarda preferencias
- Gestiona inicio automático
- Maneja primera ejecución

---

## ⚙️ Configuración

### Archivos de Configuración

#### `config/settings.json`
```json
{
  "hotkey": "ctrl+shift+a",
  "start_with_windows": false,
  "run_in_background": true,
  "first_run": false,
  "ask_background_on_startup": true
}
```

#### `data/user_dictionary.json`
```json
{
  "palabra1": "palabra1_con_tilde",
  "palabra2": "palabra2_con_tilde"
}
```

### Personalización Avanzada

Puedes editar manualmente los archivos JSON para:
- Agregar múltiples palabras rápidamente
- Exportar/importar tu diccionario personal
- Resetear configuración (elimina `settings.json`)

---

## 📦 Compilar a EXE

Para crear un ejecutable independiente:

### Paso 1: Instalar PyInstaller

```bash
pip install pyinstaller
```

### Paso 2: Crear el Ejecutable

```bash
# Ejecutable de un solo archivo
pyinstaller --onefile --windowed --name="AutocorrectorTildes" --icon=config/icon.ico main.py

# Con todas las dependencias incluidas
pyinstaller --onefile --windowed --name="AutocorrectorTildes" --add-data="data;data" --add-data="config;config" main.py
```

### Paso 3: Encontrar el EXE

El ejecutable estará en la carpeta `dist/AutocorrectorTildes.exe`

### Opciones de PyInstaller

- `--onefile`: Crear un único archivo ejecutable
- `--windowed`: Sin ventana de consola
- `--name`: Nombre del ejecutable
- `--icon`: Icono personalizado
- `--add-data`: Incluir archivos de datos

---

## ❓ Preguntas Frecuentes

### ¿Por qué necesita permisos de administrador?

Para interceptar el teclado globalmente y funcionar en todas las aplicaciones, Windows requiere permisos elevados.

### ¿El programa guarda lo que escribo?

**NO**. El programa solo lee las palabras para corregirlas en tiempo real. No almacena, registra ni transmite ningún dato.

### ¿Funciona sin internet?

**SÍ**. Todo el procesamiento es local. No necesitas conexión a internet.

### ¿Puedo usar el programa en múltiples idiomas?

Actualmente está optimizado para español. Puedes agregar palabras de otros idiomas manualmente.

### ¿Cómo agrego muchas palabras a la vez?

Edita directamente `data/user_dictionary.json` siguiendo el formato JSON.

### ¿El programa afecta el rendimiento?

No. Está optimizado para bajo consumo de CPU y memoria.

---

## 🔧 Solución de Problemas

### El programa no inicia

**Solución:**
1. Verifica que ejecutas como administrador
2. Comprueba que Python 3.11+ está instalado
3. Reinstala las dependencias: `pip install -r requirements.txt --force-reinstall`

### Las correcciones no funcionan

**Solución:**
1. Verifica que el corrector esté ACTIVO (indicador verde)
2. Comprueba que la palabra existe en el diccionario
3. Prueba en una aplicación simple como Notepad primero

### El hotkey no funciona

**Solución:**
1. Verifica que otra aplicación no esté usando la misma combinación
2. Cambia el hotkey en Configuración
3. Reinicia el programa

### Error "Access Denied" o "Acceso Denegado"

**Solución:**
Ejecuta el programa como administrador:
- Clic derecho → "Ejecutar como administrador"

### El icono de bandeja no aparece

**Solución:**
1. Verifica que `pystray` y `Pillow` estén instalados
2. Revisa la configuración de iconos de Windows
3. Reinicia el programa

### Las palabras no se guardan

**Solución:**
1. Verifica permisos de escritura en la carpeta `data/`
2. Comprueba que el archivo `user_dictionary.json` no esté corrupto
3. Elimina el archivo y deja que se regenere automáticamente

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

---

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tuusuario](https://github.com/tuusuario)
- Email: tuemail@ejemplo.com

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📊 Estadísticas

- **Palabras en diccionario base**: ~150
- **Lenguaje**: Python 3.11+
- **Frameworks**: PyQt6, keyboard, pyautogui
- **Plataforma**: Windows 10/11

---

## 🎉 Agradecimientos

- Comunidad de Python
- Colaboradores de PyQt6
- Usuarios beta testers

---

**¿Encontraste útil este proyecto? ¡Dale una ⭐ en GitHub!**