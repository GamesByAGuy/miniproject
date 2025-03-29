import pygame
from settings import comms
from entities.player import Player
from entities.object import TestObject
from entities.map import Map
from tools.camera import Camera
from tools.raycaster import Ray
from tools.renderer import Renderer
pygame.init()


class Manager:
    # performs tasks in the game engine such as state switching. final code is run here.
    def __init__(self):
        self.state = ""
        self.map = Map()
        self.player = Player(self.map)
        self.raycaster = Camera(character=self.player, world=self.map)
        self.renderer = Renderer()
        self.object = TestObject(self.map, self.player, self.raycaster)
        self.ray = Ray(50, self.player, self.map, 0, [self.object], (255, 255, 255))

        pygame.mouse.set_visible(False)

    def update(self):
        while True:
            comms.screen.fill((0, 0, 0))
            comms.display.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.map.draw()
            self.player.update()
            self.object.update()
            comms.current_camera.update()
            self.ray.update()
            self.renderer.render()
            comms.display.blit(pygame.transform.scale_by(comms.screen, (0.25, 0.25)), (5, 5))
            col_obj = self.ray.get_collided_object()
            if col_obj is None:
                pygame.draw.circle(comms.display, (255, 255, 255),
                               (comms.display.get_width() // 2, comms.display.get_height() // 2), 5)
            else:
                pygame.draw.circle(comms.display, (255, 0, 0),
                                   (comms.display.get_width() // 2, comms.display.get_height() // 2), 5)
            # comms.display.blit(comms.screen, (0, 0))
            pygame.display.update()
            comms.clock.tick(30)
            pygame.display.set_caption(str(comms.clock.get_fps()))


if __name__ == "__main__":
    Manager().update()
else:
    print("nope")
