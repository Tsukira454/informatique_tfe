# Elvin Mouyart
# UTF-8
import pygame
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, FULLSCREEN, SIZE_BLOCK
from object.maps.simple_maps import create_simple_maps
from object.personnages.robot import Robot
from object.ui.finish_menu import finish_menu


def play():
    pygame.init()
    x = LARGER_FENETRE
    y = HAUTEUR_FENETRE

    if FULLSCREEN:
        screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((x, y))

    pygame.display.set_caption("Play")

    # === Background ===
    dossier = str(ROOT / "assets/images/underground/")
    extensions_images = ('.png')
    nombre_images = 0
    background = []
    background_pos = []

    for fichier in os.listdir(dossier):
        if fichier.lower().endswith(extensions_images):
            nombre_images += 1

    # Background principal
    background_img = pygame.image.load("./assets/images/background.png")
    background_img = pygame.transform.scale(background_img, (x, y - (3 * SIZE_BLOCK)))
    background.append(background_img)

    # Background underground
    for i in range(nombre_images):
        background_img = pygame.image.load(f"{dossier}/background_underground_{i+1}.png")
        background_img = pygame.transform.scale(background_img, (1920, 1080))
        background.append(background_img)

    for i in range(len(background)):
        x_background_pos = 0
        y_background_pos = 0
        if i >= 1:
            y_background_pos = (y - (3 * SIZE_BLOCK)) - (1080 * (i - 1))
        background_pos.append((x_background_pos, y_background_pos))

    print("Background positions:", background_pos)

    # === Blocks textures ===
    block_dirt = pygame.transform.scale(pygame.image.load("./assets/blocks/blocks/dirt.png"), (SIZE_BLOCK, SIZE_BLOCK))
    block_grass_block = pygame.transform.scale(pygame.image.load("./assets/blocks/blocks/grass_block.png"), (SIZE_BLOCK, SIZE_BLOCK))
    block_stone = pygame.transform.scale(pygame.image.load("./assets/blocks/blocks/stone.png"), (SIZE_BLOCK, SIZE_BLOCK))
    block_stairs = pygame.transform.scale(pygame.image.load("./assets/blocks/blocks/stairs.png"), (SIZE_BLOCK, SIZE_BLOCK))

    # === Génération de la map ===
    maps = create_simple_maps("12345")

    # === Spawn robot ===
    robot = Robot()

    # === Fonction pour dessiner la map ===
    def place_blocks(maps, map_offset_y):
        for y_str, row in maps.items():
            y_map = int(y_str) - map_offset_y  # appliquer le scroll par bloc
            for x, block_type in enumerate(row):
                screen_x = x * SIZE_BLOCK
                screen_y = HAUTEUR_FENETRE - SIZE_BLOCK - y_map
                if block_type != "air":
                    if block_type == "dirt":
                        screen.blit(block_dirt, (screen_x, screen_y))
                    elif block_type == "grass_block":
                        screen.blit(block_grass_block, (screen_x, screen_y))
                    elif block_type == "stone":
                        screen.blit(block_stone, (screen_x, screen_y))
                    elif block_type == "stairs":
                        screen.blit(block_stairs, (screen_x, screen_y))

    # === Fonction hitbox ===
    def create_hitbox(maps, map_offset_y=0):
        collision_tiles = []
        for y_str, row in maps.items():
            y_map = int(y_str) - map_offset_y
            screen_y = HAUTEUR_FENETRE - SIZE_BLOCK - y_map
            for x, block_type in enumerate(row):
                if block_type != "air":
                    tile_rect = pygame.Rect(x * SIZE_BLOCK, screen_y, SIZE_BLOCK, SIZE_BLOCK)
                    collision_tiles.append(tile_rect)
        return collision_tiles

    def change_bg_maps(maps, background_pos, background):
        # Cette fonction va afficher le bacground et la carte celon la position du joueur
        pos_robot = robot.get_pos()
        robot_screen_y = pos_robot[1]

        return maps, background, background_pos
    
    # === Boucle principale ===
    running = True
    clock = pygame.time.Clock()

    # --- Variables scroll ---
    spawn_offset = 696            # Position du robot sur l'écran
    map_offset_y = 0              # Scroll de la map par bloc
    scroll_threshold = 300        # Seuil vertical pour que la map commence à défiler

    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Position robot ---
        pos_robot = robot.get_pos()
        robot_screen_y = pos_robot[1]

        # --- Scroll map par bloc uniquement si robot monte ---
        if robot_screen_y < scroll_threshold:
            move_amount = scroll_threshold - robot_screen_y
            if move_amount >= SIZE_BLOCK:
                map_offset_y += SIZE_BLOCK
                robot.rect.y += SIZE_BLOCK  # maintien du robot à la même position écran

        # --- Changement background et map ---
        maps, background, background_pos = change_bg_maps(maps, background_pos, background)
        

        # --- Dessin map ---
        place_blocks(maps, map_offset_y)

        # --- Hitbox ---
        collision_tiles = create_hitbox(maps, map_offset_y)

        # --- Update robot ---
        maps = robot.update(maps, collision_tiles)
        robot.draw(screen)

        pygame.display.flip()
