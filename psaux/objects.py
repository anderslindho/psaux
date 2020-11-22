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
        self.dead = False

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, value: float):
        factor = value / self.mass
        self._mass = value
        self.momentum *= factor

    @property
    def velocity(self) -> float:
        return self.momentum / self.mass

    @velocity.setter
    def velocity(self, new_velocity: Vector3):
        self.momentum = new_velocity * self.mass

    def __repr__(self):
        return str(vars(self))

    def tick(self, delta_time: float) -> None:
        # if forces too large, destroy

        self.momentum += self.forces * delta_time
        self.position = (
            self.position + self.velocity * delta_time
        )  # todo: update velocity, deal w separately // done, anything else ?
        self.forces = Vector3([0.0, 0.0, 0.0])

    @abstractmethod
    def die(self) -> None:
        self.dead = True

    @abstractmethod
    def overlaps_with(self, other) -> bool:
        return self.position == other.position

    def gravitational_force_from(self, other) -> Vector3:
        """
        :math:`\vec{F} = -G * (m_1 * m_2)/(|r|^2) * \vec{r}`
        """
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

    def elastic_collision_with(self, other):
        """conservation of momentum"""
        print(f"collision between\n- {self}\n- {other}")
        if self.mass > other.mass:
            other.die()
        else:
            self.die()


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

    def tick(self, delta_time: float) -> None:
        super(Circle, self).tick(delta_time)
        if not self.dead:
            self.vertices.position = (self.position[0], self.position[1])

    def die(self) -> None:
        super(Circle, self).die()
        self.vertices.delete()

    def overlaps_with(self, other) -> bool:
        distance_vec = self.position - other.position
        return vector.length(distance_vec) < self.radius + other.radius
