from typing import Tuple
import cairo
import xml.etree.ElementTree as ET
from bemve.vmobject import VMobject
from bemve.latex.compiler import LaTeXCompiler


class MathTex(VMobject):
    """Renders LaTeX math formulas as Pycairo vector objects."""

    def __init__(
        self,
        formula: str,
        position: Tuple[float, float] = (0.0, 0.0),
        scale: float = 1.0,
        color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    ):
        super().__init__()
        self.formula = formula
        self.position = position
        self.scale = scale
        self.color = color
        self.svg_path = LaTeXCompiler.compile_to_svg(formula)

    def draw(self, ctx: cairo.Context):
        """Draws LaTeX vector path using Cairo context."""
        ctx.save()
        ctx.translate(*self.position)
        ctx.scale(self.scale, -self.scale)  # Flip Y for Cairo coordinate space
        ctx.set_source_rgba(*self.color)

        # Parse SVG path data (e.g. from dvisvgm output)
        tree = ET.parse(self.svg_path)
        root = tree.getroot()

        for path in root.findall(".//{http://www.w3.org/2000/svg}path"):
            d = path.attrib.get("d", "")
            self._render_svg_d(ctx, d)

        ctx.fill()
        ctx.restore()

    def _render_svg_d(self, ctx: cairo.Context, d: str):
        """Simple SVG path parser for Cairo path execution."""
        # SVG path execution parsing logic (M, L, C, Z)
        tokens = d.replace(",", " ").split()
        idx = 0
        while idx < len(tokens):
            cmd = tokens[idx]
            if cmd == "M":
                ctx.move_to(float(tokens[idx+1]), float(tokens[idx+2]))
                idx += 3
            elif cmd == "L":
                ctx.line_to(float(tokens[idx+1]), float(tokens[idx+2]))
                idx += 3
            elif cmd == "C":
                ctx.curve_to(
                    float(tokens[idx+1]), float(tokens[idx+2]),
                    float(tokens[idx+3]), float(tokens[idx+4]),
                    float(tokens[idx+5]), float(tokens[idx+6])
                )
                idx += 7
            elif cmd in ("Z", "z"):
                ctx.close_path()
                idx += 1
            else:
                idx += 1
