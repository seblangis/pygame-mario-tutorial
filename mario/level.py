import pygame

from mario import settings
from mario.player import Player
from mario.tile import Tile


class Level:

    def __init__(self, level_data, surface):

        # level setup
        self.display_surface = surface
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
        for y, row in enumerate(layout):
            for x, col in enumerate(row):
                if col == ' ':
                    continue

                if col == 'X':
                    item = Tile((x * settings.tile_size, y * settings.tile_size), settings.tile_size)
                    self.tiles.add(item)
                if col == 'P':
                    item = Player((x * settings.tile_size, y * settings.tile_size))
                    self.player.add(item)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < settings.screen_scroll_limit and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x >= settings.screen_width - settings.screen_scroll_limit and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def run(self):
        self.player.update()
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.scroll_x()
