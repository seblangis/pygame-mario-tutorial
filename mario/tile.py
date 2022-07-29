import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, position: tuple[int, int], size: int):
        super().__init__()

        self.image = pygame.surface.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=position)

    def update(self, x_shift):
        self.rect.x += x_shift
