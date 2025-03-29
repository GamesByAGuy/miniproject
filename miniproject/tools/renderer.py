from settings import comms, data
import pygame


class Renderer:
    def __init__(self):
        self.shade_distance = 500
        self.shaded_textures = {}

    def get_shaded_texture(self, texture, distance):
        shade_factor = max(0.2, 1 - (distance / self.shade_distance))
        texture.fill((shade_factor * 255, shade_factor * 255, shade_factor * 255), special_flags=pygame.BLEND_MULT)

    def render(self):
        sorted_list = sorted(data.renderable_textures, key=lambda t: t[2], reverse=True)

        for texture, pos, depth in sorted_list:
            self.get_shaded_texture(texture, depth)
            comms.display.blit(texture, pos)

        data.renderable_textures.clear()
