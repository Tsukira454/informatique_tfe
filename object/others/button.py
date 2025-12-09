import pygame
import sys
from pathlib import Path
from math import floor
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, SIZE_BLOCK
from object.ui.finish_menu import finish_menu


class ButtonSettings:
    def __init__(self, largeur=10, hauteur=10, type=0):
        self.type = type
        self.hauteur = hauteur
        self.larger = largeur
        # 0 = Btn | 1 = box de choix | 2 = True/False | 3 = Sliders
        if self.type == 0:
            self.btn_Bouton()
        elif self.type == 1:
            self.btn_choix
        elif self.type == 2:
            self.btn_choix
        elif self.type == 3:
            self.btn_sliders

    def btn_Bouton(self):
        ...

    def btn_choix(self):
        ...

    def btn_box(self):
        ...

    def btn_sliders(self):
        ...

