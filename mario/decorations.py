import random

import pygame

from mario import settings
from mario.support import import_folder
from mario.tile import AnimatedTile, BackgroundTile


class Sky:

    def __init__(self, horizon):
        self.top = pygame.image.load('graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('graphics/decoration/sky/sky_middle.png').convert()

        self.horizon = horizon

        # stretch
        self.top = pygame.transform.scale(self.top, (settings.screen_width, settings.tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (settings.screen_width, settings.tile_size))
        self.middle = pygame.transform.scale(self.middle, (settings.screen_width, settings.tile_size))

    def draw(self, surface):
        for row in range(settings.vertical_tile_number):
            y = row * settings.tile_size

            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))


class Water:

    def __init__(self, top, level_width):
        self.level_width = level_width

        water_start = -settings.screen_width
        water_tile_width = 192
        tile_x_amount = (level_width + settings.screen_width * 2) // water_tile_width
        self.water_sprites = pygame.sprite.Group()
        tiles = import_folder('graphics/decoration/water')

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile((x, y), tiles)
            self.water_sprites.add(sprite)


class Clouds:

    def __init__(self, horizon, level_width, cloud_count):
        cloud_surface_list = import_folder('graphics/decoration/clouds')

        min_x = -settings.screen_width
        max_x = level_width + settings.screen_width * 2
        min_y = 0
        max_y = horizon * settings.tile_size - cloud_surface_list[0].get_rect().height

        self.cloud_sprites = pygame.sprite.Group()

        for _ in range(cloud_count):
            cloud = random.choice(cloud_surface_list)
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)

            sprite = BackgroundTile((x, y), cloud, random.randint(2, 3))
            self.cloud_sprites.add(sprite)
