from settings import comms
import pygame


class Renderer:
    def render(self, objects_to_render):
        for depth, image, pos in objects_to_render:
            comms.display.blit(image, pos)
