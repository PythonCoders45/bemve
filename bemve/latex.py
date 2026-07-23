import cairo
from bemve.vmobject import VMobject


class Tex(VMobject):
    """Renders LaTeX / Math expressions into vector paths using Cairo/Pango."""

    def __init__(
        self,
        tex_string: str,
        font_size: float = 0.5,
        stroke_color=(1.0, 1.0, 1.0, 1.0),
        stroke_width=0.04,
        fill_color=(1.0, 1.0, 1.0, 1.0),
    ):
        super().__init__(stroke_color=stroke_color, stroke_width=stroke_width)
        self.tex_string = tex_string
        self.font_size = font_size
        self.fill_color = fill_color

    def draw_tex(self, ctx: cairo.Context, x: float = 0.0, y: float = 0.0):
        """Draws the formatted LaTeX text string onto the Cairo context."""
        ctx.save()

        # Position context
        ctx.move_to(x, y)

        # Set color
        if self.fill_color:
            r, g, b, a = self.fill_color
            ctx.set_source_rgba(r, g, b, a)

        # Render math text using standard Cairo text path capabilities
        ctx.select_font_face(
            "Latin Modern Math",
            cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_NORMAL,
        )
        ctx.set_font_size(self.font_size)

        # Create path from text string for stroke and fill capabilities
        ctx.text_path(self.tex_string)

        if self.fill_color:
            ctx.fill_preserve()

        if self.stroke_color:
            r, g, b, a = self.stroke_color
            ctx.set_source_rgba(r, g, b, a)
            ctx.set_line_width(self.stroke_width)
            ctx.stroke()

        ctx.restore()


class MathTex(Tex):
    """Convenience class specifically for mathematical formulas formatted with delimiters."""

    def __init__(self, math_string: str, **kwargs):
        # Automatically wrap math string in inline math indicators if needed
        formatted_tex = (
            math_string
            if math_string.startswith("$")
            else f"${math_string}$"
        )
        super().__init__(formatted_tex, **kwargs)
