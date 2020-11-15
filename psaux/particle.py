from dataclasses import dataclass


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

    def __init__(self, position: Position, mass: float, velocity: Velocity):
        self.position = position
        self.mass = mass
        self.velocity = velocity

    def update(self, delta_time: float):
        self.position.x += self.velocity.x * delta_time
        self.position.y += self.velocity.y * delta_time
        # print(f"{self.position}")
