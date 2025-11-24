import pygame  # type: ignore

def main_menu(x=1920, y=1080):
    pygame.init()

    screen = pygame.display.set_mode((x, y))  # Pas fullscreen forcé
    pygame.display.toggle_fullscreen()        # Fullscreen borderless

    # Background
    background = pygame.image.load("./assets/images/background.png")
    background = pygame.transform.scale(background, (x, y))

    # Bouton unique, utilisé 3 fois
    btn_img = pygame.image.load("./assets/ui/ui_btn_4.png")
    btn_img = pygame.transform.scale(btn_img, (300, 100))  # taille personnalisable

    # Rect des boutons (x, y automatiques)
    btn1_rect = btn_img.get_rect(center=(x//2, y//2 - 150))
    btn2_rect = btn_img.get_rect(center=(x//2, y//2))
    btn3_rect = btn_img.get_rect(center=(x//2, y//2 + 150))

    running = True
    while running:
        for event in pygame.event.get():
            # Fermer la fenêtre
            if event.type == pygame.QUIT:
                running = False

            # Clic souris
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if btn1_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    return 1

                if btn2_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    return 2

                if btn3_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    return 3

        # Affichage
        screen.blit(background, (0, 0))
        screen.blit(btn_img, btn1_rect)
        screen.blit(btn_img, btn2_rect)
        screen.blit(btn_img, btn3_rect)

        pygame.display.flip()

    pygame.quit()
    return None  # si fermé autrement
