# Elvin Mouyart
# UTF-8
import pygame
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from config.config import *
from object.others.logger import logger

# --- Resolutions disponibles (16:9 uniquement) ---
RESOLUTIONS = [
    (1280, 720),
    (1600, 900),
    (1920, 1080),
    (2560, 1440),
]

# --- Couleurs de texte disponibles ---
TEXT_COLORS = [
    ((255, 255, 255), "Blanc"),
    ((255, 215, 0),   "Or"),
    ((125, 255, 0),   "Vert"),
    ((224, 175, 255), "Violet"),
    ((255, 100, 100), "Rouge"),
]


def save_config(resolution, fullscreen, text_color):
    """ecrit les nouvelles valeurs dans config/config.py."""
    config_path = ROOT / "config" / "config.py"

    with open(config_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("LARGER_FENETRE"):
            new_lines.append(f"LARGER_FENETRE={resolution[0]}\n")
        elif line.startswith("HAUTEUR_FENETRE"):
            new_lines.append(f"HAUTEUR_FENETRE={resolution[1]}\n")
        elif line.startswith("FULLSCREEN"):
            new_lines.append(f"FULLSCREEN={fullscreen}\n")
        elif line.startswith("TEXT_COLOR"):
            new_lines.append(f"TEXT_COLOR={text_color}\n")
        else:
            new_lines.append(line)

    with open(config_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    logger.info(f"Config sauvegardee : {resolution}, fullscreen={fullscreen}, color={text_color}")


def option_menu():
    pygame.init()

    x = LARGER_FENETRE
    y = HAUTEUR_FENETRE
    font_title = pygame.font.Font(FONT_SPECIAL, 36)
    font       = pygame.font.Font(FONT_TEXT, 20)
    font_small = pygame.font.Font(FONT_TEXT, 14)

    if FULLSCREEN:
        screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((x, y))
    pygame.display.set_caption("Options")

    try:
        background = pygame.image.load("./assets/images/background.png")
        background = pygame.transform.scale(background, (x, y))
    except:
        background = pygame.Surface((x, y))
        background.fill((30, 30, 40))

    # === Valeurs courantes (lues depuis config) ===
    current_res_index = 2  # 1920x1080 par defaut
    for i in range(len(RESOLUTIONS)):
        if RESOLUTIONS[i] == (LARGER_FENETRE, HAUTEUR_FENETRE):
            current_res_index = i

    current_color_index = 0
    for i in range(len(TEXT_COLORS)):
        if TEXT_COLORS[i][0] == TEXT_COLOR:
            current_color_index = i

    current_fullscreen = FULLSCREEN

    # Valeurs originales pour detecter si un redemarrage est necessaire
    original_res_index  = current_res_index
    original_fullscreen = current_fullscreen

    unsaved_changes = False
    needs_restart   = False

    # === Layout ===
    PANEL_X   = x // 2 - 400
    PANEL_W   = 800
    SECTION_Y = [200, 310, 420]

    btn_save_rect   = pygame.Rect(x//2 - 220, y - 120, 200, 55)
    btn_cancel_rect = pygame.Rect(x//2 + 20,  y - 120, 200, 55)

    # Zones cliquables des flèches (mises à jour dans le rendu)
    res_arrow_left  = pygame.Rect(0, 0, 30, 30)
    res_arrow_right = pygame.Rect(0, 0, 30, 30)
    col_arrow_left  = pygame.Rect(0, 0, 30, 30)
    col_arrow_right = pygame.Rect(0, 0, 30, 30)
    toggle_rect     = pygame.Rect(0, 0, 70, 30)

    clock   = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        # === evenements ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Si le popup est affiche, on gère uniquement son bouton OK
                if needs_restart:
                    btn_ok = pygame.Rect(x//2 - 60, y//2 + 45, 120, 40)
                    if btn_ok.collidepoint(mouse_pos):
                        needs_restart = False
                    continue

                # Resolution
                if res_arrow_left.collidepoint(mouse_pos):
                    current_res_index = (current_res_index - 1) % len(RESOLUTIONS)
                    unsaved_changes = True

                elif res_arrow_right.collidepoint(mouse_pos):
                    current_res_index = (current_res_index + 1) % len(RESOLUTIONS)
                    unsaved_changes = True

                # Couleur du texte
                elif col_arrow_left.collidepoint(mouse_pos):
                    current_color_index = (current_color_index - 1) % len(TEXT_COLORS)
                    unsaved_changes = True

                elif col_arrow_right.collidepoint(mouse_pos):
                    current_color_index = (current_color_index + 1) % len(TEXT_COLORS)
                    unsaved_changes = True

                # Plein ecran
                elif toggle_rect.collidepoint(mouse_pos):
                    current_fullscreen = not current_fullscreen
                    unsaved_changes = True

                # Bouton Sauvegarder
                elif btn_save_rect.collidepoint(mouse_pos):
                    save_config(
                        resolution = RESOLUTIONS[current_res_index],
                        fullscreen = current_fullscreen,
                        text_color = TEXT_COLORS[current_color_index][0],
                    )
                    unsaved_changes = False
                    if current_res_index != original_res_index or current_fullscreen != original_fullscreen:
                        needs_restart = True

                # Bouton Annuler
                elif btn_cancel_rect.collidepoint(mouse_pos):
                    return True

        # === Rendu ===
        screen.blit(background, (0, 0))

        # Overlay sombre
        overlay = pygame.Surface((x, y), pygame.SRCALPHA)
        overlay.fill((0, 0, 15, 160))
        screen.blit(overlay, (0, 0))

        # Titre
        title = font_title.render("OPTIONS", True, (200, 200, 255))
        screen.blit(title, (x//2 - title.get_width()//2, 100))

        # Panneau principal
        panel = pygame.Surface((PANEL_W, 380), pygame.SRCALPHA)
        panel.fill((20, 20, 35, 200))
        pygame.draw.rect(panel, (100, 100, 180), (0, 0, PANEL_W, 380), 2, border_radius=12)
        screen.blit(panel, (PANEL_X, 160))

        label_x   = PANEL_X + 30
        value_x   = PANEL_X + PANEL_W//2 + 20
        arrow_l_x = value_x - 45
        arrow_r_x = value_x + 215

        # --- ReSOLUTION ---
        sy = SECTION_Y[0]

        lbl = font.render("Resolution", True, (200, 200, 255))
        screen.blit(lbl, (label_x, sy))

        res_text = f"{RESOLUTIONS[current_res_index][0]} x {RESOLUTIONS[current_res_index][1]}"
        res_surf = font.render(res_text, True, (255, 255, 255))
        screen.blit(res_surf, (value_x + 90 - res_surf.get_width()//2, sy))

        hint = font_small.render("Necessite un redemarrage", True, (150, 150, 150))
        screen.blit(hint, (label_x, sy + 28))

        res_arrow_left  = pygame.Rect(arrow_l_x, sy, 30, 30)
        res_arrow_right = pygame.Rect(arrow_r_x, sy, 30, 30)
        col_l = (255, 255, 255) if res_arrow_left.collidepoint(mouse_pos) else (150, 150, 200)
        col_r = (255, 255, 255) if res_arrow_right.collidepoint(mouse_pos) else (150, 150, 200)
        pygame.draw.polygon(screen, col_l, [(arrow_l_x+20, sy+5), (arrow_l_x+20, sy+25), (arrow_l_x,    sy+15)])
        pygame.draw.polygon(screen, col_r, [(arrow_r_x,    sy+5), (arrow_r_x,    sy+25), (arrow_r_x+20, sy+15)])

        pygame.draw.line(screen, (60, 60, 100), (PANEL_X+20, sy+55), (PANEL_X+PANEL_W-20, sy+55))

        # --- COULEUR DU TEXTE ---
        sy = SECTION_Y[1]

        lbl = font.render("Couleur du texte", True, (200, 200, 255))
        screen.blit(lbl, (label_x, sy))

        col_color = TEXT_COLORS[current_color_index][0]
        col_name  = TEXT_COLORS[current_color_index][1]
        col_surf  = font.render(col_name, True, col_color)
        screen.blit(col_surf, (value_x + 90 - col_surf.get_width()//2, sy))

        pygame.draw.rect(screen, col_color,      (arrow_r_x + 35, sy, 25, 25))
        pygame.draw.rect(screen, (200, 200, 200), (arrow_r_x + 35, sy, 25, 25), 2)

        col_arrow_left  = pygame.Rect(arrow_l_x, sy, 30, 30)
        col_arrow_right = pygame.Rect(arrow_r_x, sy, 30, 30)
        col_l = (255, 255, 255) if col_arrow_left.collidepoint(mouse_pos) else (150, 150, 200)
        col_r = (255, 255, 255) if col_arrow_right.collidepoint(mouse_pos) else (150, 150, 200)
        pygame.draw.polygon(screen, col_l, [(arrow_l_x+20, sy+5), (arrow_l_x+20, sy+25), (arrow_l_x,    sy+15)])
        pygame.draw.polygon(screen, col_r, [(arrow_r_x,    sy+5), (arrow_r_x,    sy+25), (arrow_r_x+20, sy+15)])

        pygame.draw.line(screen, (60, 60, 100), (PANEL_X+20, sy+55), (PANEL_X+PANEL_W-20, sy+55))

        # --- PLEIN eCRAN ---
        sy = SECTION_Y[2]

        lbl = font.render("Plein ecran", True, (200, 200, 255))
        screen.blit(lbl, (label_x, sy))

        toggle_rect  = pygame.Rect(value_x, sy - 3, 70, 30)
        toggle_color = (60, 180, 80) if current_fullscreen else (80, 80, 100)
        pygame.draw.rect(screen, toggle_color,   (value_x, sy-3, 70, 30), border_radius=15)
        pygame.draw.rect(screen, (200, 200, 200), (value_x, sy-3, 70, 30), 2, border_radius=15)
        circle_x = value_x + 52 if current_fullscreen else value_x + 18
        pygame.draw.circle(screen, (255, 255, 255), (circle_x, sy + 12), 12)
        toggle_label = font_small.render("ON" if current_fullscreen else "OFF", True, (255, 255, 255))
        screen.blit(toggle_label, (value_x + (10 if current_fullscreen else 30), sy + 5))

        # --- Modifications non sauvegardees ---
        if unsaved_changes:
            warn = font_small.render("● Modifications non sauvegardees", True, (255, 180, 0))
            screen.blit(warn, (x//2 - warn.get_width()//2, y - 155))

        # --- Boutons ---
        save_color   = (60, 180, 80)  if btn_save_rect.collidepoint(mouse_pos)   else (40, 40, 80)
        cancel_color = (180, 60, 60)  if btn_cancel_rect.collidepoint(mouse_pos) else (40, 40, 80)

        pygame.draw.rect(screen, save_color,    btn_save_rect,   border_radius=10)
        pygame.draw.rect(screen, (200,200,200), btn_save_rect,   2, border_radius=10)
        pygame.draw.rect(screen, cancel_color,  btn_cancel_rect, border_radius=10)
        pygame.draw.rect(screen, (200,200,200), btn_cancel_rect, 2, border_radius=10)

        save_txt   = font.render("Sauvegarder", True, (255, 255, 255))
        cancel_txt = font.render("Annuler",     True, (255, 255, 255))
        screen.blit(save_txt,   (btn_save_rect.centerx   - save_txt.get_width()//2,   btn_save_rect.centery   - save_txt.get_height()//2))
        screen.blit(cancel_txt, (btn_cancel_rect.centerx - cancel_txt.get_width()//2, btn_cancel_rect.centery - cancel_txt.get_height()//2))

        esc_hint = font_small.render("eCHAP pour revenir", True, (100, 100, 120))
        screen.blit(esc_hint, (x//2 - esc_hint.get_width()//2, y - 40))

        # --- Popup redemarrage ---
        if needs_restart:
            overlay_popup = pygame.Surface((x, y), pygame.SRCALPHA)
            overlay_popup.fill((0, 0, 0, 180))
            screen.blit(overlay_popup, (0, 0))

            popup = pygame.Rect(x//2 - 300, y//2 - 90, 600, 180)
            pygame.draw.rect(screen, (20, 20, 40),  popup, border_radius=12)
            pygame.draw.rect(screen, (255, 180, 0), popup, 3, border_radius=12)

            msg1 = font.render("Redemarrage necessaire", True, (255, 180, 0))
            msg2 = font_small.render("Les changements de resolution et de plein ecran", True, (200, 200, 200))
            msg3 = font_small.render("seront appliques au prochain lancement du jeu.", True, (200, 200, 200))
            screen.blit(msg1, (x//2 - msg1.get_width()//2, y//2 - 70))
            screen.blit(msg2, (x//2 - msg2.get_width()//2, y//2 - 25))
            screen.blit(msg3, (x//2 - msg3.get_width()//2, y//2 - 5))

            btn_ok   = pygame.Rect(x//2 - 60, y//2 + 45, 120, 40)
            ok_color = (60, 120, 200) if btn_ok.collidepoint(mouse_pos) else (40, 80, 150)
            pygame.draw.rect(screen, ok_color,       btn_ok, border_radius=8)
            pygame.draw.rect(screen, (200, 200, 200), btn_ok, 2, border_radius=8)
            ok_txt = font.render("OK", True, (255, 255, 255))
            screen.blit(ok_txt, (btn_ok.centerx - ok_txt.get_width()//2, btn_ok.centery - ok_txt.get_height()//2))

        pygame.display.flip()