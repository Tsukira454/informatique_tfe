import pygame
import sys
from pathlib import Path

# === Fix du chemin d'accès ===
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# === Import config propre ===
from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, FULLSCREEN
from ..others.save import save_load
from object.others.logger import logger
from object.others.audio_manager import stop_bg_music, play_fx
#from object.ui.play_menu import play_menu


def finish_menu(reward):
    pygame.init()
    x = LARGER_FENETRE
    y = HAUTEUR_FENETRE

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

    # === Fonction utilitaire pour charger un bouton ===
    def load_btn(path, size=(300, 140)):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)

    btn_img_play = load_btn("./assets/ui/ui_btn_4_play.png")

    # === Position des boutons ===
    btn1_rect = btn_img_play.get_rect(center=(x//2, y//2 - 150))

    # == DATA ===
    old_data = save_load.load_data()
    new_data = {"money" : 3}
    new_data_keys = list(new_data.keys())
    for i in range(len(new_data)):
        logger.info(old_data[new_data_keys[i]])
        logger.info(new_data[new_data_keys[i]])
        old_data[new_data_keys[i]]+=new_data[new_data_keys[0]]
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

        pygame.display.flip()

    pygame.quit()
    return None
