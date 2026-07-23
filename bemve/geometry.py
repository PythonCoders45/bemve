from bemve.mobject import Mobject
import numpy as np


class Axes(Mobject):

    def __init__(
        self,
        x_range=(-5, 5, 1),
        y_range=(-3, 3, 1),
        width=10,
        height=6,
        color="#555566",
    ):
        super().__init__(color)
        self.x_min, self.x_max, self.x_step = x_range
        self.y_min, self.y_max, self.y_step = y_range
        self.width = width
        self.height = height

    def coords_to_point(self, x: float, y: float) -> np.ndarray:
        """Converts math space (x, y) into scene space coordinates."""
        px = (x - self.x_min) / (self.x_max - self.x_min) * self.width - (
            self.width / 2
        )
        py = (y - self.y_min) / (self.y_max - self.y_min) * self.height - (
            self.height / 2
        )
        return np.array([px, py, 0.0])

    def plot(self, func, color="#00E5FF", num_points=100) -> "FunctionGraph":
        x_vals = np.linspace(self.x_min, self.x_max, num_points)
        points = [self.coords_to_point(x, func(x)) for x in x_vals]
        return FunctionGraph(points, color=color)


class FunctionGraph(Mobject):

    def __init__(self, points, color="#00E5FF"):
        super().__init__(color)
        self.points = points  # List of 3D points defining the curve