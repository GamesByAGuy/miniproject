import pygame
import math
from settings import comms


class Player:
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

    def draw(self):
        pygame.draw.circle(comms.screen, (255, 0, 0), (self.x, self.y), self.radius)

    def get_position(self):
        return self.x, self.y

    def map_pos(self):
        return int(self.x // 60), int(self.y // 60)

    def check_wall(self, x, y):
        return ((((self.x + x) // self.tilemap.cell_size) * self.tilemap.cell_size,
                ((self.y + y) // self.tilemap.cell_size) * self.tilemap.cell_size)
                not in self.tilemap.wall_coordinates)

    def get_wall(self, x, y):
        return ((self.x + x) // self.tilemap.cell_size * self.tilemap.cell_size,
                (self.y + y) // self.tilemap.cell_size * self.tilemap.cell_size)

    def check_collision(self, dx, dy):
        if self.check_wall(int(dx * self.radius), 0):
            self.x += dx
        if self.check_wall(0, int(dy * self.radius)):
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

    def update(self):
        key = pygame.key.get_pressed()
        dx, dy = 0, 0
        sin, cos = math.sin(self.angle), math.cos(self.angle)
        speed_sin, speed_cos = self.speed * sin, self.speed * cos

        if key[pygame.K_e]:
            self.angle = 0

        if key[pygame.K_w]:
            dx = speed_cos
            dy = speed_sin
        elif key[pygame.K_s]:
            dx = -speed_cos
            dy = -speed_sin

        if key[pygame.K_a]:
            dx = speed_sin
            dy = -speed_cos
        elif key[pygame.K_d]:
            dx = -speed_sin
            dy = speed_cos

        rel_x, rel_y = self.get_mouse_movement()

        self.pitch = max(min(self.pitch + (rel_y * 0.002), math.pi / 2), -math.pi / 2)

        self.check_collision(dx, dy)

        self.angle += rel_x * 0.002

        self.angle %= math.tau

        self.draw()
        pygame.draw.circle(comms.screen, (0, 255, 255), (self.x + self.radius, self.y), 3)
