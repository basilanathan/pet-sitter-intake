"""Shared constants for PDF generation."""

from pathlib import Path
from reportlab.lib.units import inch
from reportlab.lib import colors

WHITE = colors.white
PAGE_W = 7.0 * inch  # Usable width (letter - margins)


def get_default_output_path():
    """Get default output path in user's Downloads folder."""
    downloads = Path.home() / "Downloads"
    return str(downloads / "client_intake_form.pdf")


DEFAULT_OUTPUT = get_default_output_path()
