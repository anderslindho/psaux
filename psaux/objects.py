import logging
from itertools import count
from math import log
from typing import Generator

import pyglet
import pyrr
from pyrr import vector, Vector3

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

    @velocity.setter
    def velocity(self, new_velocity: Vector3) -> None:
        self.momentum = new_velocity * self.mass

    def __repr__(self) -> str:
        return str(vars(self))

    def tick(self, delta_time: float) -> None:
        # if forces too large, destroy
        forces, self.forces = self.forces, Vector3([0.0, 0.0, 0.0])
        self.momentum += forces * delta_time  # acceleration ?
        self.position = (
            self.position + self.velocity * delta_time
        )  # todo: update velocity, deal w separately // done, anything else ?
        logging.debug(
            f"Object {self.id} at {self.position=} with {self.velocity=} experiencing {pyrr.vector.length(forces)} forces "
        )

    def die(self) -> None:
        self.dead = True
        logging.debug(f"Object {self.id} of {self.__class__} died at {self.position=}")

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

    def elastic_collision_with(self, other) -> None:
        """conservation of momentum"""
        if self.mass > other.mass:
            other.die()
        else:
            self.die()
        logging.debug(f"Collision between\n- {self}\n- {other}")


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
        distance_vec = self.position - other.position
        return vector.length(distance_vec) < self.radius + other.radius
