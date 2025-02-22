from settings import comms
import pygame


class Renderer:
    def __init__(self):
        self.textures = {
            1: pygame.image.load("testassets/1.png")
        }

    def render(self, objects_to_render):
        for depth, image, pos in self.textures:
            comms.display.blit(image, pos)
