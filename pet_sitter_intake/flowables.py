"""Custom PDF flowable elements for form fields."""

from reportlab.lib import colors
from reportlab.platypus import Flowable

from .constants import WHITE


def get_color(theme_colors, key, fallback="#000000"):
    """Get color from theme dict with fallback.
    
    Args:
        theme_colors: Dict mapping color keys to reportlab Color objects
        key: Color key to look up
        fallback: Hex color to use if key not found
    """
    if theme_colors and key in theme_colors:
        return theme_colors[key]
    return colors.HexColor(fallback)


class CheckboxRow(Flowable):
    """Draws proper open white-filled checkboxes — never unicode blobs.
    
    Args:
        options: List of checkbox label strings
        per_row: Number of checkboxes per row
        box_size: Size of checkbox in points
        font_size: Label font size
        theme_colors: Dict of theme colors (injected, not global)
    """
    
    def __init__(self, options, per_row=4, box_size=9, font_size=8.5, theme_colors=None):
        super().__init__()
        self.options = options
        self.per_row = per_row
        self.box_size = box_size
        self.font_size = font_size
        self.theme_colors = theme_colors or {}
        n_rows = -(-len(options) // per_row)
        self.height = n_rows * (box_size + 16)
        self.width = 0

    def _c(self, key):
        """Get color from theme."""
        return get_color(self.theme_colors, key)

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        col_width = self.width / self.per_row
        box = self.box_size
        for i, label in enumerate(self.options):
            row = i // self.per_row
            col = i % self.per_row
            x = col * col_width
            y = self.height - (row + 1) * (box + 16) + 5
            c.setStrokeColor(self._c("primary_dark"))
            c.setFillColor(WHITE)
            c.rect(x, y, box, box, stroke=1, fill=1)
            c.setFillColor(self._c("text"))
            c.setFont("Helvetica", self.font_size)
            c.drawString(x + box + 6, y + 1.5, label)


class FillableTextField(Flowable):
    """A fillable text field for digital forms.
    
    Args:
        name: Unique field name for the PDF form
        width: Field width in points
        height: Field height in points (auto-increased for multiline)
        multiline: If True, allows multiple lines with text wrapping
        maxlen: Maximum character limit (0 = unlimited)
        theme_colors: Dict of theme colors (injected, not global)
    """
    
    def __init__(self, name, width, height=18, multiline=False, maxlen=0, theme_colors=None):
        super().__init__()
        self.field_name = name
        self.field_width = width
        self.multiline = multiline
        self.maxlen = maxlen
        self.theme_colors = theme_colors or {}
        if multiline and height < 36:
            self.field_height = 36
        else:
            self.field_height = height
        self.width = width
        self.height = self.field_height

    def _c(self, key):
        """Get color from theme."""
        return get_color(self.theme_colors, key)

    def wrap(self, availWidth, availHeight):
        return self.field_width, self.field_height

    def draw(self):
        c = self.canv
        abs_x, abs_y = c.absolutePosition(0, 0)
        form = c.acroForm
        flags = 'multiline' if self.multiline else ''
        form.textfield(
            name=self.field_name,
            x=abs_x,
            y=abs_y,
            width=self.field_width,
            height=self.field_height,
            borderWidth=0.5,
            borderColor=self._c("primary_mid"),
            fillColor=WHITE,
            textColor=self._c("text"),
            fontSize=9 if not self.multiline else 8,
            fieldFlags=flags,
            maxlen=self.maxlen if self.maxlen > 0 else None,
        )


class FillableCheckbox(Flowable):
    """A fillable checkbox for digital forms.
    
    Args:
        name: Unique field name for the PDF form
        label: Text label for the checkbox
        box_size: Size of checkbox in points
        font_size: Label font size
        theme_colors: Dict of theme colors (injected, not global)
    """
    
    def __init__(self, name, label, box_size=12, font_size=9, theme_colors=None):
        super().__init__()
        self.field_name = name
        self.label = label
        self.box_size = box_size
        self.font_size = font_size
        self.theme_colors = theme_colors or {}
        self.width = 200
        self.height = box_size + 4

    def _c(self, key):
        """Get color from theme."""
        return get_color(self.theme_colors, key)

    def wrap(self, availWidth, availHeight):
        return availWidth, self.height

    def draw(self):
        c = self.canv
        abs_x, abs_y = c.absolutePosition(0, 0)
        form = c.acroForm
        form.checkbox(
            name=self.field_name,
            x=abs_x,
            y=abs_y,
            size=self.box_size,
            borderWidth=0.5,
            borderColor=self._c("primary_dark"),
            fillColor=WHITE,
            checked=False,
        )
        c.setFillColor(self._c("text"))
        c.setFont("Helvetica", self.font_size)
        c.drawString(self.box_size + 6, 2, self.label)


class FillableCheckboxRow(Flowable):
    """Row of fillable checkboxes for digital forms.
    
    Args:
        field_prefix: Prefix for field names (e.g., "pet1_fears")
        options: List of checkbox label strings
        per_row: Number of checkboxes per row
        box_size: Size of checkbox in points
        font_size: Label font size
        theme_colors: Dict of theme colors (injected, not global)
    """
    
    def __init__(self, field_prefix, options, per_row=4, box_size=12, font_size=9, theme_colors=None):
        super().__init__()
        self.field_prefix = field_prefix
        self.options = options
        self.per_row = per_row
        self.box_size = box_size
        self.font_size = font_size
        self.theme_colors = theme_colors or {}
        n_rows = -(-len(options) // per_row)
        self.height = n_rows * (box_size + 16)
        self.width = 0

    def _c(self, key):
        """Get color from theme."""
        return get_color(self.theme_colors, key)

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        form = c.acroForm
        col_width = self.width / self.per_row
        box = self.box_size
        
        for i, label in enumerate(self.options):
            row = i // self.per_row
            col = i % self.per_row
            local_x = col * col_width
            local_y = self.height - (row + 1) * (box + 16) + 5
            abs_x, abs_y = c.absolutePosition(local_x, local_y)
            
            safe_label = label.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
            field_name = f"{self.field_prefix}_{safe_label}"
            
            form.checkbox(
                name=field_name,
                x=abs_x,
                y=abs_y,
                size=box,
                borderWidth=0.5,
                borderColor=self._c("primary_dark"),
                fillColor=WHITE,
                checked=False,
            )
            c.setFillColor(self._c("text"))
            c.setFont("Helvetica", self.font_size)
            c.drawString(local_x + box + 6, local_y + 2, label)


class VaxCheckboxRow(Flowable):
    """Compact inline checkboxes for vaccination status (Yes/No/Exempt or N/A).
    
    Args:
        field_prefix: Prefix for field names (e.g., "pet1_vax_rabies")
        options: List of checkbox label strings
        box_size: Size of checkbox in points
        font_size: Label font size
        theme_colors: Dict of theme colors (injected, not global)
    """
    
    def __init__(self, field_prefix, options, box_size=10, font_size=8, theme_colors=None):
        super().__init__()
        self.field_prefix = field_prefix
        self.options = options
        self.box_size = box_size
        self.font_size = font_size
        self.theme_colors = theme_colors or {}
        self.height = box_size + 6
        self.width = 0

    def _c(self, key):
        """Get color from theme."""
        return get_color(self.theme_colors, key)

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        form = c.acroForm
        box = self.box_size
        num_options = len(self.options)
        spacing = self.width / num_options
        
        for i, label in enumerate(self.options):
            local_x = i * spacing
            local_y = 0
            abs_x, abs_y = c.absolutePosition(local_x, local_y)
            
            safe_label = label.replace(" ", "_").replace("/", "_")
            field_name = f"{self.field_prefix}_{safe_label}"
            
            form.checkbox(
                name=field_name,
                x=abs_x,
                y=abs_y,
                size=box,
                borderWidth=0.5,
                borderColor=self._c("primary_dark"),
                fillColor=WHITE,
                checked=False,
            )
            c.setFillColor(self._c("text"))
            c.setFont("Helvetica", self.font_size)
            c.drawString(local_x + box + 4, local_y + 1, label)
