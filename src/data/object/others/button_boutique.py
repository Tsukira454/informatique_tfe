import pygame
from config.config import *


class ButtonBoutique:
    def __init__(self, largeur=10, hauteur=10, type=0):
        self.type = type
        self.hauteur = hauteur
        self.larger = largeur
        self.image = pygame.image.load(ROOT_LOCATION / "assets/images/UI/boutique/boutique_frame.png")