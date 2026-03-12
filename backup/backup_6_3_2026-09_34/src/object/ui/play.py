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

# =========================================================
# Seuil de déclenchement de la caméra :
# Si le robot dépasse 60% de la hauteur de l'écran vers le bas,
# la caméra commence à le suivre.
# =========================================================
CAMERA_SEUIL = 0.6


def background_create():
    try:
        dossier = str(ROOT / "assets/images/underground/")
        extensions_images = ('.png')
        nombre_images = 0
        background = []
        background_pos = []

        for fichier in os.listdir(dossier):
            if fichier.lower().endswith(extensions_images):
                nombre_images += 1

        # Background principal (surface)
        background_img = pygame.image.load("./assets/images/background.png")
        background_img = pygame.transform.scale(background_img, (LARGER_FENETRE, HAUTEUR_FENETRE - (3 * SIZE_BLOCK)))
        background.append(background_img)

        # Backgrounds souterrains
        for i in range(nombre_images):
            background_img = pygame.image.load(f"{dossier}/background_underground_{i+1}.png")
            background_img = pygame.transform.scale(background_img, (1920, 1080))
            background.append(background_img)

        for i in range(len(background)):
            x_background_pos = 0
            y_background_pos = 0
            if i == 0:
                # Background de surface
                y_background_pos = 0
            else:
                # Backgrounds souterrains : chaque image va plus bas
                y_background_pos = (HAUTEUR_FENETRE - (3 * SIZE_BLOCK)) + (1080 * (i - 1))
            background_pos.append((x_background_pos, y_background_pos))

        return background, background_pos
    except Exception:
        logger.error("play - background_create() -> ", exc_info=True)


def create_textures():
    try:
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
        block_iron_ore = pygame.transform.scale(
            pygame.image.load("./assets/blocks/blocks/iron_ore.png"), (SIZE_BLOCK, SIZE_BLOCK)
        )
        return [block_dirt, block_grass_block, block_stone, block_stairs, block_iron_ore]
    except Exception:
        logger.error("Play - create_texture() -> ", exc_info=True)


