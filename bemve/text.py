from pathlib import Path
import cairo
from bemve.vmobject import VMobject


class Text(VMobject):
    """Renders text with support for custom .ttf font files."""

    def __init__(
        self,
        text: str,
        font_file: str = None,  # e.g., "Roboto-Bold.ttf"
        font_size: float = 0.5,
        color=(1.0, 1.0, 1.0, 1.0),
        stroke_width=0.0,
    ):
        super().__init__(stroke_color=color, stroke_width=stroke_width)
        self.text = text
        self.font_file = font_file
        self.font_size = font_size
        self.color = color

        # Check if font file exists in bemve/fonts/
        self.font_path = None
        if font_file:
            path = Path("bemve/fonts") / font_file
            if path.exists():
                self.font_path = str(path.resolve())

    def draw(self, ctx: cairo.Context, subpath_ratio: float = 1.0):
        """Renders text using Cairo text paths."""
        ctx.save()
        r, g, b, a = self.color
        ctx.set_source_rgba(r, g, b, a)

        # Apply font family or standard fallback
        font_family = "Sans"
        if self.font_file:
            # Strip extension for Cairo font selection
            font_family = Path(self.font_file).stem

        ctx.select_font_face(
            font_family,
            cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_BOLD,
        )
        ctx.set_font_size(self.font_size)

        # Center alignment
        extents = ctx.text_extents(self.text)
        x_off = -(extents.width / 2 + extents.x_bearing)
        y_off = -(extents.height / 2 + extents.y_bearing)

        ctx.move_to(x_off, y_off)

        # Truncate text progress if animating path creation
        visible_chars = int(len(self.text) * subpath_ratio)
        current_text = self.text[:visible_chars]

        ctx.show_text(current_text)
        ctx.restore()
