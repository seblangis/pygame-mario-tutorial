import pygame

from mario import settings
from mario.particle import ParticleEffect
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
        self.current_x = 0
        self.player_was_on_ground = True

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()

    def create_particles(self, position, particle_type):
        if self.dust_sprite.sprites():
            return

        particle_effect = ParticleEffect(position, particle_type)
        self.dust_sprite.add(particle_effect)

    def setup_level(self, layout):
        for y, row in enumerate(layout):
            for x, col in enumerate(row):
                if col == ' ':
                    continue

                if col == 'X':
                    item = Tile((x * settings.tile_size, y * settings.tile_size), settings.tile_size)
                    self.tiles.add(item)
                if col == 'P':
                    item = Player((x * settings.tile_size, y * settings.tile_size), self.display_surface, self.create_particles)
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

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        # if player.direction.x != self.current_x:
        #     player.on_right = False
        #     player.on_left = False

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

        if not self.player_was_on_ground and player.on_ground:
            self.create_particles(self.player.sprite.rect.midbottom, 'land')
        self.player_was_on_ground = player.on_ground

    def run(self):

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # dust
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
