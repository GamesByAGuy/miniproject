from settings import comms
import pygame


class Map:
    def __init__(self):
        self.wall = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.cell_size = 60

        self.wall_coordinates = []
        for row_num, row in enumerate(self.wall):
            for col_num, column in enumerate(row):
                if column == 1:
                    self.wall_coordinates.append((col_num * self.cell_size, row_num * self.cell_size))

    def is_wall(self, x, y):
        if (int(x), int(y)) in self.wall_coordinates:
            return True
        return False

    def draw(self):
        for x, y in self.wall_coordinates:
            pygame.draw.rect(comms.screen, (0, 255, 0), (x, y, 60, 60), 1)
