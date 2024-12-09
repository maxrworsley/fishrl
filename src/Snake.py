import numpy as np
from copy import deepcopy

from Circle import Circle


class Snake:

    __max_turn_angle = 50.

    def __init__(self, head_start: np.array, colour: str, num_circles: int, sizes: float | list[float]):
        self.colour = colour
        self.__circles = self.__make_circles(head_start, sizes, num_circles)

        self.__head_idx = 0

    def get_circles(self) -> [Circle]:
        return self.__circles

    def __make_circles(self, head_start: np.array, sizes: list[float] | float, num_circles: int) -> [Circle]:
        circles = []
        increment_size = int(10)  # this is only a placeholder
        for i in range(num_circles):
            size = sizes if sizes is list else sizes[i]
            circles.append(Circle(centre=head_start + np.array([i * increment_size] * 2),
                                  colour=self.colour, radius=size))
        return circles

    def get_head_points(self):
        return [self.__circles[self.__head_idx].get_side_point_from_offset(offset)
                for offset in np.linspace(90, 270, 10)]

    def move_towards(self, target_point: np.array, avoid: bool = False):

        if avoid:
            new_centre, new_angle = self.__impose_distance_constraint(-self.__circles[0].centre,
                                                                      -target_point, reverse=True)
        else:
            new_centre, new_angle = self.__impose_distance_constraint(self.__circles[0].centre, target_point)

        self.__circles[0].set_centre_and_angle(new_centre, new_angle)

        for i in range(len(self.__circles) - 1):
            new_centre, new_angle = self.__impose_distance_constraint(self.__circles[i].centre,
                                                                      self.__circles[i+1].centre)
            self.__circles[i+1].set_centre_and_angle(new_centre, new_angle)

    @classmethod
    def __impose_distance_constraint(cls, anchor_point: np.array, centre_point: np.array, reverse: bool = False) -> (np.array, float):
        sign = -1. if reverse else 1.
        diff_vec = anchor_point - centre_point
        new_point = sign*anchor_point - diff_vec/np.linalg.norm(diff_vec)
        new_angle = np.rad2deg(np.arctan2(diff_vec[1], diff_vec[0]))
        #angle = min(cls.__max_turn_angle, np.abs(new_angle))
        return deepcopy(new_point), deepcopy(new_angle)
