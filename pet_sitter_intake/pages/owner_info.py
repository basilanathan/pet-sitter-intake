"""Page 1: Pet Owner Information section."""

from reportlab.platypus import Table, TableStyle, Paragraph

from ..constants import PAGE_W, ADDRESS_COLUMNS
from ..flowables import get_color
from ..layout import sec_hdr, sp, para_row, field, two_col, three_col

from .context import FormContext


def build_hero_section(ctx: FormContext) -> list:
    """Build the hero banner at top of page 1.
    
    Args:
        ctx: Form context with business info and styles
        
    Returns:
        List of flowables for the hero section
    """
    s = ctx.styles
    hero_rows = [
        [Paragraph(ctx.business_name, s["title"])],
        [Paragraph("Client &amp; Pet Intake Form", s["subtitle"])],
        [Paragraph(f"{ctx.location}  \u00b7  {ctx.contact}", s["contact"])],
        [Paragraph(f"<b>Services:</b>  {ctx.services}", s["svc"])],
    ]
    hero = Table(hero_rows, colWidths=[PAGE_W])
    hero.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), ctx.get_color("accent_light")),
        ("TOPPADDING",    (0,0),(-1,0),  18),
        ("TOPPADDING",    (0,1),(-1,-1), 3),
        ("BOTTOMPADDING", (0,-1),(-1,-1), 16),
        ("BOTTOMPADDING", (0,0),(-1,-2), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
    ]))
    return [hero, sp(0.22)]


def build_owner_info_section(ctx: FormContext) -> list:
    """Build the pet owner information section.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables for owner info
    """
    s = ctx.styles
    tc = ctx.theme_colors
    fillable = ctx.fillable
    elements = []
    
    elements += [sec_hdr("SECTION 1  —  PET OWNER INFORMATION", s, theme_colors=tc), sp(0.25)]
    
    # Owner name and contact
    elements += field("Owner Full Name", s, extra_space=26, fillable=fillable, 
                      field_name="owner_name", theme_colors=tc)
    elements.append(two_col("Home Phone", "Cell Phone", s, fillable=fillable,
                            field_names=["home_phone", "cell_phone"], theme_colors=tc))
    elements += field("Email Address", s, extra_space=26, fillable=fillable,
                      field_name="email", theme_colors=tc)
    elements.append(sp(0.08))
    
    # Address
    elements += field("Street Address", s, extra_space=26, fillable=fillable,
                      field_name="street_address", multiline=True, theme_colors=tc)
    elements.append(three_col(
        ["City", "State / Province", "Zip / Postal Code"], s,
        widths=[ADDRESS_COLUMNS["city"], ADDRESS_COLUMNS["state"], ADDRESS_COLUMNS["zip"]],
        fillable=fillable,
        field_names=["city", "state_province", "zip_postal"],
        theme_colors=tc
    ))
    elements.append(sp(0.3))
    
    # Emergency contact
    elements.append(para_row("Emergency Contact  <i>(someone other than you)</i>", s["sublbl"]))
    elements.append(sp(0.1))
    elements.append(two_col("Emergency Contact Name", "Relationship", s, fillable=fillable,
                            field_names=["emergency_name", "emergency_relationship"], theme_colors=tc))
    elements.append(two_col("Phone", "Alt Phone", s, fillable=fillable,
                            field_names=["emergency_phone", "emergency_alt_phone"], theme_colors=tc))
    elements.append(sp(0.3))
    
    # Veterinarian
    elements.append(para_row("Veterinarian Information", s["sublbl"]))
    elements.append(sp(0.1))
    elements.append(two_col("Veterinary Clinic Name", "Clinic Phone", s, fillable=fillable,
                            field_names=["vet_clinic", "vet_phone"], theme_colors=tc))
    elements += field("Clinic Address", s, extra_space=26, fillable=fillable,
                      field_name="vet_address", multiline=True, theme_colors=tc)
    elements.append(sp(0.15))
    
    # Emergency vet
    elements.append(para_row("24-Hour Emergency Vet  <i>(if different from above)</i>", s["sublbl"]))
    elements.append(sp(0.1))
    elements.append(two_col("Emergency Vet Name", "Emergency Vet Phone", s, fillable=fillable,
                            field_names=["emergency_vet_name", "emergency_vet_phone"], theme_colors=tc))
    elements.append(sp(0.2))
    
    # Authorized pickup
    elements += field("Person(s) Authorized to Pick Up My Pet", s, extra_space=26, fillable=fillable,
                      field_name="authorized_pickup", theme_colors=tc)
    
    return elements


def build_communication_prefs(ctx: FormContext) -> list:
    """Build communication preferences section.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables
    """
    s = ctx.styles
    elements = []
    
    elements.append(sp(0.15))
    elements.append(para_row("Communication Preferences", s["sublbl"]))
    elements.append(sp(0.1))
    
    elements.append(para_row("How often would you like updates?", s["lbl"]))
    elements.append(ctx.checkbox_row(
        ["Daily", "Twice daily", "Only if needed", "Other"],
        field_prefix="update_frequency",
        per_row=4
    ))
    
    elements.append(para_row("Preferred contact method:", s["lbl"]))
    elements.append(ctx.checkbox_row(
        ["Text", "Email", "Phone call", "App (specify below)"],
        field_prefix="contact_method",
        per_row=4
    ))
    
    return elements


def build_owner_info_page(ctx: FormContext) -> list:
    """Build the complete owner info page (page 1).
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables for page 1
    """
    elements = []
    elements += build_hero_section(ctx)
    elements += build_owner_info_section(ctx)
    elements += build_communication_prefs(ctx)
    return elements
