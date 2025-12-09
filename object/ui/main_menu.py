import pygame
import sys
from pathlib import Path

# === Fix du chemin d'accès === #
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# === Import config propre === #
from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, FULLSCREEN
from object.others.particule import Particle


def main_menu():
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
    btn_img_option = load_btn("./assets/ui/ui_btn_4_options.png")
    btn_img_quitter = load_btn("./assets/ui/ui_btn_4_quitter.png")

    # --- Position des boutons --- #
    btn1_rect = btn_img_play.get_rect(center=(x//2, y//2 - 150))
    btn2_rect = btn_img_option.get_rect(center=(x//2, y//2))
    btn3_rect = btn_img_quitter.get_rect(center=(x//2, y//2 + 150))
    particles = [Particle() for _ in range(60)]
    running = True
    fade_alpha = 255

    def draw_fade():
        nonlocal fade_alpha
        if fade_alpha > 0:
            fade_alpha -= 4
            fade = pygame.Surface((LARGER_FENETRE, HAUTEUR_FENETRE))
            fade.fill((0, 0, 0))
            fade.set_alpha(fade_alpha)
            screen.blit(fade, (0, 0))

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if btn1_rect.collidepoint(mouse_pos):
                    #pygame.quit()
                    return 1

                if btn2_rect.collidepoint(mouse_pos):
                    #pygame.quit()
                    return 2

                if btn3_rect.collidepoint(mouse_pos):
                    #pygame.quit()
                    return 3

        screen.blit(background, (0, 0))
        screen.blit(btn_img_play, btn1_rect)
        screen.blit(btn_img_option, btn2_rect)
        screen.blit(btn_img_quitter, btn3_rect)
        for p in particles:
            p.update()
            p.draw(screen)
        draw_fade()

        pygame.display.flip()

    pygame.quit()
    return None
