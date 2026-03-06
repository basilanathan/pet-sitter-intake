"""Home access and property information page."""

from reportlab.platypus import PageBreak

from ..layout import sec_hdr, sp, para_row, field, pg_hdr

from .context import FormContext


def build_home_access_section(ctx: FormContext) -> list:
    """Build home access section for in-home pet sitting.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables
    """
    s = ctx.styles
    tc = ctx.theme_colors
    fillable = ctx.fillable
    elements = []
    
    elements += [sec_hdr("HOME ACCESS & PROPERTY INFORMATION", s, theme_colors=tc), sp(0.2)]
    
    # Key / Entry information
    elements.append(para_row("Key / Entry Information", s["sublbl"]))
    elements.append(sp(0.1))
    
    elements.append(para_row("Entry method:", s["lbl"]))
    elements.append(ctx.checkbox_row(
        ["Key provided", "Lockbox", "Garage code", "Door code", "Hidden key", "Other"],
        field_prefix="entry_method",
        per_row=3
    ))
    elements.append(sp(0.1))
    
    elements += field("Lockbox / key location", s, fillable=fillable, 
                      field_name="key_location", theme_colors=tc)
    elements += field("Entry code(s)", s, fillable=fillable, 
                      field_name="entry_codes", theme_colors=tc)
    elements += field("Alarm code & disarm instructions", s, fillable=fillable, 
                      field_name="alarm_code", multiline=True, theme_colors=tc)
    elements.append(sp(0.12))
    
    # Property details
    elements.append(para_row("Property Details", s["sublbl"]))
    elements.append(sp(0.1))
    elements += field("WiFi network & password", s, fillable=fillable, 
                      field_name="wifi_info", theme_colors=tc)
    elements += field("Parking instructions", s, fillable=fillable, 
                      field_name="parking", multiline=True, theme_colors=tc)
    elements += field("Thermostat / HVAC notes", s, fillable=fillable, 
                      field_name="thermostat", multiline=True, theme_colors=tc)
    elements += field("Off-limits rooms or areas", s, fillable=fillable, 
                      field_name="off_limits", theme_colors=tc)
    elements += field("Other house rules (TV on for pet, mail, plants, etc.)", s, extra_lines=2, 
                      fillable=fillable, field_name="house_rules", theme_colors=tc)
    
    return elements


def build_home_access_page(ctx: FormContext) -> list:
    """Build the complete home access page.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables including PageBreak, or empty list if disabled
    """
    if not ctx.section_enabled("home_access"):
        return []
    
    s = ctx.styles
    tc = ctx.theme_colors
    elements = []
    
    elements.append(PageBreak())
    ctx.next_page()
    elements += pg_hdr(ctx.business_name, ctx.page_label(), s, theme_colors=tc)
    elements += build_home_access_section(ctx)
    
    return elements
