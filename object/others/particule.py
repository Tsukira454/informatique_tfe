import random
import pygame
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from config.config import LARGER_FENETRE, HAUTEUR_FENETRE

class Particle:
    def __init__(self):
        self.x = random.randint(0, LARGER_FENETRE)
        self.y = random.randint(-HAUTEUR_FENETRE, 0)
        self.speed = random.uniform(0.2, 1.5)
        self.size = random.randint(2, 4)
        self.alpha = random.randint(50, 130)

    def update(self):
        self.y += self.speed
        if self.y > HAUTEUR_FENETRE:
            self.__init__()

    def draw(self, surf):
        s = pygame.Surface((self.size*3, self.size*3), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, self.alpha), (self.size, self.size), self.size)
        surf.blit(s, (self.x, self.y))
