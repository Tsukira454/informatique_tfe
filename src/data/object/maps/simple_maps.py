# Elvin Mouyart
# UTF-8
import pygame
import sys
from pathlib import Path
from random import randint

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from config.config import *


def create_simple_maps():
    pygame.init()

    block_size = SIZE_BLOCK
    maps = {}
    block_list = ["air", "grass_block", "dirt", "stone"]

    def level_y_to_pixel_y(level_index):
        # Convertit un index de ligne en position Y en pixels
        return level_index * block_size

    # === CHARGEMENT DES IMAGES ===
    block_dirt = pygame.image.load(ROOT_LOCATION / "assets/images/blocks/blocks/dirt.png")
    block_grass_block = pygame.image.load(ROOT_LOCATION / "assets/images/blocks/blocks/grass_block.png")
    block_stone = pygame.image.load(ROOT_LOCATION / "assets/images/blocks/blocks/stone.png")
    iron_ore = pygame.image.load(ROOT_LOCATION / "assets/images/blocks/blocks/iron_ore.png")
    block_dirt = pygame.transform.scale(block_dirt, (block_size, block_size))
    block_grass_block = pygame.transform.scale(block_grass_block, (block_size, block_size))
    block_stone = pygame.transform.scale(block_stone, (block_size, block_size))
    iron_ore = pygame.transform.scale(iron_ore, (block_size, block_size))

    # ===== CRÉATION DE LA MAP =====
    width_in_blocks = LARGER_FENETRE // block_size

    # --- Ciel : lignes 5 à 11 ---
    for level_y in range(5, 12):
        maps[level_y_to_pixel_y(level_y)] = ["air"] * width_in_blocks

    # --- LIGNE DE SURFACE (level 4) : air ou grass aléatoire ---
    level = [block_list[randint(0, len(block_list) - 3)] for _ in range(width_in_blocks)]
    maps[level_y_to_pixel_y(4)] = level

    # --- LIGNE 3 : herbe là où il y a de l'air au-dessus, sinon terre ---
    base_line_y = level_y_to_pixel_y(4)
    maps[level_y_to_pixel_y(3)] = [
        "grass_block" if maps[base_line_y][x] == "air" else "dirt"
        for x in range(width_in_blocks)
    ]

    # --- Sous-sol : on génère PROFONDEUR_NIVEAUX niveaux vers le bas ---
    # Chaque niveau devient progressivement plus riche en pierre
    # level 2  → surtout dirt
    # level -4 → surtout stone
    # level -20 et plus → quasi que stone
    PROFONDEUR_NIVEAUX = 100   # nombre de couches sous la surface

    for i in range(1, PROFONDEUR_NIVEAUX + 1):
        level_index = 3 - i
        level = []

        for _ in range(width_in_blocks):
            roll = randint(0, 100)
            blocs_superieurs = {nom: chance for nom, chance in BLOCK_CHANCE.items() if chance >= roll}
            bloc_choisi = min(blocs_superieurs, key=lambda x: blocs_superieurs[x])

            level.append(bloc_choisi)

        maps[level_y_to_pixel_y(level_index)] = level

    # === FIN : tri de haut en bas ===
    maps = dict(sorted(maps.items(), key=lambda x: x[0], reverse=True))
    return maps


if __name__ == "__main__":
    maps = create_simple_maps()
    print(f"Niveaux générés : {len(maps)}")
    for k in list(maps.keys())[:5]:
        print(f"  Y={k} -> {maps[k][:6]}...")