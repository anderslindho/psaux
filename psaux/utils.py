import math


class Vector2d:
    def __init__(self, x_position: float, y_position: float):
        self.x = x_position
        self.y = y_position

    @property
    def position(self) -> tuple:
        _position = (self.x, self.y)
        return _position

    @classmethod
    def from_tuple(cls, position: tuple):
        return cls(position[0], position[1])

    @staticmethod
    def distance_between(position_one: tuple, position_two: tuple) -> float:
        vector_one = Vector2d.from_tuple(position_one)
        vector_two = Vector2d.from_tuple(position_two)
        x_distance = vector_one.x - vector_two.x
        y_distance = vector_one.y - vector_two.y
        return math.sqrt(x_distance ** 2 + y_distance ** 2)
