# Elvin Mouyart
# UTF-8
import pygame
import sys
from pathlib import Path
from .option_menu import option_menu
from .play import play
from .boutique import boutique
from ..others.save import save_load


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from object.others.logger import logger


from config.config import *

def compte_menu():
    logger.info("Entrez dans compte")
    try:
        pygame.init()
        x = LARGER_FENETRE
        y = HAUTEUR_FENETRE
        block_size = 32
        font = pygame.font.Font(FONT, 24)

        # --- Configuration fenêtre --- #
        if FULLSCREEN:
            screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((x, y))

        pygame.display.set_caption("Compte - ?")

        # --- Chargement background --- #
        background = pygame.image.load("./assets/images/background.png")
        background = pygame.transform.scale(background, (x, y))
        # == Chargement des text principal ===
        text_title = font.render("Qui etez-vous ?", True, TEXT_COLOR)
        # === Chargement des bouton ===
        def load_btn(path, size=(300, 140)):
            img = pygame.image.load(path)
            return pygame.transform.scale(img, size)
        refresh_btn = load_btn("./assets/ui/refresh_btn.png", (96,96)) 
        create_compte_btn =load_btn("./assets/ui/ui_btn_compte.png", (500,150))

        refresh_btn_rect = refresh_btn.get_rect(topleft=((LARGER_FENETRE//10)*6, 125))
        create_compte_btn_rect = create_compte_btn.get_rect(topleft=(0,0))

        # === Chargement des comptes ===
        def compte_load():
            compte_list=[]
            # premier btn est la création d'un compte
            compte_list.append([font.render("Cree un compte", True, TEXT_COLOR), create_compte_btn])
            return compte_list
        compte_list = compte_load()
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
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    if refresh_btn_rect.collidepoint(mouse_pos):
                        compte_list=compte_load()
                        logger.info("Compte rafraichi")
                        return "player.json"
                    if create_compte_btn_rect.collidepoint(mouse_pos):
                        logger.info("Création d'un compte...")

            screen.blit(background, (0, 0))
            screen.blit(text_title, ((LARGER_FENETRE//10)*5-75, 50))
            screen.blit(refresh_btn, ((LARGER_FENETRE//10)*6, 125))
            for i in range(len(compte_list)):
                screen.blit(compte_list[i][1], (LARGER_FENETRE//2-300, (i+1)*250))
                screen.blit(compte_list[i][0], (LARGER_FENETRE//2-200, ((i+1)*250)+60))

            pygame.display.flip()
    except Exception:
        logger.error("Compte_menu ->", exc_info=True)
