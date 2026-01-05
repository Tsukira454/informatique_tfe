# Elvin Mouyart
# UTF-8
import pygame
import sys
import os
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from config.config import *
from object.maps.simple_maps import create_simple_maps
from object.personnages.robot import Robot
from object.others.logger import logger

def background_create():
    try:
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
        background_img = pygame.transform.scale(background_img, (LARGER_FENETRE, HAUTEUR_FENETRE - (3 * SIZE_BLOCK)))
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
                y_background_pos = (HAUTEUR_FENETRE - (3 * SIZE_BLOCK)) - (1080 * (i - 1))
            background_pos.append((x_background_pos, y_background_pos))

        return background, background_pos
    except Exception:
        logger.error("play - background_create() -> ", exc_info=True)

def create_textures():
    try:
        # === Textures blocs ===
        block_dirt = pygame.transform.scale(
            pygame.image.load("./assets/blocks/blocks/dirt.png"), (SIZE_BLOCK, SIZE_BLOCK)
        )
        block_grass_block = pygame.transform.scale(
            pygame.image.load("./assets/blocks/blocks/grass_block.png"), (SIZE_BLOCK, SIZE_BLOCK)
        )
        block_stone = pygame.transform.scale(
            pygame.image.load("./assets/blocks/blocks/stone.png"), (SIZE_BLOCK, SIZE_BLOCK)
        )
        block_stairs = pygame.transform.scale(
            pygame.image.load("./assets/blocks/blocks/stairs.png"), (SIZE_BLOCK, SIZE_BLOCK)
        )
        return [block_dirt, block_grass_block, block_stone, block_stairs]
    except Exception:
        logger.error("Play - create_texture() -> ", exc_info=True)

def play():
    try:
        pygame.init()

        # === Configuration fenêtre ===
        if FULLSCREEN:
            screen = pygame.display.set_mode((LARGER_FENETRE, HAUTEUR_FENETRE), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((LARGER_FENETRE, HAUTEUR_FENETRE))
        pygame.display.set_caption("Nexus Extraction")

        # === Background ===
        background, background_pos = background_create()

        # === Textures blocs ===
        block_texture= create_textures()

        # === Fonts ===
        font = pygame.font.Font(FONT_TEXT, 24)

        # === Map ===
        maps = create_simple_maps()

        # === Robot ===
        robot = Robot()

        # === modification du background et de la map selon la position y du robot ===
        def update_background_and_map(background, background_pos, maps):
            ...
            return background, background_pos, maps

        # === Dessin de la map ===
        def place_blocks(maps):
            for y_str, row in maps.items():
                y = int(y_str)
                for x, block_type in enumerate(row):
                    screen_x = x * SIZE_BLOCK
                    screen_y = HAUTEUR_FENETRE - SIZE_BLOCK - y

                    if block_type == "dirt":
                        screen.blit(block_texture[0], (screen_x, screen_y))
                    elif block_type == "grass_block":
                        screen.blit(block_texture[1], (screen_x, screen_y))
                    elif block_type == "stone":
                        screen.blit(block_texture[2], (screen_x, screen_y))
                    elif block_type == "stairs":
                        screen.blit(block_texture[3], (screen_x, screen_y))
        
        # === Dessin du background ===
        def draw_background(background, background_pos):
            for i in range(len(background)):
                screen.blit(background[i], background_pos[i])

        # === Hitbox ===
        def create_hitbox(maps):
            collision_tiles = []
            for y_str, row in maps.items():
                y = int(y_str)
                screen_y = HAUTEUR_FENETRE - SIZE_BLOCK - y
                for x, block_type in enumerate(row):
                    if block_type != "air":
                        rect = pygame.Rect(
                            x * SIZE_BLOCK, screen_y, SIZE_BLOCK, SIZE_BLOCK
                        )
                        collision_tiles.append(rect)
            return collision_tiles

        # === HUD blocks recuperes ===
        def hud_collected_item_format(block_list, font):
            hud_collected_item = {}
            for i in range(len(block_list)):
                item_text = font.render(f"{list(block_list.keys())[i]}: {list(block_list.values())[i]}", True, TEXT_COLOR)
                hud_collected_item[list(block_list.keys())[i]] = item_text
            return hud_collected_item
        
        # === Inventory ===
        def inventory_image_make(collected_resources, font):
            max_items = 5
            image = pygame.image.load("./assets/UI/Inventory/inventory.png")
            image = pygame.transform.scale(image, (600, 400))
            image_final=[image]
            resource_keys = list(collected_resources.keys())
            # séparation des resources par 5
            resource_index = []
            for i in range(len(resource_keys)):
                stack = collected_resources[resource_keys[i]]/max_items
                resource_index.append(stack)
            # création d'un rectangle ou on va mettre toute les resource image etc
            for i in range(len(resource_keys)):
                item_image = pygame.image.load(f"./assets/blocks/blocks/{resource_keys[i]}.png")
                item_image = pygame.transform.scale(item_image, (40, 40))
                image_final.append(item_image)
                item_text = font.render(f"{collected_resources[resource_keys[i]]}", True, (255, 255, 255))
                image_final.append(item_text)
            return image_final

        # === Timer ===
        def check_timer(last_time, cooldown):
            current_time = time.time()
            if current_time - last_time >= cooldown:
                return True, current_time
            return False, last_time
        
        # === Boucle principale ===
        clock = pygame.time.Clock()
        running = True
        inventory_open = False
        last_time_inventory_img, last_time_inventory = time.time(), time.time()

        while running:
            clock.tick(60)

            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    running = False
                if keys[pygame.K_e]:
                    if check_timer(last_time_inventory, 0.5)[0]:
                        last_time_inventory = time.time()
                        inventory_open = not inventory_open

            # --- Affichage ---
            info_robot = robot.hud_valeur()
            background, background_pos, maps = update_background_and_map(background, background_pos, maps)
            draw_background(background, background_pos)
            place_blocks(maps)

            collision_tiles = create_hitbox(maps)
            maps = robot.update(maps, collision_tiles)
            robot.draw(screen)
            hud_energy = font.render(f"Energy: {info_robot['energy']} - {info_robot['energy_max']} _{int(info_robot['energy_pourcentage'])}_", True, (255, 255, 255))
            screen.blit(hud_energy, (10, 10))
            if inventory_open:
                center_x = (LARGER_FENETRE // 2) - 300
                center_y = (HAUTEUR_FENETRE // 2) - 200
                logger.info(center_y, center_x)
                if check_timer(last_time_inventory_img, 0.2)[0]:
                    last_time_inventory_img = time.time()
                    inventory_image_final = inventory_image_make(collected_resources=robot.collected_resources, font=font)
                else:
                    inventory_image = pygame.image.load("./assets/UI/Inventory/inventory.png")
                    inventory_image = pygame.transform.scale(inventory_image, (600, 400))
                for i in range(len(inventory_image_final)):
                    if i <=2:
                        if (i-1)%2:
                            # text
                            if i <=2:
                                screen.blit(inventory_image_final[i], (center_x+(20*i),center_y+(35)))
                            else:
                                screen.blit(inventory_image_final[i], (center_x+(20*i)+20,center_y+(35)))
                        else:
                            # block
                            if i <=2:
                                screen.blit(inventory_image_final[i], (center_x+(22*i),center_y+(20)))
                            else:
                                screen.blit(inventory_image_final[i], (center_x+(22*i)+20,center_y+(20)))
                    else:
                        screen.blit(inventory_image_final[i], (center_x,center_y))

            pygame.display.flip()

        pygame.quit()
    except Exception:
        logger.error("play ->", exc_info=True)
