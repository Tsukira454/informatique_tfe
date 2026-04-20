# Elvin Mouyart
# UTF-8
import pygame
from .option_menu import option_menu
from .play import play
from .boutique import boutique
from ..others.save import save_load
from ..ui.Three_D import *
from ..personnages.bird import *
from ..others.particule import *
from random import randint
from config.config import *
from object.others.logger import logger
from object.others.audio_manager import play_bg_music

def play_menu(compte_file, death=False, asset_manager=None):
    logger.info(f"Entrez dans play_menu avec le compte {compte_file}")
    if(asset_manager!=None):
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

            btn_img_play = asset_manager.get_element("btn_play_menu")
            btn_img_boutique = asset_manager.get_element("btn_boutique_menu")
            btn_img_option = asset_manager.get_element("btn_option_menu")
            barre_laterale = asset_manager.get_element("barre_laterale")

            btn1_rect = btn_img_play.get_rect(topleft=(40,75))
            btn2_rect = btn_img_boutique.get_rect(topleft=(40,250))
            btn3_rect = btn_img_option.get_rect(topleft=(40,425))
                    
            cube = Three_D(
                images=[asset_manager.get_element(f"robot_3d_{i:04d}") for i in range(1, 241)],
                frame_delay=3
            )
            running = True
            player_data=save_load.load_data(compte_file)
            player_data_pseudo=font.render(f"Salut {player_data["pseudo"]} !",True,TEXT_COLOR)
            player_data_money=font.render(f"Argents - {player_data["money"]}",True,TEXT_COLOR)
            title_img=asset_manager.get_element("title")
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
            clock = pygame.time.Clock()
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

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = event.pos

                        if btn1_rect.collidepoint(mouse_pos):
                            play(compte_file, asset_manager=asset_manager,maps_level=0)

                        if btn2_rect.collidepoint(mouse_pos):
                            boutique(compte_file, asset_manager=asset_manager)
                        
                        if btn3_rect.collidepoint(mouse_pos):
                            option_menu()

                screen.blit(BACKGROUND, (0, 0))
                screen.blit(text_esc, (LARGER_FENETRE-text_esc.get_width(), HAUTEUR_FENETRE-text_esc.get_height()))
                random_bird=randint(0,500)
                if(random_bird==0):
                    birds.append(Bird(y=randint(0, HAUTEUR_FENETRE-100), direction=bird_D[randint(0,1)], asset_manager=asset_manager))
                birds = [bird for bird in birds if bird.update()]  # update + supprime si sorti
                for bird in birds:
                    bird.draw(screen)
                screen.blit(barre_laterale, (0, 0))
                screen.blit(btn_img_play, (40, 75))
                screen.blit(btn_img_boutique, (40, 250))
                screen.blit(btn_img_option, (40, 425))
                screen.blit(player_data_pseudo, (LARGER_FENETRE-player_data_pseudo.get_width()-180,(HAUTEUR_FENETRE-375)/2))
                screen.blit(player_data_money, (LARGER_FENETRE-player_data_money.get_width()-175,(HAUTEUR_FENETRE+375)/2))
                screen.blit(title_img, ((LARGER_FENETRE - title_img.get_width()) // 2, (title_img.get_height()//4)))
                cube.update()
                cube.draw(screen, (LARGER_FENETRE-450),(HAUTEUR_FENETRE-300)/2)
                for p in particles:
                    p.update()
                    p.draw(screen)
                draw_fade()
                pygame.display.flip()
        except Exception:
            logger.error("play_menu ->", exc_info=True)
    else:
        logger.error("play_menu -> assets manager vide")