import pygame

from overworld.game_data import levels


class Node(pygame.sprite.Sprite):

    def __init__(self, position, available):
        super().__init__()
        self.image = pygame.surface.Surface((100, 80))
        self.image.fill("red" if available else "grey")
        self.rect = self.image.get_rect(center=position)


class Icon(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()
        self.image = pygame.surface.Surface((20, 20))
        self.image.fill('yellow')
        self.rect = self.image.get_rect(center=position)


class Overworld:

    def __init__(self, start_level, max_level, surface):
        self.current_level = start_level
        self.max_level = max_level

        self.surface = surface

        # sprites
        self.nodes = pygame.sprite.Group()
        self.setup_nodes()

        # icon
        self.icon = pygame.sprite.GroupSingle()
        self.setup_icon()

    def setup_nodes(self):
        for index, node_data in levels.items():
            available = index <= self.max_level

            self.nodes.add(Node(node_data['node_pos'], available))

    def setup_icon(self):
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def draw_paths(self):
        points = [
            node['node_pos']
            for index, node in levels.items()
            if index <= self.max_level
        ]
        pygame.draw.lines(self.surface, 'red', False, points, 6)

    def run(self):
        self.surface.fill("blue")
        self.draw_paths()
        self.nodes.draw(self.surface)
        self.icon.draw(self.surface)
