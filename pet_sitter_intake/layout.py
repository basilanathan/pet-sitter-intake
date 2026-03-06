"""Layout primitives and style helpers for PDF forms."""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER

from .constants import PAGE_W
from .flowables import FillableTextField, _c


def sty():
    """Create paragraph styles using current theme colors.
    
    Returns:
        Dict mapping style names to ParagraphStyle objects.
    """
    s = {}
    
    def ps(name, **kw):
        defaults = dict(
            fontName="Helvetica", fontSize=9, textColor=_c("text"), leading=13,
            leftIndent=0, firstLineIndent=0, bulletIndent=0
        )
        defaults.update(kw)
        return ParagraphStyle(name, **defaults)

    s["title"]    = ps("title",    fontName="Helvetica-Bold", fontSize=22, textColor=_c("primary_dark"), alignment=TA_CENTER, spaceAfter=4, leading=28)
    s["subtitle"] = ps("subtitle", fontSize=11, textColor=_c("text_muted"), alignment=TA_CENTER, spaceAfter=3)
    s["contact"]  = ps("contact",  fontSize=9,  textColor=_c("text_muted"), alignment=TA_CENTER, spaceAfter=2)
    s["svc"]      = ps("svc",      fontSize=8.5, textColor=_c("text_muted"), alignment=TA_CENTER)
    s["sec"]      = ps("sec",      fontName="Helvetica-Bold", fontSize=11, textColor=_c("primary_dark"))
    s["lbl"]      = ps("lbl",      fontName="Helvetica-Bold", fontSize=8.5, textColor=_c("text_muted"), spaceAfter=3, leading=12)
    s["sublbl"]   = ps("sublbl",   fontName="Helvetica-Bold", fontSize=9,   textColor=_c("primary_dark"), spaceAfter=3, leading=13)
    s["note"]     = ps("note",     fontName="Helvetica-Oblique", fontSize=8, textColor=_c("text_light"), spaceAfter=6, leading=11)
    s["body"]     = ps("body",     fontSize=8.5, textColor=_c("text"), spaceAfter=3, leading=13)
    s["foot"]     = ps("foot",     fontSize=7.5, textColor=_c("text_light"), alignment=TA_CENTER)
    s["th"]       = ps("th",       fontName="Helvetica-Bold", fontSize=8.5, textColor=_c("primary_dark"), leading=11)
    s["td"]       = ps("td",       fontSize=8.5, textColor=_c("text_muted"), leading=11)
    s["office"]   = ps("office",   fontName="Helvetica-Oblique", fontSize=7.5, textColor=_c("text_light"), alignment=TA_CENTER)
    return s


def sp(h=0.1):
    """Vertical spacer.
    
    Args:
        h: Height in inches (default 0.1)
    """
    return Spacer(1, h * inch)


def hr(color=None, thick=1.0, after=8):
    """Horizontal rule.
    
    Args:
        color: Line color (default: accent color from theme)
        thick: Line thickness in points
        after: Space after in points
    """
    return HRFlowable(width="100%", thickness=thick, color=color or _c("accent"), spaceAfter=after)


def sec_hdr(title, s):
    """Section header band with background color.
    
    Args:
        title: Section title text
        s: Styles dict from sty()
    """
    t = Table([[Paragraph(title, s["sec"])]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), _c("primary")),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
    ]))
    return t


