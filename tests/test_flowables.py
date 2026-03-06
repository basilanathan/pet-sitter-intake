"""Tests for custom flowable elements."""

import pytest
from reportlab.lib import colors

from pet_sitter_intake.flowables import (
    CheckboxRow,
    FillableCheckboxRow,
    FillableTextField,
    VaxCheckboxRow,
    get_color,
)


class TestGetColor:
    """Tests for get_color helper function."""
    
    def test_returns_color_from_theme(self):
        """Should return color from theme dict."""
        theme_colors = {"primary": colors.HexColor("#FF0000")}
        result = get_color(theme_colors, "primary")
        assert result.hexval() == "0xff0000"
    
    def test_returns_fallback_when_key_missing(self):
        """Should return fallback color when key not in theme."""
        theme_colors = {"primary": colors.HexColor("#FF0000")}
        result = get_color(theme_colors, "nonexistent")
        assert result.hexval() == "0x000000"  # Default fallback
    
    def test_returns_fallback_when_theme_is_none(self):
        """Should return fallback when theme_colors is None."""
        result = get_color(None, "primary")
        assert result.hexval() == "0x000000"
    
    def test_custom_fallback(self):
        """Should use custom fallback when provided."""
        result = get_color(None, "primary", fallback="#FFFFFF")
        assert result.hexval() == "0xffffff"


class TestCheckboxRow:
    """Tests for CheckboxRow flowable."""
    
    def test_creates_with_options(self):
        """Should create with list of options."""
        options = ["Option 1", "Option 2", "Option 3"]
        row = CheckboxRow(options)
        assert row.options == options
        assert row.per_row == 4  # Default
    
    def test_respects_per_row(self):
        """Should respect per_row parameter."""
        row = CheckboxRow(["A", "B", "C", "D", "E"], per_row=2)
        assert row.per_row == 2
    
    def test_calculates_height_for_single_row(self):
        """Height should be correct for single row."""
        row = CheckboxRow(["A", "B"], per_row=4)
        expected_height = 1 * (9 + 16)  # 1 row, box_size=9
        assert row.height == expected_height
    
    def test_calculates_height_for_multiple_rows(self):
        """Height should be correct for multiple rows."""
        row = CheckboxRow(["A", "B", "C", "D", "E"], per_row=2)
        expected_height = 3 * (9 + 16)  # 3 rows
        assert row.height == expected_height
    
    def test_accepts_theme_colors(self):
        """Should accept theme_colors parameter."""
        theme = {"primary_dark": colors.HexColor("#FF0000")}
        row = CheckboxRow(["A"], theme_colors=theme)
        assert row.theme_colors == theme
    
    def test_wrap_returns_dimensions(self):
        """wrap() should return width and height."""
        row = CheckboxRow(["A", "B"])
        width, height = row.wrap(500, 1000)
        assert width == 500
        assert height == row.height


class TestFillableCheckboxRow:
    """Tests for FillableCheckboxRow flowable."""
    
    def test_creates_with_field_prefix(self):
        """Should create with field prefix and options."""
        row = FillableCheckboxRow("pet_fears", ["Storm", "Vacuum"])
        assert row.field_prefix == "pet_fears"
        assert row.options == ["Storm", "Vacuum"]
    
    def test_uses_larger_box_size(self):
        """Fillable checkboxes should use larger default box size."""
        row = FillableCheckboxRow("test", ["A"])
        assert row.box_size == 12  # Larger than non-fillable
    
    def test_accepts_theme_colors(self):
        """Should accept theme_colors parameter."""
        theme = {"primary_dark": colors.HexColor("#0000FF")}
        row = FillableCheckboxRow("test", ["A"], theme_colors=theme)
        assert row.theme_colors == theme


class TestFillableTextField:
    """Tests for FillableTextField flowable."""
    
    def test_creates_with_name_and_width(self):
        """Should create with field name and width."""
        field = FillableTextField("owner_name", 300)
        assert field.field_name == "owner_name"
        assert field.field_width == 300
    
    def test_default_height(self):
        """Default height should be 18."""
        field = FillableTextField("test", 200)
        assert field.field_height == 18
    
    def test_multiline_minimum_height(self):
        """Multiline fields should have minimum height of 36."""
        field = FillableTextField("test", 200, height=20, multiline=True)
        assert field.field_height == 36
    
    def test_multiline_respects_larger_height(self):
        """Multiline fields should respect heights larger than minimum."""
        field = FillableTextField("test", 200, height=60, multiline=True)
        assert field.field_height == 60
    
    def test_single_line_respects_height(self):
        """Single-line fields should respect custom height."""
        field = FillableTextField("test", 200, height=25)
        assert field.field_height == 25
    
    def test_accepts_theme_colors(self):
        """Should accept theme_colors parameter."""
        theme = {"primary_mid": colors.HexColor("#AABBCC")}
        field = FillableTextField("test", 200, theme_colors=theme)
        assert field.theme_colors == theme
    
    def test_wrap_returns_dimensions(self):
        """wrap() should return field dimensions."""
        field = FillableTextField("test", 300, height=25)
        width, height = field.wrap(500, 1000)
        assert width == 300
        assert height == 25


class TestVaxCheckboxRow:
    """Tests for VaxCheckboxRow flowable."""
    
    def test_creates_with_prefix_and_options(self):
        """Should create with field prefix and status options."""
        row = VaxCheckboxRow("pet1_vax_rabies", ["Yes", "No", "Exempt"])
        assert row.field_prefix == "pet1_vax_rabies"
        assert row.options == ["Yes", "No", "Exempt"]
    
    def test_compact_height(self):
        """Should have compact height for inline display."""
        row = VaxCheckboxRow("test", ["Yes", "No"])
        expected_height = 10 + 6  # box_size + padding
        assert row.height == expected_height
    
    def test_accepts_theme_colors(self):
        """Should accept theme_colors parameter."""
        theme = {"primary_dark": colors.HexColor("#123456")}
        row = VaxCheckboxRow("test", ["Yes", "No"], theme_colors=theme)
        assert row.theme_colors == theme
