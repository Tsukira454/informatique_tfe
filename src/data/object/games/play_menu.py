# Elvin Mouyart
# UTF-8
import pygame
import sys
from pathlib import Path
from .option_menu import option_menu
from .play import play
from .boutique import boutique
from ..others.save import save_load
from ..ui.Three_D import *
from ..personnages.bird import *
from ..others.particule import *
from random import randint

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


from config.config import *
from object.others.logger import logger
from object.others.audio_manager import play_bg_music

def play_menu(compte_file, death=False):
    logger.info(f"Entrez dans play_menu avec le compte {compte_file}")
    try:
        pygame.init()
        if death:
            pygame.mixer.init()
            play_bg_music(ROOT_LOCATION / "assets/music/music_nexus_bg.wav")
        x = LARGER_FENETRE
        y = HAUTEUR_FENETRE
        font = pygame.font.Font(FONT_TEXT, 24)

        # --- Configuration fenêtre --- #
        if FULLSCREEN:
            screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((x, y))

        pygame.display.set_caption("Menu Play")

        def load_btn(path, size=(300, 140)):
            img = pygame.image.load(path)
            return pygame.transform.scale(img, size)

        btn_img_play = load_btn(ROOT_LOCATION / "assets/images/ui/ui_btn_1_play.png")
        btn_img_boutique = load_btn(ROOT_LOCATION / "assets/images/ui/ui_btn_2_boutique.png")
        btn_img_option = load_btn(ROOT_LOCATION / "assets/images/ui/ui_btn_4_options.png")

        barre_laterale = pygame.image.load(ROOT_LOCATION / "assets/images/UI/menu/barre_lateral.png")
        barre_laterale = pygame.transform.scale(barre_laterale, (250, y))

        btn1_rect = btn_img_play.get_rect(topleft=(40,75))
        btn2_rect = btn_img_boutique.get_rect(topleft=(40,250))
        btn3_rect = btn_img_option.get_rect(topleft=(40,425))
                
        cube = Three_D(
            folder_images=ROOT_LOCATION / "assets/images/sprites/3d/robots",
            width=300,
            height=300,
            frame_delay=3  # 1 image toutes les 3 frames
        )
        print(f"Nombre d'images chargées : {cube.file_number}")
        running = True
        player_data=save_load.load_data(compte_file)
        player_data_pseudo=font.render(f"Salut {player_data["pseudo"]} !",True,TEXT_COLOR)
        player_data_money=font.render(f"Argents - {player_data["money"]}",True,TEXT_COLOR)
        font = pygame.font.Font(FONT_TEXT, 50)
        game_title=font.render(f"Nexus Extraction",True,TEXT_COLOR)
        birds = []
        bird_D=["left","right"]
        particles = [Particle() for _ in range(60)]
        fade_alpha = 255
        font = pygame.font.SysFont(None, 36)
        text_esc = font.render("Esc pour revenir en arrière...", True, (255, 255, 255))
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
                        play(compte_file)

                    if btn2_rect.collidepoint(mouse_pos):
                        boutique(compte_file)
                    
                    if btn3_rect.collidepoint(mouse_pos):
                        option_menu()

            screen.blit(BACKGROUND, (0, 0))
            screen.blit(text_esc, (LARGER_FENETRE-text_esc.get_width(), HAUTEUR_FENETRE-text_esc.get_height()))
            random_bird=randint(0,500)
            if(random_bird==0):
                birds.append(Bird(y=randint(0,HAUTEUR_FENETRE-100), direction=bird_D[randint(0,1)]))
            birds = [bird for bird in birds if bird.update()]  # update + supprime si sorti
            for bird in birds:
                bird.draw(screen)
            screen.blit(barre_laterale, (0, 0))
            screen.blit(btn_img_play, (40, 75))
            screen.blit(btn_img_boutique, (40, 250))
            screen.blit(btn_img_option, (40, 425))
            screen.blit(player_data_pseudo, (LARGER_FENETRE-player_data_pseudo.get_width()-180,(HAUTEUR_FENETRE-375)/2))
            screen.blit(player_data_money, (LARGER_FENETRE-player_data_money.get_width()-175,(HAUTEUR_FENETRE+375)/2))
            screen.blit(game_title, (((LARGER_FENETRE/2)-(game_title.get_width()/2)),(game_title.get_height()/2)))
            cube.update()
            cube.draw(screen, (LARGER_FENETRE-450),(HAUTEUR_FENETRE-300)/2)
            for p in particles:
                p.update()
                p.draw(screen)
            draw_fade()
            pygame.display.flip()
    except Exception:
        logger.error("play_menu ->", exc_info=True)