def play(compte_file):
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
        block_texture = create_textures()
        blue_storm = pygame.image.load(f"./assets/UI/play/blue_storm.png")
        danger = pygame.image.load(f"./assets/UI/play/danger.png")
        pression = pygame.image.load(f"./assets/UI/play/pression.png")
        blue_storm = pygame.transform.scale(blue_storm, (25, 25))
        pression = pygame.transform.scale(pression, (25, 25))
        danger = pygame.transform.scale(danger, (35, 35))

        # === Fonts ===
        font = pygame.font.Font(FONT_TEXT, 24)

        # === Map ===
        maps = create_simple_maps()

        # === Robot ===
        robot = Robot(compte_file)

        # =========================================================
        # CAMÉRA
        # camera_y = décalage vertical en pixels entre le monde et l'écran.
        # Tous les éléments du monde (blocs, robot) sont dessinés à :
        #     position_monde_y - camera_y
        # Quand camera_y augmente, la vue descend → les blocs remontent à l'écran.
        # =========================================================
        camera_y = 0
        seuil_px = int(HAUTEUR_FENETRE * CAMERA_SEUIL)  # pixel Y limite sur l'écran

        def update_camera(robot_rect, camera_y):
            if robot_rect.y > seuil_px:
                camera_y += robot_rect.y - seuil_px
            return camera_y

        # === Dessin de la map avec décalage caméra ===
        def place_blocks(maps, camera_y):
            texture_map = {
                "dirt":        block_texture[0],
                "grass_block": block_texture[1],
                "stone":       block_texture[2],
                "stairs":      block_texture[3],
                "iron_ore": block_texture[4],
            }
            for y_str, row in maps.items():
                y = int(y_str)
                # Position Y sur l'écran = position monde - décalage caméra
                screen_y = (HAUTEUR_FENETRE - SIZE_BLOCK - y) - camera_y

                # Culling : ne pas dessiner ce qui est hors écran
                if screen_y > HAUTEUR_FENETRE or screen_y < -SIZE_BLOCK:
                    continue

                for x, block_type in enumerate(row):
                    if block_type in texture_map:
                        screen.blit(texture_map[block_type], (x * SIZE_BLOCK, screen_y))

        # === Dessin du background avec parallaxe légère selon camera_y ===
        def draw_background(background, background_pos, camera_y):
            for i, (img, (bx, by)) in enumerate(zip(background, background_pos)):
                # Le background de surface défile à 30% de la vitesse caméra (parallaxe)
                # Les backgrounds souterrains défilent à 100%
                parallax = 0.3 if i == 0 else 1.0
                screen.blit(img, (bx, by - int(camera_y * parallax)))

        # --- Preview du butin ---
        def draw_reward_preview(collected_resources):
            reward_total = sum(
                collected_resources.get(bloc, 0) * REWARD_VALEUR.get(bloc, 0)
                for bloc in REWARD_VALEUR
            )
            text = font.render(f"Butin : {reward_total}", True, (255, 215, 0))  # couleur or
            screen.blit(text, (40, 80))
            
        # === Hitbox avec décalage caméra ===
        def create_hitbox(maps, camera_y):
            """
            Les hitboxes sont calculées dans les coordonnées ÉCRAN (avec camera_y).
            Ainsi les collisions restent correctes peu importe où est la caméra.
            """
            collision_tiles = []
            for y_str, row in maps.items():
                y = int(y_str)
                screen_y = (HAUTEUR_FENETRE - SIZE_BLOCK - y) - camera_y

                # Optimisation : ignorer les lignes hors écran (+ marge de 2 blocs)
                if screen_y > HAUTEUR_FENETRE + SIZE_BLOCK * 2:
                    continue
                if screen_y < -SIZE_BLOCK * 2:
                    continue

                for x, block_type in enumerate(row):
                    if block_type != "air":
                        rect = pygame.Rect(x * SIZE_BLOCK, screen_y, SIZE_BLOCK, SIZE_BLOCK)
                        collision_tiles.append(rect)
            return collision_tiles

        # === Inventory ===
        def inventory_image_make(collected_resources, font):
            image = pygame.image.load("./assets/UI/Inventory/inventory.png")
            image = pygame.transform.scale(image, (600, 400))
            image_final = [image]
            resource_keys = list(collected_resources.keys())

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

        # === DrawBar ===
        def DrawBar(pos, size, borderC, barC, progress):
            pygame.draw.rect(screen, borderC, (*pos, *size), 1)
            innerPos  = (pos[0]+3, pos[1]+3)
            innerSize = ((size[0]-6) * progress, size[1]-6)
            pygame.draw.rect(screen, barC, (*innerPos, *innerSize))

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

            # --- Mise à jour caméra ---
            # On met à jour camera_y AVANT de calculer les hitboxes et de dessiner,
            # pour que tout soit cohérent dans le même frame.
            camera_y = update_camera(robot.rect, camera_y)

            # --- Hitbox recalculées avec la nouvelle camera_y ---
            collision_tiles = create_hitbox(maps, camera_y)

            # --- Mise à jour robot (physique + inputs) ---
            # On transmet camera_y au robot pour que get_closest_map_y
            # puisse reconvertir les coordonnées écran en clés de map.
            robot.camera_y = camera_y
            maps = robot.update(maps, collision_tiles)
            info_robot = robot.hud_valeur()

            # --- Rendu ---
            draw_background(background, background_pos, camera_y)
            place_blocks(maps, camera_y)
            robot.draw(screen)

            # HUD (toujours en position fixe, pas affecté par camera_y)
            DrawBar((40, 20), (200, 20), (0, 0, 0), (0, 0, 255), info_robot['energy'] / info_robot['energy_max'])
            DrawBar((40, 50), (200, 20), (0, 0, 0), (0, 255, 0), (info_robot['y']) / info_robot['pression'])
            screen.blit(blue_storm, (10, 20))
            screen.blit(pression, (10, 50))
            if((info_robot['y'] / info_robot['pression'])*100<=30):
                screen.blit(danger, (250, 50))
            draw_reward_preview(robot.collected_resources)

            # Inventaire (toujours fixe à l'écran)
            if inventory_open:
                center_x = (LARGER_FENETRE // 2) - 300
                center_y = (HAUTEUR_FENETRE // 2) - 200

                if check_timer(last_time_inventory_img, 0.2)[0]:
                    last_time_inventory_img = time.time()
                    inventory_image_final = inventory_image_make(
                        collected_resources=robot.collected_resources, font=font
                    )
                screen.blit(inventory_image_final[0], (center_x, center_y))

                SLOT_SIZE     = 46
                SLOT_MARGIN   = 12
                COLS          = 10
                GRID_OFFSET_X = 21
                GRID_OFFSET_Y = 19
                item_pairs    = (len(inventory_image_final) - 1) // 2

                for slot in range(item_pairs):
                    item_img  = inventory_image_final[1 + slot * 2]
                    item_text = inventory_image_final[2 + slot * 2]
                    col    = slot % COLS
                    row    = slot // COLS
                    slot_x = center_x + GRID_OFFSET_X + col * (SLOT_SIZE + SLOT_MARGIN)
                    slot_y = center_y + GRID_OFFSET_Y + row * (SLOT_SIZE + SLOT_MARGIN)
                    screen.blit(item_img, (slot_x, slot_y))
                    text_x = slot_x + SLOT_SIZE - item_text.get_width()
                    text_y = slot_y + SLOT_SIZE - item_text.get_height() + 2
                    screen.blit(item_text, (text_x, text_y))

            pygame.display.flip()

        pygame.quit()
    except Exception:
        logger.error("play ->", exc_info=True)