# ============================================================================
# core/__init__.py
# ============================================================================
"""
Módulo core - Lógica principal del autocorrector
"""

from .dictionary_manager import DictionaryManager
from .autocorrect_engine import AutocorrectEngine
from .keyboard_listener import KeyboardListener

__all__ = ['DictionaryManager', 'AutocorrectEngine', 'KeyboardListener']