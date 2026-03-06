"""Command-line interface for pet sitter intake form generator."""

import argparse

from .constants import DEFAULT_OUTPUT
from .config import load_config, list_sections, SECTION_NAMES
from .themes import THEMES, list_themes
from .builder import build_form


def main():
    """Main CLI entrypoint."""
    p = argparse.ArgumentParser(
        description="Generate professional pet sitter client intake forms.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --business-name "Pawsitive Care" --contact "555-1234"
  %(prog)s --config my_business.yaml --fillable
  %(prog)s --pets 2 --service-type boarding
  %(prog)s --service-type walking --include-section vaccinations
  %(prog)s --service-type general --exclude-section home_access
  %(prog)s --list-sections
        """
    )
    
    # Config file (highest priority for defaults)
    p.add_argument("--config", "-c", metavar="FILE",
                   help="YAML config file for business presets")
    
    # Business info (override config)
    p.add_argument("--business-name", metavar="NAME",
                   help="Business name for header")
    p.add_argument("--sitter-name", metavar="NAME",
                   help="Individual sitter name (for authorization text)")
    p.add_argument("--services", metavar="LIST",
                   help="Comma-separated services offered")
    p.add_argument("--location", metavar="LOC",
                   help="Business location/city")
    p.add_argument("--contact", metavar="INFO",
                   help="Contact info (phone, email, website)")
    
    # Form options
    p.add_argument("--service-type", choices=["general", "boarding", "walking", "drop_in"],
                   help="Service type for specialized sections (sets section defaults)")
    p.add_argument("--pets", type=int, metavar="N",
                   help="Number of pet profile pages to generate (default: 1)")
    
    # Section overrides
    p.add_argument("--include-section", action="append", dest="include_sections",
                   metavar="NAME", choices=SECTION_NAMES,
                   help=f"Include a section (can repeat). Options: {', '.join(SECTION_NAMES)}")
    p.add_argument("--exclude-section", action="append", dest="exclude_sections",
                   metavar="NAME", choices=SECTION_NAMES,
                   help=f"Exclude a section (can repeat). Options: {', '.join(SECTION_NAMES)}")
    p.add_argument("--list-sections", action="store_true",
                   help="Show section defaults by service type and exit")
    
    # Theme options
    theme_names = list(THEMES.keys())
    p.add_argument("--theme", choices=theme_names + ["custom"], metavar="NAME",
                   help=f"Color theme: {', '.join(theme_names)}, or 'custom'")
    p.add_argument("--list-themes", action="store_true",
                   help="Show available color themes and exit")
    
    p.add_argument("--fillable", action="store_true", default=None,
                   help="Generate fillable PDF form fields (default: enabled)")
    p.add_argument("--no-fillable", action="store_true",
                   help="Generate print-only form (static lines instead of fields)")
    
    # Legacy flag (kept for backward compatibility)
    p.add_argument("--no-home-access", action="store_true",
                   help="Omit home access section (legacy; prefer --exclude-section home_access)")
    
    # Output
    p.add_argument("--output", "-o", default=DEFAULT_OUTPUT, metavar="FILE",
                   help="Output PDF path (default: ~/Downloads/client_intake_form.pdf)")
    
    args = p.parse_args()
    
    # Handle info-only flags
    if args.list_themes:
        list_themes()
        return 0
    
    if args.list_sections:
        list_sections()
        return 0
    
    # Load config file first, then override with CLI args
    config = load_config(args.config)
    
    # CLI args override config file
    if args.theme:
        config["theme"] = args.theme
    if args.business_name:
        config["business_name"] = args.business_name
    if args.sitter_name:
        config["sitter_name"] = args.sitter_name
    if args.services:
        config["services"] = args.services
    if args.location:
        config["location"] = args.location
    if args.contact:
        config["contact"] = args.contact
    if args.service_type:
        config["service_type"] = args.service_type
    if args.pets:
        config["num_pets"] = args.pets
    if args.no_fillable:
        config["fillable"] = False
    elif args.fillable:
        config["fillable"] = True
    
    # Legacy --no-home-access support
    if args.no_home_access:
        config["include_home_access"] = False
    
    # Apply section overrides from CLI
    if args.include_sections or args.exclude_sections:
        if "sections" not in config:
            config["sections"] = {}
        for section in (args.include_sections or []):
            config["sections"][section] = True
        for section in (args.exclude_sections or []):
            config["sections"][section] = False
    
    # Determine output path
    if args.output != DEFAULT_OUTPUT:
        output_path = args.output
    else:
        output_path = config.get("output", DEFAULT_OUTPUT)
    
    build_form(config, output_path)
    return 0


if __name__ == "__main__":
    exit(main())
