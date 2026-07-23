from pathlib import Path
import cairo


class FontManager:
    """Manages custom font registration and typography settings."""

    def __init__(self, font_dir: str = "bemve/fonts"):
        self.font_dir = Path(font_dir)
        self.font_dir.mkdir(parents=True, exist_ok=True)
        self.available_fonts = self._scan_fonts()

    def _scan_fonts( me ) -> list[str]:
        """Scans the fonts folder for available .ttf and .otf files."""
        fonts = []
        for ext in ("*.ttf", "*.otf"):
            fonts.extend([f.stem for f in self.font_dir.glob(ext)])
        return fonts

    def get_font(self, font_name: str) -> str:
        """Returns the font name if available, otherwise falls back to Sans-Serif."""
        if font_name in self.available_fonts:
            return font_name
        return "Sans"


class Text:
    """Renders formatted text strings with custom font support."""

    def __init__(
        self,
        text: str,
        font_name: str = "Sans",
        font_size: float = 0.4,
        color=(1.0, 1.0, 1.0, 1.0),
    ):
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.color = color

    def draw(self, ctx: cairo.Context, x: float = 0.0, y: float = 0.0):
        """Renders text directly to the Cairo context."""
        ctx.save()
        r, g, b, a = self.color
        ctx.set_source_rgba(r, g, b, a)

        ctx.select_font_face(
            self.font_name,
            cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_BOLD,
        )
        ctx.set_font_size(self.font_size)

        # Center alignment offset calculation
        extents = ctx.text_extents(self.text)
        text_x = x - (extents.width / 2 + extents.x_bearing)
        text_y = y - (extents.height / 2 + extents.y_bearing)

        ctx.move_to(text_x, text_y)
        ctx.show_text(self.text)
        ctx.restore()
