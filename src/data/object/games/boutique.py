# Elvin Mouyart
# UTF-8
import pygame
from ..others.button_boutique import ButtonBoutique
from config.config import *
from ..ui.Three_D import *
from ..others.save import *

def boutique(compte_file, asset_manager=None):
    pygame.init()
    font = pygame.font.Font(FONT_TEXT, 80)
    if FULLSCREEN:
        screen = pygame.display.set_mode((LARGER_FENETRE, HAUTEUR_FENETRE), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((LARGER_FENETRE, HAUTEUR_FENETRE))

    pygame.display.set_caption("Menu Play")
    
    # === Boutique ===
    boutique_bg = asset_manager.get_element("boutique_bg")
    cube = Three_D(
        images=[asset_manager.get_element(f"robot_3d_{i:04d}") for i in range(1, 241)],
        frame_delay=3
    )
    def load_boutique():
        frame_list = []
        btn_list = []  # on garde les objets aussi
        for i in range(len(BOUTIQUE_ITEM)):
            btn = ButtonBoutique(BOUTIQUE_ITEM[i], BOUTIQUE_ITEM[i], compte_file)
            frame_list.append(btn.get_hud())
            btn_list.append(btn)
        data_player =save_load.load_data(compte_file)
        prix = font.render(f"Votre argents {data_player["money"]}",True,TEXT_COLOR)
        return frame_list, btn_list, prix
    btn_rects = []
    boutique_title = font.render("Boutique",True,TEXT_COLOR)
    font = pygame.font.Font(FONT_TEXT, 24)
    frame_list, btn_list, prix = load_boutique()

    running = True

    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for i in range(len(btn_rects)):
                    if btn_rects[i].collidepoint(mouse_pos):
                        success = btn_list[i].buy()
                        if success:
                            frame_list, btn_list, prix = load_boutique()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                running = False


        screen.blit(BACKGROUND, (0,0))
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
        cube.update()
        cube.draw(screen, (LARGER_FENETRE-450),(HAUTEUR_FENETRE-300)/2)
        screen.blit(boutique_title, ((LARGER_FENETRE/2)-boutique_title.get_width(), 40))
        screen.blit(prix, (LARGER_FENETRE-prix.get_width()-175,(HAUTEUR_FENETRE+375)/2))
        pygame.display.flip()
