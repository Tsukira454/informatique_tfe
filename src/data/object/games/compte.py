# Elvin Mouyart
# UTF-8
import pygame
import os
from ..others.save import save_load
from ..others.button_compte import *
from ..others.logger import logger
from ..others.save import *
from config.config import *
from .load_screen import *

def compte_menu():
    logger.info("Entrez dans compte")
    try:
        pygame.init()
        x = LARGER_FENETRE
        y = HAUTEUR_FENETRE
        font        = pygame.font.Font(FONT_TEXT, 24)
        font_title  = pygame.font.Font(FONT_SPECIAL, 48)
        font_medium = pygame.font.Font(FONT_TEXT, 20)

        if FULLSCREEN:
            screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((x, y))
        pygame.display.set_caption("Compte - ?")

        refresh_btn = pygame.transform.scale(
            pygame.image.load(ROOT_LOCATION / "assets/images/ui/refresh_btn.png"), (48, 48))
        refresh_btn_rect = refresh_btn.get_rect(topleft=(PANEL_LEFT_W - 70, 20))

        def draw_panel(px, py, pw, ph, title_str, color=(255, 60, 60)):
            panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
            panel.fill((10, 10, 20, 200))
            pygame.draw.rect(panel, color, (0, 0, pw, ph), 2, border_radius=16)
            screen.blit(panel, (px, py))
            t = font.render(title_str, True, color)
            screen.blit(t, (px + pw//2 - t.get_width()//2, py + 15))
            pygame.draw.line(screen, color, (px + 20, py + 55), (px + pw - 20, py + 55), 1)

        def compte_load():
            compte_list = []
            compte_list_rect = []
            compte_child = []

            button_new = ButtonCompte(new=True, file=False, data=False)
            surface_new = button_new.button_img()
            rect_new = surface_new.get_rect(topleft=(
                PANEL_LEFT_W//2 - CARD_W//2, 80))
            compte_list.append(surface_new)
            compte_list_rect.append(rect_new)
            compte_child.append(button_new)

            i = 0
            for fichier in os.listdir(ACCOUNT_LOCATION):
                if fichier.lower().endswith(".json") and i < MAX_COMPTES:
                    data = save_load.load_data(file=fichier)
                    if data is None:
                        continue
                    btn = ButtonCompte(new=False, file=fichier, data=data)
                    surface = btn.button_img()
                    rect = surface.get_rect(topleft=(
                        PANEL_LEFT_W//2 - CARD_W//2,
                        80 + CARD_H + CARD_MARGIN + i * (CARD_H + CARD_MARGIN)
                    ))
                    compte_list.append(surface)
                    compte_list_rect.append(rect)
                    compte_child.append(btn)
                    i += 1

            return compte_list, compte_list_rect, compte_child

        compte_list, compte_list_rect, compte_child = compte_load()

        def draw_popup(screen, font, input_text):
            popup = pygame.Rect(0, 0, 500, 240)
            popup.center = (x//2, y//2)
            overlay = pygame.Surface((x, y), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen, (10, 10, 20),    popup, border_radius=16)
            pygame.draw.rect(screen, (255, 60, 60),   popup, 2, border_radius=16)
            title = font.render("Entrer votre pseudo", True, (255, 60, 60))
            screen.blit(title, (popup.x + 20, popup.y + 20))
            pygame.draw.line(screen, (255, 60, 60), (popup.x + 20, popup.y + 55), (popup.x + 480, popup.y + 55), 1)
            input_rect = pygame.Rect(popup.x + 20, popup.y + 75, 460, 44)
            pygame.draw.rect(screen, (20, 20, 35),    input_rect, border_radius=8)
            pygame.draw.rect(screen, (100, 100, 180), input_rect, 2, border_radius=8)
            text_surface = font.render(input_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))
            validate_rect = pygame.Rect(popup.x + 60,  popup.y + 150, 140, 44)
            cancel_rect   = pygame.Rect(popup.x + 300, popup.y + 150, 140, 44)
            pygame.draw.rect(screen, (40, 160, 80),  validate_rect, border_radius=10)
            pygame.draw.rect(screen, (160, 40, 40),  cancel_rect,   border_radius=10)
            screen.blit(font.render("Ok", True, (255,255,255)), validate_rect.move(45, 8))
            screen.blit(font.render("X",  True, (255,255,255)), cancel_rect.move(55, 8))
            return validate_rect, cancel_rect

        running = True
        popup_open = False
        input_text = ""
        validate_rect = None
        cancel_rect = None

        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False

                if popup_open:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            popup_open = False
                        elif event.key == pygame.K_ESCAPE:
                            popup_open = False
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            if len(input_text) < 20:
                                input_text += event.unicode
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if validate_rect and validate_rect.collidepoint(event.pos):
                            if len(input_text) >= 3:
                                popup_open = False
                                compte_child[0].button_fontion(pseudo=input_text)
                                compte_list, compte_list_rect, compte_child = compte_load()
                        elif cancel_rect and cancel_rect.collidepoint(event.pos):
                            popup_open = False
                    continue

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    return True

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if refresh_btn_rect.collidepoint(event.pos):
                        compte_list, compte_list_rect, compte_child = compte_load()
                    elif compte_list_rect[0].collidepoint(event.pos):
                        popup_open = True
                        input_text = ""
                    else:
                        for i in range(1, len(compte_list)):
                            if compte_list_rect[i].collidepoint(event.pos):
                                selected_file = compte_child[i].button_fontion()
                                load_menu(compte_file=selected_file)
                                return True

            # === RENDU ===
            screen.blit(BACKGROUND, (0, 0))
            overlay = pygame.Surface((x, y), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            # === PANNEAU GAUCHE ===
            draw_panel(20, 20, PANEL_LEFT_W - 40, y - 40, "SELECTION DU COMPTE")
            screen.blit(refresh_btn, refresh_btn_rect)

            # cards avec hover
            for i, (surface, rect) in enumerate(zip(compte_list, compte_list_rect)):
                hovered = rect.collidepoint(mouse_pos)
                surface = compte_child[i].button_img(hovered=hovered)
                screen.blit(surface, rect)

            # === PANNEAU DROIT ===
            draw_panel(PANEL_LEFT_W + 20, 20, PANEL_RIGHT_W - 40, y - 40, "LEADERBOARD", color=(255, 215, 0))
            soon = font_medium.render("(bientot disponible)", True, (100, 100, 130))
            screen.blit(soon, (
                PANEL_LEFT_W + 20 + (PANEL_RIGHT_W - 40)//2 - soon.get_width()//2,
                y//2
            ))

            if popup_open:
                validate_rect, cancel_rect = draw_popup(screen, font, input_text)

            pygame.display.flip()

    except Exception:
        logger.error("Compte_menu ->", exc_info=True)