"""Tests for theme configuration and color handling."""

import pytest
from reportlab.lib import colors

from pet_sitter_intake.themes import (
    THEMES,
    get_theme_colors,
    list_themes,
)


class TestThemes:
    """Tests for theme definitions."""
    
    def test_all_themes_have_required_keys(self):
        """All themes should have all required color keys."""
        required_keys = [
            "primary", "primary_mid", "primary_dark",
            "accent", "accent_light",
            "text", "text_muted", "text_light",
        ]
        for theme_name, theme_colors in THEMES.items():
            for key in required_keys:
                assert key in theme_colors, f"Theme '{theme_name}' missing key '{key}'"
    
    def test_all_theme_colors_are_hex(self):
        """All theme color values should be valid hex strings."""
        for theme_name, theme_colors in THEMES.items():
            for key, value in theme_colors.items():
                assert isinstance(value, str), f"{theme_name}.{key} should be string"
                assert value.startswith("#"), f"{theme_name}.{key} should start with #"
                assert len(value) == 7, f"{theme_name}.{key} should be 7 chars (#RRGGBB)"
    
    def test_expected_themes_exist(self):
        """Expected theme names should exist."""
        expected = [
            "lavender", "ocean", "forest", "rose", "sunset",
            "neutral", "midnight", "summer", "neon", "berry",
            "fiery", "blush", "deepblue",
        ]
        for theme_name in expected:
            assert theme_name in THEMES, f"Expected theme '{theme_name}' not found"


class TestGetThemeColors:
    """Tests for get_theme_colors function."""
    
    def test_returns_reportlab_colors(self):
        """get_theme_colors should return reportlab Color objects."""
        config = {"theme": "lavender"}
        theme_colors = get_theme_colors(config)
        
        for key, color in theme_colors.items():
            assert isinstance(color, colors.Color), f"{key} should be a Color object"
    
    def test_default_theme_is_lavender(self):
        """Default theme should be lavender when not specified."""
        config = {}
        theme_colors = get_theme_colors(config)
        lavender_colors = get_theme_colors({"theme": "lavender"})
        
        assert theme_colors["primary"].hexval() == lavender_colors["primary"].hexval()
    
    def test_unknown_theme_falls_back_to_lavender(self):
        """Unknown theme should fall back to lavender."""
        config = {"theme": "nonexistent_theme"}
        theme_colors = get_theme_colors(config)
        lavender_colors = get_theme_colors({"theme": "lavender"})
        
        assert theme_colors["primary"].hexval() == lavender_colors["primary"].hexval()
    
    def test_custom_theme_uses_lavender_base(self):
        """Custom theme without colors should use lavender as base."""
        config = {"theme": "custom"}
        theme_colors = get_theme_colors(config)
        lavender_colors = get_theme_colors({"theme": "lavender"})
        
        assert theme_colors["primary"].hexval() == lavender_colors["primary"].hexval()
    
    def test_custom_color_override(self):
        """Custom colors should override base theme."""
        config = {
            "theme": "lavender",
            "colors": {
                "primary": "#FF0000",
            }
        }
        theme_colors = get_theme_colors(config)
        
        assert theme_colors["primary"].hexval() == "0xff0000"
    
    def test_partial_custom_colors(self):
        """Only specified custom colors should be overridden."""
        config = {
            "theme": "ocean",
            "colors": {
                "accent": "#123456",
            }
        }
        theme_colors = get_theme_colors(config)
        ocean_colors = get_theme_colors({"theme": "ocean"})
        
        # Accent should be custom
        assert theme_colors["accent"].hexval() == "0x123456"
        # Primary should still be ocean
        assert theme_colors["primary"].hexval() == ocean_colors["primary"].hexval()
    
    def test_all_themes_produce_valid_colors(self):
        """All built-in themes should produce valid color objects."""
        for theme_name in THEMES:
            config = {"theme": theme_name}
            theme_colors = get_theme_colors(config)
            
            assert len(theme_colors) >= 8, f"Theme '{theme_name}' has too few colors"
            for key, color in theme_colors.items():
                assert isinstance(color, colors.Color), f"{theme_name}.{key} invalid"


class TestListThemes:
    """Tests for list_themes function."""
    
    def test_list_themes_runs_without_error(self, capsys):
        """list_themes should run without raising exceptions."""
        list_themes()
        captured = capsys.readouterr()
        assert "Available themes" in captured.out
    
    def test_list_themes_shows_all_themes(self, capsys):
        """list_themes should list all available themes."""
        list_themes()
        captured = capsys.readouterr()
        
        for theme_name in THEMES:
            assert theme_name in captured.out, f"Theme '{theme_name}' not in output"
