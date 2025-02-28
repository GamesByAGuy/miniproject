import pygame
import math
from settings import comms


class Player:
    def __init__(self, tilemap):
        self.tilemap = tilemap

        self.x = 350
        self.y = 200
        self.z = 0

        self.velocity = pygame.math.Vector2(0, 0)

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

    def check_collision(self):
        if not self.tilemap.is_wall(int(self.x + self.velocity.x * self.radius), self.y):
            self.x += self.velocity.x
        if not self.tilemap.is_wall(self.x, int(self.y + self.velocity.y * self.radius)):
            self.y += self.velocity.y

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

    def handle_input(self, key, forward=pygame.K_w, backward=pygame.K_s, left=pygame.K_a, right=pygame.K_d):
        sin, cos = math.sin(self.angle), math.cos(self.angle)
        speed_sin, speed_cos = self.speed * sin, self.speed * cos

        self.velocity.x = 0
        self.velocity.y = 0

        if key[forward]:
            self.velocity.x = speed_cos
            self.velocity.y = speed_sin
        elif key[backward]:
            self.velocity.x = -speed_cos
            self.velocity.y = -speed_sin

        if key[left]:
            self.velocity.x = speed_sin
            self.velocity.y = -speed_cos
        elif key[right]:
            self.velocity.x = -speed_sin
            self.velocity.y = speed_cos

    def update(self):
        key = pygame.key.get_pressed()

        self.handle_input(key)

        if key[pygame.K_g]:
            self.z += 0.1
        elif key[pygame.K_b]:
            self.z -= 0.1

        rel_x, rel_y = self.get_mouse_movement()

        self.pitch = max(min(self.pitch + (rel_y * 0.002), math.pi / 2), -math.pi / 2)
        self.angle += rel_x * 0.002
        self.angle %= math.tau

        self.z = min(max(self.z, 1), 2)

        self.check_collision()

        self.draw()
