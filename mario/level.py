import pygame

from mario import settings, game_data
from mario.particle import ParticleEffect
from mario.player import Player
from mario.support import import_csv_layout, import_cut_graphics, import_single_tile, import_folder
from mario.tile import StaticTile, CrateTile, PalmTile, CoinTile, EnemyTile, ConstraintTile, Goal


class Level:

    def __init__(self, level_data, surface):

        # game setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = 0

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        self.player_was_on_ground = True

        # level setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        terrain_tiles = import_cut_graphics(game_data.tilesets['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, terrain_tiles, StaticTile)

        grass_layout = import_csv_layout(level_data['grass'])
        grass_tiles = import_cut_graphics(game_data.tilesets['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, grass_tiles, StaticTile)

        crate_layout = import_csv_layout(level_data['crates'])
        crate_tiles = import_single_tile(game_data.tilesets['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, crate_tiles, CrateTile)

        coin_layout = import_csv_layout(level_data['coins'])
        coin_tiles = [
            import_folder(game_data.tilesets['coins'][0]),
            import_folder(game_data.tilesets['coins'][1]),
        ]
        self.coin_sprites = self.create_tile_group(coin_layout, coin_tiles, CoinTile)

        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        palm_tiles = [
            import_folder(game_data.tilesets['palms'][0]),
            import_folder(game_data.tilesets['palms'][1]),
            import_folder(game_data.tilesets['palms'][2]),
        ]
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, palm_tiles, PalmTile)

        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, palm_tiles, PalmTile)

        # enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        enemy_tiles = [import_folder(game_data.tilesets['enemies'])]
        self.enemy_sprites = self.create_tile_group(enemy_layout, enemy_tiles, EnemyTile)
        constraint_layout = import_csv_layout(level_data['constraints'])
        constrait_tiles = [None, pygame.surface.Surface((64, 64))]
        constrait_tiles[1].fill('red')
        self.constraint_sprites = self.create_tile_group(constraint_layout, constrait_tiles, ConstraintTile)

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()

    def create_particles(self, position, particle_type):
        if self.dust_sprite.sprites():
            return

        particle_effect = ParticleEffect(position, particle_type)
        self.dust_sprite.add(particle_effect)

    def create_tile_group(self, layout, tiles, tile_class):
        sprite_group = pygame.sprite.Group()

        for y, row in enumerate(layout):
            for x, col in enumerate(row):
                if col == -1:
                    continue

                item = tile_class((x * settings.tile_size, y * settings.tile_size), tiles[col])
                sprite_group.add(item)

        return sprite_group

    def player_setup(self, layout):
        for y, row in enumerate(layout):
            for x, col in enumerate(row):
                if col == -1:
                    continue

                if col == 0:
                    item = Player((x * settings.tile_size, y * settings.tile_size), self.display_surface,
                                  self.create_particles)
                    self.player.add(item)

                if col == 1:
                    goal_tile = pygame.image.load('graphics/character/hat.png').convert_alpha()

                    item = Goal((x * settings.tile_size, y * settings.tile_size), goal_tile)
                    self.goal.add(item)

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

        for sprite in self.terrain_sprites.sprites():
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

        for sprite in self.terrain_sprites.sprites():
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

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def run(self):
        self.enemy_collision_reverse()
        self.constraint_sprites.update(self.world_shift)

        # background level tiles
        for sprite_group in [
            self.bg_palm_sprites,
            self.crate_sprites,
            self.grass_sprites,
            self.terrain_sprites,
            self.coin_sprites,
            self.dust_sprite,
            self.enemy_sprites,
            self.goal,
        ]:
            sprite_group.update(self.world_shift)
            sprite_group.draw(self.display_surface)

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

        # foreground level tiles
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)
        self.scroll_x()
