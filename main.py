import pygame
import sys

from mario import settings
from overworld.game import Game

pygame.init()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))  # , pygame.SCALED
clock = pygame.time.Clock()
game = Game(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    game.run()

    pygame.display.update()
    clock.tick(60)
