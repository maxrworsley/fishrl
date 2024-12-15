import numpy as np
import pygame
from copy import deepcopy

from Circle import Circle
from Snake import Snake


class PygameGUI:

    __col_lookup = {
        'white': (255, 255, 255),
        'off-white': (210, 206, 235),
        'blue': (0, 0, 255),
        'black': (0, 0, 0),
        'blue-midnight': (62, 81, 176),
        'blue-grey': (36, 57, 69),
        'blue-sky': (50, 130, 173)
    }

    def __init__(self, bg_colour: str, screen_size: [int, int], sim_bounds: np.array, fps: int):
        self.__bg_colour = self.__lookup_colour(bg_colour)
        self.__screen_size = screen_size
        self.__sim_bounds = sim_bounds
        self.__fps = fps
        self.__clock = pygame.time.Clock()

        self.__zoom = 1.

        pygame.init()
        self.__screen = pygame.display.set_mode(screen_size)

    def tick(self):
        self.__clock.tick(self.__fps)

    # DRAW FUNCTIONS

    def draw_bg(self):
        self.__screen.fill(self.__bg_colour)

    def draw_snake(self, snake: Snake, should_draw_circles: bool = True):
        head_pts, pts_lower, pts_upper = [], [], []
        for idx, circle in enumerate(snake.get_circles()):

            if should_draw_circles:
                self.__draw_circle(circle)

            if idx == 0:
                continue

            pt_lower, pt_upper = circle.get_side_points()
            pts_lower.append(deepcopy(pt_lower))
            pts_upper.append(deepcopy(pt_upper))

        combined_pts = snake.get_head_points() + pts_lower + pts_upper[::-1]

        self.__draw_snake_body(snake, combined_pts)

    def __draw_circle(self, circle: Circle):
        centre = self.__sim_2_screen_map_fn(circle.centre)
        col = self.__lookup_colour(circle.colour)
        pygame.draw.circle(self.__screen, col, centre, self.__sim_2_screen_scale(circle.radius), width=1)

    def __draw_snake_body(self, snake: Snake, combined_pts: [np.array]):
        combined_mapped = [self.__sim_2_screen_map_fn(pt) for pt in combined_pts]
        col = self.__lookup_colour(snake.colour)
        pygame.draw.lines(self.__screen, col, closed=True, points=combined_mapped)

    def __lookup_colour(self, col: str):
        try:
            return self.__col_lookup[col]
        except KeyError:
            return self.__col_lookup['black']

    # MAP FUNCTIONS

    def __sim_2_screen_map_fn(self, sim_coord: [int, int]):
        rescaled = ((np.array(sim_coord) * self.__zoom) / self.__sim_bounds) * self.__screen_size
        translated_x = rescaled[0].item(0) + self.__screen_size[0] / 2
        translated_y = -rescaled[1].item(0) + self.__screen_size[1] / 2
        return translated_x, translated_y

    def screen_2_sim_map_fn(self, screen_coord: np.array) -> np.array:
        rescaled = ((np.array(screen_coord) * self.__zoom) / np.array(self.__screen_size)) * np.array(self.__sim_bounds)
        translated_x = rescaled[0].item(0) - self.__sim_bounds[0] / 2
        translated_y = -rescaled[1].item(0) + self.__sim_bounds[1] / 2
        return np.array([translated_x, translated_y])

    def __sim_2_screen_scale(self, length: float):
        return int(((length * self.__zoom) / self.__sim_bounds[0]) * self.__screen_size[0])
