import cairo
import numpy as np
from bemve.vmobject import VMobject


class Matrix2D:
    """Represents a 2x2 linear transformation matrix."""

    def __init__(self, matrix=None):
        if matrix is None:
            self.matrix = np.identity(2)
        else:
            self.matrix = np.array(matrix, dtype=float)

    def apply(self, point: tuple[float, float]) -> tuple[float, float]:
        res = self.matrix @ np.array(point)
        return (res[0], res[1])


class LinearTransform(VMobject):
    """Applies matrix transformations to basis vectors and grids in 2D space."""

    def __init__(self, matrix: Matrix2D, color_i=(1.0, 0.2, 0.3, 1.0), color_j=(0.2, 1.0, 0.4, 1.0)):
        super().__init__()
        self.matrix = matrix
        self.color_i = color_i
        self.color_j = color_j

    def draw(self, ctx: cairo.Context):
        ctx.save()

        # Transformed Basis Vector i_hat (1, 0)
        i_transformed = self.matrix.apply((1.0, 0.0))
        ctx.set_source_rgba(*self.color_i)
        ctx.set_line_width(0.05)
        ctx.move_to(0, 0)
        ctx.line_to(*i_transformed)
        ctx.stroke()

        # Transformed Basis Vector j_hat (0, 1)
        j_transformed = self.matrix.apply((0.0, 1.0))
        ctx.set_source_rgba(*self.color_j)
        ctx.set_line_width(0.05)
        ctx.move_to(0, 0)
        ctx.line_to(*j_transformed)
        ctx.stroke()

        ctx.restore()
