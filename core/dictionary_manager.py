# core/dictionary_manager.py

import json
from pathlib import Path
from typing import Dict, Set, Tuple


class DictionaryManager:
    """Gestiona los diccionarios de palabras con y sin tilde."""

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.data_dir = self.base_dir / "data"
        self.default_dict_path = self.data_dir / "default_dictionary.json"
        self.user_dict_path = self.data_dir / "user_dictionary.json"

        # Diccionarios internos
        self.dictionary: Dict[str, str] = {}
        self.user_words: Set[str] = set()

        self._ensure_directories()
        self._load_dictionaries()

    # ────────────────────────────────
    # Inicialización de archivos
    # ────────────────────────────────
    def _ensure_directories(self):
        """Crea las carpetas y archivos necesarios si no existen."""
        self.data_dir.mkdir(parents=True, exist_ok=True)

        if not self.default_dict_path.exists():
            self._create_default_dictionary()

        if not self.user_dict_path.exists():
            self.user_dict_path.write_text("{}", encoding="utf-8")

    def _create_default_dictionary(self):
        """Crea el diccionario base con palabras comunes en español."""
        default_words = {
            # Sustantivos
            "arbol": "árbol", "arboles": "árboles",
            "camion": "camión", "camiones": "camiones",
            "cancion": "canción", "canciones": "canciones",
            "razon": "razón", "razones": "razones",
            "nacion": "nación", "avion": "avión", "aviones": "aviones",
            "corazon": "corazón", "corazones": "corazones",

            # Verbos comunes
            "esta": "está", "estan": "están",
            "sera": "será", "seran": "serán",
            "podria": "podría", "podrian": "podrían",
            "haria": "haría", "harian": "harían",
            "tendria": "tendría", "tendrian": "tendrían",
            "daria": "daría", "darian": "darían",
            "pondria": "pondría", "pondrian": "pondrían",
            "vendria": "vendría", "vendrian": "vendrían",

            # Adjetivos
            "facil": "fácil", "faciles": "fáciles",
            "dificil": "difícil", "dificiles": "difíciles",
            "util": "útil", "utiles": "útiles",
            "debil": "débil", "debiles": "débiles",
            "movil": "móvil", "moviles": "móviles",
            "rapido": "rápido", "rapida": "rápida",
            "ultimo": "último", "ultima": "última",
            "unico": "único", "unica": "única",

            # Pronombres y artículos
            "el": "él", "tu": "tú", "mi": "mí",
            "si": "sí", "mas": "más", "solo": "sólo",
            "aun": "aún", "como": "cómo", "donde": "dónde",
            "cuando": "cuándo", "cual": "cuál", "cuales": "cuáles",
            "quien": "quién", "quienes": "quiénes",
            "que": "qué", "porque": "porqué",

            # Adverbios
            "tambien": "también", "ademas": "además",
            "despues": "después", "asi": "así",
            "alli": "allí", "aqui": "aquí", "ahi": "ahí",
            "jamas": "jamás", "quizas": "quizás",

            # Palabras frecuentes
            "informacion": "información",
            "solucion": "solución", "soluciones": "soluciones",
            "educacion": "educación", "comunicacion": "comunicación",
            "administracion": "administración", "operacion": "operación",
            "operaciones": "operaciones", "atencion": "atención",
            "direccion": "dirección", "direcciones": "direcciones",

            # Días y meses
            "sabado": "sábado", "miercoles": "miércoles",

            # Otros
            "cafe": "café", "papa": "papá", "mama": "mamá",
            "calculo": "cálculo", "calculos": "cálculos",
            "telefono": "teléfono", "telefonos": "teléfonos",
            "musica": "música", "matematicas": "matemáticas",
            "ingles": "inglés", "frances": "francés",
            "aleman": "alemán", "japones": "japonés",
        }

        self.default_dict_path.write_text(
            json.dumps(default_words, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    # ────────────────────────────────
    # Carga y actualización
    # ────────────────────────────────
    def _load_dictionaries(self):
        """Carga ambos diccionarios y los fusiona (prioriza el usuario)."""
        try:
            default_dict = json.loads(self.default_dict_path.read_text(encoding="utf-8"))
            user_dict = json.loads(self.user_dict_path.read_text(encoding="utf-8"))

            self.user_words = set(user_dict.keys())
            self.dictionary = {**default_dict, **user_dict}

        except Exception as e:
            print(f"[Error] Cargando diccionarios: {e}")
            self.dictionary = {}
            self.user_words = set()

    def reload(self):
        """Recarga los diccionarios desde disco."""
        self._load_dictionaries()

    # ────────────────────────────────
    # Operaciones CRUD de palabras
    # ────────────────────────────────
    def add_word(self, word_without: str, word_with: str) -> Tuple[bool, str]:
        """Agrega una palabra personalizada al diccionario del usuario."""
        word_without = word_without.strip().lower()
        word_with = word_with.strip()

        if not word_without or not word_with:
            return False, "Las palabras no pueden estar vacías."

        if not any(c in "áéíóúÁÉÍÓÚüÜñÑ" for c in word_with):
            return False, "La palabra corregida debe contener al menos una tilde o carácter especial."

        if word_without in self.dictionary:
            tipo = "usuario" if word_without in self.user_words else "base"
            return False, f"Esa palabra ya existe en el diccionario {tipo}: {self.dictionary[word_without]}"

        try:
            user_dict = json.loads(self.user_dict_path.read_text(encoding="utf-8"))
            user_dict[word_without] = word_with

            self.user_dict_path.write_text(
                json.dumps(user_dict, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )

            self.dictionary[word_without] = word_with
            self.user_words.add(word_without)
            return True, f"✅ '{word_with}' añadida correctamente."

        except Exception as e:
            return False, f"Error al guardar palabra: {e}"

    def remove_word(self, word_without: str) -> Tuple[bool, str]:
        """Elimina una palabra del diccionario de usuario."""
        word_without = word_without.strip().lower()

        if word_without not in self.user_words:
            return False, "Solo puedes eliminar palabras que hayas agregado."

        try:
            user_dict = json.loads(self.user_dict_path.read_text(encoding="utf-8"))
            user_dict.pop(word_without, None)

            self.user_dict_path.write_text(
                json.dumps(user_dict, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )

            self.dictionary.pop(word_without, None)
            self.user_words.discard(word_without)

            return True, f"✅ Palabra '{word_without}' eliminada correctamente."

        except Exception as e:
            return False, f"Error al eliminar palabra: {e}"

    # ────────────────────────────────
    # Búsqueda y utilidades
    # ────────────────────────────────
    def get_corrected_word(self, word: str) -> str:
        """Devuelve la palabra corregida manteniendo la capitalización."""
        word_lower = word.lower()
        corrected = self.dictionary.get(word_lower, word)

        # Mantener formato de mayúsculas
        if word.isupper():
            return corrected.upper()
        elif word[0].isupper():
            return corrected.capitalize()
        return corrected

    def get_all_words(self) -> Dict[str, Tuple[str, bool]]:
        """Devuelve todas las palabras con info si son del usuario."""
        return {
            w: (c, w in self.user_words)
            for w, c in self.dictionary.items()
        }
