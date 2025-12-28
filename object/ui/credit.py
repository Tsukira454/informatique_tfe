# Elvin Mouyart
# UTF-8
import pygame
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from config.config import *
from object.maps.simple_maps import create_simple_maps
from object.personnages.robot import Robot
from object.others.logger import logger

def credit_menu():
    logger.info("Enter -> crédit")
    try:
        pygame.init()
        font = pygame.font.Font(FONT, 24)

        # === Configuration fenêtre ===
        if FULLSCREEN:
            screen = pygame.display.set_mode((LARGER_FENETRE, HAUTEUR_FENETRE), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((LARGER_FENETRE, HAUTEUR_FENETRE))
        pygame.display.set_caption("Nexus Extraction")

        # === Background ===
        background = pygame.image.load("./assets/images/background.png")
        background = pygame.transform.scale(background, (LARGER_FENETRE, HAUTEUR_FENETRE))

        # === credits ===
        list_acteurs=[]
        creator_image = pygame.image.load("./assets/images/creator.jpg")
        creator_image = pygame.transform.scale(creator_image, (300,300))
        creator_text = font.render("Tsukira", True, (224, 175, 255))
        list_acteurs.append([creator_image, creator_text])

        # === Boucle principale ===
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(60)

            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    running = False
                    return False
                if keys[pygame.K_ESCAPE]:
                    running = False
                    return True

            screen.blit(background, (0,0))
            for i in range(len(list_acteurs)):
                screen.blit(list_acteurs[i][0], (LARGER_FENETRE//2-150, 50))
                screen.blit(list_acteurs[i][1], (LARGER_FENETRE//2-75, 370))
            pygame.display.flip()
    except Exception:
        logger.error("Crédit page erreur ->", exc_info=True)
