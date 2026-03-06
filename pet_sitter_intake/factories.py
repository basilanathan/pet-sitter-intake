"""Factory functions for creating form elements.

These factories abstract the fillable vs non-fillable branching,
reducing repetitive if/else blocks throughout the codebase.
"""

from reportlab.platypus import Spacer, HRFlowable, Paragraph, Table, TableStyle
from reportlab.lib.units import inch

from .constants import (
    PAGE_W, FIELD_HEIGHTS, FIELD_EXTRA_SPACE, CHECKBOX,
    GUTTER, SPACING,
)
from .flowables import (
    CheckboxRow, FillableCheckboxRow, FillableTextField, VaxCheckboxRow,
    get_color,
)


def checkbox_row(options, per_row=4, fillable=False, field_prefix=None, theme_colors=None):
    """Create a checkbox row, either fillable or static.
    
    Args:
        options: List of checkbox label strings
        per_row: Number of checkboxes per row
        fillable: Whether to create interactive form fields
        field_prefix: Required for fillable mode - prefix for field names
        theme_colors: Dict of theme colors
        
    Returns:
        CheckboxRow or FillableCheckboxRow flowable
    """
    if fillable and field_prefix:
        return FillableCheckboxRow(
            field_prefix, 
            options, 
            per_row=per_row,
            box_size=CHECKBOX["box_size_lg"],
            font_size=CHECKBOX["font_size_lg"],
            theme_colors=theme_colors
        )
    return CheckboxRow(
        options, 
        per_row=per_row,
        box_size=CHECKBOX["box_size"],
        font_size=CHECKBOX["font_size"],
        theme_colors=theme_colors
    )


def vax_checkbox_row(field_prefix, options, fillable=False, theme_colors=None):
    """Create a compact vaccination status checkbox row.
    
    Args:
        field_prefix: Prefix for field names (e.g., "pet1_vax_rabies")
        options: List of status options (e.g., ["Yes", "No", "Exempt"])
        fillable: Whether to create interactive form fields
        theme_colors: Dict of theme colors
        
    Returns:
        VaxCheckboxRow flowable (fillable) or formatted Paragraph (static)
    """
    if fillable:
        return VaxCheckboxRow(
            field_prefix, 
            options,
            box_size=CHECKBOX["vax_box_size"],
            font_size=CHECKBOX["vax_font_size"],
            theme_colors=theme_colors
        )
    opts_str = "   /   ".join(options)
    return Paragraph(opts_str, _get_td_style(theme_colors))


