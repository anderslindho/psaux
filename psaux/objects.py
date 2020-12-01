import logging
from itertools import count
from math import log
from typing import Generator

import numpy as np
import pyglet
import pyrr
from pyrr import Vector3, vector

from psaux.config import WorldSettings


class PhysicalObject:
    _id: Generator = count(1)

    def __init__(
        self,
        position: Vector3,
        mass: float,
        velocity: Vector3,
    ):
        self.id = next(self._id)
        self.position = position  # [metres, metres, metres]
        self._mass = mass  # kg
        self.momentum = mass * velocity
        self.forces = Vector3([0.0, 0.0, 0.0])
        self.intersecting = False
        self.dead = False

        logging.debug(
            f"Spawned {self.id=} type {self.__class__} at {self.position=} with {self.velocity=}"
        )

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, new_mass: float) -> None:
        factor = new_mass / self.mass
        self._mass = new_mass
        self.momentum *= factor

    @property
    def velocity(self) -> Vector3:
        return self.momentum / self.mass

    def __repr__(self) -> str:
        return str(vars(self))

    def tick(self, delta_time: float) -> None:
        logging.debug(
            f"Object {self.id} at {self.position=} with {self.velocity=} experiencing {pyrr.vector.length(self.forces)} forces"
        )

        # todo: if forces too large, destroy
        self.momentum += self.forces * delta_time
        # todo: overlap adjustment should happen here; after momentum is adjusted
        self.position += self.velocity * delta_time
        self.forces = Vector3([0.0, 0.0, 0.0])

    def die(self) -> None:
        self.dead = True

        logging.debug(f"Object {self.id} of {self.__class__} died at {self.position=}")

    def vector_to(self, other) -> Vector3:
        return self.position - other.position

    def distance_to(self, other) -> float:
        return vector.length(self.vector_to(other))

    def overlaps_with(self, other) -> bool:
        return bool(
            self.distance_to(other) <= 0.0
        )  # cast to bool because we get np.bool_

    def gravitational_force_from(self, other) -> Vector3:
        """
        :math:`\vec{F} = -G * (m_1 * m_2)/(|r|^2) * \vec{r}`
        """
        if self.intersecting and other.intersecting:
            return Vector3([0.0, 0.0, 0.0])

        distance = self.distance_to(other)
        unit_vector = self.vector_to(other) / distance
        force_magnitude = (
            WorldSettings.gravity_constant * self.mass * other.mass / distance ** 2
        )
        force_vector = -force_magnitude * unit_vector
        return force_vector

    def elastic_collision_with(self, other) -> tuple:
        """conservation of momentum"""

        logging.debug(f"Collision between\n- {self}\n- {other}")

        sum_of_masses = self.mass + other.mass
        vector_to = self.vector_to(other)
        distance_squared = self.distance_to(other) ** 2

        self_new_momentum = (
            self.velocity
            - 2
            * other.mass
            / sum_of_masses
            * np.dot(self.velocity - other.velocity, vector_to)
            / distance_squared
            * vector_to
            * self.mass
        )
        other_new_momentum = (
            other.velocity
            - 2
            * self.mass
            / sum_of_masses
            * np.dot(other.velocity - self.velocity, -vector_to)
            / distance_squared
            * (-vector_to)
            * other.mass
        )
        # todo: take derivative of momentum to get force instead ?

        return self_new_momentum, other_new_momentum


class Circle(PhysicalObject):
    def __init__(
        self,
        color: tuple = (255, 255, 255),
        batch=None,
        *args,
        **kwargs,
    ):
        super(Circle, self).__init__(*args, **kwargs)
        self.radius = log(self.mass, 2)  # metres
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
        return self.distance_to(other) < self.radius + other.radius
