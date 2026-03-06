"""PDF form builder - main form orchestrator.

This module coordinates the page builders from the pages subpackage
to generate complete intake form PDFs. It handles document setup,
page ordering, and final output.
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate

from .constants import MARGINS
from .pages import (
    FormContext,
    build_owner_info_page,
    build_home_access_page,
    build_all_pet_profiles,
    build_service_specific_page,
    build_authorization_page,
)


def build_form(config, output_path):
    """Build the intake form PDF from config dict.
    
    This is the main entry point for PDF generation. It creates a FormContext
    from the config, calls each page builder in order, and writes the final PDF.
    
    Args:
        config: Dict with business info, theme, service_type, etc.
        output_path: Path to save the generated PDF
        
    Returns:
        None. Prints status messages and saves PDF to output_path.
    """
    # Ensure output directory exists
    output_path = os.path.expanduser(output_path)
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Created directory: {output_dir}")
    
    # Create form context from config
    ctx = FormContext.from_config(config)
    ctx.total_pages = ctx.calculate_total_pages()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=MARGINS["left"],
        rightMargin=MARGINS["right"],
        topMargin=MARGINS["top"],
        bottomMargin=MARGINS["bottom"],
    )
    
    # Build story by calling page builders in order
    story = []
    
    # Page 1: Owner information
    story += build_owner_info_page(ctx)
    
    # Page 2 (optional): Home access
    story += build_home_access_page(ctx)
    
    # Pet profile pages (1-2 pages per pet)
    story += build_all_pet_profiles(ctx)
    
    # Service-specific page (optional)
    story += build_service_specific_page(ctx)
    
    # Authorization page (always last)
    story += build_authorization_page(ctx)
    
    # Build the PDF
    doc.build(story)
    
    # Print summary
    _print_summary(ctx, output_path)


def _print_summary(ctx: FormContext, output_path: str):
    """Print generation summary to console.
    
    Args:
        ctx: Form context with generation info
        output_path: Path where PDF was saved
    """
    theme_name = ctx.config.get("theme", "lavender")
    
    print(f"✅  Form saved to: {output_path}")
    print(f"   Pages: {ctx.total_pages}, Pets: {ctx.num_pets}, "
          f"Service type: {ctx.service_type}, Theme: {theme_name}")
    
    if ctx.fillable:
        print("   📝 Fillable PDF fields enabled")
    
    enabled = [sec for sec, v in ctx.sections.items() if v]
    disabled = [sec for sec, v in ctx.sections.items() if not v]
    
    if disabled:
        print(f"   Sections: {', '.join(enabled)}")
        print(f"   Excluded: {', '.join(disabled)}")
