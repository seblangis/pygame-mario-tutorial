import os

import pygame

from mario.support import walk_folders, import_folder


class Player(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()

        # animations
        self.animations = {}
        self.import_character_assets()

        # character
        self.frame_index = 0
        self.image = self.animations['idle'][self.frame_index]
        self.animation_speed = 0.15
        self.rect = self.image.get_rect(topleft=position)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        character_path = 'graphics/character'

        for folder in walk_folders(character_path):
            if folder == 'dust_particles':
                self.animations[folder] = {}
                for particle_folder in walk_folders(os.path.join(character_path, folder)):
                    particle_animation_path = os.path.join(character_path, folder, particle_folder)
                    self.animations[folder][particle_folder] = import_folder(particle_animation_path)

                continue

            animation_path = os.path.join(character_path, folder)
            self.animations[folder] = import_folder(animation_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        self.frame_index %= len(animation)

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        # set the rect
        if self.on_ground:
            if self.on_right:
                self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
            elif self.on_left:
                self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
            else:
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling:
            if self.on_right:
                self.rect = self.image.get_rect(topright=self.rect.topright)
            elif self.on_left:
                self.rect = self.image.get_rect(topleft=self.rect.topleft)
            else:
                self.rect = self.image.get_rect(midtop=self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > self.gravity:
            self.status = 'fall'
        elif self.direction.x == 0:
            self.status = 'idle'
        else:
            self.status = 'run'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
