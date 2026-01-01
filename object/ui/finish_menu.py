import pygame
import sys
from pathlib import Path

# === Fix du chemin d'accès ===
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# === Import config propre ===
from config.config import *
from ..others.save import *
from object.others.logger import logger
from object.others.audio_manager import stop_bg_music, play_fx
#from object.ui.play_menu import play_menu


def finish_menu(reward):
    pygame.init()
    x = LARGER_FENETRE
    y = HAUTEUR_FENETRE
    font = pygame.font.Font(FONT, 24)

    # === Configuration fenêtre ===
    if FULLSCREEN:
        screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((x, y))

    pygame.display.set_caption("Mort :/")

    # === Chargement background ===
    try:
        background = pygame.image.load("./assets/images/background.png")
        background = pygame.transform.scale(background, (x, y))
    except:
        background = pygame.Surface((x, y))
        background.fill((40, 40, 40))

    # === Texture + btn ===
    def load_btn(path, size=(300, 140)):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)

    btn_img_play = load_btn("./assets/ui/ui_btn_4_play.png")
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
    block_list_img=[block_dirt, block_grass_block, block_stairs, block_stone]
    block_list_str=BLOCK_LIST

    # === Position des boutons ===
    reward_final = 0
    for i in range(len(reward)):
        reward_final+= reward[str(block_list_str[i])]*REWARD_VALEUR[str(block_list_str[i])]
    def reward_blit(reward, block_list_img, block_list_str, reward_final):
        for i in range(len(reward)):
            screen.blit(block_list_img[i], (x//2-SIZE_BLOCK, ((y//10)*2)+(i)*75))
            text=font.render(f"{reward[str(block_list_str[i])]}", True, TEXT_COLOR)
            screen.blit(text, (x//2+SIZE_BLOCK, (((y//10)*2)+(i)*75)+10))
        text=font.render(f"{reward_final}", True, TEXT_COLOR)
        screen.blit(text, (x//2+SIZE_BLOCK, ((y//10)*2)+(len(reward)+1)*75))
    btn1_rect = btn_img_play.get_rect(center=(x//2, y//2 + 300))
    

    # == DATA ===
    data = save_load.load_data()
    data = save_load.build_data(pseudo=data["pseudo"], money=(data["money"]+reward_final))
    save_load.save_data(data)
    # === Couper la music et mettre la music de mort
    stop_bg_music()
    play_fx("./assets/sounds/music_nexus_death.wav")
    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if btn1_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    # Chargement du module play menu ici pour éviter des erreur d'une boucle d'import
                    from object.ui.play_menu import play_menu
                    #compte wait
                    file="player.json"
                    play_menu(file, death=True)

        screen.blit(background, (0, 0))
        screen.blit(btn_img_play, btn1_rect)
        reward_blit(reward, block_list_img, block_list_str, reward_final)

        pygame.display.flip()

    pygame.quit()
    return None
