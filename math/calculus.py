import cairo
import numpy as np
from bemve.vmobject import VMobject


class DynamicFunction(VMobject):
    """Renders continuous functions f(x) over a mathematical domain."""

    def __init__(self, func, x_range=(-4.0, 4.0), color=(0.1, 0.9, 0.4, 1.0), samples=200):
        super().__init__()
        self.func = func
        self.x_range = x_range
        self.color = color
        self.samples = samples

    def draw(self, ctx: cairo.Context):
        ctx.save()
        ctx.set_source_rgba(*self.color)
        ctx.set_line_width(0.04)

        xs = np.linspace(self.x_range[0], self.x_range[1], self.samples)
        first = True

        for x in xs:
            y = self.func(x)
            if first:
                ctx.move_to(x, y)
                first = False
            else:
                ctx.line_to(x, y)

        ctx.stroke()
        ctx.restore()


class RiemannSum(VMobject):
    """Animatable rectangular approximation of definite integrals."""

    def __init__(
        self,
        func,
        x_range=(0.0, 3.0),
        num_rectangles=10,
        color=(0.2, 0.6, 1.0, 0.5),
    ):
        super().__init__()
        self.func = func
        self.x_min, self.x_max = x_range
        self.num_rectangles = num_rectangles
        self.color = color

    def draw(self, ctx: cairo.Context):
        ctx.save()
        dx = (self.x_max - self.x_min) / self.num_rectangles

        for i in range(self.num_rectangles):
            x = self.x_min + i * dx
            y = self.func(x)

            ctx.rectangle(x, 0, dx, y)
            ctx.set_source_rgba(*self.color)
            ctx.fill_preserve()

            ctx.set_source_rgba(1.0, 1.0, 1.0, 0.8)
            ctx.set_line_width(0.015)
            ctx.stroke()

        ctx.restore()


class IntegralRegion(VMobject):
    """Highlights the continuous shaded area beneath a function continuous curve."""

    def __init__(self, func, x_range=(0.0, 2.0), color=(1.0, 0.8, 0.0, 0.4)):
        super().__init__()
        self.func = func
        self.x_min, self.x_max = x_range
        self.color = color

    def draw(self, ctx: cairo.Context):
        ctx.save()
        ctx.set_source_rgba(*self.color)

        xs = np.linspace(self.x_min, self.x_max, 100)
        ctx.move_to(self.x_min, 0)

        for x in xs:
            ctx.line_to(x, self.func(x))

        ctx.line_to(self.x_max, 0)
        ctx.close_path()
        ctx.fill()
        ctx.restore()
