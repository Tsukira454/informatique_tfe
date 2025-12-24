import pygame
import sys
from pathlib import Path
from math import floor
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, SIZE_BLOCK
from object.ui.finish_menu import finish_menu


class Boutique:
    def __init__(self):
        self.image = 

