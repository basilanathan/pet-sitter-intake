"""Configuration loading and section defaults."""

import os

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from .constants import DEFAULT_OUTPUT

DEFAULT_CONFIG = {
    "business_name": "Your Business Name",
    "sitter_name": "",
    "services": "Pet Sitting, Dog Walking, Boarding",
    "location": "",
    "contact": "",
    "service_type": "general",  # general, boarding, walking, drop_in
    "num_pets": 1,
    "fillable": True,  # Generate fillable PDF fields by default
    "theme": "lavender",  # Color theme name or "custom"
    "colors": {},  # Custom color overrides (when theme is "custom")
    "output": DEFAULT_OUTPUT,  # Output filename
    "sections": {},  # Section overrides (merged with SECTION_DEFAULTS)
}

# Section defaults by service type
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


def get_section_config(config):
    """Get final section configuration by merging defaults with user overrides.
    
    Args:
        config: Dict containing 'service_type' and optional 'sections' overrides.
        
    Returns:
        Dict mapping section names to boolean enabled status.
    """
    service_type = config.get("service_type", "general")
    defaults = SECTION_DEFAULTS.get(service_type, SECTION_DEFAULTS["general"]).copy()
    
    # Legacy support: include_home_access overrides sections.home_access
    if "include_home_access" in config:
        defaults["home_access"] = config["include_home_access"]
    
    # Apply user section overrides
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
    
    # Header
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


def load_config(config_path=None):
    """Load config from YAML file, falling back to defaults.
    
    Args:
        config_path: Optional path to YAML config file.
        
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
    
    return config
