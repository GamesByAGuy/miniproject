import pygame
import math
from settings import comms, data


class Object:
    def __init__(self, world, character, camera):
        self.world = world
        self.character = character
        self.camera = camera
        self.images = [
            pygame.image.load("testassets/candlebra1.png").convert_alpha(),
            pygame.image.load("testassets/candlebra2.png").convert_alpha(),
            pygame.image.load("testassets/candlebra3.png").convert_alpha(),
            pygame.image.load("testassets/candlebra4.png").convert_alpha(),
            pygame.image.load("testassets/candlebra5.png").convert_alpha(),
            pygame.image.load("testassets/candlebra6.png").convert_alpha(),
            pygame.image.load("testassets/candlebra7.png").convert_alpha(),
            pygame.image.load("testassets/candlebra8.png").convert_alpha(),
        ]

        self.x, self.y = 13 * self.world.cell_size, 5 * self.world.cell_size
        self.angle = 0

    def update(self):
        dx, dy = self.x - self.character.x, self.y - self.character.y
        theta = math.atan2(dy, dx)

        delta = theta - self.character.angle
        if (dx > 0 and self.character.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        angle = (math.radians(self.angle) - theta + math.pi) % (2 * math.pi)

        delta_rays = delta / ((math.pi / 3) / (comms.display.get_width() // 6))
        screen_x = ((((comms.display.get_width() // 6) / 2) + delta_rays) *
                    (comms.display.get_width() / (comms.display.get_width() // 6)))

        dist = math.hypot(dx, dy)
        dist *= math.cos(delta)

        if (-(self.images[0].get_width() // 2) < screen_x < (comms.display.get_width() + self.images[0].get_width() // 2)
                and dist > 10):
            proj = (((comms.display.get_width() / 2) / math.tan((math.pi / 3) / 2)) * 60) / dist
            proj_w, proj_h = proj * (self.images[0].get_width() / self.images[0].get_height()), proj

            image = pygame.transform.scale(self.images[int(math.degrees(angle) // 45)], (proj_w, proj_h))

            half_width = proj_w // 2
            pos = (screen_x - half_width, self.camera.raycaster.horizon - proj_h // 2)

            data.add_texture_slices(image, pos, dist)
