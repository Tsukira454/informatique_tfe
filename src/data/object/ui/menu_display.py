import pygame
from config.config import *

class menu_display:
    def __init__(self, width, height, border_color, bg_color, title_label, label, sublabel=""):
        self.width = width
        self.height = height
        self.border_color = border_color
        self.bg_color = bg_color
        self.title_label = title_label
        self.label = label
        self.sublabel = sublabel
        
    def get_element(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.fill((*self.bg_color, 180))
        pygame.draw.rect(surface, self.border_color, (0, 0, self.width, self.height), width=2, border_radius=12)
        font = pygame.font.Font(FONT_TEXT, 24)
        text = font.render(self.label, True, (255, 255, 255))
        surface.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
        if self.sublabel:
            sub = font.render(self.sublabel, True, (180, 180, 180))
            surface.blit(sub, (self.width//2 - sub.get_width()//2, self.height//2 + 10))
        return surface
    
    def get_button(self, pos):
        surface = self.get_element()
        rect = surface.get_rect(topleft=pos)
        return surface, rect

class menu_display_countainer:
    def __init__(self, width, height, border_color, bg_color, title):
        self.width = width
        self.height = height
        self.border_color = border_color
        self.bg_color = bg_color
        self.title = title
        
    def get_element(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.fill((*self.bg_color, 180))
        pygame.draw.rect(surface, self.border_color, (0, 0, self.width, self.height), width=2, border_radius=12)
        font = pygame.font.Font(FONT_TEXT, 24)
        text = font.render(self.title, True, (255, 255, 255))
        surface.blit(text, (self.width//2 - text.get_width()//2, 10))
        return surface