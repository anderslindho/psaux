import math
import random

import pyglet
from pyglet.gl import GL_POINTS

from psaux.utils import Vector2d
from psaux.config import WIDTH, HEIGHT

GRAVITY = 1.5

SUN_MASS = 500000
SUN_RADIUS = 25
SUN_COLOR = (255, 255, 0)
SUN_POSITION = (WIDTH / 2, HEIGHT / 2)

PARTICLE_START_POINT = [WIDTH / 2, 500]


class World:
    def __init__(self):
        # create sun
        self.sun = pyglet.shapes.Circle(
            SUN_POSITION[0], SUN_POSITION[1], SUN_RADIUS, color=SUN_COLOR
        )
        self.sun.x, self.sun.y = self.sun.position
        self.sun.dx, self.sun.dy = 0, 0
        self.sun.mass = SUN_MASS

        # create particles
        self.particle_batch = pyglet.graphics.Batch()
        self.particles = list()

    def add_particle(self):
        starting_point = list(PARTICLE_START_POINT)
        starting_point[1] += (random.random() - 0.5) * 50
        particle = self.particle_batch.add(
            1, GL_POINTS, None, ("v2f/stream", starting_point)
        )
        particle.dx = (random.random()) * WIDTH / 2
        particle.dy = (random.random() - 0.5) * HEIGHT / 4
        particle.mass = 1
        particle.dead = False
        self.particles.append(particle)

    def apply_forces(self, delta_time: float):
        for particle in self.particles:
            vertices = particle.vertices
            x_position = vertices[0]
            y_position = vertices[1]

            # check boundaries, else kill
            if (math.fabs(x_position - self.sun.x) < self.sun.radius) and (
                math.fabs(y_position - self.sun.y) < self.sun.radius
            ):
                particle.delete()
                particle.dead = True
                print(f"particle died at ({x_position}, {y_position})")

            # apply "gravity"
            particle.dy -= (
                GRAVITY
                * self.sun.mass
                * (y_position - self.sun.y)
                * delta_time
                / Vector2d.distance_between(particle.vertices, self.sun.position) ** 3
            )
            particle.dx -= (
                GRAVITY
                * self.sun.mass
                * (x_position - self.sun.x)
                * delta_time
                / Vector2d.distance_between(particle.vertices, self.sun.position) ** 3
            )
            vertices[0] += particle.dx * delta_time
            vertices[1] += particle.dy * delta_time
            # todo: apply forces onto sun
        self.particles = [p for p in self.particles if not p.dead]
