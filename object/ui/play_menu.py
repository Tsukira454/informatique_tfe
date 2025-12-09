# Elvin Mouyart
# UTF-8
import pygame
import sys
from pathlib import Path
from .option_menu import option_menu
from .play import play

# === Fix du chemin d'accès === #
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# === Import config propre === #
from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, FULLSCREEN

def play_menu():
    pygame.init()
    x = LARGER_FENETRE
    y = HAUTEUR_FENETRE
    block_size = 32

    # --- Configuration fenêtre --- #
    if FULLSCREEN:
        screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((x, y))

    pygame.display.set_caption("Menu Play")

    # --- Chargement background --- #
    try:
        background = pygame.image.load("./assets/images/background.png")
        background = pygame.transform.scale(background, (x, y))
    except:
        background = pygame.Surface((x, y))
        background.fill((40, 40, 40))

    def load_btn(path, size=(300, 140)):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)

    btn_img_play = load_btn("./assets/ui/ui_btn_1_play.png")
    btn_img_boutique = load_btn("./assets/ui/ui_btn_2_boutique.png")
    btn_img_option = load_btn("./assets/ui/ui_btn_4_options.png")

    barre_laterale = pygame.image.load("./assets/ui/ui_barre_lateral.png")
    barre_laterale_grosse = pygame.image.load("./assets/ui/ui_barre_lateral_grosse.png")
    barre_laterale = pygame.transform.scale(barre_laterale, (150, y))
    barre_laterale_grosse = pygame.transform.scale(barre_laterale_grosse, (1344, y))

    btn1_rect = btn_img_play.get_rect(topleft=(40,75))
    btn2_rect = btn_img_boutique.get_rect(topleft=(40,250))
    btn3_rect = btn_img_option.get_rect(topleft=(40,425))
    barre_laterale_rect = barre_laterale.get_rect(topleft=(0, 0))
    barre_laterale_grosse_rect = barre_laterale_grosse.get_rect(topleft=(0, 0))
    
    # Chargement de toute les images du jeux
    block_dirt = pygame.image.load("./assets/blocks/blocks/dirt.png")
    block_grass_block = pygame.image.load("./assets/blocks/blocks/grass_block.png")
    block_stone = pygame.image.load("./assets/blocks/blocks/stone.png")
    
    # Redimentionnement des images
    block_dirt = pygame.transform.scale(block_dirt, (block_size, block_size))
    block_grass_block = pygame.transform.scale(block_grass_block, (block_size, block_size))
    block_stone = pygame.transform.scale(block_stone, (block_size, block_size))

    running = True
    in_boutique = False

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if btn1_rect.collidepoint(mouse_pos):
                    play()

                if btn2_rect.collidepoint(mouse_pos):
                    in_boutique = True
                
                if btn3_rect.collidepoint(mouse_pos):
                    option_menu()
        while in_boutique:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_boutique = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        in_boutique = False
            screen.blit(background, (0, 0))
            screen.blit(barre_laterale_grosse, barre_laterale_grosse_rect)
            pygame.display.flip()
            
        screen.blit(background, (0, 0))
        screen.blit(barre_laterale, barre_laterale_rect)
        screen.blit(btn_img_play, btn1_rect)
        screen.blit(btn_img_boutique, btn2_rect)
        screen.blit(btn_img_option, btn3_rect)

        pygame.display.flip()
