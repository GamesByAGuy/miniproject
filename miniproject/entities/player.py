import pygame
import math
from entities.character import Character


class Player(Character):
    def __init__(self, tilemap):
        super().__init__(tilemap)
        self.x = 300
        self.y = 400
        self.tilemap = tilemap

    def update(self):
        key = pygame.key.get_pressed()

        self.handle_input(key)

        if key[pygame.K_g]:
            self.z += 0.01
        elif key[pygame.K_b]:
            self.z -= 0.01

        rel_x, rel_y = self.get_mouse_movement()

        self.pitch = max(min(self.pitch + (rel_y * 0.004), math.pi / 10), -math.pi / 10)
        self.angle += rel_x * 0.004
        self.angle %= math.tau

        # self.z = min(max(self.z, 1), 2)

        self.check_collision()

        self.draw()
