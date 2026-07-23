import cairo
import numpy as np


class VMobject:
    """Vector Mobject powered by Cubic Bézier curves."""

    def __init__(
        self,
        stroke_color=(0.0, 0.9, 1.0, 1.0),
        stroke_width=0.08,
        fill_color=None,
    ):
        # Points stored in groups of 4: [P0 (start), P1 (control1), P2 (control2), P3 (end)]
        self.points = np.zeros((0, 3))
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.fill_color = fill_color

    def set_points(self, points: np.ndarray):
        self.points = np.array(points, dtype=float)
        return self

    def interpolate(self, target_vmobject: "VMobject", alpha: float):
        """Linearly interpolates points towards another VMobject for morphing."""
        # Align point counts between shapes
        p1 = self.points
        p2 = target_vmobject.points

        if len(p1) != len(p2):
            p1, p2 = self._align_points(p1, p2)

        interpolated_points = p1 + (p2 - p1) * alpha
        result = VMobject(
            stroke_color=self.stroke_color, stroke_width=self.stroke_width
        )
        result.set_points(interpolated_points)
        return result

    def _align_points(self, p1, p2):
        """Pad the smaller point list so both vector shapes match during Transform."""
        max_len = max(len(p1), len(p2))
        if len(p1) < max_len:
            p1 = np.pad(p1, ((0, max_len - len(p1)), (0, 0)), mode="edge")
        if len(p2) < max_len:
            p2 = np.pad(p2, ((0, max_len - len(p2)), (0, 0)), mode="edge")
        return p1, p2

    def draw(self, ctx: cairo.Context, subpath_ratio: float = 1.0):
        """Renders the Bézier path onto Cairo context, supporting progressive Create tracing."""
        if len(self.points) < 4:
            return

        ctx.save()
        r, g, b, a = self.stroke_color
        ctx.set_source_rgba(r, g, b, a)
        ctx.set_line_width(self.stroke_width)

        num_curves = len(self.points) // 4
        curves_to_draw = int(num_curves * subpath_ratio)

        if num_curves > 0:
            # Move to starting point
            ctx.move_to(self.points[0][0], self.points[0][1])

            for i in range(curves_to_draw):
                idx = i * 4
                p1 = self.points[idx + 1]
                p2 = self.points[idx + 2]
                p3 = self.points[idx + 3]
                ctx.curve_to(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])

            ctx.stroke()
        ctx.restore()


class VSquare(VMobject):
    """Square defined via cubic Bézier segments."""

    def __init__(self, side_length=2.0, **kwargs):
        super().__init__(**kwargs)
        s = side_length / 2.0
        # 4 straight sides represented as Bézier curves
        pts = [
            [-s, -s, 0],
            [-s, -s, 0],
            [s, -s, 0],
            [s, -s, 0],  # Bottom edge
            [s, -s, 0],
            [s, -s, 0],
            [s, s, 0],
            [s, s, 0],  # Right edge
            [s, s, 0],
            [s, s, 0],
            [-s, s, 0],
            [-s, s, 0],  # Top edge
            [-s, s, 0],
            [-s, s, 0],
            [-s, -s, 0],
            [-s, -s, 0],  # Left edge
        ]
        self.set_points(np.array(pts))


class VCircle(VMobject):
    """Circle constructed from 4 cubic Bézier splines."""

    def __init__(self, radius=1.0, **kwargs):
        super().__init__(**kwargs)
        k = 0.552284749831 * radius  # Magic constant for circle Bézier control points
        r = radius
        pts = [
            [0, r, 0],
            [k, r, 0],
            [r, k, 0],
            [r, 0, 0],  # Quadrant 1
            [r, 0, 0],
            [r, -k, 0],
            [k, -r, 0],
            [0, -r, 0],  # Quadrant 2
            [0, -r, 0],
            [-k, -r, 0],
            [-r, -k, 0],
            [-r, 0, 0],  # Quadrant 3
            [-r, 0, 0],
            [-r, k, 0],
            [-k, r, 0],
            [0, r, 0],  # Quadrant 4
        ]
        self.set_points(np.array(pts))