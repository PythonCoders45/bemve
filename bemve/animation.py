class Animation:

    def __init__(self, mobject, duration=1.0):
        self.mobject = mobject
        self.duration = duration

    def update(self, alpha: float):
        """Override to update mobject properties based on timeline alpha."""
        pass


class FadeIn(Animation):

    def update(self, alpha: float):
        self.mobject.opacity = alpha


class FadeOut(Animation):

    def update(self, alpha: float):
        self.mobject.opacity = 1.0 - alpha


class Shift(Animation):

    def __init__(self, mobject, direction, duration=1.0):
        super().__init__(mobject, duration)
        self.direction = np.array(direction, dtype=float)
        self.start_pos = None

    def update(self, alpha: float):
        if self.start_pos is None:
            self.start_pos = np.copy(self.mobject.center)
        self.mobject.center = self.start_pos + (self.direction * alpha)

class Create:

    def __init__(self, vmobject: VMobject):
        self.vmobject = vmobject

    def update(self, ctx: cairo.Context, alpha: float):
        # Draw progressively up to subpath_ratio = alpha
        self.vmobject.draw(ctx, subpath_ratio=alpha)


class Transform:

    def __init__(self, source_vmobject: VMobject, target_vmobject: VMobject):
        self.source = source_vmobject
        self.target = target_vmobject

    def update(self, ctx: cairo.Context, alpha: float):
        interpolated = self.source.interpolate(self.target, alpha)
        interpolated.draw(ctx, subpath_ratio=1.0)