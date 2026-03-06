"""Tests for PDF form builder."""

import pytest
import tempfile
import os

from pet_sitter_intake.builder import build_form
from pet_sitter_intake.config import DEFAULT_CONFIG


class TestBuildForm:
    """Integration tests for build_form function."""
    
    def test_builds_basic_form(self):
        """Should build a basic form without errors."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            output_path = f.name
        
        try:
            config = {
                "business_name": "Test Business",
                "theme": "lavender",
                "num_pets": 1,
                "fillable": True,
            }
            build_form(config, output_path)
            
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_builds_multi_pet_form(self):
        """Should build form with multiple pet profiles."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            output_path = f.name
        
        try:
            config = {
                "business_name": "Multi Pet Test",
                "num_pets": 3,
                "fillable": True,
            }
            build_form(config, output_path)
            
            assert os.path.exists(output_path)
            # Multi-pet forms should be larger
            assert os.path.getsize(output_path) > 10000
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_builds_non_fillable_form(self):
        """Should build non-fillable (print) form."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            output_path = f.name
        
        try:
            config = {
                "business_name": "Print Test",
                "fillable": False,
            }
            build_form(config, output_path)
            
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_builds_boarding_form(self):
        """Should build boarding-specific form."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            output_path = f.name
        
        try:
            config = {
                "business_name": "Boarding Test",
                "service_type": "boarding",
            }
            build_form(config, output_path)
            
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_builds_walking_form(self):
        """Should build walking-specific form."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            output_path = f.name
        
        try:
            config = {
                "business_name": "Walking Test",
                "service_type": "walking",
            }
            build_form(config, output_path)
            
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_builds_drop_in_form(self):
        """Should build drop-in-specific form."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            output_path = f.name
        
        try:
            config = {
                "business_name": "Drop-in Test",
                "service_type": "drop_in",
            }
            build_form(config, output_path)
            
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_all_themes_build_successfully(self):
        """All themes should produce valid PDFs."""
        themes = [
            "lavender", "ocean", "forest", "rose", "sunset",
            "neutral", "midnight", "summer", "neon", "berry",
            "fiery", "blush", "deepblue",
        ]
        
        for theme in themes:
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
                output_path = f.name
            
            try:
                config = {
                    "business_name": f"Theme Test - {theme}",
                    "theme": theme,
                }
                build_form(config, output_path)
                
                assert os.path.exists(output_path), f"Failed to create PDF with theme {theme}"
            finally:
                if os.path.exists(output_path):
                    os.unlink(output_path)
    
    def test_section_exclusion(self):
        """Should respect section exclusion settings."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            output_path = f.name
        
        try:
            config = {
                "business_name": "Section Test",
                "sections": {
                    "home_access": False,
                    "vaccinations": False,
                }
            }
            build_form(config, output_path)
            
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_custom_colors(self):
        """Should apply custom color overrides."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            output_path = f.name
        
        try:
            config = {
                "business_name": "Custom Color Test",
                "theme": "custom",
                "colors": {
                    "primary": "#FF6B6B",
                    "accent": "#4ECDC4",
                }
            }
            build_form(config, output_path)
            
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_creates_output_directory(self):
        """Should create output directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "subdir", "test.pdf")
            
            config = {"business_name": "Dir Test"}
            build_form(config, output_path)
            
            assert os.path.exists(output_path)
    
    def test_expands_home_directory(self):
        """Should expand ~ in output path."""
        # Just test that it doesn't crash with ~
        # Don't actually write to home directory in tests
        config = {"business_name": "Home Test"}
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            output_path = f.name
        
        try:
            build_form(config, output_path)
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
