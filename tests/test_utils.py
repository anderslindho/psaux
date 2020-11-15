from psaux.utils import Vector2d


def test_generate_vector_from_coordinates():
    vector = Vector2d(2, 2)
    assert vector.x == vector.y == 2
    assert vector.position == (2, 2)


def test_generate_vector_from_tuple():
    vector = Vector2d.from_tuple((3, 4))
    assert vector.x == 3
    assert vector.y == 4
    assert vector.position == (3, 4)


def test_properties():
    vector = Vector2d(2, 0)
    assert vector.angle == 0
    assert vector.magnitude == 2


def test_generate_tuple_from_vector():
    vector = Vector2d(5, 7)
    assert vector.as_tuple() == (5, 7)


def test_distance_between():
    vector_one = Vector2d(0, 0)
    vector_two = Vector2d(6, 0)
    assert Vector2d.distance_between(vector_one.position, vector_two.position) == 6.0
    assert Vector2d.distance_between(
        vector_one.position, vector_two.position
    ) == Vector2d.distance_between(vector_two.position, vector_one.position)
