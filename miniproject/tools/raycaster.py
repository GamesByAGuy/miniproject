import math
import pygame
import numpy as np
from settings import comms, data


class Ray:
    def __init__(self, depth, character, world_map, offset=0, collision_objects=None, debug_color=(255, 255, 0)):
        self.depth = depth
        self.character = character
        self.map = world_map
        self.offset = offset
        self.collision_objects = collision_objects
        self.debug_color = debug_color

        self.horizontal_collisions = []
        self.vertical_collisions = []

        self.collided_object = None

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
        collided_object = None

        for _ in range(self.depth):
            hyp = math.hypot(x, y)
            self.horizontal_collisions.append((self.character.x + x, self.character.y + y, hyp, "h"))

            if self.map.is_wall(self.character.x + x, self.character.y + y):
                break

            if self.collision_objects is not None:
                break_loop = False
                for obj in self.collision_objects:
                    if self.map.is_character_in_cell(obj.rect, ray_pos=(self.character.x + x, self.character.y + y)):
                        for _ in range(self.map.cell_size):
                            if (obj.rect.collidepoint(self.character.x + x, self.character.y + y) and
                               obj.sprite.rect.collidepoint(comms.display.get_width() // 2, comms.display.get_height() // 2)):
                                collided_object = obj
                                break_loop = True
                                break

                            x += dx / self.map.cell_size
                            y += dy / self.map.cell_size

                if break_loop:
                    break

            x += dx
            y += dy

        hyp = math.hypot(x, y)

        return x, y, hyp, collided_object

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
        collided_object = None

        for _ in range(self.depth):
            hyp = math.hypot(x, y)
            self.vertical_collisions.append((self.character.x + x, self.character.y + y, hyp, "v"))

            if self.map.is_wall(self.character.x + x, self.character.y + y):
                break

            break_loop = False
            if self.collision_objects is not None:
                for obj in self.collision_objects:
                    if self.map.is_character_in_cell(obj.rect, ray_pos=(self.character.x + x, self.character.y + y)):
                        for _ in range(self.map.cell_size):
                            if (obj.rect.collidepoint(self.character.x + x, self.character.y + y) and
                               obj.sprite.rect.collidepoint(comms.display.get_width() // 2, comms.display.get_height() // 2)):
                                collided_object = obj
                                break_loop = True
                                break

                            x += dx / self.map.cell_size
                            y += dy / self.map.cell_size

            if break_loop:
                break

            x += dx
            y += dy

        hyp = math.hypot(x, y)

        return x, y, hyp, collided_object

    def get_collided_object(self):
        return self.collided_object

    def update(self):
        self.angle = self.character.angle + self.offset + 1e-6
        sin = math.sin(self.angle)
        cos = math.cos(self.angle)
        tan = math.tan(self.angle)

        # get the collision points, and choose the one with the smallest hypotenuse.
        x_hor, y_hor, hyp_hor, collided_object_hor = self.check_horizontal_collision(sin, cos, tan)
        x_vert, y_vert, hyp_vert, collided_object_vert = self.check_vertical_collision(sin, cos, tan)

        if hyp_hor < hyp_vert:
            x, y = self.character.x + x_hor, self.character.y + y_hor
            hyp = hyp_hor
            offset = (x % self.map.cell_size) / self.map.cell_size
            collision_list = self.horizontal_collisions
            collided_object = collided_object_hor
        else:
            x, y = self.character.x + x_vert, self.character.y + y_vert
            hyp = hyp_vert
            offset = (y % self.map.cell_size) / self.map.cell_size
            collision_list = self.vertical_collisions
            collided_object = collided_object_vert

        self.vertical_collisions = []
        self.horizontal_collisions = []

        # pygame.draw.line(comms.screen, self.debug_color, self.character.get_position(), (x, y), 2)
        self.collided_object = collided_object

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
            self.rays.append(Ray(self.depth, character, world, offset=current_angle, debug_color=(50, 50, 50)))
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
