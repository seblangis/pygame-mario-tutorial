import pygame
from .support import import_folder


class ParticleEffect(pygame.sprite.Sprite):

    def __init__(self, position, particle_type):
        super().__init__()

        self.frame_index = 0
        self.animation_speed = 0.5

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