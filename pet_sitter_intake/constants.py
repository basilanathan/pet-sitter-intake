"""Shared constants for PDF generation."""

from pathlib import Path
from reportlab.lib.units import inch
from reportlab.lib import colors

# ══════════════════════════════════════════════════════════════════════════════
# COLORS
# ══════════════════════════════════════════════════════════════════════════════

WHITE = colors.white

# ══════════════════════════════════════════════════════════════════════════════
# PAGE DIMENSIONS
# ══════════════════════════════════════════════════════════════════════════════

PAGE_W = 7.0 * inch  # Usable width (letter - margins)

MARGINS = {
    "left": 0.75 * inch,
    "right": 0.75 * inch,
    "top": 0.6 * inch,
    "bottom": 0.6 * inch,
}

# ══════════════════════════════════════════════════════════════════════════════
# SPACING SYSTEM (8pt baseline grid)
# ══════════════════════════════════════════════════════════════════════════════

SPACING = {
    "xs": 0.08,      # 6pt - tight spacing within groups
    "sm": 0.12,      # 9pt - between related fields
    "md": 0.18,      # 13pt - between field groups
    "lg": 0.25,      # 18pt - after section headers
    "xl": 0.30,      # 22pt - between major sections
    "xxl": 0.40,     # 29pt - page-level breaks
}

# Legacy spacing values (for gradual migration)
SP_AFTER_HERO = 0.22
SP_AFTER_SEC_HDR = 0.25
SP_BETWEEN_FIELDS = 0.1
SP_AFTER_CHECKBOX = 0.1
SP_SUBSECTION_GAP = 0.15
SP_SECTION_GAP = 0.2
SP_PAGE_BREAK = 0.3

# ══════════════════════════════════════════════════════════════════════════════
# FIELD DIMENSIONS
# ══════════════════════════════════════════════════════════════════════════════

FIELD_HEIGHTS = {
    "single_line": 18,
    "single_line_tall": 20,
    "multiline_sm": 36,
    "multiline_md": 40,
    "multiline_lg": 60,
}

FIELD_EXTRA_SPACE = {
    "default": 24,
    "compact": 20,
    "relaxed": 26,
}

# Checkbox dimensions
CHECKBOX = {
    "box_size": 9,
    "box_size_lg": 12,
    "font_size": 8.5,
    "font_size_lg": 9,
    "vax_box_size": 10,
    "vax_font_size": 8,
}

# ══════════════════════════════════════════════════════════════════════════════
# COLUMN WIDTHS
# ══════════════════════════════════════════════════════════════════════════════

GUTTER = {
    "two_col": 0.25 * inch,
    "three_col": 0.1 * inch,
}

# Vaccination table columns
VAX_COLUMNS = {
    "name": 2.8 * inch,
    "status": 2.6 * inch,
    "date": 1.6 * inch,
}

# Medication table columns
MED_COLUMNS = {
    "name": 2.2 * inch,
    "dosage": 1.2 * inch,
    "frequency": 1.3 * inch,
    "instructions": 2.3 * inch,
}

# Address row columns
ADDRESS_COLUMNS = {
    "city": 2.8 * inch,
    "state": 2.0 * inch,
    "zip": 1.9 * inch,
}

# Pet profile columns
PET_PROFILE_COLUMNS = {
    "age": 1.7 * inch,
    "weight": 1.7 * inch,
    "color": 3.3 * inch,
}

# ══════════════════════════════════════════════════════════════════════════════
# TABLE STYLING
# ══════════════════════════════════════════════════════════════════════════════

TABLE_PADDING = {
    "cell": 8,
    "cell_lg": 14,
    "header": 10,
    "section": 12,
}

TABLE_BORDER = {
    "thin": 0.4,
    "medium": 0.8,
    "thick": 1.5,
}

# ══════════════════════════════════════════════════════════════════════════════
# TYPOGRAPHY
# ══════════════════════════════════════════════════════════════════════════════

FONT_SIZES = {
    "title": 22,
    "subtitle": 11,
    "section": 11,
    "subsection": 9,
    "label": 8.5,
    "body": 8.5,
    "note": 8,
    "footer": 7.5,
    "table_header": 8.5,
    "table_cell": 8.5,
}

LINE_HEIGHTS = {
    "title": 28,
    "normal": 13,
    "tight": 11,
    "relaxed": 15,
}

# ══════════════════════════════════════════════════════════════════════════════
# VALIDATION LIMITS
# ══════════════════════════════════════════════════════════════════════════════

LIMITS = {
    "min_pets": 1,
    "max_pets": 10,
    "min_business_name_len": 1,
    "max_business_name_len": 100,
}

# ══════════════════════════════════════════════════════════════════════════════
# OUTPUT PATHS
# ══════════════════════════════════════════════════════════════════════════════

def get_default_output_path():
    """Get default output path in user's Downloads folder."""
    downloads = Path.home() / "Downloads"
    return str(downloads / "client_intake_form.pdf")


DEFAULT_OUTPUT = get_default_output_path()
