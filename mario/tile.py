import pygame
from pygame.surface import Surface


class Tile(pygame.sprite.Sprite):

    def __init__(self, position: tuple[int, int], size):
        super().__init__()

        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=position)

    def update(self, x_shift):
        self.rect.x += x_shift


class StaticTile(Tile):

    def __init__(self, position: tuple[int, int], image: Surface):
        super().__init__(position, image.get_rect().width)
        self.image = image
