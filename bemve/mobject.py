import numpy as np


class Mobject:

    def __init__(self, color="#00E5FF"):
        self.center = np.array([0.0, 0.0])
        self.color = color
        self.opacity = 1.0
        self.scale_factor = 1.0

    # --- Manipulation Methods ---
    def shift(self, vector):
        self.center += np.array(vector, dtype=float)
        return self

    def move_to(self, point):
        self.center = np.array(point, dtype=float)
        return self

    def scale(self, factor):
        self.scale_factor *= factor
        return self

    def copy(self):
        import copy

        return copy.deepcopy(self)

    # --- Drawing hook ---
    def draw(self, draw_context, canvas):
        pass


class Circle(Mobject):

    def __init__(self, radius=1.0, color="#00E5FF"):
        super().__init__(color)
        self.radius = radius

    def draw(self, draw_context, canvas):
        if self.opacity <= 0:
            return

        r = self.radius * self.scale_factor
        p1 = canvas.math_to_pixel((self.center[0] - r, self.center[1] - r))
        p2 = canvas.math_to_pixel((self.center[0] + r, self.center[1] + r))

        # Convert hex color to RGBA to support opacity (FadeIn/FadeOut)
        draw_context.ellipse([p1, p2], outline=self.color, width=4)