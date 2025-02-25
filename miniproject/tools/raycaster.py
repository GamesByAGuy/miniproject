import math
import pygame
from settings import comms


class Ray:
    def __init__(self, depth, character, world_map, offset=0):
        self.depth = depth
        self.character = character
        self.map = world_map
        self.offset = offset

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
            position_x = ((self.character.x + x) // self.map.cell_size) * self.map.cell_size
            position_y = ((self.character.y + y) // self.map.cell_size) * self.map.cell_size
            if self.map.is_wall(position_x, position_y):
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
            position_x = ((self.character.x + x) // self.map.cell_size) * self.map.cell_size
            position_y = ((self.character.y + y) // self.map.cell_size) * self.map.cell_size
            if self.map.is_wall(position_x, position_y):
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
        else:
            x, y = self.character.x + x_vert, self.character.y + y_vert
            hyp = hyp_vert
            offset = (y % self.map.cell_size) / self.map.cell_size

        pygame.draw.line(comms.screen, (255, 255, 0), self.character.get_position(),
                         (x, y), 2)

        return x, y, hyp, offset


class RayCaster:
    def __init__(self, character, world):
        self.character = character
        self.world = world

        # render
        self.test = pygame.image.load("testassets/1.png").convert_alpha()

        # ray casting
        self.fov = math.pi / 3
        self.half_fov = self.fov / 2
        self.num_of_rays = comms.display.get_width() // 4
        self.depth = 80

        # pseudo 3d projection
        self.screen_distance = comms.display.get_width() / math.tan(self.half_fov)
        self.scale = comms.display.get_width() / self.num_of_rays

        self.rays = []
        current_angle = self.character.angle - self.half_fov
        for ray in range(self.num_of_rays):
            self.rays.append(Ray(self.depth, character, world, offset=current_angle))
            current_angle += self.fov / self.num_of_rays

    def render_walls(self, offset, proj_height, horizon, ray_num):
        # if proj_height < comms.display.get_height():
        wall_column = self.test.subsurface(
            offset * (self.test.get_width() - self.scale), 0, self.scale, self.test.get_height()
        )

        wall_column = pygame.transform.scale(wall_column, (self.scale, proj_height))
        wall_pos = (ray_num * self.scale, horizon - proj_height // 2)
        # else:
        #     texture_height = self.test.get_height() * (comms.display.get_height() / proj_height)
        #     vertical_distance = max(0, min(horizon, self.test.get_height() - texture_height))
        #     vertical_position = max(horizon - proj_height // 2, horizon - texture_height)
        #     # print(vertical_position)
        #     wall_column = self.test.subsurface(
        #         offset * (self.test.get_width() - self.scale),
        #         vertical_distance,
        #         self.scale, texture_height
        #     )
        #     wall_column = pygame.transform.scale(wall_column, (self.scale, comms.display.get_height()))
        #     wall_pos = (ray_num * self.scale, vertical_position)

        return wall_column, wall_pos

    def update(self):
        for ray_num, ray in enumerate(self.rays):
            x, y, depth, offset = ray.update()

            depth *= math.cos(self.character.angle - ray.angle)
            if depth < 10:
                depth = 10

            proj_height = ((self.screen_distance * self.world.cell_size / 2) / (depth + 1e-6))
            brightness = max(255 * (0.9 ** (depth * 0.02)), 30)
            color = (int(brightness), int(brightness), int(brightness))
            horizon = (comms.display.get_height() // 2) - int(math.tan(self.character.pitch) * self.screen_distance)

            pygame.draw.rect(comms.display, color,
                             (ray_num * self.scale, (horizon - proj_height // 2),
                              self.scale, proj_height))

            wall_column, wall_pos = self.render_walls(offset, proj_height, horizon, ray_num)
            comms.display.blit(wall_column, wall_pos)
            # pygame.draw.circle(comms.display, (255, 0, 0),
            #                    (ray_num * self.scale, (horizon - proj_height // 2)), 3)
