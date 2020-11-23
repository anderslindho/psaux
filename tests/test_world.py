import pytest
from pyrr import Vector3

from psaux.world import World
from psaux.config import PsauxConfig


class TestWorld:
    @pytest.fixture(autouse=True)
    def prepare(self):
        self.world = World()

    def test_generated_particles(self):
        assert len(self.world.entities) == 3

    def test_spawn_planet(self):
        self.world.spawn_planet(0.0, 0.0, 0.0, 0.0)

        assert len(self.world.entities) == 4

    def test_sun_position(self):
        assert self.world.sun.position == Vector3(
            [PsauxConfig.width / 2, PsauxConfig.height / 2, 0.0]
        )

    def test_place_sun(self):
        self.world.place_sun(2.0, 3.0)

        assert self.world.sun.position == Vector3([2.0, 3.0, 0.0])