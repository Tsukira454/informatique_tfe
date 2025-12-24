import pygame
import sys
from pathlib import Path
from math import floor
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, SIZE_BLOCK
from object.ui.finish_menu import finish_menu


class ButtonBoutique:
    def __init__(self, largeur=10, hauteur=10, type=0):
        self.type = type
        self.hauteur = hauteur
        self.larger = largeur
        self.image = pygame.image.load("./assets/UI/boutique/boutique_frame.png")