"""Service-specific pages for walking, boarding, drop-in."""

from reportlab.platypus import PageBreak

from ..layout import sec_hdr, sp, para_row, field, pg_hdr

from .context import FormContext


def build_walking_section(ctx: FormContext) -> list:
    """Build dog walking details section.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables
    """
    s = ctx.styles
    tc = ctx.theme_colors
    fillable = ctx.fillable
    elements = []
    
    elements += [sec_hdr("DOG WALKING DETAILS", s, theme_colors=tc), sp(0.2)]
    elements += field("Leash & harness location", s, fillable=fillable, 
                      field_name="leash_location", theme_colors=tc)
    elements += field("Poop bag location", s, fillable=fillable, 
                      field_name="poop_bags", theme_colors=tc)
    
    elements.append(para_row("Leash behavior:", s["lbl"]))
    elements.append(ctx.checkbox_row(
        ["Loose leash", "Pulls — needs management", "Reactive on leash", "Heel trained"],
        field_prefix="leash_behavior",
        per_row=4
    ))
    elements.append(sp(0.1))
    
    elements += field("Preferred walking route / areas to avoid", s, fillable=fillable,
                      field_name="walk_route", multiline=True, theme_colors=tc)
    elements += field("Walk duration preference", s, fillable=fillable, 
                      field_name="walk_duration", theme_colors=tc)
    
    return elements


def build_boarding_section(ctx: FormContext) -> list:
    """Build boarding details section.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables
    """
    s = ctx.styles
    tc = ctx.theme_colors
    fillable = ctx.fillable
    elements = []
    
    elements += [sec_hdr("BOARDING DETAILS", s, theme_colors=tc), sp(0.2)]
    
    elements.append(para_row("Items to bring:", s["lbl"]))
    elements.append(ctx.checkbox_row(
        ["Food", "Bed/blanket", "Favorite toys", "Medications", "Crate", "Treats"],
        field_prefix="boarding_items",
        per_row=3
    ))
    elements.append(sp(0.1))
    
    elements += field("Drop-off date & time", s, fillable=fillable, 
                      field_name="dropoff_datetime", theme_colors=tc)
    elements += field("Pick-up date & time", s, fillable=fillable, 
                      field_name="pickup_datetime", theme_colors=tc)
    elements += field("Special items or comfort objects", s, fillable=fillable,
                      field_name="comfort_items", theme_colors=tc)
    
    return elements


def build_dropin_section(ctx: FormContext) -> list:
    """Build drop-in visit details section.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables
    """
    s = ctx.styles
    tc = ctx.theme_colors
    fillable = ctx.fillable
    elements = []
    
    elements += [sec_hdr("DROP-IN VISIT DETAILS", s, theme_colors=tc), sp(0.2)]
    
    elements.append(para_row("Tasks per visit (check all that apply):", s["lbl"]))
    elements.append(ctx.checkbox_row(
        ["Feed", "Fresh water", "Potty break/walk", "Playtime", "Medication",
         "Scoop litter", "Bring in mail", "Water plants", "Rotate lights"],
        field_prefix="dropin_tasks",
        per_row=3
    ))
    elements.append(sp(0.1))
    
    elements += field("Visit time preference", s, fillable=fillable, 
                      field_name="visit_time", theme_colors=tc)
    elements += field("Visit duration needed", s, fillable=fillable, 
                      field_name="visit_duration", theme_colors=tc)
    
    return elements


def build_service_specific_page(ctx: FormContext) -> list:
    """Build service-specific page based on service type.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables including PageBreak, or empty list if not needed
    """
    if not ctx.section_enabled("service_specific"):
        return []
    
    if ctx.service_type == "general":
        return []
    
    s = ctx.styles
    tc = ctx.theme_colors
    elements = []
    
    elements.append(PageBreak())
    ctx.next_page()
    elements += pg_hdr(ctx.business_name, ctx.page_label(), s, theme_colors=tc)
    
    if ctx.service_type == "walking":
        elements += build_walking_section(ctx)
    elif ctx.service_type == "boarding":
        elements += build_boarding_section(ctx)
    elif ctx.service_type == "drop_in":
        elements += build_dropin_section(ctx)
    
    return elements
