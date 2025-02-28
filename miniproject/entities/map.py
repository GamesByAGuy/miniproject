from settings import comms, data
import pygame


class Map:
    def __init__(self):
        self.wall = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.wall_textures = {
            1: data.get_texture("testassets/1.png"),
            2: data.get_texture("testassets/2.png")
        }
        self.floor_texture = data.get_texture("testassets/2.png")
        self.cell_size = 60

        self.wall_coordinates = []
        for row_num, row in enumerate(self.wall):
            for col_num, column in enumerate(row):
                if column != 0:
                    self.wall_coordinates.append((col_num * self.cell_size, row_num * self.cell_size))

    def is_wall(self, x, y):
        return ((x // self.cell_size) * self.cell_size,
                (y // self.cell_size) * self.cell_size) in self.wall_coordinates

    def get_wall_index(self, x, y):
        return self.wall[
            min(max(int(y // self.cell_size), 0), len(self.wall) - 1)
        ][
            min(max(int(x // self.cell_size), 0), len(self.wall[0]) - 1)
        ]

    def get_wall_texture(self, x, y):
        return self.wall_textures[self.get_wall_index(x, y)]

    def draw(self):
        for x, y in self.wall_coordinates:
            pygame.draw.rect(comms.screen, (0, 255, 0), (x, y, 60, 60), 1)
