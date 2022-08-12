import os
from csv import reader

import pygame

from mario.settings import tile_size


def import_csv_layout(path: str) -> list[list[int]]:
    layout = []
    with open(path) as level_map:
        lines = (reader(level_map, delimiter=','))

        for line in lines:
            layout.append([int(val) for val in line])

    return layout


def import_cut_graphics(path):
    tiles = []

    surface = pygame.image.load(path).convert_alpha()
    tile_count_x = surface.get_rect().width // tile_size
    tile_count_y = surface.get_rect().height // tile_size

    for row in range(tile_count_y):
        for col in range(tile_count_x):
            new_surface = pygame.surface.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), (col * tile_size, row * tile_size, tile_size, tile_size))

            tiles.append(new_surface)

    return tiles


def import_single_tile(path):
    return [pygame.image.load(path)]


def import_folder(path: str):
    surfaces = []

    for file in walk_files(path):
        full_path = os.path.join(path, file)
        surfaces.append(pygame.image.load(full_path).convert_alpha())

    return surfaces


def walk_folders(path: str):
    for _, folders, __ in os.walk(path):
        for folder in sorted(folders):
            yield folder


def walk_files(path: str):
    for _, __, files in os.walk(path):
        for file in sorted(files):
            yield file
