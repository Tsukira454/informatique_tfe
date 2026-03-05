# Elvin Mouyart
# UTF-8
import pygame
import sys
from pathlib import Path

# === Fix du chemin d'accès === #
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# === Import config propre === #
from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, FULLSCREEN


def option_menu():
    pygame.init()
    x = LARGER_FENETRE
    y = HAUTEUR_FENETRE


    # --- Configuration fenêtre --- #
    if FULLSCREEN:
        screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((x, y))

    pygame.display.set_caption("Menu Options")

    # --- Chargement background --- #
    try:
        background = pygame.image.load("./assets/images/background.png")
        background = pygame.transform.scale(background, (x, y))
    except:
        background = pygame.Surface((x, y))
        background.fill((40, 40, 40))

    running = True
    while running:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                return False
            if keys[pygame.K_ESCAPE]:
                running = False
                return True

        screen.blit(background, (0, 0))
        pygame.display.flip()