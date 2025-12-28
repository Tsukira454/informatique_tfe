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


from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, FULLSCREEN, FONT
from object.others.logger import logger

def play_menu(compte_file):
    logger.info(f"Entrez dans play_menu avec le compte {compte_file}")
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

        pygame.display.set_caption("Menu Play")

        # --- Chargement background --- #
        background = pygame.image.load("./assets/images/background.png")
        background = pygame.transform.scale(background, (x, y))

        def load_btn(path, size=(300, 140)):
            img = pygame.image.load(path)
            return pygame.transform.scale(img, size)

        btn_img_play = load_btn("./assets/ui/ui_btn_1_play.png")
        btn_img_boutique = load_btn("./assets/ui/ui_btn_2_boutique.png")
        btn_img_option = load_btn("./assets/ui/ui_btn_4_options.png")

        barre_laterale = pygame.image.load("./assets/UI/menu/barre_lateral.png")
        barre_laterale = pygame.transform.scale(barre_laterale, (250, y))

        btn1_rect = btn_img_play.get_rect(topleft=(40,75))
        btn2_rect = btn_img_boutique.get_rect(topleft=(40,250))
        btn3_rect = btn_img_option.get_rect(topleft=(40,425))

        # === Chargement des stats ===
        data = save_load.load_data()
        # data = {'money' : 2}
        data_keys = list(data.keys())
        data_values = list(data.values())
        text_final = []
        for i in range(len(data_keys)):
            if data_keys[i] == "pseudo":
                text_final.append(font.render(f"{data_values[i]} :", True, (125,255,0)))
            else:
                text_final.append(font.render(f"{data_keys[i]} -> {data_values[i]}", True, (125,255,0)))
        
        def stat_blit(text_final):
            for i in range(len(text_final)):
                screen.blit(text_final[i], (LARGER_FENETRE-400, (i+1)*25))
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

                    if btn1_rect.collidepoint(mouse_pos):
                        play()

                    if btn2_rect.collidepoint(mouse_pos):
                        boutique()
                    
                    if btn3_rect.collidepoint(mouse_pos):
                        option_menu()

            screen.blit(background, (0, 0))
            screen.blit(barre_laterale, (0,0))
            screen.blit(btn_img_play, (40,75))
            screen.blit(btn_img_boutique,(40,250))
            screen.blit(btn_img_option, (40,425))
            stat_blit(text_final)

            pygame.display.flip()
    except Exception:
        logger.error("play_menu ->", exc_info=True)