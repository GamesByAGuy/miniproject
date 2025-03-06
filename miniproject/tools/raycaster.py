import math
import pygame
import numpy as np
from settings import comms, data


class Ray:
    def __init__(self, depth, character, world_map, offset=0):
        self.depth = depth
        self.character = character
        self.map = world_map
        self.offset = offset

        self.horizontal_collisions = []
        self.vertical_collisions = []

        self.angle = self.character.angle + self.offset + 1e-6

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
            hyp = math.hypot(x, y)
            self.horizontal_collisions.append((self.character.x + x, self.character.y + y, hyp, "h"))
            if self.map.is_wall(self.character.x + x, self.character.y + y):
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
            hyp = math.hypot(x, y)
            self.vertical_collisions.append((self.character.x + x, self.character.y + y, hyp, "v"))
            if self.map.is_wall(self.character.x + x, self.character.y + y):
                break
            x += dx
            y += dy

        hyp = math.hypot(x, y)

        return x, y, hyp

    def update(self):
        self.angle = self.character.angle + self.offset + 1e-6
        sin = math.sin(self.angle)
        cos = math.cos(self.angle)
        tan = math.tan(self.angle)

        # get the collision points, and choose the one with the smallest hypotenuse.
        x_hor, y_hor, hyp_hor = self.check_horizontal_collision(sin, cos, tan)
        x_vert, y_vert, hyp_vert = self.check_vertical_collision(sin, cos, tan)

        if hyp_hor < hyp_vert:
            x, y = self.character.x + x_hor, self.character.y + y_hor
            hyp = hyp_hor
            offset = (x % self.map.cell_size) / self.map.cell_size
            collision_list = self.horizontal_collisions
        else:
            x, y = self.character.x + x_vert, self.character.y + y_vert
            hyp = hyp_vert
            offset = (y % self.map.cell_size) / self.map.cell_size
            collision_list = self.vertical_collisions

        self.vertical_collisions = []
        self.horizontal_collisions = []

        pygame.draw.line(comms.screen, (255, 255, 0), self.character.get_position(),
                         (x, y), 2)

        return x, y, hyp, offset, collision_list


class RayCaster:
    def __init__(self, character, world):
        self.character = character
        self.world = world

        # ray casting
        self.fov = math.pi / 3
        self.half_fov = self.fov / 2
        self.num_of_rays = comms.display.get_width() // 6
        self.depth = 20
        self.horizon = comms.display.get_height() // 2

        # pseudo 3d projection
        self.screen_distance = comms.display.get_width() / math.tan(self.half_fov)
        self.scale = comms.display.get_width() / self.num_of_rays

        self.rays = []
        current_angle = self.character.angle - self.half_fov
        for ray in range(self.num_of_rays):
            self.rays.append(Ray(self.depth, character, world, offset=current_angle))
            current_angle += self.fov / self.num_of_rays

    def render_walls(self, offset, proj_height, horizon, ray_num, texture):
        wall_column = texture.subsurface(
            offset * (texture.get_width() - self.scale), 0, self.scale, texture.get_height()
        )

        wall_column = pygame.transform.scale(wall_column, (self.scale, proj_height))
        wall_pos = (ray_num * self.scale, (horizon - proj_height // 2) * self.character.z)

        return wall_column, wall_pos

    def render_floor(self, horizon, ray, ray_num, collision_list):
        pygame.draw.rect(comms.display, (20, 20, 20), (0, horizon,
                                                          comms.display.get_width(),
                                                          comms.display.get_height() - horizon))

    def render_ceiling(self, horizon):
        pygame.draw.rect(comms.display, (40, 40, 40), (0, 0,
                                                      comms.display.get_width(),
                                                      horizon))

    def update(self):
        horizon = (comms.display.get_height() // 2) - int(math.tan(self.character.pitch) * self.screen_distance)
        self.horizon = horizon

        for ray_num, ray in enumerate(self.rays):
            x, y, depth, offset, collision_list = ray.update()

            depth *= math.cos(self.character.angle - ray.angle)
            if depth < 10:
                depth = 10

            proj_height = ((self.screen_distance * self.world.cell_size / 2) / (depth + 1e-6))
            brightness = max(255 * (0.9 ** (depth * 0.02)), 30)
            color = (int(brightness), int(brightness), int(brightness))

            wall_column, wall_pos = self.render_walls(
                offset,
                proj_height,
                horizon,
                ray_num,
                self.world.get_wall_texture(x, y)
            )
            self.render_floor(horizon, ray, ray_num, collision_list)
            self.render_ceiling(horizon)
            data.add_texture_slices(wall_column, wall_pos, depth)
