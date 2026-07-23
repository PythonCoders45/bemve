import cairo
import numpy as np


class FadeIn:
    """Fades an object in from transparent to full opacity."""

    def __init__(self, mobject, duration: float = 1.0):
        self.mobject = mobject
        self.duration = duration

    def update(self, ctx: cairo.Context, alpha: float):
        # Scale alpha directly for transparency
        if hasattr(self.mobject, "draw"):
            ctx.save()
            # If object supports color with alpha
            if hasattr(self.mobject, "color"):
                r, g, b, _ = self.mobject.color
                self.mobject.color = (r, g, b, alpha)
            self.mobject.draw(ctx)
            ctx.restore()


class FadeOut:
    """Fades an object out to full transparency."""

    def __init__(self, mobject, duration: float = 1.0):
        self.mobject = mobject
        self.duration = duration

    def update(self, ctx: cairo.Context, alpha: float):
        if hasattr(self.mobject, "draw"):
            ctx.save()
            if hasattr(self.mobject, "color"):
                r, g, b, _ = self.mobject.color
                self.mobject.color = (r, g, b, 1.0 - alpha)
            self.mobject.draw(ctx)
            ctx.restore()


class SlideIn:
    """Slides an object onto the screen from a offset direction."""

    def __init__(self, mobject, direction=(0.0, -3.0), duration: float = 1.0):
        self.mobject = mobject
        self.start_offset = np.array(direction, dtype=float)
        self.duration = duration

    def update(self, ctx: cairo.Context, alpha: float):
        ctx.save()
        # Interpolate translation position from offset to (0,0)
        current_offset = self.start_offset * (1.0 - alpha)
        ctx.translate(current_offset[0], current_offset[1])
        self.mobject.draw(ctx)
        ctx.restore()


class GrowFromCenter:
    """Scales an object up from 0% size to 100% size."""

    def __init__(self, mobject, duration: float = 1.0):
        self.mobject = mobject
        self.duration = duration

    def update(self, ctx: cairo.Context, alpha: float):
        ctx.save()
        # Scale smoothly from 0 to 1
        ctx.scale(alpha, alpha)
        self.mobject.draw(ctx)
        ctx.restore()
