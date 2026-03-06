"""Color themes for intake forms."""

from reportlab.lib import colors

THEMES = {
    "lavender": {
        "primary": "#DDD6F3",       # Light lavender - section headers, backgrounds
        "primary_mid": "#B8ABDF",   # Medium lavender - borders, lines
        "primary_dark": "#6B5B9E",  # Dark lavender - headings, checkbox borders
        "accent": "#FAC8A0",        # Peach - decorative elements
        "accent_light": "#FEF0E7",  # Light peach - hero background, highlights
        "text": "#2D2926",          # Near-black - main text
        "text_muted": "#6B6560",    # Warm gray - labels, secondary text
        "text_light": "#B0A9A4",    # Light gray - notes, hints
    },
    "ocean": {
        "primary": "#D4E8F2",       # Light blue
        "primary_mid": "#8BC4E0",   # Medium blue
        "primary_dark": "#2B7A9E",  # Dark teal
        "accent": "#F9D977",        # Sandy yellow
        "accent_light": "#FFF8E7",  # Cream
        "text": "#1A3A4A",          # Dark blue-gray
        "text_muted": "#4A6670",    # Muted teal
        "text_light": "#8A9EA6",    # Light blue-gray
    },
    "forest": {
        "primary": "#D5E8D4",       # Light sage
        "primary_mid": "#97C9A0",   # Medium green
        "primary_dark": "#4A7C59",  # Forest green
        "accent": "#F4D03F",        # Golden yellow
        "accent_light": "#FDF9E7",  # Light cream
        "text": "#2D3A2E",          # Dark green-gray
        "text_muted": "#5A6B5C",    # Muted green
        "text_light": "#9AAA9C",    # Light sage
    },
    "rose": {
        "primary": "#F8E1E8",       # Light pink
        "primary_mid": "#E8B4C4",   # Medium rose
        "primary_dark": "#B85C7A",  # Deep rose
        "accent": "#C9A87C",        # Warm tan
        "accent_light": "#FDF5F0",  # Blush cream
        "text": "#3D2B32",          # Dark burgundy
        "text_muted": "#6B5560",    # Muted mauve
        "text_light": "#A8929A",    # Dusty rose
    },
    "sunset": {
        "primary": "#FFE4D6",       # Light coral
        "primary_mid": "#FFAA85",   # Medium orange
        "primary_dark": "#D4652F",  # Burnt orange
        "accent": "#7EC8E3",        # Sky blue
        "accent_light": "#FFF5EE",  # Seashell
        "text": "#3D2516",          # Dark brown
        "text_muted": "#6B5144",    # Warm brown
        "text_light": "#A89080",    # Tan
    },
    "neutral": {
        "primary": "#E8E8E8",       # Light gray
        "primary_mid": "#CCCCCC",   # Medium gray
        "primary_dark": "#666666",  # Dark gray
        "accent": "#B8D4E8",        # Soft blue
        "accent_light": "#F5F5F5",  # Off-white
        "text": "#333333",          # Charcoal
        "text_muted": "#666666",    # Medium gray
        "text_light": "#999999",    # Light gray
    },
    "midnight": {
        "primary": "#E0E4F0",       # Pale blue-gray
        "primary_mid": "#9BA4C0",   # Slate blue
        "primary_dark": "#4A5578",  # Deep blue-gray
        "accent": "#C5A880",        # Warm gold
        "accent_light": "#F0EDE8",  # Warm white
        "text": "#2A2D35",          # Near-black blue
        "text_muted": "#555A68",    # Muted slate
        "text_light": "#888D9A",    # Light slate
    },
    "summer": {
        "primary": "#8ECAE6",       # Sky blue
        "primary_mid": "#219EBC",   # Teal
        "primary_dark": "#023047",  # Deep navy
        "accent": "#FFB703",        # Golden yellow
        "accent_light": "#FFF8E7",  # Warm cream
        "text": "#023047",          # Deep navy
        "text_muted": "#2A5A6C",    # Muted teal
        "text_light": "#6A9AAC",    # Soft blue-gray
    },
    "neon": {
        "primary": "#FFE4DC",       # Light coral (derived for readability)
        "primary_mid": "#FE8405",   # Vibrant orange
        "primary_dark": "#002F5D",  # Deep navy
        "accent": "#FBA625",        # Golden orange
        "accent_light": "#FFF5E6",  # Warm cream
        "text": "#001B39",          # Darkest navy
        "text_muted": "#2A4A6A",    # Muted navy
        "text_light": "#6A8A9A",    # Soft blue-gray
    },
    "berry": {
        "primary": "#F9DBBD",       # Light peachy pink
        "primary_mid": "#DA627D",   # Rose berry
        "primary_dark": "#A53860",  # Deep berry
        "accent": "#FFA5AB",        # Salmon pink
        "accent_light": "#FEF0ED",  # Blush white
        "text": "#450920",          # Dark burgundy
        "text_muted": "#6B3A4A",    # Muted wine
        "text_light": "#A86878",    # Dusty rose
    },
    "fiery": {
        "primary": "#FFE8DC",       # Light coral (derived for readability)
        "primary_mid": "#E36414",   # Burnt orange
        "primary_dark": "#9A031E",  # Deep red
        "accent": "#FB8B24",        # Bright orange
        "accent_light": "#FFF5EE",  # Warm cream
        "text": "#5F0F40",          # Dark maroon
        "text_muted": "#0F4C5C",    # Dark teal
        "text_light": "#4A7A8A",    # Muted teal
    },
    "blush": {
        "primary": "#FFC2D1",       # Light pink
        "primary_mid": "#FF8FAB",   # Medium pink
        "primary_dark": "#FB6F92",  # Vibrant pink
        "accent": "#FFB3C6",        # Soft pink
        "accent_light": "#FFE5EC",  # Palest pink
        "text": "#4A2A3A",          # Dark mauve
        "text_muted": "#7A5A6A",    # Muted plum
        "text_light": "#AA8A9A",    # Dusty pink
    },
    "deepblue": {
        "primary": "#D4E8F2",       # Pale blue
        "primary_mid": "#3E92CC",   # Bright blue
        "primary_dark": "#2A628F",  # Medium navy
        "accent": "#5AA8D8",        # Sky blue
        "accent_light": "#E8F4FA",  # Ice blue
        "text": "#13293D",          # Deep navy
        "text_muted": "#16324F",    # Dark blue
        "text_light": "#4A6A8A",    # Slate blue
    },
}


