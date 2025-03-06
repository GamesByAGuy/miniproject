import pygame
from settings import comms
from entities.player import Player
from entities.object import Object
from entities.map import Map
from tools.camera import Camera
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
        self.object = Object(self.map, self.player, self.raycaster)

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
            self.raycaster.update()
            self.object.update()
            self.renderer.render()
            comms.display.blit(pygame.transform.scale_by(comms.screen, (0.25, 0.25)), (5, 5))
            pygame.display.update()
            comms.clock.tick(60)
            pygame.display.set_caption(str(comms.clock.get_fps()))


if __name__ == "__main__":
    Manager().update()
else:
    print("nope")
