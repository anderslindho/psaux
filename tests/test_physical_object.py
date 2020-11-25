import pytest

import pyglet
from pyrr import Vector3

from psaux.objects import Circle, PhysicalObject

VECTOR3_TENS = Vector3([10.0, 10.0, 10.0])
VECTOR3_ONES = Vector3([1.0, 1.0, 1.0])
VECTOR3_ZEROS = Vector3([0.0, 0.0, 0.0])
FLOAT_100 = 100.0


class TestPhysicalObject:
    @pytest.fixture(autouse=True)
    def prepare(self):
        self.test_object = PhysicalObject(
            position=VECTOR3_ONES,
            mass=FLOAT_100,
            velocity=VECTOR3_ONES,
        )

    def test_physical_object(self):
        assert self.test_object.mass == FLOAT_100
        assert self.test_object.forces == VECTOR3_ZEROS
        assert self.test_object.momentum == VECTOR3_ONES * FLOAT_100
        assert self.test_object.__repr__() is not None
        assert self.test_object.dead is False

    def test_modify_mass(self):
        multiplier = 10
        self.test_object.mass = FLOAT_100 * multiplier

        new_momentum = VECTOR3_ONES * FLOAT_100 * multiplier

        assert self.test_object.mass == FLOAT_100 * multiplier
        assert self.test_object.momentum == new_momentum

    def test_modify_velocity(self):
        multiplier = 10
        self.test_object.velocity = VECTOR3_ONES * multiplier

        assert self.test_object.mass == FLOAT_100
        assert self.test_object.momentum == VECTOR3_TENS * FLOAT_100

    def test_tick_with_no_time_diff(self):
        self.test_object.tick(0)

        assert self.test_object.position == VECTOR3_ONES

    def test_die(self):
        self.test_object.die()

        assert self.test_object.dead is True

    def test_overlaps_with_self(self):
        assert self.test_object.overlaps_with(self.test_object) is True


class TestCircle:
    @pytest.fixture(autouse=True)
    def prepare(self):
        self.test_object = Circle(
            position=VECTOR3_ONES,
            mass=FLOAT_100,
            velocity=VECTOR3_ONES,
        )

    def test_circle(self):
        assert hasattr(self.test_object, "radius")
        assert isinstance(self.test_object.vertices, pyglet.shapes.Circle)
