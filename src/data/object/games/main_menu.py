import pygame
from random import randint
# === Import config propre === #
from config.config import *
from object.others.particule import Particle
from .credit import credit_menu
from object.others.logger import logger
from object.personnages.bird import Bird


def main_menu():
    logger.info("Main Menu")
    try:
        pygame.init()
        x = LARGER_FENETRE
        y = HAUTEUR_FENETRE
        font = pygame.font.Font(FONT_TEXT, 24)

        # --- Configuration fenêtre --- #
        if FULLSCREEN:
            screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((x, y))

        pygame.display.set_caption("Menu Principal")

        # --- Fonction utilitaire pour charger un bouton --- #
        def load_btn(path, size=(300, 140)):
            img = pygame.image.load(path)
            return pygame.transform.scale(img, size)

        btn_img_play = load_btn(ROOT_LOCATION / "./assets/images/ui/ui_btn_4_play.png")
        btn_img_option = load_btn(ROOT_LOCATION / "./assets/images/ui/ui_btn_4_options.png")
        btn_img_quitter = load_btn(ROOT_LOCATION / "./assets/images/ui/ui_btn_4_quitter.png")
        title_img=pygame.image.load(ROOT_LOCATION / "assets/images/images/title.png")
        title_img=pygame.transform.scale(title_img, (1200,125))
        btn_credit = pygame.Surface((150, 40), pygame.SRCALPHA)

        text_credit = font.render("Credits", True, (255, 255, 255))

        # --- Position des boutons --- #
        btn1_rect = btn_img_play.get_rect(center=(x//2, y//2 - 150))
        btn2_rect = btn_img_option.get_rect(center=(x//2, y//2))
        btn3_rect = btn_img_quitter.get_rect(center=(x//2, y//2 + 150))
        btn_credit_rect = btn_credit.get_rect(bottomright=(LARGER_FENETRE - 20, HAUTEUR_FENETRE - 10))
        particles = [Particle() for _ in range(60)]
        running = True
        fade_alpha = 255
        # bird
        birds = []
        bird_D=["left","right"]
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
                    return 3

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    if btn1_rect.collidepoint(mouse_pos):
                        return 1

                    if btn2_rect.collidepoint(mouse_pos):
                        return 2

                    if btn3_rect.collidepoint(mouse_pos):
                        return 3
                    if btn_credit_rect.collidepoint(mouse_pos):
                        credit_menu()
            screen.blit(BACKGROUND, (0, 0))
            random_bird=randint(0,500)
            if(random_bird==0):
                birds.append(Bird(y=randint(0,HAUTEUR_FENETRE-100), direction=bird_D[randint(0,1)]))
            birds = [bird for bird in birds if bird.update()]  # update + supprime si sorti
            for bird in birds:
                bird.draw(screen)
            screen.blit(btn_img_play, btn1_rect)
            screen.blit(btn_img_option, btn2_rect)
            screen.blit(btn_img_quitter, btn3_rect)
            screen.blit(text_credit, (LARGER_FENETRE-150, HAUTEUR_FENETRE-35))
            screen.blit(btn_credit, (150, 35))
            screen.blit(title_img, ((LARGER_FENETRE - title_img.get_width()) // 2, (title_img.get_height()//2)))
            for p in particles:
                p.update()
                p.draw(screen)
            draw_fade()
            pygame.display.flip()

        pygame.quit()
        return None
    except Exception:
        logger.error("Main_menu erreur -> ", exc_info=True)