# Elvin Mouyart
# UTF-8
import pygame
import sys
from pathlib import Path
from random import randint

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, SIZE_BLOCK


def create_simple_maps():
    pygame.init()

    block_size = SIZE_BLOCK
    maps = {}
    block_list = ["air", "grass_block", "dirt", "stone"]

    # --- Fonction : convertir un index de ligne en pixels (Pygame Y) ---
    def level_y_to_pixel_y(level_index):
        return level_index * block_size

    # === CHARGEMENT DES IMAGES ===
    block_dirt = pygame.image.load("./assets/blocks/blocks/dirt.png")
    block_grass_block = pygame.image.load("./assets/blocks/blocks/grass_block.png")
    block_stone = pygame.image.load("./assets/blocks/blocks/stone.png")

    block_dirt = pygame.transform.scale(block_dirt, (block_size, block_size))
    block_grass_block = pygame.transform.scale(block_grass_block, (block_size, block_size))
    block_stone = pygame.transform.scale(block_stone, (block_size, block_size))

    # ===== CRÉATION DE LA MAP =====

    width_in_blocks = LARGER_FENETRE // block_size

    # --- Ciel : lignes 5 à 11 ---
    for level_y in range(5, 12):
        pixel_y = level_y_to_pixel_y(level_y)
        maps[pixel_y] = ["air"] * width_in_blocks

    # --- LIGNE D’HERBE (ou air) : level 4 ---
    level = []
    for _ in range(width_in_blocks):
        level.append(block_list[randint(0, len(block_list) - 3)])
    maps[level_y_to_pixel_y(4)] = level

    # --- LIGNE DU DESSOUS (3) ---
    base_line_y = level_y_to_pixel_y(4)
    new_line = []
    for x in range(width_in_blocks):
        if maps[base_line_y][x] == "air":
            new_line.append("grass_block")
        else:
            new_line.append("dirt")
    maps[level_y_to_pixel_y(3)] = new_line

    # --- Terre en-dessous : lignes 2 à -4 ---
    for i in range(1, 8):
        level = []
        for _ in range(width_in_blocks):
            level.append(block_list[randint(2, len(block_list)-1)])
        maps[level_y_to_pixel_y(3 - i)] = level

    # === FIN ===
    maps = dict(sorted(maps.items(), key=lambda x: x[0], reverse=True))
    return maps


if __name__ == "__main__":
    maps = create_simple_maps()
