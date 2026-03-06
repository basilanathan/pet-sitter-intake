"""Configuration loading and section defaults."""

import os

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from .constants import DEFAULT_OUTPUT, LIMITS


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""
    pass


DEFAULT_CONFIG = {
    "business_name": "Your Business Name",
    "sitter_name": "",
    "services": "Pet Sitting, Dog Walking, Boarding",
    "location": "",
    "contact": "",
    "service_type": "general",
    "num_pets": 1,
    "fillable": True,
    "theme": "lavender",
    "colors": {},
    "output": DEFAULT_OUTPUT,
    "sections": {},
}

SECTION_DEFAULTS = {
    "general": {
        "home_access": True,
        "vaccinations": True,
        "health_medications": True,
        "feeding_daily_care": True,
        "behavior_temperament": True,
        "service_specific": False,
    },
    "boarding": {
        "home_access": False,
        "vaccinations": True,
        "health_medications": True,
        "feeding_daily_care": True,
        "behavior_temperament": True,
        "service_specific": True,
    },
    "walking": {
        "home_access": False,
        "vaccinations": False,
        "health_medications": False,
        "feeding_daily_care": False,
        "behavior_temperament": True,
        "service_specific": True,
    },
    "drop_in": {
        "home_access": True,
        "vaccinations": True,
        "health_medications": True,
        "feeding_daily_care": True,
        "behavior_temperament": True,
        "service_specific": True,
    },
}

SECTION_NAMES = list(SECTION_DEFAULTS["general"].keys())

VALID_SERVICE_TYPES = list(SECTION_DEFAULTS.keys())

VALID_COLOR_KEYS = [
    "primary", "primary_mid", "primary_dark",
    "accent", "accent_light",
    "text", "text_muted", "text_light",
]


def validate_config(config, strict=False):
    """Validate configuration values.
    
    Args:
        config: Configuration dict to validate
        strict: If True, raise exception on errors. If False, print warnings and fix.
        
    Returns:
        Tuple of (validated_config, list of warning messages)
        
    Raises:
        ConfigValidationError: If strict=True and validation fails
    """
    warnings = []
    validated = config.copy()
    
    # Validate num_pets
    num_pets = validated.get("num_pets", 1)
    if not isinstance(num_pets, int):
        try:
            num_pets = int(num_pets)
            validated["num_pets"] = num_pets
        except (TypeError, ValueError):
            msg = f"num_pets must be an integer, got {type(num_pets).__name__}"
            if strict:
                raise ConfigValidationError(msg)
            warnings.append(msg)
            validated["num_pets"] = 1
    
    if num_pets < LIMITS["min_pets"]:
        msg = f"num_pets must be at least {LIMITS['min_pets']}, got {num_pets}"
        if strict:
            raise ConfigValidationError(msg)
        warnings.append(msg)
        validated["num_pets"] = LIMITS["min_pets"]
    elif num_pets > LIMITS["max_pets"]:
        msg = f"num_pets must be at most {LIMITS['max_pets']}, got {num_pets}"
        if strict:
            raise ConfigValidationError(msg)
        warnings.append(msg)
        validated["num_pets"] = LIMITS["max_pets"]
    
    # Validate service_type
    service_type = validated.get("service_type", "general")
    if service_type not in VALID_SERVICE_TYPES:
        msg = f"Invalid service_type '{service_type}'. Valid options: {', '.join(VALID_SERVICE_TYPES)}"
        if strict:
            raise ConfigValidationError(msg)
        warnings.append(msg)
        validated["service_type"] = "general"
    
    # Validate theme (deferred to themes.py, but do basic check)
    theme = validated.get("theme", "lavender")
    if not isinstance(theme, str):
        msg = f"theme must be a string, got {type(theme).__name__}"
        if strict:
            raise ConfigValidationError(msg)
        warnings.append(msg)
        validated["theme"] = "lavender"
    
    # Validate business_name
    business_name = validated.get("business_name", "")
    if not business_name or not isinstance(business_name, str):
        msg = "business_name is required and must be a non-empty string"
        if strict:
            raise ConfigValidationError(msg)
        warnings.append(msg)
        validated["business_name"] = DEFAULT_CONFIG["business_name"]
    elif len(business_name) > LIMITS["max_business_name_len"]:
        msg = f"business_name exceeds {LIMITS['max_business_name_len']} characters"
        if strict:
            raise ConfigValidationError(msg)
        warnings.append(msg)
        validated["business_name"] = business_name[:LIMITS["max_business_name_len"]]
    
    # Validate fillable
    fillable = validated.get("fillable", True)
    if not isinstance(fillable, bool):
        if isinstance(fillable, str):
            validated["fillable"] = fillable.lower() in ("true", "yes", "1")
        else:
            msg = f"fillable must be a boolean, got {type(fillable).__name__}"
            if strict:
                raise ConfigValidationError(msg)
            warnings.append(msg)
            validated["fillable"] = True
    
    # Validate colors dict
    colors = validated.get("colors", {})
    if not isinstance(colors, dict):
        msg = f"colors must be a dict, got {type(colors).__name__}"
        if strict:
            raise ConfigValidationError(msg)
        warnings.append(msg)
        validated["colors"] = {}
    else:
        for key in colors:
            if key not in VALID_COLOR_KEYS:
                warnings.append(f"Unknown color key '{key}' in colors. Valid keys: {', '.join(VALID_COLOR_KEYS)}")
        
        for key, value in colors.items():
            if key in VALID_COLOR_KEYS:
                if not isinstance(value, str) or not value.startswith("#"):
                    msg = f"Color value for '{key}' must be a hex string (e.g., '#FF0000'), got '{value}'"
                    if strict:
                        raise ConfigValidationError(msg)
                    warnings.append(msg)
    
    # Validate sections dict
    sections = validated.get("sections", {})
    if not isinstance(sections, dict):
        msg = f"sections must be a dict, got {type(sections).__name__}"
        if strict:
            raise ConfigValidationError(msg)
        warnings.append(msg)
        validated["sections"] = {}
    else:
        for section, enabled in sections.items():
            if section not in SECTION_NAMES:
                warnings.append(f"Unknown section '{section}'. Valid sections: {', '.join(SECTION_NAMES)}")
            elif not isinstance(enabled, bool):
                msg = f"Section '{section}' value must be boolean, got {type(enabled).__name__}"
                warnings.append(msg)
    
    return validated, warnings


