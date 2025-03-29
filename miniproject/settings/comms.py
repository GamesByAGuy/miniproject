import pygame

# stuff used for regular game stuff
clock = pygame.time.Clock()
screen = pygame.Surface((960, 540))
display = pygame.display.set_mode((960, 540), pygame.HWSURFACE)

# game objects used
current_camera = None
renderer = None