def para_row(text, style):
    """Wrap a single Paragraph in a full-width Table for consistent alignment."""
    t = Table([[Paragraph(text, style)]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    return t


def field(label, s, extra_space=24, extra_lines=1, fillable=False, field_name=None, multiline=None):
    """Label + one or more write-on underlines (or fillable text fields).
    
    Args:
        label: Field label text
        s: Styles dict from sty()
        extra_space: Space after field (for print version)
        extra_lines: Number of lines (for print version); if >1, fillable becomes multiline
        fillable: Whether to generate interactive form field
        field_name: Unique name for fillable field
        multiline: Force multiline mode (auto-detected from extra_lines if None)
    """
    cell = []
    if label:
        cell.append(Paragraph(label, s["lbl"]))
    
    if fillable and field_name:
        is_multiline = multiline if multiline is not None else (extra_lines > 1)
        if is_multiline:
            height = max(40, 22 * extra_lines)
        else:
            height = 20
        cell.append(FillableTextField(field_name, PAGE_W - 4, height=height, multiline=is_multiline))
        cell.append(Spacer(1, extra_space - 10 if not is_multiline else 6))
    else:
        for _ in range(extra_lines):
            cell.append(HRFlowable(width="100%", thickness=0.8, color=_c("primary_mid"), spaceAfter=extra_space))
    
    t = Table([[cell]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    return [t]


def two_col(left_label, right_label, s, lw=None, rw=None, fillable=False, field_names=None):
    """Two fields side by side.
    
    Args:
        left_label: Label for left field
        right_label: Label for right field
        s: Styles dict from sty()
        lw: Left column width (default: half of PAGE_W minus gutter)
        rw: Right column width (default: half of PAGE_W minus gutter)
        fillable: Whether to generate interactive form fields
        field_names: Tuple of (left_field_name, right_field_name)
    """
    gutter = 0.25 * inch
    lw = lw or (PAGE_W - gutter) / 2
    rw = rw or (PAGE_W - gutter) / 2
    
    if fillable and field_names:
        cell_l = [
            Paragraph(left_label, s["lbl"]),
            FillableTextField(field_names[0], lw - 4, height=18),
            Spacer(1, 10),
        ]
        cell_r = [
            Paragraph(right_label, s["lbl"]),
            FillableTextField(field_names[1], rw - 4, height=18),
            Spacer(1, 10),
        ]
    else:
        cell_l = [
            Paragraph(left_label, s["lbl"]),
            HRFlowable(width="100%", thickness=0.8, color=_c("primary_mid"), spaceAfter=20),
        ]
        cell_r = [
            Paragraph(right_label, s["lbl"]),
            HRFlowable(width="100%", thickness=0.8, color=_c("primary_mid"), spaceAfter=20),
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


def three_col(labels, s, widths=None, fillable=False, field_names=None):
    """Three fields side by side.
    
    Args:
        labels: List of three label strings
        s: Styles dict from sty()
        widths: List of three column widths (default: equal thirds)
        fillable: Whether to generate interactive form fields
        field_names: List of three field names
    """
    gutter = 0.1 * inch
    widths = widths or [(PAGE_W - 3 * gutter) / 3] * 3
    cells = []
    
    if fillable and field_names:
        for lbl, w, fname in zip(labels, widths, field_names):
            cells.append([
                Paragraph(lbl, s["lbl"]),
                FillableTextField(fname, w - 4, height=18),
                Spacer(1, 10),
            ])
    else:
        for lbl, w in zip(labels, widths):
            cells.append([
                Paragraph(lbl, s["lbl"]),
                HRFlowable(width="100%", thickness=0.8, color=_c("primary_mid"), spaceAfter=20),
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


def pg_hdr(name, label, s):
    """Page header with business name and page indicator.
    
    Args:
        name: Business name
        label: Page label (e.g., "Page 2 of 5")
        s: Styles dict from sty()
    """
    return [
        Paragraph(name, s["title"]),
        Paragraph(f"Client &amp; Pet Intake Form  \u00b7  {label}", s["subtitle"]),
        hr(None, 1.5, 12),
    ]


def auth_block(title, body, s):
    """Full-width authorization block with background.
    
    Args:
        title: Block title (rendered bold)
        body: Block body text
        s: Styles dict from sty()
    """
    content = [
        Paragraph(f"<b>{title}</b>", s["sublbl"]),
        Paragraph(body, s["body"]),
    ]
    t = Table([[content]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), _c("accent_light")),
        ("TOPPADDING",    (0,0),(-1,-1), 9),
        ("BOTTOMPADDING", (0,0),(-1,-1), 9),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    return t
