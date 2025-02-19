import math
import pygame
from settings import comms


class Ray:
    def __init__(self, depth, character, world_map):
        self.depth = depth
        self.character = character
        self.map = world_map

    def check_horizontal_collision(self, sin, cos, tan):
        """returns the coordinate offsets and hypotenuse of the wall that is hit by the ray horizontally."""
        # check horizontal intersections inside the cell player is in.
        # sin > 0, pointing down. else, up.
        if sin > 0:
            y = self.map.cell_size - (self.character.y % self.map.cell_size)
            dy = self.map.cell_size
        else:
            y = -(self.character.y % self.map.cell_size) - 1e-6
            dy = -self.map.cell_size

        x = y / tan
        dx = dy / tan

        # increment until wall hit.
        # also, calculate the grid position of the tile being hit.
        for _ in range(self.depth):
            if self.map.is_wall(((self.character.x + x) // self.map.cell_size) * self.map.cell_size,
                                ((self.character.y + y) // self.map.cell_size) * self.map.cell_size):
                break
            x += dx
            y += dy

        hyp = math.hypot(x, y)

        return x, y, hyp

    def check_vertical_collision(self, sin, cos, tan):
        # check vertical intersections for the same
        # cos > 0, pointing right. else, left
        if cos > 0:
            x = self.map.cell_size - (self.character.x % self.map.cell_size)
            dx = self.map.cell_size
        else:
            x = -(self.character.x % self.map.cell_size) - 1e-6
            dx = -self.map.cell_size

        y = x * tan
        dy = dx * tan

        # increment until wall hit.
        for _ in range(self.depth):
            if self.map.is_wall(((self.character.x + x) // self.map.cell_size) * self.map.cell_size,
                                ((self.character.y + y) // self.map.cell_size) * self.map.cell_size):
                break
            x += dx
            y += dy

        hyp = math.hypot(x, y)

        return x, y, hyp

    def update(self, angle):
        sin = math.sin(angle)
        cos = math.cos(angle)
        tan = math.tan(angle)

        # get the collision points, and choose the one with the smallest hypotenuse.
        x_hor, y_hor, hyp_hor = self.check_horizontal_collision(sin, cos, tan)
        x_vert, y_vert, hyp_vert = self.check_vertical_collision(sin, cos, tan)

        if hyp_hor < hyp_vert:
            x, y = self.character.x + x_hor, self.character.y + y_hor
        else:
            x, y = self.character.x + x_vert, self.character.y + y_vert

        pygame.draw.line(comms.screen, (255, 255, 0), self.character.get_position(),
                         (x, y), 2)


class RayCaster:
    def __init__(self, character, world):
        self.character = character
        self.world = world

        self.fov = math.pi / 3
        self.half_fov = self.fov / 2
        self.num_of_rays = 150
        self.depth = 100

        self.ray = Ray(self.depth, character, world)

    def update(self):
        current_angle = self.character.angle - self.half_fov + 1e-6

        for _ in range(self.num_of_rays):
            self.ray.update(current_angle)
            current_angle += self.fov / self.num_of_rays
