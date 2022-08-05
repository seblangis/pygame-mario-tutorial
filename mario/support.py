import os
from csv import reader

import pygame


def import_csv_layout(path: str) -> list[list[int]]:
    layout = []
    with open(path) as level_map:
        lines = (reader(level_map, delimiter=','))

        for line in lines:
            layout.append([int(val) for val in line])

    return layout


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
