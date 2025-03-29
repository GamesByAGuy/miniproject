import pygame
import math
from settings import comms, data
from tools.sound import PositionalSound


class Sprite:
    def __init__(self, x, y, z, world, character, camera, image_list):
        if image_list is None:
            image_list = []
        self.world = world
        self.character = character
        self.camera = camera
        self.images = image_list
        self.x = x
        self.y = y
        self.z = z

        self.angle = 0
        self.rect = self.images[0].get_rect()

    def update(self):
        dx, dy = self.x - self.character.x, self.y - self.character.y
        theta = math.atan2(dy, dx)

        delta = theta - self.character.angle
        if (dx > 0 and self.character.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        angle = (math.radians(self.angle) - theta + math.pi) % (2 * math.pi)

        delta_rays = delta / (comms.current_camera.fov / comms.current_camera.num_of_rays)
        screen_x = (((comms.current_camera.num_of_rays / 2) + delta_rays) *
                    (comms.display.get_width() / comms.current_camera.num_of_rays))

        dist = math.hypot(dx, dy)
        dist *= math.cos(delta)

        if (-(self.images[0].get_width() // 2) < screen_x < (
                comms.display.get_width() + self.images[0].get_width() // 2)
                and dist > 20):
            proj = (((comms.display.get_width() / 2) /
                     math.tan(comms.current_camera.fov / 2)) *
                    self.world.cell_size) / dist

            proj_w, proj_h = proj * (self.images[0].get_width() / self.images[0].get_height()), proj

            image = pygame.transform.scale(
                self.images[int(math.degrees(angle) // (360 // len(self.images)))],
                (proj_w, proj_h)
            )

            half_width = proj_w // 2
            pos = (screen_x - half_width,
                   comms.current_camera.horizon - proj_h // 2 + (self.z * proj_h / self.world.cell_size)
            )
            self.rect.update(pos[0], pos[1], proj_w, proj_h)

            data.add_texture_slices(image, pos, dist)


class Object:
    def __init__(self, world, character, camera):
        self.x = 0
        self.y = 0
        self.z = 0
        self.world = world
        self.character = character
        self.camera = camera

        self.sprite = None
        self.angle = 0
        self.radius = 15

        self.rect = pygame.Rect(
            self.x - ((self.radius * math.sqrt(2)) // 2),
            self.y - ((self.radius * math.sqrt(2)) // 2),
            self.radius * math.sqrt(2),
            self.radius * math.sqrt(2)
        )

    def debug(self):
        pygame.draw.circle(comms.screen, (0, 255, 0), (self.x, self.y), self.radius)
        pygame.draw.rect(comms.screen, (255, 255, 255), self.rect, 2)

    def update_rect(self):
        self.rect.update(self.x - ((self.radius * math.sqrt(2)) // 2),
                         self.y - ((self.radius * math.sqrt(2)) // 2),
                         self.radius * math.sqrt(2),
                         self.radius * math.sqrt(2)
        )

    def update(self):
        pass


class TestObject(Object):
    def __init__(self, world, character, camera):
        super().__init__(world, character, camera)
        self.x = 200
        self.y = 400
        self.z = 10
        self.sound = PositionalSound("testassets/test.ogg", self, character)
        self.sprite = Sprite(self.x, self.y, self.z, world, character, camera, [
            data.get_texture("testassets/candlebra1.png"),
            data.get_texture("testassets/candlebra2.png"),
            data.get_texture("testassets/candlebra3.png"),
            data.get_texture("testassets/candlebra4.png"),
            data.get_texture("testassets/candlebra5.png"),
            data.get_texture("testassets/candlebra6.png"),
            data.get_texture("testassets/candlebra7.png"),
            data.get_texture("testassets/candlebra8.png")
        ])

    def update(self):
        self.sprite.update()
        self.update_rect()
        self.sound.play()
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.z = self.z
        self.debug()
