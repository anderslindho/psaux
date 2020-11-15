from dataclasses import dataclass

from pyglet.graphics.vertexdomain import VertexList

GRAVITY = -100


@dataclass
class Position:
    x: float
    y: float


@dataclass
class Velocity:
    x: float
    y: float


class Particle:
    """particle class"""

    def __init__(self, position: VertexList, mass: float, velocity: tuple):
        self.position = Position(position.vertices)
        self.mass = mass
        self.velocity = Velocity(velocity)

    def update(self, delta_time: float):
        self.velocity.y += GRAVITY * delta_time
        position = self.position.vertices
        position[0] += self.velocity.x * delta_time
        position[1] += self.velocity.y * delta_time

    @property
    def dead(self):
        if self.position[0] < 0:
            self.position.delete()
            return True
        return False
