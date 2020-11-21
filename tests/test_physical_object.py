import pytest

import pyglet
from pyrr import Vector3

from psaux.objects import PhysicalObject

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
        assert isinstance(self.test_object.vertices, pyglet.shapes.Circle)

    def test_modify_mass(self):
        multiplier = 10
        self.test_object.mass = FLOAT_100 * multiplier

        new_momentum = VECTOR3_ONES * FLOAT_100 * multiplier

        assert self.test_object.mass == FLOAT_100 * multiplier
        assert self.test_object.momentum == new_momentum
