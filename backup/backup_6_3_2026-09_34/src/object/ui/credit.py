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
        font = pygame.font.Font(FONT_TEXT, 24)

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
        creator_text_role = font.render("Creator :", True, (255,255,255))
        music_creator_img = pygame.image.load("./assets/images/music_creator.png")
        music_creator_text = font.render("Majinn", True, (255,0,0))
        music_creator_img = pygame.transform.scale(music_creator_img, (300,300))
        music_creator_text_role = font.render("Music - fx :", True, (255,255,255))
        list_acteurs.append([creator_image, creator_text, creator_text_role])
        list_acteurs.append([music_creator_img, music_creator_text, music_creator_text_role])
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
            screen.blit(list_acteurs[0][0], (LARGER_FENETRE//4-150, 50))
            screen.blit(list_acteurs[0][1], (LARGER_FENETRE//4-75, 390))
            screen.blit(list_acteurs[0][2], (LARGER_FENETRE//4-75, 355))
            screen.blit(list_acteurs[1][0], (LARGER_FENETRE//4-150, 500))
            screen.blit(list_acteurs[1][2], (LARGER_FENETRE//4-100, 820))
            screen.blit(list_acteurs[1][1], (LARGER_FENETRE//4-70, 850))
            pygame.display.flip()
    except Exception:
        logger.error("Crédit page erreur ->", exc_info=True)
