import pygame.draw

from tools.raycaster import RayCaster
from settings import comms, data
import math


class Camera(RayCaster):
    def __init__(self, character=None, world=None):
        comms.current_camera = self

        self.x = 300
        self.y = 100
        self.z = 0

        self.angle = 0
        self.pitch = 0

        if character is None:
            super().__init__(self, world)
        else:
            super().__init__(character, world)

    def get_position(self):
        return self.x, self.y

    def update(self):
        horizon = (comms.display.get_height() // 2) - int(math.tan(self.character.pitch) * self.screen_distance)
        self.horizon = horizon

        for ray_num, ray in enumerate(self.rays):
            x, y, depth, offset, collision_list = ray.update()

            depth *= math.cos(self.character.angle - ray.angle)
            if depth < 20:
                depth = 20

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
