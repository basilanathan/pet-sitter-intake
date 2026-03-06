"""Form context for passing state through page builders."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..config import DEFAULT_CONFIG, get_section_config
from ..themes import get_theme_colors
from ..layout import sty
from ..flowables import CheckboxRow, FillableCheckboxRow, FillableTextField, get_color
from ..constants import PAGE_W, CHECKBOX


@dataclass
class FormContext:
    """Context object carrying all state needed for form generation.
    
    This replaces passing 5-6 parameters (s, fillable, theme_colors, etc.)
    to every function. Page builders receive a single FormContext.
    
    Attributes:
        config: Full configuration dict
        theme_colors: Dict mapping color keys to reportlab Color objects
        styles: Dict of ParagraphStyle objects from sty()
        fillable: Whether to generate interactive form fields
        sections: Dict mapping section names to enabled status
        num_pets: Number of pet profiles to generate
        service_type: Service type (general, boarding, walking, drop_in)
    """
    config: Dict[str, Any]
    theme_colors: Dict[str, Any] = field(default_factory=dict)
    styles: Dict[str, Any] = field(default_factory=dict)
    fillable: bool = True
    sections: Dict[str, bool] = field(default_factory=dict)
    num_pets: int = 1
    service_type: str = "general"
    
    # Page tracking
    current_page: int = 1
    total_pages: int = 1
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "FormContext":
        """Create FormContext from a config dict.
        
        Args:
            config: Configuration dict with business info, theme, etc.
            
        Returns:
            Fully initialized FormContext
        """
        theme_colors = get_theme_colors(config)
        styles = sty(theme_colors)
        sections = get_section_config(config)
        
        return cls(
            config=config,
            theme_colors=theme_colors,
            styles=styles,
            fillable=config.get("fillable", DEFAULT_CONFIG["fillable"]),
            sections=sections,
            num_pets=config.get("num_pets", DEFAULT_CONFIG["num_pets"]),
            service_type=config.get("service_type", DEFAULT_CONFIG["service_type"]),
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # Business info properties (convenience accessors)
    # ─────────────────────────────────────────────────────────────────────────
    
    @property
    def business_name(self) -> str:
        return self.config.get("business_name", DEFAULT_CONFIG["business_name"])
    
    @property
    def sitter_name(self) -> str:
        return self.config.get("sitter_name", DEFAULT_CONFIG["sitter_name"])
    
    @property
    def services(self) -> str:
        return self.config.get("services", DEFAULT_CONFIG["services"])
    
    @property
    def location(self) -> str:
        return self.config.get("location", DEFAULT_CONFIG["location"])
    
    @property
    def contact(self) -> str:
        return self.config.get("contact", DEFAULT_CONFIG["contact"])
    
    @property
    def sitter_display_name(self) -> str:
        """Return sitter_name if set, otherwise business_name."""
        return self.sitter_name if self.sitter_name else self.business_name
    
    # ─────────────────────────────────────────────────────────────────────────
    # Field name helpers
    # ─────────────────────────────────────────────────────────────────────────
    
    def pet_field_name(self, base_name: str, pet_num: int) -> str:
        """Generate field name with pet prefix if multi-pet form.
        
        Args:
            base_name: Base field name (e.g., "name", "breed")
            pet_num: Pet number (1-indexed)
            
        Returns:
            Field name like "pet2_name" for multi-pet, or "name" for single pet
        """
        if self.num_pets > 1:
            return f"pet{pet_num}_{base_name}"
        return base_name
    
    def pet_label(self, pet_num: int) -> str:
        """Generate pet label suffix for multi-pet forms.
        
        Args:
            pet_num: Pet number (1-indexed)
            
        Returns:
            Label like " #2" for multi-pet, or "" for single pet
        """
        if self.num_pets > 1:
            return f" #{pet_num}"
        return ""
    
    # ─────────────────────────────────────────────────────────────────────────
    # Factory methods for form elements
    # ─────────────────────────────────────────────────────────────────────────
    
    def checkbox_row(self, options: List[str], field_prefix: Optional[str] = None,
                     per_row: int = 4):
        """Create a checkbox row, automatically handling fillable toggle.
        
        Args:
            options: List of checkbox label strings
            field_prefix: Required for fillable mode - prefix for field names
            per_row: Number of checkboxes per row
            
        Returns:
            CheckboxRow or FillableCheckboxRow flowable
        """
        if self.fillable and field_prefix:
            return FillableCheckboxRow(
                field_prefix,
                options,
                per_row=per_row,
                box_size=CHECKBOX["box_size_lg"],
                font_size=CHECKBOX["font_size_lg"],
                theme_colors=self.theme_colors
            )
        return CheckboxRow(
            options,
            per_row=per_row,
            box_size=CHECKBOX["box_size"],
            font_size=CHECKBOX["font_size"],
            theme_colors=self.theme_colors
        )
    
    def text_field(self, field_name: str, width: Optional[float] = None,
                   height: int = 18, multiline: bool = False) -> Optional[FillableTextField]:
        """Create a fillable text field if in fillable mode.
        
        Args:
            field_name: Unique field name
            width: Field width in points (default: PAGE_W - 4)
            height: Field height in points
            multiline: Whether to allow multiple lines
            
        Returns:
            FillableTextField if fillable mode, None otherwise
        """
        if not self.fillable:
            return None
        width = width or (PAGE_W - 4)
        return FillableTextField(
            field_name, width, height=height,
            multiline=multiline, theme_colors=self.theme_colors
        )
    
    def get_color(self, key: str):
        """Get a color from the theme palette.
        
        Args:
            key: Color key (primary, accent, text, etc.)
            
        Returns:
            reportlab Color object
        """
        return get_color(self.theme_colors, key)
    
    # ─────────────────────────────────────────────────────────────────────────
    # Section checks
    # ─────────────────────────────────────────────────────────────────────────
    
    def section_enabled(self, section_name: str) -> bool:
        """Check if a section is enabled.
        
        Args:
            section_name: Section key (e.g., "vaccinations", "home_access")
            
        Returns:
            True if section should be included
        """
        return self.sections.get(section_name, True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # Page tracking
    # ─────────────────────────────────────────────────────────────────────────
    
    def calculate_total_pages(self) -> int:
        """Calculate total page count based on config.
        
        Returns:
            Total number of pages in the form
        """
        pages = 1  # Owner info (always page 1)
        
        if self.section_enabled("home_access"):
            pages += 1
        
        # Pet pages: 1-2 pages per pet
        pet_page_2_sections = ["health_medications", "behavior_temperament", "feeding_daily_care"]
        pages_per_pet = 1
        if any(self.section_enabled(sec) for sec in pet_page_2_sections):
            pages_per_pet = 2
        pages += pages_per_pet * self.num_pets
        
        if self.section_enabled("service_specific") and self.service_type != "general":
            pages += 1
        
        pages += 1  # Authorization (always last)
        
        return pages
    
    def next_page(self) -> int:
        """Increment page counter and return new page number."""
        self.current_page += 1
        return self.current_page
    
    def page_label(self) -> str:
        """Get current page label like 'Page 2 of 5'."""
        return f"Page {self.current_page} of {self.total_pages}"
