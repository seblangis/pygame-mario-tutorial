import pygame

from mario import settings
from mario.tile import Tile


class Level:

    def __init__(self, level_data, surface):

        # level setup
        self.display_surface = surface
        self.tiles = pygame.sprite.Group()
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
        for y, row in enumerate(layout):
            for x, col in enumerate(row):
                if col == ' ':
                    continue

                self.tiles.add(
                    Tile((x * settings.tile_size, y * settings.tile_size), settings.tile_size)
                )

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
