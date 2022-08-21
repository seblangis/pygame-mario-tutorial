import pygame
from .support import import_folder


class ParticleEffect(pygame.sprite.Sprite):

    def __init__(self, position, particle_type):
        super().__init__()

        self.frame_index = 0
        self.animation_speed = 0.5

        if particle_type == 'explosion':
            self.frames = import_folder(f'graphics/enemy/{particle_type}')
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect(center=position)
        else:
            self.frames = import_folder(f'graphics/character/dust_particles/{particle_type}')
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect(midbottom=position)

    def animate(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
