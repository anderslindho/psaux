import math
import random

import pyglet
from pyglet.gl import GL_POINTS

from psaux.utils import Vector2d
from psaux.config import (
    WIDTH,
    HEIGHT,
    GRAVITY,
    PARTICLE_START_POINT,
    SUN_MASS,
    SUN_RADIUS,
    SUN_COLOR,
)


class World:
    def __init__(self):
        sun_position = (WIDTH / 2, HEIGHT / 2)

        # create sun
        self.sun = pyglet.shapes.Circle(
            sun_position[0], sun_position[1], SUN_RADIUS, color=SUN_COLOR
        )
        self.sun.x, self.sun.y = self.sun.position
        self.sun.dx, self.sun.dy = 0, 0
        self.sun.mass = SUN_MASS

        # create particles
        self.particle_batch = pyglet.graphics.Batch()
        self.particles = list()

    def spawn_particle(self, x: float = None, y: float = None):
        if x is None and y is None:
            starting_point = list(PARTICLE_START_POINT)
            starting_point[1] += (random.random() - 0.5) * 50
        else:
            starting_point = [x, y]

        particle = self.particle_batch.add(
            1, GL_POINTS, None, ("v2f/stream", starting_point)
        )
        particle.dx = (random.random() + 0.1) * 100
        particle.dy = (random.random() - 0.5) * HEIGHT / 8
        particle.acc_x, particle.acc_y = 0.0, 0.0
        particle.mass = 0.1
        particle.dead = False
        movement_vector = Vector2d(particle.dx, particle.dy)
        print(
            f"particle spawned at {tuple(starting_point)} with angle {movement_vector.angle} and magnitude {movement_vector.magnitude}"
        )
        self.particles.append(particle)

    def apply_forces(self, delta_time: float):
        for particle in self.particles:
            # todo: modify acceleration instead of velocity
            vertices = particle.vertices
            x_position = vertices[0]
            y_position = vertices[1]

            # check boundaries, else kill
            # todo: transfer force onto sun when colliding
            if (math.fabs(x_position - self.sun.x) < self.sun.radius) and (
                math.fabs(y_position - self.sun.y) < self.sun.radius
            ):
                particle.delete()
                particle.dead = True
                print(f"particle died at ({x_position}, {y_position})")
                continue

            # apply forces onto particles from sun
            particle.dy -= (
                GRAVITY
                * self.sun.mass
                * (y_position - self.sun.y)
                / Vector2d.distance_between(particle.vertices, self.sun.position) ** 3
            )
            particle.dx -= (
                GRAVITY
                * self.sun.mass
                * (x_position - self.sun.x)
                / Vector2d.distance_between(particle.vertices, self.sun.position) ** 3
            )
            vertices[0] += particle.dx * delta_time
            vertices[1] += particle.dy * delta_time

            # apply forces onto sun from particles
            self.sun.dy -= (
                GRAVITY
                * particle.mass
                * (self.sun.y - y_position)
                / Vector2d.distance_between(particle.vertices, self.sun.position) ** 3
            )
            self.sun.dx -= (
                GRAVITY
                * particle.mass
                * (self.sun.x - x_position)
                / Vector2d.distance_between(particle.vertices, self.sun.position) ** 3
            )
            self.sun.x += self.sun.dx * delta_time
            self.sun.y += self.sun.dy * delta_time
            self.sun.position = (self.sun.x, self.sun.y)
        self.particles = [p for p in self.particles if not p.dead]

    def place_sun(self, x, y):
        self.sun.position = (x, y)
        self.sun.dx, self.sun.dy = 0, 0
