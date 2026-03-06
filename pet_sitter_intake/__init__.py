"""Pet Sitter Client Intake Form Generator.

Generate professional PDF client intake forms for pet sitting businesses.
"""

__version__ = "5.4.0"

from .config import (
    load_config, 
    get_section_config, 
    validate_config,
    ConfigValidationError,
    DEFAULT_CONFIG, 
    SECTION_DEFAULTS,
)
from .themes import THEMES, get_theme_colors, list_themes
from .builder import build_form
from .constants import SPACING, LIMITS

__all__ = [
    "__version__",
    "build_form",
    "load_config",
    "get_section_config",
    "validate_config",
    "ConfigValidationError",
    "get_theme_colors",
    "list_themes",
    "DEFAULT_CONFIG",
    "SECTION_DEFAULTS",
    "THEMES",
    "SPACING",
    "LIMITS",
]
