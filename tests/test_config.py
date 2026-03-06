"""Tests for configuration loading and validation."""

import pytest
import tempfile
import os

from pet_sitter_intake.config import (
    load_config,
    validate_config,
    get_section_config,
    ConfigValidationError,
    DEFAULT_CONFIG,
    SECTION_DEFAULTS,
    SECTION_NAMES,
)


class TestValidateConfig:
    """Tests for validate_config function."""
    
    def test_valid_config_passes(self):
        """Valid config should pass without warnings."""
        config = {
            "business_name": "Test Business",
            "num_pets": 2,
            "service_type": "boarding",
            "fillable": True,
            "theme": "ocean",
        }
        validated, warnings = validate_config(config)
        assert validated["business_name"] == "Test Business"
        assert validated["num_pets"] == 2
        assert validated["service_type"] == "boarding"
        assert len(warnings) == 0
    
    def test_num_pets_too_low(self):
        """num_pets below minimum should be corrected."""
        config = {"business_name": "Test", "num_pets": 0}
        validated, warnings = validate_config(config)
        assert validated["num_pets"] == 1
        assert any("num_pets" in w for w in warnings)
    
    def test_num_pets_too_high(self):
        """num_pets above maximum should be corrected."""
        config = {"business_name": "Test", "num_pets": 100}
        validated, warnings = validate_config(config)
        assert validated["num_pets"] == 10
        assert any("num_pets" in w for w in warnings)
    
    def test_num_pets_string_converted(self):
        """num_pets as string should be converted to int."""
        config = {"business_name": "Test", "num_pets": "3"}
        validated, warnings = validate_config(config)
        assert validated["num_pets"] == 3
    
    def test_invalid_service_type(self):
        """Invalid service_type should fall back to 'general'."""
        config = {"business_name": "Test", "service_type": "invalid"}
        validated, warnings = validate_config(config)
        assert validated["service_type"] == "general"
        assert any("service_type" in w for w in warnings)
    
    def test_valid_service_types(self):
        """All valid service types should pass."""
        for service_type in ["general", "boarding", "walking", "drop_in"]:
            config = {"business_name": "Test", "service_type": service_type}
            validated, warnings = validate_config(config)
            assert validated["service_type"] == service_type
    
    def test_empty_business_name(self):
        """Empty business_name should use default."""
        config = {"business_name": ""}
        validated, warnings = validate_config(config)
        assert validated["business_name"] == DEFAULT_CONFIG["business_name"]
        assert any("business_name" in w for w in warnings)
    
    def test_business_name_too_long(self):
        """Business name exceeding max length should be truncated."""
        long_name = "A" * 150
        config = {"business_name": long_name}
        validated, warnings = validate_config(config)
        assert len(validated["business_name"]) == 100
        assert any("business_name" in w for w in warnings)
    
    def test_fillable_string_true(self):
        """fillable as string 'true' should be converted to True."""
        config = {"business_name": "Test", "fillable": "true"}
        validated, warnings = validate_config(config)
        assert validated["fillable"] is True
    
    def test_fillable_string_false(self):
        """fillable as string 'false' should be converted to False."""
        config = {"business_name": "Test", "fillable": "false"}
        validated, warnings = validate_config(config)
        assert validated["fillable"] is False
    
    def test_invalid_color_key(self):
        """Unknown color keys should generate warning."""
        config = {
            "business_name": "Test",
            "colors": {"invalid_color": "#FF0000"}
        }
        validated, warnings = validate_config(config)
        assert any("invalid_color" in w for w in warnings)
    
    def test_invalid_color_value(self):
        """Non-hex color values should generate warning."""
        config = {
            "business_name": "Test",
            "colors": {"primary": "not-a-color"}
        }
        validated, warnings = validate_config(config)
        assert any("primary" in w for w in warnings)
    
    def test_valid_colors(self):
        """Valid hex colors should pass."""
        config = {
            "business_name": "Test",
            "colors": {
                "primary": "#DDD6F3",
                "accent": "#FAC8A0",
            }
        }
        validated, warnings = validate_config(config)
        color_warnings = [w for w in warnings if "color" in w.lower()]
        assert len(color_warnings) == 0
    
    def test_invalid_section_name(self):
        """Unknown section names should generate warning."""
        config = {
            "business_name": "Test",
            "sections": {"invalid_section": True}
        }
        validated, warnings = validate_config(config)
        assert any("invalid_section" in w for w in warnings)
    
    def test_strict_mode_raises(self):
        """Strict mode should raise exception on error."""
        config = {"business_name": "", "num_pets": 100}
        with pytest.raises(ConfigValidationError):
            validate_config(config, strict=True)


