from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Velocity:
    x: float
    y: float


class Particle:
    """particle class"""

    def __init__(self, position: Position, mass: float, velocity: Velocity):
        self.position = position
        self.mass = mass
        self.velocity = velocity

    def update(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
