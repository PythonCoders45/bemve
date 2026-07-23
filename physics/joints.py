import cairo
import numpy as np
import pymunk
from bemve.physics import PhysicsBody


class SpringJoint:
    """Connects two physical bodies with an elastic damped spring constraint."""

    def __init__(
        self,
        body_a: PhysicsBody,
        body_b: PhysicsBody,
        rest_length: float = 2.0,
        stiffness: float = 100.0,
        damping: float = 5.0,
        color=(1.0, 0.8, 0.2, 1.0),
    ):
        self.body_a = body_a
        self.body_b = body_b
        self.color = color

        self.constraint = pymunk.DampedSpring(
            body_a.body,
            body_b.body,
            (0, 0),
            (0, 0),
            rest_length,
            stiffness,
            damping,
        )

    def draw(self, ctx: cairo.Context):
        ctx.save()
        pos_a = self.body_a.body.position
        pos_b = self.body_b.body.position

        ctx.set_source_rgba(*self.color)
        ctx.set_line_width(0.03)

        # Draw spring line connection
        ctx.move_to(pos_a.x, pos_a.y)
        ctx.line_to(pos_b.x, pos_b.y)
        ctx.stroke()
        ctx.restore()


class PivotJoint:
    """Attaches two bodies at a shared pivot point (ideal for pendulums and ragdolls)."""

    def __init__(
        self,
        body_a: PhysicsBody,
        body_b: PhysicsBody,
        pivot_point: tuple[float, float],
        color=(0.9, 0.9, 0.9, 1.0),
    ):
        self.body_a = body_a
        self.body_b = body_b
        self.pivot_point = pivot_point
        self.color = color

        self.constraint = pymunk.PivotJoint(
            body_a.body, body_b.body, pivot_point
        )

    def draw(self, ctx: cairo.Context):
        ctx.save()
        pos = self.constraint.a.position
        ctx.arc(pos.x, pos.y, 0.08, 0, 2 * np.pi)
        ctx.set_source_rgba(*self.color)
        ctx.fill()
        ctx.restore()