def get_section_config(config):
    """Get final section configuration by merging defaults with user overrides.
    
    Args:
        config: Dict containing 'service_type' and optional 'sections' overrides.
        
    Returns:
        Dict mapping section names to boolean enabled status.
    """
    service_type = config.get("service_type", "general")
    defaults = SECTION_DEFAULTS.get(service_type, SECTION_DEFAULTS["general"]).copy()
    
    if "include_home_access" in config:
        defaults["home_access"] = config["include_home_access"]
    
    user_sections = config.get("sections", {})
    for section, enabled in user_sections.items():
        if section in defaults:
            defaults[section] = enabled
        else:
            print(f"⚠️  Unknown section '{section}', ignoring. Valid: {', '.join(SECTION_NAMES)}")
    
    return defaults


def list_sections(service_type=None):
    """Print section defaults for each service type."""
    print("\nSection defaults by service type:")
    print("-" * 70)
    
    print(f"{'Section':<22} {'general':^10} {'boarding':^10} {'walking':^10} {'drop_in':^10}")
    print("-" * 70)
    
    for section in SECTION_NAMES:
        row = f"{section:<22}"
        for stype in ["general", "boarding", "walking", "drop_in"]:
            val = SECTION_DEFAULTS[stype][section]
            mark = "✓" if val else "—"
            row += f" {mark:^10}"
        print(row)
    
    print("-" * 70)
    print("\nOverride in config.yaml:")
    print("  sections:")
    print("    vaccinations: true")
    print("    health_medications: true")
    print("\nOr via CLI:")
    print("  --include-section vaccinations --include-section health_medications")
    print("  --exclude-section home_access")
    print()


def load_config(config_path=None, validate=True):
    """Load config from YAML file, falling back to defaults.
    
    Args:
        config_path: Optional path to YAML config file.
        validate: Whether to validate the config after loading.
        
    Returns:
        Dict with configuration values.
    """
    config = DEFAULT_CONFIG.copy()
    
    if config_path:
        if not os.path.exists(config_path):
            print(f"❌ Config file not found: {config_path}")
            print("   Using default settings instead.")
            return config
            
        if not YAML_AVAILABLE:
            print("=" * 60)
            print("❌ ERROR: PyYAML is required to load config files!")
            print("   Install it with: pip install pyyaml")
            print("   ")
            print("   Your config file was NOT loaded. Using defaults.")
            print("=" * 60)
            return config
            
        with open(config_path, "r") as f:
            user_config = yaml.safe_load(f) or {}
            config.update(user_config)
            print(f"📄 Loaded config from: {config_path}")
    
    if validate:
        config, warnings = validate_config(config, strict=False)
        for warning in warnings:
            print(f"⚠️  Config warning: {warning}")
    
    return config
