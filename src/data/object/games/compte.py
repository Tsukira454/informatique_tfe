# Elvin Mouyart
# UTF-8
import pygame
import os
import threading
import uuid as uuid_lib
from ..others.save import save_load
from ..others.button_compte import *
from ..others.logger import logger
from ..others.save import *
from ..others.leaderboard_api import get_leaderboard, submit_score
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
        font_small  = pygame.font.Font(FONT_TEXT, 17)

        if FULLSCREEN:
            screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((x, y))
        pygame.display.set_caption("Compte - ?")

        refresh_btn = pygame.transform.scale(
            pygame.image.load(ROOT_LOCATION / "assets/images/ui/refresh_btn.png"), (48, 48))
        refresh_btn_rect = refresh_btn.get_rect(topleft=(PANEL_LEFT_W - 70, 20))

        # === Leaderboard state ===
        lb_data      = []       # liste de {rank, pseudo, money}
        lb_status    = "loading"  # "loading" | "ok" | "error"
        lb_lock      = threading.Lock()

        def fetch_lb():
            nonlocal lb_data, lb_status
            result = get_leaderboard()
            with lb_lock:
                if result is None:
                    lb_status = "error"
                else:
                    lb_data   = result
                    lb_status = "ok"

        def start_lb_fetch():
            nonlocal lb_status
            lb_status = "loading"
            threading.Thread(target=fetch_lb, daemon=True).start()

        start_lb_fetch()

        # === Helpers ===
        def draw_panel(px, py, pw, ph, title_str, color=(255, 60, 60)):
            panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
            panel.fill((10, 10, 20, 200))
            pygame.draw.rect(panel, color, (0, 0, pw, ph), 2, border_radius=16)
            screen.blit(panel, (px, py))
            t = font.render(title_str, True, color)
            screen.blit(t, (px + pw//2 - t.get_width()//2, py + 15))
            pygame.draw.line(screen, color, (px + 20, py + 55), (px + pw - 20, py + 55), 1)

        def draw_leaderboard(px, py, pw, ph):
            GOLD   = (255, 215,   0)
            draw_panel(px, py, pw, ph, "LEADERBOARD", color=GOLD)

            with lb_lock:
                status = lb_status
                data   = list(lb_data)

            if status == "loading":
                t = font_medium.render("Chargement...", True, (150, 150, 200))
                screen.blit(t, (px + pw//2 - t.get_width()//2, py + ph//2))
                return

            if status == "error":
                t = font_medium.render("Serveur inaccessible", True, (200, 80, 80))
                screen.blit(t, (px + pw//2 - t.get_width()//2, py + ph//2 - 15))
                t2 = font_small.render("(verifie ta connexion)", True, (120, 120, 150))
                screen.blit(t2, (px + pw//2 - t2.get_width()//2, py + ph//2 + 15))
                return

            if not data:
                t = font_medium.render("Aucun score enregistre", True, (120, 120, 150))
                screen.blit(t, (px + pw//2 - t.get_width()//2, py + ph//2))
                return

            # En-tête colonnes
            COL_RANK  = px + 30
            COL_PSEUDO = px + 90
            COL_MONEY  = px + pw - 30
            header_y   = py + 70
            screen.blit(font_small.render("#",      True, GOLD), (COL_RANK,   header_y))
            screen.blit(font_small.render("Pseudo", True, GOLD), (COL_PSEUDO, header_y))
            m_h = font_small.render("Coins", True, GOLD)
            screen.blit(m_h, (COL_MONEY - m_h.get_width(), header_y))
            pygame.draw.line(screen, GOLD, (px + 20, header_y + 22), (px + pw - 20, header_y + 22), 1)

            ROW_H = 38
            for entry in data:
                row_y = header_y + 30 + (entry["rank"] - 1) * ROW_H
                if row_y + ROW_H > py + ph - 10:
                    break

                rank = entry["rank"]
                if rank == 1:
                    color = (255, 215,   0)   # or
                elif rank == 2:
                    color = (200, 200, 220)   # argent
                elif rank == 3:
                    color = (205, 127,  50)   # bronze
                else:
                    color = (180, 180, 180)

                rank_t  = font_small.render(str(rank),            True, color)
                pseudo_t = font_small.render(entry["pseudo"][:18], True, color)
                money_t  = font_small.render(f"{entry['money']}",  True, color)

                screen.blit(rank_t,   (COL_RANK,                    row_y))
                screen.blit(pseudo_t, (COL_PSEUDO,                  row_y))
                screen.blit(money_t,  (COL_MONEY - money_t.get_width(), row_y))

        # === Sync state par fichier : "idle" | "syncing" | "ok" | "error" ===
        sync_states  = {}   # {fichier: "idle"|"syncing"|"ok"|"error"}
        sync_timers  = {}   # {fichier: frames restantes pour afficher ok/error}
        SYNC_BTN_SIZE = 40
        SYNC_BTN_X_OFFSET = 16  # à droite de la carte

        def sync_btn_rect(card_rect):
            return pygame.Rect(
                card_rect.right + SYNC_BTN_X_OFFSET,
                card_rect.centery - SYNC_BTN_SIZE // 2,
                SYNC_BTN_SIZE, SYNC_BTN_SIZE
            )

        def draw_sync_btn(rect, fichier):
            status = sync_states.get(fichier, "idle")
            colors = {
                "idle":    (60, 100, 220),
                "syncing": (200, 170, 30),
                "ok":      (40, 190, 70),
                "error":   (200, 50, 50),
            }
            color = colors.get(status, colors["idle"])
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)

            cx, cy = rect.centerx, rect.centery

            if status == "idle":
                # Flèche vers le haut
                pts = [(cx, cy - 10), (cx - 7, cy + 2), (cx - 3, cy + 2),
                       (cx - 3, cy + 10), (cx + 3, cy + 10), (cx + 3, cy + 2), (cx + 7, cy + 2)]
                pygame.draw.polygon(screen, (255, 255, 255), pts)

            elif status == "syncing":
                # Trois points horizontaux
                for dx in (-9, 0, 9):
                    pygame.draw.circle(screen, (255, 255, 255), (cx + dx, cy), 3)

            elif status == "ok":
                # Coche
                pygame.draw.lines(screen, (255, 255, 255), False,
                                  [(cx - 8, cy), (cx - 2, cy + 7), (cx + 9, cy - 8)], 3)

            else:
                # Croix
                pygame.draw.line(screen, (255, 255, 255), (cx - 8, cy - 8), (cx + 8, cy + 8), 3)
                pygame.draw.line(screen, (255, 255, 255), (cx + 8, cy - 8), (cx - 8, cy + 8), 3)

        def do_sync(fichier, data):
            sync_states[fichier] = "syncing"
            acct_uuid = data.get("uuid")
            if not acct_uuid:
                acct_uuid = str(uuid_lib.uuid4())
                data["uuid"] = acct_uuid
                save_load.save_data(file=fichier, data=data)

            def _after(t):
                t.join()
                sync_states[fichier] = "ok" if True else "error"
                sync_timers[fichier] = 180

            t = submit_score(account_uuid=acct_uuid, pseudo=data["pseudo"], money=data["money"])

            def _wait():
                t.join()
                try:
                    import requests as _req
                    r = _req.post(
                        __import__('object.others.leaderboard_api', fromlist=['API_BASE']).API_BASE + "/score",
                    )
                except Exception:
                    pass
                sync_states[fichier] = "ok"
                sync_timers[fichier] = 180

            threading.Thread(target=lambda: (t.join(), _set_ok(fichier)), daemon=True).start()

        def _set_ok(fichier):
            sync_states[fichier] = "ok"
            sync_timers[fichier] = 180

        def trigger_sync(fichier):
            data = save_load.load_data(fichier)
            if data is None:
                return
            sync_states[fichier] = "syncing"
            acct_uuid = data.get("uuid")
            if not acct_uuid:
                acct_uuid = str(uuid_lib.uuid4())
                data["uuid"] = acct_uuid
                save_load.save_data(file=fichier, data=data)

            def _run():
                try:
                    import requests as _req
                    from object.others.leaderboard_api import API_BASE, API_KEY, TIMEOUT
                    r = _req.post(
                        f"{API_BASE}/score",
                        json={"uuid": acct_uuid, "pseudo": data["pseudo"], "money": int(data["money"])},
                        headers={"x-api-key": API_KEY},
                        timeout=TIMEOUT,
                    )
                    sync_states[fichier] = "ok" if r.status_code == 200 else "error"
                except Exception:
                    sync_states[fichier] = "error"
                sync_timers[fichier] = 180

            threading.Thread(target=_run, daemon=True).start()

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
                    # Migration UUID pour anciens comptes
                    if "uuid" not in data:
                        data["uuid"] = str(uuid_lib.uuid4())
                        save_load.save_data(file=fichier, data=data)
                    btn = ButtonCompte(new=False, file=fichier, data=data)
                    surface = btn.button_img()
                    rect = surface.get_rect(topleft=(
                        PANEL_LEFT_W//2 - CARD_W//2,
                        80 + CARD_H + CARD_MARGIN + i * (CARD_H + CARD_MARGIN)
                    ))
                    compte_list.append(surface)
                    compte_list_rect.append(rect)
                    compte_child.append(btn)
                    if fichier not in sync_states:
                        sync_states[fichier] = "idle"
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
                        start_lb_fetch()
                    elif compte_list_rect[0].collidepoint(event.pos):
                        popup_open = True
                        input_text = ""
                    else:
                        clicked = False
                        for i in range(1, len(compte_list)):
                            fichier = compte_child[i].file
                            sbr = sync_btn_rect(compte_list_rect[i])
                            if sbr.collidepoint(event.pos) and sync_states.get(fichier) != "syncing":
                                trigger_sync(fichier)
                                clicked = True
                                break
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

            for i, (surface, rect) in enumerate(zip(compte_list, compte_list_rect)):
                hovered = rect.collidepoint(mouse_pos)
                surface = compte_child[i].button_img(hovered=hovered)
                screen.blit(surface, rect)
                # Bouton sync sur les comptes existants (pas le bouton "nouveau")
                if i > 0:
                    fichier = compte_child[i].file
                    # Décrémenter timer feedback
                    if sync_timers.get(fichier, 0) > 0:
                        sync_timers[fichier] -= 1
                        if sync_timers[fichier] == 0:
                            sync_states[fichier] = "idle"
                    draw_sync_btn(sync_btn_rect(rect), fichier)

            # === PANNEAU DROIT — leaderboard ===
            draw_leaderboard(PANEL_LEFT_W + 20, 20, PANEL_RIGHT_W - 40, y - 40)

            if popup_open:
                validate_rect, cancel_rect = draw_popup(screen, font, input_text)

            pygame.display.flip()

    except Exception:
        logger.error("Compte_menu ->", exc_info=True)
