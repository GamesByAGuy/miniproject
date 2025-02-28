import pygame
import math
from settings import comms


class Character:
    def __init__(self, tilemap):
        self.tilemap = tilemap

        self.x = 350
        self.y = 200
        self.z = 0

        self.speed = 2
        self.angle = 0
        self.pitch = 0
        self.radius = 15

        self.mouse_border_x = ((comms.display.get_width() // 2) - 200, (comms.display.get_width() // 2) + 200)
        self.mouse_border_y = ((comms.display.get_height() // 2) - 200, (comms.display.get_height() // 2) + 200)
        self.rel_x = 0
        self.rel_y = 0
        self.max_rel = 40

    def check_collision(self, dx, dy):
        if not self.tilemap.check_wall(int(self.x + dx * self.radius), self.y):
            self.x += dx
        if not self.tilemap.check_wall(self.x, int(self.y + dy * self.radius)):
            self.y += dy

    def get_mouse_movement(self):
        mx, my = pygame.mouse.get_pos()
        if ((mx < self.mouse_border_x[0] or mx > self.mouse_border_x[1]) or
                (my < self.mouse_border_y[0] or my > self.mouse_border_y[1])):
            pygame.mouse.set_pos(comms.display.get_width() // 2, comms.display.get_height() // 2)

        rel_x, rel_y = pygame.mouse.get_rel()

        self.rel_x = rel_x
        self.rel_x = max(-self.max_rel, min(self.max_rel, self.rel_x))

        self.rel_y = rel_y
        self.rel_y = max(-self.max_rel, min(self.max_rel, self.rel_y))

        return self.rel_x, self.rel_y