def text_field(label, styles, fillable=False, field_name=None, 
               extra_space=None, extra_lines=1, multiline=None, theme_colors=None):
    """Create a labeled text field, either fillable or with underlines.
    
    Args:
        label: Field label text (can be None for label-less field)
        styles: Dict of paragraph styles from sty()
        fillable: Whether to create interactive form field
        field_name: Required for fillable mode - unique field name
        extra_space: Space after field in points (default: 24)
        extra_lines: Number of lines for static mode
        multiline: Force multiline mode (auto-detected from extra_lines if None)
        theme_colors: Dict of theme colors
        
    Returns:
        List of flowables (label + field + spacer)
    """
    extra_space = extra_space or FIELD_EXTRA_SPACE["default"]
    cell = []
    
    if label:
        cell.append(Paragraph(label, styles["lbl"]))
    
    if fillable and field_name:
        is_multiline = multiline if multiline is not None else (extra_lines > 1)
        if is_multiline:
            height = max(FIELD_HEIGHTS["multiline_md"], 22 * extra_lines)
        else:
            height = FIELD_HEIGHTS["single_line_tall"]
        cell.append(FillableTextField(
            field_name, 
            PAGE_W - 4, 
            height=height, 
            multiline=is_multiline,
            theme_colors=theme_colors
        ))
        cell.append(Spacer(1, extra_space - 10 if not is_multiline else 6))
    else:
        for _ in range(extra_lines):
            cell.append(HRFlowable(
                width="100%", 
                thickness=0.8, 
                color=get_color(theme_colors, "primary_mid"),
                spaceAfter=extra_space
            ))
    
    t = Table([[cell]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    return [t]


def two_col_field(left_label, right_label, styles, fillable=False, 
                  field_names=None, widths=None, theme_colors=None):
    """Create two side-by-side fields.
    
    Args:
        left_label: Label for left field
        right_label: Label for right field
        styles: Dict of paragraph styles from sty()
        fillable: Whether to create interactive form fields
        field_names: Tuple of (left_name, right_name) for fillable mode
        widths: Tuple of (left_width, right_width) in points
        theme_colors: Dict of theme colors
        
    Returns:
        Table flowable with two fields
    """
    gutter = GUTTER["two_col"]
    lw = widths[0] if widths else (PAGE_W - gutter) / 2
    rw = widths[1] if widths else (PAGE_W - gutter) / 2
    
    if fillable and field_names:
        cell_l = [
            Paragraph(left_label, styles["lbl"]),
            FillableTextField(field_names[0], lw - 4, height=18, theme_colors=theme_colors),
            Spacer(1, 10),
        ]
        cell_r = [
            Paragraph(right_label, styles["lbl"]),
            FillableTextField(field_names[1], rw - 4, height=18, theme_colors=theme_colors),
            Spacer(1, 10),
        ]
    else:
        cell_l = [
            Paragraph(left_label, styles["lbl"]),
            HRFlowable(width="100%", thickness=0.8, 
                       color=get_color(theme_colors, "primary_mid"), spaceAfter=20),
        ]
        cell_r = [
            Paragraph(right_label, styles["lbl"]),
            HRFlowable(width="100%", thickness=0.8, 
                       color=get_color(theme_colors, "primary_mid"), spaceAfter=20),
        ]
    
    t = Table([[cell_l, cell_r]], colWidths=[lw, rw + gutter])
    t.setStyle(TableStyle([
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(0,-1),  0),
        ("RIGHTPADDING",  (0,0),(0,-1),  gutter),
        ("LEFTPADDING",   (1,0),(1,-1),  0),
        ("RIGHTPADDING",  (1,0),(1,-1),  0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    return t


def three_col_field(labels, styles, fillable=False, field_names=None, 
                    widths=None, theme_colors=None):
    """Create three side-by-side fields.
    
    Args:
        labels: List of three label strings
        styles: Dict of paragraph styles from sty()
        fillable: Whether to create interactive form fields
        field_names: List of three field names for fillable mode
        widths: List of three column widths in points
        theme_colors: Dict of theme colors
        
    Returns:
        Table flowable with three fields
    """
    gutter = GUTTER["three_col"]
    widths = widths or [(PAGE_W - 3 * gutter) / 3] * 3
    cells = []
    
    if fillable and field_names:
        for lbl, w, fname in zip(labels, widths, field_names):
            cells.append([
                Paragraph(lbl, styles["lbl"]),
                FillableTextField(fname, w - 4, height=18, theme_colors=theme_colors),
                Spacer(1, 10),
            ])
    else:
        for lbl, w in zip(labels, widths):
            cells.append([
                Paragraph(lbl, styles["lbl"]),
                HRFlowable(width="100%", thickness=0.8, 
                           color=get_color(theme_colors, "primary_mid"), spaceAfter=20),
            ])
    
    col_widths = [w + gutter for w in widths]
    t = Table([cells], colWidths=col_widths)
    t.setStyle(TableStyle([
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), gutter),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    return t


def spacer(size_key="md"):
    """Create a vertical spacer using the spacing system.
    
    Args:
        size_key: One of 'xs', 'sm', 'md', 'lg', 'xl', 'xxl' or a float
        
    Returns:
        Spacer flowable
    """
    if isinstance(size_key, (int, float)):
        height = size_key
    else:
        height = SPACING.get(size_key, SPACING["md"])
    return Spacer(1, height * inch)


def _get_td_style(theme_colors):
    """Get a basic table cell paragraph style. Internal helper."""
    from reportlab.lib.styles import ParagraphStyle
    return ParagraphStyle(
        "td_factory",
        fontName="Helvetica",
        fontSize=8.5,
        textColor=get_color(theme_colors, "text_muted"),
        leading=11
    )
