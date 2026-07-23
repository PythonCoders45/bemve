import cairo
import numpy as np
from bemve.vmobject import VMobject


class CoordinatePlane(VMobject):
    """Renders a 2D grid/coordinate plane with axes, tick marks, and custom bounds."""

    def __init__(
        self,
        x_range=(-5.0, 5.0, 1.0),
        y_range=(-3.0, 3.0, 1.0),
        axis_color=(0.8, 0.8, 0.9, 1.0),
        grid_color=(0.2, 0.25, 0.35, 0.5),
    ):
        super().__init__()
        self.x_min, self.x_max, self.x_step = x_range
        self.y_min, self.y_max, self.y_step = y_range
        self.axis_color = axis_color
        self.grid_color = grid_color

    def draw(self, ctx: cairo.Context):
        ctx.save()

        # Grid Lines
        ctx.set_source_rgba(*self.grid_color)
        ctx.set_line_width(0.015)

        x = self.x_min
        while x <= self.x_max:
            ctx.move_to(x, self.y_min)
            ctx.line_to(x, self.y_max)
            x += self.x_step
        ctx.stroke()

        y = self.y_min
        while y <= self.y_max:
            ctx.move_to(self.x_min, y)
            ctx.line_to(self.x_max, y)
            y += self.y_step
        ctx.stroke()

        # Axes
        ctx.set_source_rgba(*self.axis_color)
        ctx.set_line_width(0.035)

        # X-Axis
        ctx.move_to(self.x_min, 0)
        ctx.line_to(self.x_max, 0)
        # Y-Axis
        ctx.move_to(0, self.y_min)
        ctx.line_to(0, self.y_max)
        ctx.stroke()

        ctx.restore()


class VectorField(VMobject):
    """Renders vector fields F(x, y) = (P(x,y), Q(x,y))."""

    def __init__(self, func, x_range=(-4, 4, 1.0), y_range=(-3, 3, 1.0), color=(0.0, 0.8, 1.0, 0.8)):
        super().__init__()
        self.func = func
        self.x_range = x_range
        self.y_range = y_range
        self.color = color

    def draw(self, ctx: cairo.Context):
        ctx.save()
        ctx.set_source_rgba(*self.color)
        ctx.set_line_width(0.025)

        x_min, x_max, x_step = self.x_range
        y_min, y_max, y_step = self.y_range

        for x in np.arange(x_min, x_max + x_step, x_step):
            for y in np.arange(y_min, y_max + y_step, y_step):
                vx, vy = self.func(x, y)
                mag = np.hypot(vx, vy)
                if mag == 0:
                    continue
                # Normalize length for grid display
                dx, dy = (vx / mag) * 0.4, (vy / mag) * 0.4

                ctx.move_to(x, y)
                ctx.line_to(x + dx, y + dy)
                ctx.stroke()

        ctx.restore()


class Polygon(VMobject):
    """Custom N-sided polygon with stroke and fill controls."""

    def __init__(self, vertices: list[tuple[float, float]], color=(1.0, 0.5, 0.2, 0.8)):
        super().__init__()
        self.vertices = vertices
        self.color = color

    def draw(self, ctx: cairo.Context):
        if not self.vertices:
            return
        ctx.save()
        ctx.set_source_rgba(*self.color)
        ctx.move_to(*self.vertices[0])
        for v in self.vertices[1:]:
            ctx.line_to(*v)
        ctx.close_path()
        ctx.fill_preserve()

        ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        ctx.set_line_width(0.03)
        ctx.stroke()
        ctx.restore()


class Arc(VMobject):
    """Circular arc segment for geometry and angle visualizers."""

    def __init__(self, center=(0.0, 0.0), radius=1.0, start_angle=0.0, end_angle=np.pi / 2):
        super().__init__()
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

    def draw(self, ctx: cairo.Context):
        ctx.save()
        ctx.arc(self.center[0], self.center[1], self.radius, self.start_angle, self.end_angle)
        ctx.set_source_rgba(0.9, 0.3, 0.9, 1.0)
        ctx.set_line_width(0.04)
        ctx.stroke()
        ctx.restore()
