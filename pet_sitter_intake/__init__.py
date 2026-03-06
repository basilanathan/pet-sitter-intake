"""Pet Sitter Client Intake Form Generator.

Generate professional PDF client intake forms for pet sitting businesses.
"""

__version__ = "5.3.0"

from .config import load_config, get_section_config, DEFAULT_CONFIG, SECTION_DEFAULTS
from .themes import THEMES, get_theme_colors, list_themes
from .builder import build_form

__all__ = [
    "__version__",
    "build_form",
    "load_config",
    "get_section_config",
    "get_theme_colors",
    "list_themes",
    "DEFAULT_CONFIG",
    "SECTION_DEFAULTS",
    "THEMES",
]