def get_theme_colors(config):
    """Get color palette from theme name or custom colors.
    
    Args:
        config: Dict with 'theme' key (theme name) and optional 'colors' dict for overrides.
        
    Returns:
        Dict mapping color keys to reportlab Color objects.
    """
    theme_name = config.get("theme", "lavender")
    custom_colors = config.get("colors", {})
    
    # Start with base theme
    if theme_name == "custom":
        base_colors = THEMES["lavender"].copy()
    elif theme_name in THEMES:
        base_colors = THEMES[theme_name].copy()
    else:
        print(f"⚠️  Unknown theme '{theme_name}', using 'lavender'")
        base_colors = THEMES["lavender"].copy()
    
    # Apply custom color overrides
    for key, value in custom_colors.items():
        if key in base_colors:
            base_colors[key] = value
        else:
            print(f"⚠️  Unknown color key '{key}', ignoring")
    
    # Convert hex strings to reportlab colors
    return {k: colors.HexColor(v) for k, v in base_colors.items()}


def list_themes():
    """Print available themes to stdout."""
    print("\nAvailable themes:")
    print("-" * 50)
    for name, palette in THEMES.items():
        print(f"  {name:12} - Primary: {palette['primary']}, Accent: {palette['accent']}")
    print()
    print("Use --theme <name> or set 'theme: <name>' in config.yaml")
    print("For custom colors, set 'theme: custom' and define 'colors:' in config.\n")
