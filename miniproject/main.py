import pygame
from settings import comms
from entities.player import Player
from entities.map import Map
from tools.raycaster import RayCaster
pygame.init()


class Manager:
    # performs tasks in the game engine such as state switching. final code is run here.
    def __init__(self):
        self.state = ""
        self.player = Player()
        self.map = Map()
        self.raycaster = RayCaster(self.player, self.map)

    def update(self):
        while True:
            comms.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.map.draw()
            self.player.update()
            self.raycaster.update()
            pygame.display.update()
            comms.clock.tick(60)
            pygame.display.set_caption(str(comms.clock.get_fps()))


if __name__ == "__main__":
    Manager().update()
else:
    print("nope")
