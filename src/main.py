import pygame
import numpy as np

from Snake import Snake
from GUI import PygameGUI

if __name__ == '__main__':

    num_circles = 100
    sizes = list(np.linspace(0, 3, num_circles))[::-1]
    snake = Snake(head_start=np.array([0, 0]), colour='blue-sky', num_circles=num_circles, sizes=sizes)

    gui = PygameGUI(bg_colour='blue-grey', screen_size=[1_000, 1_000], sim_bounds=np.array([200, 200]), fps=22)

    running = True
    while running:

        gui.tick()
        gui.draw_bg()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_position = gui.screen_2_sim_map_fn(pygame.mouse.get_pos())

        snake.move_towards(mouse_position, avoid=False)

        gui.draw_snake(snake, should_draw_circles=False)

        pygame.display.flip()

    pygame.quit()
