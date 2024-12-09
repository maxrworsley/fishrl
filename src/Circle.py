import numpy as np


class Circle:
    def __init__(self, centre: np.array, colour: str, radius: float = 10.):
        self.radius = radius
        self.centre = centre
        self.colour = colour
        self.rotation_angle: float = 0.  # in deg

    def get_side_points(self) -> [np.array, np.array]:
        return self.get_side_point_from_offset(90.), self.get_side_point_from_offset(270.)

    def get_side_point_from_offset(self, offset: float):
        angle = np.deg2rad(offset + self.rotation_angle)
        return self.centre + self.radius * np.array([np.cos(angle), np.sin(angle)])

    def set_centre_and_angle(self, new_centre: np.array, new_angle: np.array):
        self.centre = new_centre
        self.rotation_angle = new_angle