class TestGetSectionConfig:
    """Tests for get_section_config function."""
    
    def test_general_defaults(self):
        """General service type should have correct defaults."""
        config = {"service_type": "general"}
        sections = get_section_config(config)
        assert sections["home_access"] is True
        assert sections["vaccinations"] is True
        assert sections["service_specific"] is False
    
    def test_boarding_defaults(self):
        """Boarding service type should have correct defaults."""
        config = {"service_type": "boarding"}
        sections = get_section_config(config)
        assert sections["home_access"] is False
        assert sections["vaccinations"] is True
        assert sections["service_specific"] is True
    
    def test_walking_defaults(self):
        """Walking service type should have correct defaults."""
        config = {"service_type": "walking"}
        sections = get_section_config(config)
        assert sections["home_access"] is False
        assert sections["vaccinations"] is False
        assert sections["behavior_temperament"] is True
        assert sections["service_specific"] is True
    
    def test_drop_in_defaults(self):
        """Drop-in service type should have correct defaults."""
        config = {"service_type": "drop_in"}
        sections = get_section_config(config)
        assert sections["home_access"] is True
        assert sections["service_specific"] is True
    
    def test_section_override(self):
        """User section overrides should take precedence."""
        config = {
            "service_type": "walking",
            "sections": {"vaccinations": True}
        }
        sections = get_section_config(config)
        assert sections["vaccinations"] is True
    
    def test_legacy_include_home_access(self):
        """Legacy include_home_access flag should work."""
        config = {
            "service_type": "boarding",
            "include_home_access": True
        }
        sections = get_section_config(config)
        assert sections["home_access"] is True
    
    def test_unknown_service_type_uses_general(self):
        """Unknown service type should fall back to general."""
        config = {"service_type": "unknown"}
        sections = get_section_config(config)
        assert sections == SECTION_DEFAULTS["general"]


class TestLoadConfig:
    """Tests for load_config function."""
    
    def test_no_config_file_returns_defaults(self):
        """No config file should return default config."""
        config = load_config(None, validate=False)
        assert config["business_name"] == DEFAULT_CONFIG["business_name"]
        assert config["theme"] == DEFAULT_CONFIG["theme"]
    
    def test_missing_file_returns_defaults(self):
        """Missing config file should return defaults with message."""
        config = load_config("/nonexistent/path.yaml", validate=False)
        assert config["business_name"] == DEFAULT_CONFIG["business_name"]
    
    def test_load_valid_yaml(self):
        """Valid YAML file should be loaded correctly."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("business_name: Test Business\n")
            f.write("theme: ocean\n")
            f.write("num_pets: 2\n")
            temp_path = f.name
        
        try:
            config = load_config(temp_path, validate=False)
            assert config["business_name"] == "Test Business"
            assert config["theme"] == "ocean"
            assert config["num_pets"] == 2
        finally:
            os.unlink(temp_path)
    
    def test_load_with_validation(self):
        """Config should be validated when validate=True."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("business_name: Valid Name\n")
            f.write("num_pets: 50\n")  # Invalid, should be capped
            temp_path = f.name
        
        try:
            config = load_config(temp_path, validate=True)
            assert config["num_pets"] == 10  # Should be capped to max
        finally:
            os.unlink(temp_path)


class TestSectionNames:
    """Tests for section name constants."""
    
    def test_all_section_names_defined(self):
        """All section names should be in SECTION_NAMES."""
        expected = [
            "home_access", "vaccinations", "health_medications",
            "feeding_daily_care", "behavior_temperament", "service_specific"
        ]
        assert set(SECTION_NAMES) == set(expected)
    
    def test_all_service_types_have_all_sections(self):
        """All service types should define all sections."""
        for service_type, sections in SECTION_DEFAULTS.items():
            for section_name in SECTION_NAMES:
                assert section_name in sections, f"{service_type} missing {section_name}"
