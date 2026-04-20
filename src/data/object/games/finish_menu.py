import pygame
import math
from config.config import *
from ..others.save import *
from ..others.leaderboard_api import submit_score
from object.others.logger import logger
from object.others.audio_manager import stop_bg_music, play_fx

def finish_menu(reward, compte_file, asset_manager=None, maps_level=0):
    pygame.init()
    x = LARGER_FENETRE
    y = HAUTEUR_FENETRE
    font_title  = pygame.font.Font(FONT_SPECIAL, 72)
    font_text   = pygame.font.Font(FONT_TEXT, 20)
    font_medium = pygame.font.Font(FONT_TEXT, 24)
    font_big    = pygame.font.Font(FONT_TEXT, 32)

    if FULLSCREEN:
        screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((x, y))
    pygame.display.set_caption("Mort :/")

    # === Assets ===

    # icones blocs
    block_icons = {}
    for bloc in REWARD_VALEUR.keys():
        img = asset_manager.get_element(bloc)
        if img:
            block_icons[bloc] = pygame.transform.scale(img, (40, 40))

    # === Calcul reward ===
    reward_final = 0
    for bloc, valeur in REWARD_VALEUR.items():
        if bloc in reward:
            reward_final += reward[bloc] * valeur

    # === Sauvegarde ===
    data = save_load.load_data(compte_file)
    data = save_load.build_data(
        file=compte_file,
        pseudo=data["pseudo"],
        money=(data["money"] + reward_final),
        inventory=data["inventory"]
    )
    save_load.save_data(file=compte_file, data=data)
    if "uuid" in data:
        submit_score(account_uuid=data["uuid"], pseudo=data["pseudo"], money=data["money"])
    stop_bg_music()
    play_fx(ROOT_LOCATION / "assets/music/music_nexus_death.wav")

    # === Titre animé ===
    title_surf  = font_title.render("EXTRACTION TERMINEE", True, (255, 60, 60))
    title_y     = -100  # démarre hors écran
    title_target = 60

    space_text = font_medium.render("Appuyer sur 'espace' pour continuer...", True, (255,60,60))
    # === Panneaux ===
    PANEL_W = (x // 2) - 80
    PANEL_H = y - 280
    PANEL_Y = 160

    def draw_panel(px, py, pw, ph, title_str):
        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        panel.fill((10, 10, 20, 200))
        pygame.draw.rect(panel, (255, 60, 60), (0, 0, pw, ph), 2, border_radius=16)
        screen.blit(panel, (px, py))
        t = font_medium.render(title_str, True, (255, 60, 60))
        screen.blit(t, (px + pw // 2 - t.get_width() // 2, py + 15))
        pygame.draw.line(screen, (255, 60, 60), (px + 20, py + 55), (px + pw - 20, py + 55), 1)

    def draw_butin(px, py):
        draw_panel(px, py, PANEL_W, PANEL_H, "BUTIN")
        scroll_y = 75
        for bloc, valeur in REWARD_VALEUR.items():
            if bloc not in reward or reward[bloc] == 0:
                continue
            if scroll_y + 50 > PANEL_H:
                break
            # icone depuis block_icons directement
            if bloc in block_icons:
                screen.blit(block_icons[bloc], (px + 20, py + scroll_y))
            else:
                # fallback si pas d'icone
                pygame.draw.rect(screen, (100, 100, 100), (px + 20, py + scroll_y, 40, 40))
            
            nom = font_text.render(bloc.replace("_", " "), True, (200, 200, 200))
            screen.blit(nom, (px + 70, py + scroll_y + 5))
            
            qte = font_text.render(f"x{reward[bloc]}", True, (255, 255, 100))
            val = font_text.render(f"= {reward[bloc] * valeur} coins", True, (100, 255, 150))
            screen.blit(qte, (px + PANEL_W - 200, py + scroll_y + 5))
            screen.blit(val, (px + PANEL_W - 140, py + scroll_y + 5))
            scroll_y += 48
            
    def draw_stats(px, py):
        draw_panel(px, py, PANEL_W, PANEL_H, "STATS")
        # total coins gagnés
        t1 = font_big.render(f"+ {int(reward_final)} coins", True, (255, 215, 0))
        screen.blit(t1, (px + PANEL_W // 2 - t1.get_width() // 2, py + 80))
        # total blocs minés
        total_blocs = sum(reward.get(b, 0) for b in REWARD_VALEUR)
        t2 = font_medium.render(f"Blocs mines : {total_blocs}", True, (200, 200, 255))
        screen.blit(t2, (px + PANEL_W // 2 - t2.get_width() // 2, py + 150))
        # solde total
        solde = font_medium.render(f"Solde total : {int(data['money'])} coins", True, (100, 255, 180))
        screen.blit(solde, (px + PANEL_W // 2 - solde.get_width() // 2, py + 210))

    clock = pygame.time.Clock()
    running = True
    timer = 0

    while running:
        clock.tick(60)
        timer += 1

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_SPACE]:
                pygame.quit()
                from object.games.play_menu import play_menu
                play_menu(compte_file, death=True, asset_manager=asset_manager)
                return
            

        # === titre descend avec easing ===
        if title_y < title_target:
            title_y += max(2, (title_target - title_y) * 0.12)

        # === fond ===
        screen.blit(BACKGROUND, (0, 0))
        overlay = pygame.Surface((x, y), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        # === titre ===
        # effet pulse sur la couleur
        pulse = int(abs(math.sin(timer * 0.05)) * 80)
        title_surf = font_title.render("EXTRACTION TERMINEE", True, (255, 60 + pulse, 60))
        screen.blit(title_surf, (x // 2 - title_surf.get_width() // 2, int(title_y)))

        # === panneaux ===
        draw_butin(40, PANEL_Y)
        draw_stats(x // 2 + 40, PANEL_Y)
        
        # === space to leave ===
        pulse_alpha = int(abs(math.sin(timer * 0.05)) * 155) + 100
        space_text = font_medium.render("Appuyer sur 'espace' pour continuer...", True, (255, 60, 60))
        space_text.set_alpha(pulse_alpha)
        screen.blit(space_text, (x // 2 - space_text.get_width() // 2, y - 60))

        pygame.display.flip()

    pygame.quit()
    return None