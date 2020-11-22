from abc import abstractmethod
from math import log

import pyglet
from pyrr import vector, Vector3

from psaux.config import WorldSettings


class PhysicalObject:
    def __init__(
        self,
        position: Vector3,
        mass: float,
        velocity: Vector3,
    ):
        self.position = position  # [m, m, m]
        self._mass = mass  # kg
        self.momentum = mass * velocity
        self.forces = Vector3([0.0, 0.0, 0.0])

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value: float):
        factor = value / self.mass
        self._mass = value
        self.momentum *= factor

    def __repr__(self):
        return str(vars(self))

    def tick(self, delta_time: float):
        self.momentum += self.forces * delta_time
        self.position = self.position + self.momentum / self.mass * delta_time
        self.forces = Vector3([0.0, 0.0, 0.0])

    @abstractmethod
    def overlaps_with(self, other) -> bool:
        return

    def gravitational_force_from(self, other):
        """F_v = -G * (M_1 * M_2)/(r^2) * r_v"""
        distance_vec = self.position - other.position
        distance_vec_magnitude = vector.length(distance_vec)
        unit_vector = distance_vec / distance_vec_magnitude

        force_magnitude = (
            WorldSettings.gravity_constant
            * self.mass
            * other.mass
            / distance_vec_magnitude ** 2
        )
        force_vector = -force_magnitude * unit_vector
        return force_vector

    def elastic_collision_force_from(self, other):
        """conservation of momentum"""
        print(f"collision between\n- {self}\n- {other}")


class Circle(PhysicalObject):
    def __init__(
        self,
        color: tuple = (255, 255, 255),
        batch=None,
        *args,
        **kwargs,
    ):
        super(Circle, self).__init__(*args, **kwargs)

        self.radius = log(self.mass, 2)  # m
        self.vertices = pyglet.shapes.Circle(
            self.position[0], self.position[1], self.radius, color=color, batch=batch
        )

    def tick(self, delta_time: float):
        super(Circle, self).tick(delta_time)
        self.vertices.position = (self.position[0], self.position[1])

    def overlaps_with(self, other) -> bool:
        distance_vec = self.position - other.position
        return vector.length(distance_vec) < self.radius + other.radius
