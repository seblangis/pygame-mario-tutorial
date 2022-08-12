import random

import pygame
from pygame.surface import Surface

from mario.settings import tile_size
from mario.support import import_folder


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


class CrateTile(StaticTile):

    def __init__(self, position: tuple[int, int], surface: Surface):
        offset = pygame.math.Vector2(
            0,
            tile_size - surface.get_rect().height,
        )

        super().__init__(position + offset, surface)


class AnimatedTile(Tile):

    def __init__(self, position: tuple[int, int], frames: list[Surface]):
        super().__init__(position, frames[0].get_rect().width)

        self.frames = frames
        self.image = frames[0]
        self.current_frame = 0
        self.animation_speed = 0.15

    def update(self, x_shift):
        super().update(x_shift)
        self.animate()

    def animate(self):
        self.current_frame += self.animation_speed
        self.current_frame %= len(self.frames)
        self.image = self.frames[int(self.current_frame)]


class CenteredAnimatedTile(AnimatedTile):
    def __init__(self, position: tuple[int, int], frames: list[Surface]):
        offset = pygame.math.Vector2(
            (tile_size - frames[0].get_rect().width) / 2,
            (tile_size - frames[0].get_rect().height) / 2,
        )

        super().__init__(position + offset, frames)


class CoinTile(CenteredAnimatedTile):
    pass


class BasedAnimatedTile(AnimatedTile):
    def __init__(self, position: tuple[int, int], frames: list[Surface]):
        offset = pygame.math.Vector2(
            0,
            tile_size - frames[0].get_rect().height,
        )

        super().__init__(position + offset, frames)


class PalmTile(BasedAnimatedTile):
    pass


class EnemyTile(BasedAnimatedTile):

    def __init__(self, position: tuple[int, int], frames: list[Surface]):
        super().__init__(position, frames)

        self.speed = random.randint(3, 5)

    def move(self):
        self.rect.x += self.speed

    def reverse(self):
        self.speed *= -1

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, shift):
        super().update(shift)
        self.reverse_image()
        self.move()


class ConstraintTile(StaticTile):
    pass


class Goal(StaticTile):
    pass
