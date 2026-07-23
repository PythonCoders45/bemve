from typing import List, Tuple, Optional
import cairo
import numpy as np
import pymunk

from bemve.vmobject import VMobject


class PhysicsWorld:
    """Manages the 2D physics space, gravity, and body updates."""

    def __init__(self, gravity: Tuple[float, float] = (0.0, -9.81)):
        self.space = pymunk.Space()
        # Set gravity (PyMunk uses standard X, Y coordinates)
        self.space.gravity = gravity
        self.bodies: List["PhysicsBody"] = []

    def add(self, *bodies: "PhysicsBody"):
        """Adds physical bodies to the simulation space."""
        for b in bodies:
            self.space.add(b.body, b.shape)
            self.bodies.append(b)

    def step(self, dt: float = 1.0 / 60.0):
        """Advances the physics simulation by dt seconds."""
        self.space.step(dt)

    def draw(self, ctx: cairo.Context):
        """Draws all physical bodies onto the Cairo context."""
        for b in self.bodies:
            b.draw(ctx)


class PhysicsBody(VMobject):
    """Base physical body wrapper connecting PyMunk logic to Cairo drawing."""

    def __init__(
        self,
        position: Tuple[float, float] = (0.0, 0.0),
        body_type: str = "dynamic",
        color: Tuple[float, float, float, float] = (0.2, 0.8, 1.0, 1.0),
    ):
        super().__init__()
        self.color = color

        if body_type == "static":
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        elif body_type == "kinematic":
            self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        else:
            self.body = pymunk.Body(1.0, 100)  # Mass, Moment (overridden by shapes)

        self.body.position = position
        self.shape: Optional[pymunk.Shape] = None


class PhysicsCircle(PhysicsBody):
    """A rigid physical circle subject to gravity and collisions."""

    def __init__(
        self,
        radius: float = 0.5,
        position: Tuple[float, float] = (0.0, 5.0),
        mass: float = 1.0,
        elasticity: float = 0.8,
        friction: float = 0.5,
        color: Tuple[float, float, float, float] = (1.0, 0.3, 0.4, 1.0),
        body_type: str = "dynamic",
    ):
        super().__init__(position=position, body_type=body_type, color=color)
        self.radius = radius

        if body_type == "dynamic":
            moment = pymunk.moment_for_circle(mass, 0, radius)
            self.body = pymunk.Body(mass, moment)
            self.body.position = position

        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = elasticity
        self.shape.friction = friction

    def draw(self, ctx: cairo.Context):
        ctx.save()
        pos = self.body.position
        
        # Translate Cairo context to body location
        ctx.translate(pos.x, pos.y)
        ctx.rotate(self.body.angle)

        # Draw Circle
        ctx.arc(0, 0, self.radius, 0, 2 * np.pi)
        ctx.set_source_rgba(*self.color)
        ctx.fill_preserve()

        ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        ctx.set_line_width(0.03)
        ctx.stroke()

        # Draw Orientation Line (shows rotation)
        ctx.move_to(0, 0)
        ctx.line_to(self.radius, 0)
        ctx.stroke()

        ctx.restore()


class PhysicsBox(PhysicsBody):
    """A rigid physical rectangle shape."""

    def __init__(
        self,
        width: float = 1.0,
        height: float = 1.0,
        position: Tuple[float, float] = (0.0, 0.0),
        mass: float = 1.0,
        elasticity: float = 0.5,
        friction: float = 0.6,
        color: Tuple[float, float, float, float] = (0.2, 0.9, 0.4, 1.0),
        body_type: str = "dynamic",
    ):
        super().__init__(position=position, body_type=body_type, color=color)
        self.width = width
        self.height = height

        if body_type == "dynamic":
            moment = pymunk.moment_for_box(mass, (width, height))
            self.body = pymunk.Body(mass, moment)
            self.body.position = position

        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = elasticity
        self.shape.friction = friction

    def draw(self, ctx: cairo.Context):
        ctx.save()
        pos = self.body.position

        ctx.translate(pos.x, pos.y)
        ctx.rotate(self.body.angle)

        w, h = self.width, self.height
        ctx.rectangle(-w / 2.0, -h / 2.0, w, h)
        
        ctx.set_source_rgba(*self.color)
        ctx.fill_preserve()

        ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        ctx.set_line_width(0.03)
        ctx.stroke()

        ctx.restore()


class PhysicsFloor(PhysicsBody):
    """A static ground surface that objects bounce off of."""

    def __init__(
        self,
        y_position: float = -3.0,
        width: float = 12.0,
        thickness: float = 0.2,
        elasticity: float = 0.8,
        friction: float = 0.8,
        color: Tuple[float, float, float, float] = (0.5, 0.5, 0.6, 1.0),
    ):
        super().__init__(position=(0.0, y_position), body_type="static", color=color)
        self.width = width
        self.thickness = thickness

        self.shape = pymunk.Poly.create_box(self.body, (width, thickness))
        self.shape.elasticity = elasticity
        self.shape.friction = friction

    def draw(self, ctx: cairo.Context):
        ctx.save()
        pos = self.body.position
        w, h = self.width, self.thickness

        ctx.rectangle(pos.x - w / 2.0, pos.y - h / 2.0, w, h)
        ctx.set_source_rgba(*self.color)
        ctx.fill_preserve()

        ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        ctx.set_line_width(0.02)
        ctx.stroke()

        ctx.restore()
