import pytest

from psaux.utils import Vector2d


def test_vector_with_coordinates():
    vector = Vector2d(2, 2)
    assert vector.x == vector.y == 2
    assert vector.position == (2, 2)


def test_vector_with_tuple():
    vector = Vector2d.from_tuple((3, 4))
    assert vector.x == 3
    assert vector.y == 4
    assert vector.position == (3, 4)


def test_distance_between():
    vector_one = Vector2d(0, 0)
    vector_two = Vector2d(6, 0)
    assert Vector2d.distance_between(vector_one.position, vector_two.position) == 6.0
    assert Vector2d.distance_between(
        vector_one.position, vector_two.position
    ) == Vector2d.distance_between(vector_two.position, vector_one.position)
