"""Tests for FormContext class."""

from pet_sitter_intake.pages import FormContext
from pet_sitter_intake.flowables import CheckboxRow, FillableCheckboxRow


class TestFormContext:
    """Unit tests for FormContext."""
    
    def test_from_config_basic(self):
        """Should create context from minimal config."""
        config = {"business_name": "Test Business"}
        ctx = FormContext.from_config(config)
        
        assert ctx.business_name == "Test Business"
        assert ctx.fillable is True  # Default
        assert ctx.num_pets == 1  # Default
        assert ctx.service_type == "general"  # Default
    
    def test_from_config_full(self):
        """Should create context from full config."""
        config = {
            "business_name": "Full Config Test",
            "sitter_name": "Jane Doe",
            "services": "Walking, Sitting",
            "location": "Portland, OR",
            "contact": "555-1234",
            "theme": "ocean",
            "service_type": "boarding",
            "num_pets": 3,
            "fillable": False,
        }
        ctx = FormContext.from_config(config)
        
        assert ctx.business_name == "Full Config Test"
        assert ctx.sitter_name == "Jane Doe"
        assert ctx.services == "Walking, Sitting"
        assert ctx.location == "Portland, OR"
        assert ctx.contact == "555-1234"
        assert ctx.service_type == "boarding"
        assert ctx.num_pets == 3
        assert ctx.fillable is False
    
    def test_sitter_display_name_with_sitter(self):
        """Should return sitter_name when set."""
        ctx = FormContext.from_config({
            "business_name": "Business",
            "sitter_name": "Jane",
        })
        assert ctx.sitter_display_name == "Jane"
    
    def test_sitter_display_name_without_sitter(self):
        """Should return business_name when sitter_name not set."""
        ctx = FormContext.from_config({
            "business_name": "Business",
            "sitter_name": "",
        })
        assert ctx.sitter_display_name == "Business"
    
    def test_pet_field_name_single_pet(self):
        """Should return base name for single pet."""
        ctx = FormContext.from_config({"business_name": "Test", "num_pets": 1})
        assert ctx.pet_field_name("name", 1) == "name"
        assert ctx.pet_field_name("breed", 1) == "breed"
    
    def test_pet_field_name_multi_pet(self):
        """Should prefix with pet number for multi-pet."""
        ctx = FormContext.from_config({"business_name": "Test", "num_pets": 3})
        assert ctx.pet_field_name("name", 1) == "pet1_name"
        assert ctx.pet_field_name("breed", 2) == "pet2_breed"
        assert ctx.pet_field_name("age", 3) == "pet3_age"
    
    def test_pet_label_single_pet(self):
        """Should return empty string for single pet."""
        ctx = FormContext.from_config({"business_name": "Test", "num_pets": 1})
        assert ctx.pet_label(1) == ""
    
    def test_pet_label_multi_pet(self):
        """Should return numbered label for multi-pet."""
        ctx = FormContext.from_config({"business_name": "Test", "num_pets": 3})
        assert ctx.pet_label(1) == " #1"
        assert ctx.pet_label(2) == " #2"
        assert ctx.pet_label(3) == " #3"
    
    def test_checkbox_row_fillable(self):
        """Should return FillableCheckboxRow when fillable."""
        ctx = FormContext.from_config({"business_name": "Test", "fillable": True})
        row = ctx.checkbox_row(["A", "B", "C"], field_prefix="test")
        assert isinstance(row, FillableCheckboxRow)
    
    def test_checkbox_row_non_fillable(self):
        """Should return CheckboxRow when not fillable."""
        ctx = FormContext.from_config({"business_name": "Test", "fillable": False})
        row = ctx.checkbox_row(["A", "B", "C"], field_prefix="test")
        assert isinstance(row, CheckboxRow)
    
    def test_checkbox_row_no_prefix(self):
        """Should return CheckboxRow when no prefix (even if fillable)."""
        ctx = FormContext.from_config({"business_name": "Test", "fillable": True})
        row = ctx.checkbox_row(["A", "B", "C"])
        assert isinstance(row, CheckboxRow)
    
    def test_text_field_fillable(self):
        """Should return FillableTextField when fillable."""
        ctx = FormContext.from_config({"business_name": "Test", "fillable": True})
        field = ctx.text_field("test_field")
        assert field is not None
        assert field.field_name == "test_field"
    
    def test_text_field_non_fillable(self):
        """Should return None when not fillable."""
        ctx = FormContext.from_config({"business_name": "Test", "fillable": False})
        field = ctx.text_field("test_field")
        assert field is None
    
    def test_section_enabled_default(self):
        """Should return default section state."""
        ctx = FormContext.from_config({
            "business_name": "Test",
            "service_type": "general",
        })
        assert ctx.section_enabled("home_access") is True
        assert ctx.section_enabled("vaccinations") is True
        assert ctx.section_enabled("service_specific") is False
    
    def test_section_enabled_walking(self):
        """Walking service should have minimal sections by default."""
        ctx = FormContext.from_config({
            "business_name": "Test",
            "service_type": "walking",
        })
        assert ctx.section_enabled("home_access") is False
        assert ctx.section_enabled("vaccinations") is False
        assert ctx.section_enabled("behavior_temperament") is True
        assert ctx.section_enabled("service_specific") is True
    
    def test_calculate_total_pages_general(self):
        """General form should have correct page count."""
        ctx = FormContext.from_config({
            "business_name": "Test",
            "service_type": "general",
            "num_pets": 1,
        })
        # Page 1: owner info, Page 2: home access, Pages 3-4: pet profile, Page 5: auth
        assert ctx.calculate_total_pages() == 5
    
    def test_calculate_total_pages_multi_pet(self):
        """Multi-pet form should scale page count."""
        ctx = FormContext.from_config({
            "business_name": "Test",
            "service_type": "general",
            "num_pets": 3,
        })
        # Page 1: owner info, Page 2: home access, Pages 3-8: 3 pets x 2 pages, Page 9: auth
        assert ctx.calculate_total_pages() == 9
    
    def test_calculate_total_pages_walking(self):
        """Walking form should have fewer pages."""
        ctx = FormContext.from_config({
            "business_name": "Test",
            "service_type": "walking",
            "num_pets": 1,
        })
        # Walking has minimal sections: page 1, pet page, service page, auth
        pages = ctx.calculate_total_pages()
        # No home access, no health/feeding pages
        assert pages < 5
    
    def test_page_tracking(self):
        """Should track current page correctly."""
        ctx = FormContext.from_config({"business_name": "Test"})
        ctx.total_pages = 5
        
        assert ctx.current_page == 1
        assert ctx.page_label() == "Page 1 of 5"
        
        ctx.next_page()
        assert ctx.current_page == 2
        assert ctx.page_label() == "Page 2 of 5"
    
    def test_get_color(self):
        """Should retrieve theme colors."""
        ctx = FormContext.from_config({"business_name": "Test", "theme": "lavender"})
        primary = ctx.get_color("primary")
        assert primary is not None
    
    def test_styles_created(self):
        """Should have paragraph styles."""
        ctx = FormContext.from_config({"business_name": "Test"})
        assert "title" in ctx.styles
        assert "lbl" in ctx.styles
        assert "body" in ctx.styles
        assert "note" in ctx.styles
