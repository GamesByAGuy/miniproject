from settings import comms, data
import pygame


class Map:
    def __init__(self):
        self.wall = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0, 1],
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
        self.ceiling_texture = data.get_texture("testassets/2.png")
        self.cell_size = 60

        self.wall_coordinates = []
        for row_num, row in enumerate(self.wall):
            for col_num, column in enumerate(row):
                if column != 0:
                    self.wall_coordinates.append((col_num * self.cell_size, row_num * self.cell_size))

    def is_wall(self, x, y):
        return ((x // self.cell_size) * self.cell_size,
                (y // self.cell_size) * self.cell_size) in self.wall_coordinates

    def is_character_in_cell(self, character_rect, ray_pos=(0, 0)):
        tile_rect = pygame.Rect(
            (ray_pos[0] // self.cell_size) * self.cell_size,
            (ray_pos[1] // self.cell_size) * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        return tile_rect.colliderect(character_rect)

    def draw_rect(self, x, y):
        tile_rect = pygame.Rect(
            (x // self.cell_size) * self.cell_size,
            (y // self.cell_size) * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(comms.screen, (255, 255, 255), tile_rect, 2)

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
