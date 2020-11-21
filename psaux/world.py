import itertools

import pyglet

from pyrr import Vector3

from psaux.config import (
    WIDTH,
    HEIGHT,
    BLUE,
    RED,
    GREEN,
)
from psaux.objects import PhysicalObject


class World:
    def __init__(self):
        self.real_time = 0.0  # seconds
        self.physics_time = 0.0  # seconds
        self.time_warp_factor = 1e5

        self.particles = list()
        self.particle_batch = pyglet.graphics.Batch()

        # create sun
        self.sun = PhysicalObject(
            position=Vector3([WIDTH / 2.0, HEIGHT / 2.0, 0.0]),
            mass=100000.0,
            velocity=Vector3([0.0, 0.0, 0.0]),
            color=RED,
            batch=self.particle_batch,
        )
        self.particles.append(self.sun)

        # create starting planets
        self.particles.append(
            PhysicalObject(
                position=Vector3([200.0, 700.0, 0.0]),
                mass=1000.0,
                velocity=Vector3([1e-4, 4e-5, 0.0]),
                color=GREEN,
                batch=self.particle_batch,
            )
        )
        self.particles.append(
            PhysicalObject(
                position=Vector3([400.0, 480.0, 0.0]),
                mass=1000.0,
                velocity=Vector3([2e-4, 2e-4, 0.0]),
                color=GREEN,
                batch=self.particle_batch,
            )
        )

    def update(self, delta_time: float):
        time_step = delta_time * self.time_warp_factor
        for first, second in itertools.combinations(self.particles, 2):
            if not first.boundary_check(second):
                first.forces += first.gravitational_force(second)
                second.forces -= first.forces
            else:
                first.elastic_collision_force(second)

        for particle in self.particles:
            particle.update(time_step)

        self.real_time += delta_time
        self.physics_time += delta_time * self.time_warp_factor

    def draw(self):
        self.particle_batch.draw()

    def spawn_planet(
        self, x: float, y: float, velocity_right: float, velocity_up: float
    ):
        mass = 100.0
        velocity = Vector3([velocity_right, velocity_up, 0.0])
        planet = PhysicalObject(
            position=Vector3([x, y, 0.0]),
            mass=mass,
            velocity=velocity,
            color=BLUE,
            batch=self.particle_batch,
        )
        self.particles.append(planet)

    def place_sun(self, x, y):
        self.sun.position = Vector3([x, y, 0])
