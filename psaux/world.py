import itertools
import logging

import pyglet
from pyrr import Vector3

from psaux.config import PsauxConfig, WorldSettings
from psaux.objects import Circle
from psaux.utils import BLUE, GREEN, RED


class World:
    def __init__(self, settings: WorldSettings = None):
        if settings is None:
            self.settings = WorldSettings()
        else:
            self.settings = settings

        self.real_time = 0.0  # seconds
        self.physics_time = 0.0  # seconds

        self.entities = list()
        self.entity_batch = pyglet.graphics.Batch()

        # create sun
        self.sun = Circle(
            position=Vector3([PsauxConfig.width / 2.0, PsauxConfig.height / 2.0, 0.0]),
            mass=1e6,
            velocity=Vector3([0.0, 0.0, 0.0]),
            color=RED,
            batch=self.entity_batch,
        )
        self.entities.append(self.sun)

        # create starting planets
        self.entities.append(
            Circle(
                position=Vector3([200.0, 700.0, 0.0]),
                mass=1e4,
                velocity=Vector3([3e-4, 4e-5, 0.0]),
                color=GREEN,
                batch=self.entity_batch,
            )
        )
        self.entities.append(
            Circle(
                position=Vector3([400.0, 480.0, 0.0]),
                mass=1e4,
                velocity=Vector3([5e-4, 2e-4, 0.0]),
                color=GREEN,
                batch=self.entity_batch,
            )
        )

        logging.debug(
            f"World created at {self.real_time=}, {self.physics_time=} with {len(self.entities)} entities\n"
            f"{vars(self.settings)}"
        )

    def update(self, delta_time: float) -> None:
        time_step = delta_time * self.settings.time_warp_factor

        for first, second in itertools.combinations(self.entities, 2):
            first.forces += first.gravitational_force_from(second)
            second.forces -= first.forces

            if first.overlaps_with(second):
                first.elastic_collision_with(second)

        for entity in self.entities:
            entity.tick(time_step)
        self.entities = [entity for entity in self.entities if not entity.dead]

        self.real_time += delta_time
        self.physics_time += delta_time * self.settings.time_warp_factor

        logging.debug(
            f"{len(self.entities)} existing at {self.real_time=}, {self.physics_time=}"
        )

    def modify_time_warp(self, change: float) -> None:
        self.settings.time_warp_factor += change * self.settings.time_warp_multiplier

        logging.debug(f"Changing time warp to {self.settings.time_warp_factor}")

    def draw(self):
        self.entity_batch.draw()

    def spawn_planet(
        self, x: float, y: float, velocity_right: float, velocity_up: float
    ):
        mass = 1e2
        velocity = Vector3([velocity_right, velocity_up, 0.0])
        planet = Circle(
            position=Vector3([x, y, 0.0]),
            mass=mass,
            velocity=velocity,
            color=BLUE,
            batch=self.entity_batch,
        )
        self.entities.append(planet)

        logging.debug(
            f"Object {planet.id} spawned at {x=}, {y=} with {velocity_right=}, {velocity_up=}"
        )

    def place_sun(self, x, y):
        self.sun.position = Vector3([x, y, 0])

        logging.debug(f"Sun is moved to {x=}, {y=}")
