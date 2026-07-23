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