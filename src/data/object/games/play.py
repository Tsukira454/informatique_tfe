# Elvin Mouyart
# UTF-8
import pygame
import os
import time
from config.config import *
from object.maps.maps import create_simple_maps
from object.personnages.robot import Robot
from object.others.logger import logger
from ..others.audio_manager import *
from ..ui.moving_block import *
from object.personnages.rocket import *

def transition(screen, font, maps_level, asset_manager):
    void_full = asset_manager.get_element("the_void_full")
    void_full = pygame.transform.scale(void_full, (LARGER_FENETRE, HAUTEUR_FENETRE))
    
    level_name = WORLD_LEVEL[maps_level][0]
    text = pygame.font.Font(FONT_SPECIAL, 64).render(level_name, True, (255, 215, 0))
    
    clock = pygame.time.Clock()
    
    # position de départ hors écran à gauche
    text_x = -text.get_width()
    center_x = LARGER_FENETRE // 2 - text.get_width() // 2
    text_y = HAUTEUR_FENETRE // 2 - text.get_height() // 2
    
    # phase : "entree", "attente", "sortie"
    phase = "entree"
    wait_timer = 0
    wait_duration = 90  # frames d'attente au centre

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # === mouvement du texte ===
        if phase == "entree":
            # ralentit en approchant du centre (easing)
            distance = center_x - text_x
            text_x += max(4, distance * 0.12)  # rapide puis lent
            if text_x >= center_x:
                text_x = center_x
                phase = "attente"

        elif phase == "attente":
            wait_timer += 1
            if wait_timer >= wait_duration:
                phase = "sortie"

        elif phase == "sortie":
            text_x += 80  # part rapidement vers la droite
            if text_x > LARGER_FENETRE:
                running = False

        # === rendu ===
        screen.blit(void_full, (0, 0))
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()

def background_create(asset_manager=None, maps_level=0):
    try:
        nombre_images = 0
        background = []
        background_pos = []

        for fichier in os.listdir(UNDERGROUND_FOLDER / f"maps_level_{maps_level}"):
            if fichier.lower().endswith('.png'):
                nombre_images += 1

        background_img = asset_manager.get_element("background")
        background_img = pygame.transform.scale(background_img, (LARGER_FENETRE, HAUTEUR_FENETRE - (3 * SIZE_BLOCK)))
        background.append(background_img)

        for i in range(nombre_images):
            background.append(asset_manager.get_element(f"underground_{i+1}"))

        # ← the_void : toujours en dernier
        background.append(asset_manager.get_element("the_void"))

        for i in range(len(background)):
            if i == 0:
                background_pos.append((0, 0))
            elif i == len(background) - 1:
                # the_void : position juste après le dernier underground, répété à l'infini via le draw
                background_pos.append((0, (HAUTEUR_FENETRE - (3 * SIZE_BLOCK)) + (1080 * (i - 1))))
            else:
                background_pos.append((0, (HAUTEUR_FENETRE - (3 * SIZE_BLOCK)) + (1080 * (i - 1))))

        return background, background_pos
    except Exception:
        logger.error("play - background_create() -> ", exc_info=True)


