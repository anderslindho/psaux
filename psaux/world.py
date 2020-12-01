import datetime
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
        self.drawing_batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label(
            "",
            x=10,
            y=10,
            font_size=18,
            color=(200, 200, 100, 200),
            batch=self.drawing_batch,
        )

        logging.debug(
            f"World created at {self.real_time=}, {self.physics_time=} with {len(self.entities)} entities\n"
            f"{vars(self.settings)}"
        )

        self.sun = None
        self.spawn_initial_planets()

    def spawn_initial_planets(self):
        # create sun
        self.sun = Circle(
            position=Vector3([PsauxConfig.width / 2.0, PsauxConfig.height / 2.0, 0.0]),
            mass=1e6,
            velocity=Vector3([0.0, 0.0, 0.0]),
            color=RED,
            batch=self.drawing_batch,
        )
        self.entities.append(self.sun)

        # create starting planets
        self.spawn_planet(
            position=Vector3([200.0, 700.0, 0.0]),
            velocity=Vector3([3e-4, 4e-5, 0.0]),
            mass=1e4,
            color=GREEN,
        )
        self.spawn_planet(
            position=Vector3([400.0, 480.0, 0.0]),
            velocity=Vector3([5e-4, 2e-4, 0.0]),
            mass=1e4,
            color=GREEN,
        )

    def update(self, delta_time: float) -> None:
        time_step = delta_time * self.settings.time_warp_factor

        for first, second in itertools.combinations(self.entities, 2):
            if first.overlaps_with(second):
                first.intersecting = (
                    second.intersecting
                ) = True  # todo: change so they keep track of what they intersect with?

                # self.move_apart_planets(first, second)

                (
                    first_momentum,
                    second_momentum,
                ) = first.elastic_collision_with(second)
                first.momentum += first_momentum
                second.momentum += second_momentum

            first.forces += first.gravitational_force_from(second)
            second.forces -= first.forces

        for entity in self.entities:
            entity.tick(time_step)
            entity.intersecting = False

        self.entities = [entity for entity in self.entities if not entity.dead]
        self.real_time += delta_time
        self.physics_time += delta_time * self.settings.time_warp_factor
        passed_time = datetime.timedelta(seconds=self.physics_time)
        self.label.text = f"{len(self.entities) - 1} planets: {round(self.real_time, 2)} seconds (rt) - {passed_time.days} days (in-game)"

        logging.debug(
            f"{len(self.entities)} existing at {self.real_time=}, {self.physics_time=}"
        )

    @staticmethod
    def move_apart_planets(first, second):
        distance_between_centres = first.distance_to(second)
        unit_vector_to_other = first.vector_to(second) / distance_between_centres
        needed_movement_from_second = unit_vector_to_other * (
            distance_between_centres - first.radius + second.radius
        )
        # todo: make them move relative to their weight? m_1 / m_1 + m_2
        # _some_ sort of improvement is necessary here
        if first.mass < second.mass:
            first.position += needed_movement_from_second / 4
        else:
            second.position -= needed_movement_from_second / 4

    def draw(self):
        self.drawing_batch.draw()

    def modify_time_warp(self, change: float) -> None:
        self.settings.time_warp_factor += change * self.settings.time_warp_multiplier

        logging.debug(f"Changing time warp to {self.settings.time_warp_factor}")

    # todo: accept vectors instead
    def spawn_planet(
        self,
        position: Vector3,
        velocity: Vector3,
        mass: float = 1e2,
        color: tuple = BLUE,
    ):
        planet = Circle(
            position=position,
            mass=mass,
            velocity=velocity,
            color=color,
            batch=self.drawing_batch,
        )
        self.entities.append(planet)

        logging.debug(f"Object {planet.id} spawned at {position=} with {velocity=}")

    def place_sun(self, x, y):
        self.sun.position = Vector3([x, y, 0])

        logging.debug(f"Sun is moved to {x=}, {y=}")
