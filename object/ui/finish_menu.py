import pygame
import sys
from pathlib import Path

# === Fix du chemin d'accès === #
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# === Import config propre === #
from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, FULLSCREEN
#from object.ui.play_menu import play_menu


def finish_menu(reward):
    pygame.init()
    x = LARGER_FENETRE
    y = HAUTEUR_FENETRE

    # --- Configuration fenêtre --- #
    if FULLSCREEN:
        screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((x, y))

    pygame.display.set_caption("Menu Principal")

    # --- Chargement background --- #
    try:
        background = pygame.image.load("./assets/images/background.png")
        background = pygame.transform.scale(background, (x, y))
    except:
        background = pygame.Surface((x, y))
        background.fill((40, 40, 40))

    # --- Fonction utilitaire pour charger un bouton --- #
    def load_btn(path, size=(300, 140)):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)

    btn_img_play = load_btn("./assets/ui/ui_btn_4_play.png")

    # --- Position des boutons --- #
    btn1_rect = btn_img_play.get_rect(center=(x//2, y//2 - 150))

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
                    play_menu()

        screen.blit(background, (0, 0))
        screen.blit(btn_img_play, btn1_rect)

        pygame.display.flip()

    pygame.quit()
    return None
