import random
import cairo
import numpy as np


class Particle:
    def __init__(self, position: tuple[float, float], velocity: tuple[float, float], lifetime: float, color: tuple):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color

    def update(self, dt: float, gravity: tuple[float, float]):
        self.velocity += np.array(gravity) * dt
        self.position += self.velocity * dt
        self.lifetime -= dt

    def is_alive(self) -> bool:
        return self.lifetime > 0.0


class ParticleEmitter:
    """Generates kinetic particle effects like explosions, fluid drops, or sparks."""

    def __init__(
        self,
        position: tuple[float, float] = (0.0, 0.0),
        rate: int = 20,
        gravity: tuple[float, float] = (0.0, -9.81),
    ):
        self.position = np.array(position, dtype=float)
        self.rate = rate
        self.gravity = gravity
        self.particles: list[Particle] = []

    def emit(self, count: int = 5):
        for _ in range(count):
            angle = random.uniform(0, 2 * np.pi)
            speed = random.uniform(1.0, 4.0)
            vx = speed * np.cos(angle)
            vy = speed * np.sin(angle)
            lifetime = random.uniform(0.5, 1.5)
            color = (
                random.uniform(0.8, 1.0),
                random.uniform(0.3, 0.6),
                0.1,
                1.0,
            )
            self.particles.append(Particle(self.position, (vx, vy), lifetime, color))

    def update(self, dt: float):
        self.emit(self.rate // 10)
        alive_particles = []
        for p in self.particles:
            p.update(dt, self.gravity)
            if p.is_alive():
                alive_particles.append(p)
        self.particles = alive_particles

    def draw(self, ctx: cairo.Context):
        ctx.save()
        for p in self.particles:
            alpha = p.lifetime / p.max_lifetime
            r, g, b, _ = p.color
            ctx.arc(p.position[0], p.position[1], 0.04 * alpha, 0, 2 * np.pi)
            ctx.set_source_rgba(r, g, b, alpha)
            ctx.fill()
        ctx.restore()
