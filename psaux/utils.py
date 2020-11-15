import math


class Vector2d:
    def __init__(self, x_position: float, y_position: float):
        self.x = x_position
        self.y = y_position

    @property
    def position(self) -> tuple:
        _position = (self.x, self.y)
        return _position

    @property
    def angle(self) -> float:
        radians = math.atan2(self.y, self.x)
        return math.degrees(radians)

    @property
    def magnitude(self) -> float:
        return math.hypot(self.x, self.y)

    def as_tuple(self):
        return self.x, self.y

    @classmethod
    def from_tuple(cls, position: tuple):
        return cls(position[0], position[1])

    @classmethod
    def from_difference(cls, start: tuple, end: tuple):
        difference = end[0] - start[0], end[1] - start[1]
        return cls.from_tuple(difference)

    @staticmethod
    def distance_between(position_one: tuple, position_two: tuple) -> float:
        vector_one = Vector2d.from_tuple(position_one)
        vector_two = Vector2d.from_tuple(position_two)
        x_distance = vector_one.x - vector_two.x
        y_distance = vector_one.y - vector_two.y
        return math.sqrt(x_distance ** 2 + y_distance ** 2)
