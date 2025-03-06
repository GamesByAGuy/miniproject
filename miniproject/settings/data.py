import pygame

# lists for stuff like collision, rendering, etc
renderable_textures = []
collidables = []

# dictionary to store every single texture used in the game
textures = {}

err_texture = pygame.image.load("testassets/err.png").convert_alpha()


# function to add image to dictionary
def get_texture(image_path):
    try:
        if image_path not in textures:
            texture = pygame.image.load(image_path).convert_alpha()
            textures[image_path] = texture
            return texture

        return textures[image_path]
    except Exception as e:
        raise Exception("file name error: bruh i asked for an image path.")


# function to add wall slices and their respective positions in the directory
def add_texture_slices(texture_slice, position, depth):
    renderable_textures.append((texture_slice, position, depth))
