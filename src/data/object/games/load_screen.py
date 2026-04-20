# Elvin Mouyart
# UTF-8
import pygame
import time
from ..personnages.bird import *
from ..others.particule import *
from ..others.assets_manager import Assets_manager
from random import randint
from config.config import *
from object.others.logger import logger
from .play_menu import *

def load_menu(compte_file):
    logger.info(f"Entrez dans load_menu avec le compte -> {compte_file}")
    try:
        pygame.init()
        x = LARGER_FENETRE
        y = HAUTEUR_FENETRE
        normal_font = pygame.font.SysFont(None, 36)

        if FULLSCREEN:
            screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((x, y))

        pygame.display.set_caption("Nexus Extraction - Load Menu")

        title_img = pygame.image.load(ROOT_LOCATION / "assets/images/images/title.png")
        title_img = pygame.transform.scale(title_img, (1200, 125))
        birds = []
        bird_D = ["left", "right"]
        particles = [Particle() for _ in range(60)]
        fade_alpha = 255
        start_time = time.time()
        converted = False


        asset_manager = Assets_manager(ELEMENT_LOAD, ELEMENT_LOAD_SIZE, ELEMENT_LOAD_NAME)

        def text_load():
            nonlocal start_time
            points = int(time.time() - start_time)
            if time.time() - start_time >= 4:
                start_time = time.time()
            text = "chargement" + "." * points
            surface = normal_font.render(text, True, TEXT_COLOR)
            bg = pygame.Surface((surface.get_width() + 10, surface.get_height() + 6), pygame.SRCALPHA)
            bg.fill((0, 0, 0, 180))
            final = pygame.Surface((surface.get_width() + 10, surface.get_height() + 6), pygame.SRCALPHA)
            final.blit(bg, (0, 0))
            final.blit(surface, (5, 3))
            return final

        def draw_fade():
            nonlocal fade_alpha
            if fade_alpha > 0:
                fade_alpha -= 4
                fade = pygame.Surface((LARGER_FENETRE, HAUTEUR_FENETRE))
                fade.fill((0, 0, 0))
                fade.set_alpha(fade_alpha)
                screen.blit(fade, (0, 0))

        def DrawBar(pos, size, borderC, barC, progress):
            pygame.draw.rect(screen, borderC, (*pos, *size), 1)
            innerPos  = (pos[0]+3, pos[1]+3)
            innerSize = ((size[0]-6) * progress, size[1]-6)
            pygame.draw.rect(screen, barC, (*innerPos, *innerSize))

        running = True
        while running:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    running=False
                    return False
                if keys[pygame.K_e]:
                    birds.append(Bird(y=randint(0, HAUTEUR_FENETRE-100), direction=bird_D[randint(0,1)]))

            # chargement terminé → convert + redirect
            if asset_manager.loaded and not converted:
                for key in asset_manager.element_load:
                    asset_manager.element_load[key] = asset_manager.element_load[key].convert_alpha()
                converted = True
                logger.info("Assets chargés, redirect vers play_menu")
                play_menu(compte_file=compte_file, death=False, asset_manager=asset_manager)
                return True

            birds = [bird for bird in birds if bird.update()]
            for bird in birds:
                bird.draw(screen)
            screen.blit(title_img, ((LARGER_FENETRE - title_img.get_width()) // 2, title_img.get_height()//4))
            for p in particles:
                p.update()
                p.draw(screen)
            draw_fade()
            DrawBar(
                (LARGER_FENETRE/10, HAUTEUR_FENETRE-100),
                ((LARGER_FENETRE/10)*7, 50),
                (0, 255, 0),
                (139, 0, 139),
                asset_manager.get_load_completion() / 100
            )
            screen.blit(text_load(), (LARGER_FENETRE/10, HAUTEUR_FENETRE-135))
            pygame.display.flip()

    except Exception:
        logger.error("load_menu ->", exc_info=True)