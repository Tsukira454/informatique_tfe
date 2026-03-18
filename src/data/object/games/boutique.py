# Elvin Mouyart
# UTF-8
import pygame
from ..others.button_boutique import ButtonBoutique
from config.config import *

def boutique(compte_file):
    pygame.init()

    if FULLSCREEN:
        screen = pygame.display.set_mode((LARGER_FENETRE, HAUTEUR_FENETRE), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((LARGER_FENETRE, HAUTEUR_FENETRE))

    pygame.display.set_caption("Menu Play")

    # === Chargement images bg ===
    background = pygame.image.load(ROOT_LOCATION / "assets/images/images/background.png")
    background = pygame.transform.scale(background, (LARGER_FENETRE, HAUTEUR_FENETRE))
    
    # === Boutique ===
    boutique_bg = pygame.image.load(ROOT_LOCATION / "assets/images/UI/boutique/boutique_bg.png")
    boutique_bg = pygame.transform.scale(boutique_bg, (int((LARGER_FENETRE/7)*5), HAUTEUR_FENETRE))

    def load_boutique():
        frame_list = []
        btn_list = []  # on garde les objets aussi
        for i in range(len(BOUTIQUE_ITEM)):
            btn = ButtonBoutique(BOUTIQUE_ITEM[i], BOUTIQUE_ITEM[i], compte_file)
            frame_list.append(btn.get_hud())
            btn_list.append(btn)
        return frame_list, btn_list
    btn_rects = []
    frame_list, btn_list = load_boutique()
    running = True

    while running:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for i in range(len(btn_rects)):
                    if btn_rects[i].collidepoint(mouse_pos):
                        success = btn_list[i].buy()
                        if success:
                            frame_list, btn_list = load_boutique()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                running = False


        screen.blit(background, (0,0))
        screen.blit(boutique_bg, (0,0))
        h = 0
        l = 0
        btn_rects = []
        for i in range(len(frame_list)):
            if i % 6 == 0:
                h += 1
                l = 0
            pos = (100 + (200 * l), (200 * h))
            screen.blit(frame_list[i], pos)
            btn_rects.append(pygame.Rect(pos[0], pos[1], 150, 220))
            l += 1
        h = 0
        


        pygame.display.flip()
