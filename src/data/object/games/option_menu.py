# Elvin Mouyart
# UTF-8
import pygame
from config.config import *
from object.others.logger import logger



def save_config(resolution, fullscreen, text_color):
    """ecrit les nouvelles valeurs dans config/config.py."""
    config_path = ROOT_LOCATION / "data/config/config.py"

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

    if FULLSCREEN:
        screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((x, y))
    pygame.display.set_caption("Options")
    clock   = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        # === evenements ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

        # === Rendu ===
        screen.blit(BACKGROUND, (0, 0))
        pygame.display.flip()