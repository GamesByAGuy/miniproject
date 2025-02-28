from settings import comms, data
import pygame


class Renderer:
    def __init__(self):
        self.test = 1

    def render(self):
        if data.renderable_textures:
            comms.display.blits(data.renderable_textures)

        data.renderable_textures.clear()
        self.test = 1
