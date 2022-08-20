from typing import Literal

import pygame

from mario.decorations import OverworldSky
from mario.support import import_folder
from overworld.game_data import levels


class Node(pygame.sprite.Sprite):

    def __init__(self, position, available, path):
        super().__init__()

        self.frames = import_folder(path)
        self.frame_index = 0
        self.animation_speed = 0.12

        self.image = self.frames[self.frame_index]
        self.available = available

        self.rect = self.image.get_rect(center=position)

    def animate(self):
        # TODO: hériter de AnimatedTile plutôt que de copier le code!
        self.frame_index += self.animation_speed
        self.frame_index %= len(self.frames)
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.available:
            self.animate()
        else:
            tint_surface = self.image.copy()
            tint_surface.fill('black', special_flags=pygame.BLEND_RGB_MULT)
            self.image.blit(tint_surface, (0, 0))


class Icon(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center=position)


class Overworld:

    def __init__(self, start_level, max_level, surface, select_level_func):
        self.current_level = start_level
        self.max_level = max_level

        self.surface = surface

        # sprites
        self.nodes = pygame.sprite.Group()
        self.setup_nodes()

        # icon
        self.icon = pygame.sprite.GroupSingle()
        self.setup_icon()
        self.move_direction = None
        self.movement_parts_count = 20
        self.movement_part = 0

        # gamepad
        if pygame.joystick.get_count():
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
        else:
            self.gamepad = None

        self.select_level = select_level_func

        self.global_cooldown = None
        self.reset_cooldown()

        self.sky = OverworldSky(horizon=8)

    def reset_cooldown(self):
        self.global_cooldown = 30

    def setup_nodes(self):
        for index, node_data in levels.items():
            available = index <= self.max_level

            self.nodes.add(Node(node_data['node_pos'], available, node_data['node_graphics']))

    def setup_icon(self):
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def draw_paths(self):
        points = [
            node['node_pos']
            for index, node in levels.items()
            if index <= self.max_level
        ]

        if len(points) > 1:
            pygame.draw.lines(self.surface, '#a04f45', False, points, 6)

    def get_input(self):
        if self.global_cooldown:
            self.global_cooldown -= 1
            return

        if self.movement_part:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.constants.K_SPACE] or (self.gamepad and self.gamepad.get_button(0)):
            self.select_level(self.current_level)
            return

        # Movement
        direction = keys[pygame.constants.K_RIGHT] - keys[pygame.constants.K_LEFT]

        if self.gamepad:
            direction += round(self.gamepad.get_axis(0))

        if direction < 0 < self.current_level:
            self.move_direction = self.get_movement_data(-1)
            self.current_level -= 1
        elif direction > 0 and self.current_level < self.max_level:
            self.move_direction = self.get_movement_data(1)
            self.current_level += 1

    def get_movement_data(self, offset: Literal[-1, 1]):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + offset].rect.center)
        self.movement_part = 1

        return end - start

    def update_icon_position(self):
        if not self.movement_part:
            return

        if self.movement_part == self.movement_parts_count:
            self.icon.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center
            self.movement_part = 0
        else:
            self.icon.sprite.rect.center += self.move_direction / self.movement_parts_count
            self.movement_part += 1

    def run(self):
        self.get_input()
        self.update_icon_position()
        self.nodes.update()

        self.sky.draw(self.surface)
        self.draw_paths()
        self.nodes.draw(self.surface)
        self.icon.draw(self.surface)

