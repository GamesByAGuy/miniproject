from settings import comms, data
import pygame


class Renderer:
    def __init__(self):
        self.shade_distance = 0.7

    def render(self):
        sorted_list = sorted(data.renderable_textures, key=lambda t: t[2], reverse=True)

        for texture, pos, depth in sorted_list:
            shade = pygame.Surface(texture.get_size(), pygame.SRCALPHA)
            alpha = max(0, min(245, int(depth * self.shade_distance)))
            shade.fill((0, 0, 0, alpha))
            texture.blit(shade, (0, 0))
            comms.display.blit(texture, pos)

        data.renderable_textures.clear()