def play(compte_file, asset_manager=None,maps_level=0):
    try:
        pygame.init()

        if FULLSCREEN:
            screen = pygame.display.set_mode((LARGER_FENETRE, HAUTEUR_FENETRE), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((LARGER_FENETRE, HAUTEUR_FENETRE))
        pygame.display.set_caption(f"Nexus Extraction | {WORLD_LEVEL[maps_level][0]}")

        # === Background ===
        background, background_pos = background_create(asset_manager=asset_manager,maps_level=0)
        water = MovingBlock("water", asset_manager=asset_manager)
        lava  = MovingBlock("lava",  asset_manager=asset_manager)
        # === Textures blocs ===
        block_texture = []
        for i in range(len(WORLD_LEVEL[maps_level][1])):
            block_texture.append(asset_manager.get_element(f"{WORLD_LEVEL[maps_level][1][i]}"))
        blue_storm = asset_manager.get_element("blue_storm")
        danger     = asset_manager.get_element("danger")
        pression   = asset_manager.get_element("pression_icon")

        # === Fonts ===
        font = pygame.font.Font(FONT_TEXT, 24)

        # === Map ===
        maps = create_simple_maps(asset_manager=asset_manager,maps_level=maps_level)

        # === Robot ===
        robot = Robot(compte_file, asset_manager=asset_manager, maps_level=maps_level)

        # === Rocket ===
        if maps_level==0:
            rocket     = Animation_rocket("rocket", asset_manager)
            spawn_done = False
        else:
            spawn_done=True

        # === Camera ===
        camera_y = 0
        seuil_px = int(HAUTEUR_FENETRE * CAMERA_SEUIL)

        def update_camera(robot_rect, camera_y):
            if robot_rect.y > seuil_px:
                camera_y += robot_rect.y - seuil_px
            return camera_y

        def place_blocks(maps, camera_y):
            texture_map = {}
            for i in range(len(WORLD_LEVEL[maps_level][1])):
                texture_map[str(WORLD_LEVEL[maps_level][1][i])] = block_texture[i]
            texture_map["lava"] = lava.get_image()
            texture_map["water"] = water.get_image()
            for y_str, row in maps.items():
                y = int(y_str)
                screen_y = (HAUTEUR_FENETRE - SIZE_BLOCK - y) - camera_y
                if screen_y > HAUTEUR_FENETRE or screen_y < -SIZE_BLOCK:
                    continue
                for x, block_type in enumerate(row):
                    if block_type in texture_map:
                        screen.blit(texture_map[block_type], (x * SIZE_BLOCK, screen_y))

        def draw_background(background, background_pos, camera_y):
            for i, (img, (bx, by)) in enumerate(zip(background, background_pos)):
                parallax = 0.3 if i == 0 else 1.0
                screen.blit(img, (bx, by - int(camera_y * parallax)))

        def draw_reward_preview(collected_resources):
            reward_total = sum(
                collected_resources.get(bloc, 0) * REWARD_VALEUR.get(bloc, 0)
                for bloc in REWARD_VALEUR
            )
            text = font.render(f"Butin : {reward_total}", True, (255, 215, 0))
            screen.blit(text, (40, 80))

        def create_hitbox(maps, camera_y):
            no_collision = {"water", "lava", "air", "SPECIAL_BLOCK_TP", "water_full", "lava_full"}
            collision_tiles = []
            for y_str, row in maps.items():
                y = int(y_str)
                screen_y = (HAUTEUR_FENETRE - SIZE_BLOCK - y) - camera_y
                if screen_y > HAUTEUR_FENETRE + SIZE_BLOCK * 2:
                    continue
                if screen_y < -SIZE_BLOCK * 2:
                    continue
                for x, block_type in enumerate(row):
                    if block_type != "air" and block_type not in no_collision:
                        rect = pygame.Rect(x * SIZE_BLOCK, screen_y, SIZE_BLOCK, SIZE_BLOCK)
                        collision_tiles.append(rect)
            return collision_tiles

        def inventory_image_make(collected_resources, font):
            if asset_manager is not None:
                image = asset_manager.get_element("inventory")
            else:
                image = pygame.transform.scale(
                    pygame.image.load(ROOT_LOCATION / "assets/images/UI/Inventory/inventory.png"), (600, 400))
            image_final = [image]
            resource_keys = list(collected_resources.keys())
            for i in range(len(resource_keys)):
                if asset_manager is not None:
                    item_image = asset_manager.get_element(resource_keys[i])
                else:
                    item_image = pygame.transform.scale(
                        pygame.image.load(ROOT_LOCATION / f"assets/images/blocks/blocks/{resource_keys[i]}.png"), (40, 40))
                image_final.append(item_image)
                item_text = font.render(f"{collected_resources[resource_keys[i]]}", True, (255, 255, 255))
                image_final.append(item_text)
            return image_final

        def check_timer(last_time, cooldown):
            current_time = time.time()
            if current_time - last_time >= cooldown:
                return True, current_time
            return False, last_time

        def DrawBar(pos, size, borderC, barC, progress):
            pygame.draw.rect(screen, borderC, (*pos, *size), 1)
            innerPos  = (pos[0]+3, pos[1]+3)
            innerSize = ((size[0]-6) * progress, size[1]-6)
            pygame.draw.rect(screen, barC, (*innerPos, *innerSize))

        # === Boucle principale ===
        clock = pygame.time.Clock()
        running = True
        inventory_open = False
        inventory_image_final = None
        last_time_inventory_img, last_time_inventory = time.time(), time.time()
        new_maps_check=False
        new_maps_check_dev_tool=False
        if(maps_level==0):
            transition(screen, font, maps_level, asset_manager)
        while running:
            clock.tick(60)

            # === Events ===
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    running = False
                if keys[pygame.K_e]:
                    if check_timer(last_time_inventory, 0.5)[0]:
                        last_time_inventory = time.time()
                        inventory_open = not inventory_open
                if keys[pygame.K_n]:
                    new_maps_check_dev_tool=True

            # === Update logique ===
            camera_y = update_camera(robot.rect, camera_y)
            collision_tiles = create_hitbox(maps, camera_y)
            robot.camera_y = camera_y

            if spawn_done:
                maps,new_maps_check = robot.update(maps, collision_tiles)
            else:
                # robot suit la rocket pendant la descente
                if not rocket.show_robot():
                    rocket_x, rocket_y = rocket.get_pos()
                    robot.rect.x = (LARGER_FENETRE//10)*8
                    robot.rect.y = rocket_y + 100
                maps = robot.move_gravity(maps, collision_tiles)
            if new_maps_check or new_maps_check_dev_tool:
                maps_level += 1
                transition(screen, font, maps_level, asset_manager)
                play(compte_file=compte_file, asset_manager=asset_manager, maps_level=maps_level)
                return

            info_robot = robot.hud_valeur()

            # === Rendu ===
            draw_background(background, background_pos, camera_y)
            water.update()
            lava.update()
            place_blocks(maps, camera_y)

            # robot visible seulement quand la rocket atterrit
            if spawn_done or rocket.show_robot():
                robot.draw(screen)

            # rocket par dessus tout
            if not spawn_done:
                rocket.update()
                rocket.draw(screen)
                if rocket.is_done():
                    spawn_done = True
                    robot.speed_y = 0
                    robot.on_ground = False

            # === HUD ===
            DrawBar((40, 20), (200, 20), (0, 0, 0), (0, 0, 255), info_robot['energy'] / info_robot['energy_max'])
            if(info_robot['y']>=0) or not spawn_done:
                profondeur = 0
            else:
                profondeur = abs(info_robot['y']) / info_robot['pression']
            couleur_pression = (255, 0, 0) if profondeur >= 0.75 else (0, 255, 0)
            if profondeur >= 0.75:
                if spawn_done:
                    play_fx(ROOT_LOCATION / "assets/sounds/warning.mp3")
                    
            DrawBar((40, 50), (200, 20), (0, 0, 0), couleur_pression, 1 - profondeur)
            screen.blit(blue_storm, (10, 20))
            screen.blit(pression,   (10, 50))
            if (abs(info_robot['y']) / info_robot['pression']) * 100 >= 70 and spawn_done:
                screen.blit(danger, (250, 50))
            draw_reward_preview(robot.collected_resources)

            # === Inventaire ===
            if inventory_open and spawn_done:
                center_x = (LARGER_FENETRE // 2) - 300
                center_y = (HAUTEUR_FENETRE // 2) - 200
                if check_timer(last_time_inventory_img, 0.2)[0]:
                    last_time_inventory_img = time.time()
                    inventory_image_final = inventory_image_make(
                        collected_resources=robot.collected_resources, font=font)
                if inventory_image_final:
                    screen.blit(inventory_image_final[0], (center_x, center_y))
                    SLOT_SIZE, SLOT_MARGIN, COLS = 46, 12, 10
                    GRID_OFFSET_X, GRID_OFFSET_Y = 21, 19
                    item_pairs = (len(inventory_image_final) - 1) // 2
                    for slot in range(item_pairs):
                        item_img  = inventory_image_final[1 + slot * 2]
                        item_text = inventory_image_final[2 + slot * 2]
                        col    = slot % COLS
                        row    = slot // COLS
                        slot_x = center_x + GRID_OFFSET_X + col * (SLOT_SIZE + SLOT_MARGIN)
                        slot_y = center_y + GRID_OFFSET_Y + row * (SLOT_SIZE + SLOT_MARGIN)
                        screen.blit(item_img, (slot_x, slot_y))
                        screen.blit(item_text, (
                            slot_x + SLOT_SIZE - item_text.get_width(),
                            slot_y + SLOT_SIZE - item_text.get_height() + 2
                        ))

            pygame.display.flip()

        pygame.quit()
    except Exception:
        logger.error("play ->", exc_info=True)