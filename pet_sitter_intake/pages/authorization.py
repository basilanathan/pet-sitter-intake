"""Authorization and signature page."""

from reportlab.platypus import Table, TableStyle, Paragraph, PageBreak

from ..constants import PAGE_W
from ..flowables import get_color
from ..layout import sec_hdr, sp, para_row, field, two_col, hr, pg_hdr, auth_block

from .context import FormContext


def build_authorization_blocks(ctx: FormContext) -> list:
    """Build the authorization agreement blocks.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables
    """
    s = ctx.styles
    tc = ctx.theme_colors
    sitter = ctx.sitter_display_name
    elements = []
    
    auth_items = [
        ("Emergency Veterinary Care",
         f"I authorize <b>{sitter}</b> to seek emergency veterinary care for my pet(s) if I cannot "
         f"be reached and the situation requires immediate attention. I understand I am responsible "
         f"for all veterinary fees incurred."),
        ("Transport Authorization",
         f"I authorize <b>{sitter}</b> to transport my pet(s) in their vehicle if necessary for "
         f"veterinary care or other emergency situations."),
        ("Photo &amp; Social Media Release",
         f"I give permission for photos and videos of my pet(s) to be shared on social media or "
         f"used for marketing by <b>{sitter}</b>."),
        ("Cancellation Policy",
         "Please refer to our separate service agreement for cancellation and refund terms. By "
         "signing below, I acknowledge I have read and agree to all stated terms."),
        ("Liability",
         "I confirm my pet(s) is/are current on required vaccinations, has/have not shown "
         "aggression toward people or other animals without prior written disclosure, and I accept "
         "full liability for any damage or injury caused by my pet(s)."),
    ]
    
    for title, body in auth_items:
        elements.append(auth_block(title, body, s, theme_colors=tc))
        elements.append(sp(0.08))
    
    return elements


def build_permission_checkboxes(ctx: FormContext) -> list:
    """Build photo/transport permission checkboxes.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables
    """
    s = ctx.styles
    elements = []
    
    elements.append(sp(0.06))
    elements.append(para_row("Photo / video permission:", s["lbl"]))
    elements.append(ctx.checkbox_row(
        ["Yes, I give permission", "No, please do not share"],
        field_prefix="photo_permission",
        per_row=2
    ))
    elements.append(sp(0.06))
    
    elements.append(para_row("Transport authorization:", s["lbl"]))
    elements.append(ctx.checkbox_row(
        ["Yes, I authorize transport", "No, do not transport"],
        field_prefix="transport_permission",
        per_row=2
    ))
    elements.append(sp(0.2))
    
    return elements


def build_signature_block(ctx: FormContext) -> list:
    """Build signature fields.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables
    """
    s = ctx.styles
    tc = ctx.theme_colors
    fillable = ctx.fillable
    elements = []
    
    elements.append(two_col("Client Signature", "Date", s, fillable=fillable,
                            field_names=["signature", "signature_date"], theme_colors=tc))
    elements.append(sp(0.1))
    elements += field("Printed Name", s, fillable=fillable, field_name="printed_name", theme_colors=tc)
    elements.append(sp(0.2))
    
    return elements


def build_office_use_block(ctx: FormContext) -> list:
    """Build 'for office use' footer block.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables
    """
    s = ctx.styles
    tc = ctx.theme_colors
    elements = []
    
    ot = Table([[Paragraph(
        "For office use only  \u00b7  Client ID: _________________   Date on file: _________________   "
        "Last updated: _________________",
        s["office"]
    )]], colWidths=[PAGE_W])
    ot.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), get_color(tc, "primary")),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
    ]))
    elements.append(ot)
    elements.append(sp(0.15))
    
    return elements


def build_page_footer(ctx: FormContext) -> list:
    """Build thank-you footer.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables
    """
    s = ctx.styles
    tc = ctx.theme_colors
    elements = []
    
    elements.append(hr(tc, 0.8, 6))
    elements.append(Paragraph(
        f"{ctx.business_name}  \u00b7  {ctx.location}  \u00b7  {ctx.contact}", s["foot"]
    ))
    elements.append(Paragraph("Thank you for trusting us with your furry family member!", s["foot"]))
    
    return elements


def build_authorization_page(ctx: FormContext) -> list:
    """Build the complete authorization and signature page.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables including PageBreak
    """
    s = ctx.styles
    tc = ctx.theme_colors
    elements = []
    
    elements.append(PageBreak())
    ctx.next_page()
    elements += pg_hdr(ctx.business_name, ctx.page_label(), s, theme_colors=tc)
    elements += [sec_hdr("AUTHORIZATION & AGREEMENT", s, theme_colors=tc), sp(0.18)]
    
    elements += build_authorization_blocks(ctx)
    elements += build_permission_checkboxes(ctx)
    elements += build_signature_block(ctx)
    elements += build_office_use_block(ctx)
    elements += build_page_footer(ctx)
    
    return elements
