# Elvin Mouyart
# UTF-8
import pygame
import os
from ..others.save import save_load
from ..others.button_compte import *
from ..others.logger import logger
from ..others.save import *
from config.config import *
from ..others.button_compte import *

def compte_menu():
    logger.info("Entrez dans compte")
    try:
        pygame.init()
        x = LARGER_FENETRE
        y = HAUTEUR_FENETRE
        block_size = 32
        font = pygame.font.Font(FONT_TEXT, 24)

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
        validate_rect = pygame.Rect(0, 0, 120, 40)
        cancel_rect = pygame.Rect(0, 0, 120, 40)
        refresh_btn = load_btn("./assets/ui/refresh_btn.png", (96,96)) 

        refresh_btn_rect = refresh_btn.get_rect(topleft=((LARGER_FENETRE//10)*6, 125))

        # === Chargement des comptes ===
        def compte_load():
            compte_list=[]
            compte_list_rect=[]
            compte_child=[]
            # premier btn est la création d'un compte
            button_new = ButtonCompte(new=True, file=False, data=False)
            surface_btn_new = button_new.button_img()
            create_compte_btn_rect = surface_btn_new.get_rect(topleft=(LARGER_FENETRE//2-300, (0+1)*250))
            compte_list.append(surface_btn_new)
            compte_list_rect.append(create_compte_btn_rect)
            compte_child.append(button_new)
            # compte :
            i=0
            for fichier in os.listdir(ACCOUNT_LOCATION):
                if fichier.lower().endswith(".json"):
                    data = save_load.load_data(file=fichier)
                    button_compte = ButtonCompte(new=False, file=fichier, data=data)
                    button_compte_img = button_compte.button_img()
                    button_compte_rect=button_compte_img.get_rect(topleft=(LARGER_FENETRE//2-300, (i+1)*250))
                    compte_list.append(button_compte_img)
                    compte_child.append(button_compte)
                    compte_list_rect.append(button_compte_rect)
                    i+=1
            return compte_list, compte_list_rect, compte_child
        compte_list, compte_list_rect, compte_child = compte_load()
    
        # == pop up ===
        def draw_popup(screen, font, input_text):
            popup = pygame.Rect(0, 0, 450, 220)
            popup.center = (x // 2, y // 2)

            # fond sombre
            overlay = pygame.Surface((x, y), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            # popup
            pygame.draw.rect(screen, (50, 50, 80), popup, border_radius=12)
            pygame.draw.rect(screen, (200, 200, 255), popup, 3, border_radius=12)

            title = font.render("Entrer votre pseudo", True, (255, 255, 255))
            screen.blit(title, (popup.x + 20, popup.y + 20))

            # input box
            input_rect = pygame.Rect(popup.x + 20, popup.y + 70, 410, 40)
            pygame.draw.rect(screen, (30, 30, 50), input_rect, border_radius=6)
            pygame.draw.rect(screen, (120, 120, 200), input_rect, 2, border_radius=6)

            text_surface = font.render(input_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 8, input_rect.y + 8))

            # boutons
            validate_rect = pygame.Rect(popup.x + 60, popup.y + 140, 120, 40)
            cancel_rect = pygame.Rect(popup.x + 270, popup.y + 140, 120, 40)

            pygame.draw.rect(screen, (60, 180, 100), validate_rect, border_radius=8)
            pygame.draw.rect(screen, (180, 60, 60), cancel_rect, border_radius=8)

            screen.blit(font.render("Ok", True, (0, 0, 0)), validate_rect.move(22, 8))
            screen.blit(font.render("X", True, (0, 0, 0)), cancel_rect.move(18, 8))

            return validate_rect, cancel_rect

        running = True
        popup_open = False
        input_text = ""
        validate_rect = None
        cancel_rect = None

        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    return False

                # ================= POPUP ACTIVE =================
                if popup_open:

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            logger.info(f"Nom entré : {input_text}")
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
                            logger.info(f"Nom validé : {input_text}")
                            if len(input_text) > 0:
                                popup_open = False
                                compte_child[0].button_fontion(pseudo=input_text)
                                compte_list, compte_list_rect, compte_child = compte_load()

                        elif cancel_rect and cancel_rect.collidepoint(event.pos):
                            popup_open = False

                    continue  # ⛔ bloque le reste du menu

                # ================= MENU NORMAL =================
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        return True

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    if refresh_btn_rect.collidepoint(mouse_pos):
                        compte_list, compte_list_rect, compte_child = compte_load()
                        logger.info("Compte rafraichi")

                    if compte_list_rect[0].collidepoint(mouse_pos):
                        logger.info("Création d'un compte...")
                        popup_open = True
                        input_text = ""
                    else:
                        print("prout")
                        for i in range(len(compte_list)-1):
                            if compte_list_rect[i].collidepoint(mouse_pos):
                                print("caca")
                                return compte_child[i].button_fontion()


            screen.blit(background, (0, 0))
            screen.blit(text_title, ((LARGER_FENETRE//10)*5-75, 50))
            screen.blit(refresh_btn, ((LARGER_FENETRE//10)*6, 125))
            for i in range(len(compte_list)):
                screen.blit(compte_list[i], (LARGER_FENETRE//2-250, (HAUTEUR_FENETRE//10)+(i+1)*175))
            if popup_open:
                validate_rect, cancel_rect = draw_popup(screen, font, input_text)

            pygame.display.flip()
    except Exception:
        logger.error("Compte_menu ->", exc_info=True)
