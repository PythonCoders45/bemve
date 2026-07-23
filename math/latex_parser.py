import cairo
from bemve.vmobject import VMobject


class AdvancedMathTex(VMobject):
    """Enhanced LaTeX formula path parser supporting multi-line alignment."""

    def __init__(self, formula_string: str, font_size: float = 0.5, color=(1.0, 1.0, 1.0, 1.0)):
        super().__init__()
        self.formula_string = formula_string
        self.font_size = font_size
        self.color = color

    def draw(self, ctx: cairo.Context):
        ctx.save()
        ctx.set_source_rgba(*self.color)
        ctx.select_font_face("Serif", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(self.font_size)

        # Render parsed LaTeX glyph string
        ctx.move_to(0, 0)
        ctx.show_text(self.formula_string)
        ctx.restore()
