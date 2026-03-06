"""Custom PDF flowable elements for form fields."""

from reportlab.lib import colors
from reportlab.platypus import Flowable

from .constants import WHITE

# Module-level theme colors - set by builder before rendering
_theme_colors = None


def set_theme_colors(theme_colors):
    """Set the active theme colors for flowables to use."""
    global _theme_colors
    _theme_colors = theme_colors


def _c(key):
    """Get color from current theme."""
    return _theme_colors[key] if _theme_colors else colors.HexColor("#000000")


class CheckboxRow(Flowable):
    """Draws proper open white-filled checkboxes — never unicode blobs."""
    
    def __init__(self, options, per_row=4, box_size=9, font_size=8.5):
        super().__init__()
        self.options = options
        self.per_row = per_row
        self.box_size = box_size
        self.font_size = font_size
        n_rows = -(-len(options) // per_row)
        self.height = n_rows * (box_size + 16)
        self.width = 0

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
            c.setStrokeColor(_c("primary_dark"))
            c.setFillColor(WHITE)
            c.rect(x, y, box, box, stroke=1, fill=1)
            c.setFillColor(_c("text"))
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
    """
    
    def __init__(self, name, width, height=18, multiline=False, maxlen=0):
        super().__init__()
        self.field_name = name
        self.field_width = width
        self.multiline = multiline
        self.maxlen = maxlen
        if multiline and height < 36:
            self.field_height = 36
        else:
            self.field_height = height
        self.width = width
        self.height = self.field_height

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
            borderColor=_c("primary_mid"),
            fillColor=WHITE,
            textColor=_c("text"),
            fontSize=9 if not self.multiline else 8,
            fieldFlags=flags,
            maxlen=self.maxlen if self.maxlen > 0 else None,
        )


class FillableCheckbox(Flowable):
    """A fillable checkbox for digital forms."""
    
    def __init__(self, name, label, box_size=12, font_size=9):
        super().__init__()
        self.field_name = name
        self.label = label
        self.box_size = box_size
        self.font_size = font_size
        self.width = 200
        self.height = box_size + 4

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
            borderColor=_c("primary_dark"),
            fillColor=WHITE,
            checked=False,
        )
        c.setFillColor(_c("text"))
        c.setFont("Helvetica", self.font_size)
        c.drawString(self.box_size + 6, 2, self.label)


class FillableCheckboxRow(Flowable):
    """Row of fillable checkboxes for digital forms."""
    
    def __init__(self, field_prefix, options, per_row=4, box_size=12, font_size=9):
        super().__init__()
        self.field_prefix = field_prefix
        self.options = options
        self.per_row = per_row
        self.box_size = box_size
        self.font_size = font_size
        n_rows = -(-len(options) // per_row)
        self.height = n_rows * (box_size + 16)
        self.width = 0

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
                borderColor=_c("primary_dark"),
                fillColor=WHITE,
                checked=False,
            )
            c.setFillColor(_c("text"))
            c.setFont("Helvetica", self.font_size)
            c.drawString(local_x + box + 6, local_y + 2, label)


class VaxCheckboxRow(Flowable):
    """Compact inline checkboxes for vaccination status (Yes/No/Exempt or N/A)."""
    
    def __init__(self, field_prefix, options, box_size=10, font_size=8):
        super().__init__()
        self.field_prefix = field_prefix
        self.options = options
        self.box_size = box_size
        self.font_size = font_size
        self.height = box_size + 6
        self.width = 0

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
                borderColor=_c("primary_dark"),
                fillColor=WHITE,
                checked=False,
            )
            c.setFillColor(_c("text"))
            c.setFont("Helvetica", self.font_size)
            c.drawString(local_x + box + 4, local_y + 1, label)
