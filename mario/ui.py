import pygame

from mario import settings


class UI:

    def __init__(self, surface):
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load("graphics/ui/health_bar.png").convert_alpha()
        self.health_bar_top_left = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        # coins
        self.coin = pygame.image.load("graphics/ui/coin.png").convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))
        self.font = pygame.font.Font('graphics/ui/ARCADEPI.TTF', 24)

    def show_health(self, current_health, full_health):
        self.display_surface.blit(self.health_bar, (20, 10))

        bar_width = current_health * self.bar_max_width / full_health
        bar_rect = pygame.rect.Rect(
            self.health_bar_top_left[0],
            self.health_bar_top_left[1],
            bar_width,
            self.bar_height,
        )
        pygame.draw.rect(self.display_surface, '#dc4949', bar_rect)

    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)

        coins_count = self.font.render(str(amount), True, '#a04f45')
        coins_count_rect = coins_count.get_rect(midleft=self.coin_rect.midright)
        self.display_surface.blit(coins_count, coins_count_rect)
