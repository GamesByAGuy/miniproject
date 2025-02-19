import pygame
import math
from settings import comms


class Player:
    def __init__(self):
        self.x = 100
        self.y = 100

        self.speed = 10
        self.angle = 0

    def draw(self):
        pygame.draw.circle(comms.screen, (255, 0, 0), (self.x, self.y), 15)

    def get_position(self):
        return self.x, self.y

    def map_pos(self):
        return int(self.x // 60), int(self.y // 60)

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

        self.x += dx
        self.y += dy

        if key[pygame.K_LEFT]:
            self.angle += -0.05
        elif key[pygame.K_RIGHT]:
            self.angle += 0.05

        self.angle %= math.tau

        self.draw()
