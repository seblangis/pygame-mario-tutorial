import pygame
import sys

from mario import settings
from mario.tile import Tile
from mario.level import Level

pygame.init()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height), pygame.SCALED)
clock = pygame.time.Clock()
level = Level(settings.level_map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(60)
