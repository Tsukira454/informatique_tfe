import pygame
import os
import json
import uuid as uuid_lib
from config.config import *
from object.others.save import save_load

MAX_COMPTES = 3
CARD_W = 600
CARD_H = 130
CARD_MARGIN = 20
PANEL_LEFT_W = int(LARGER_FENETRE * (2/3))
PANEL_RIGHT_W = LARGER_FENETRE - PANEL_LEFT_W

class ButtonCompte:
    def __init__(self, new, file, data):
        self.new = new
        self.compte_loc = ACCOUNT_LOCATION
        self.font_title = pygame.font.Font(FONT_TEXT, 22)
        self.font_stat  = pygame.font.Font(FONT_TEXT, 16)
        self.width  = CARD_W
        self.height = CARD_H

        if not self.new:
            self.file           = file
            self.data           = data
            self.money          = self.data["money"]
            self.pseudo         = self.data["pseudo"]
            self.energy_level   = self.data["inventory"]["energy"]
            self.pression_level = self.data["inventory"]["pression"]

        self.avatar = pygame.image.load(ROOT_LOCATION / "assets/images/sprites/robots/robots_50.png")
        self.avatar = pygame.transform.scale(self.avatar, (80, 80))
        self.icon_energy   = pygame.transform.scale(pygame.image.load(ROOT_LOCATION / "assets/images/UI/boutique/energy.png"),   (24, 24))
        self.icon_pression = pygame.transform.scale(pygame.image.load(ROOT_LOCATION / "assets/images/UI/boutique/pression.png"), (24, 24))
        self.icon_money    = pygame.transform.scale(pygame.image.load(ROOT_LOCATION / "assets/images/UI/play/blue_storm.png"),   (24, 24))

    def button_img(self, hovered=False):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        border_color = (255, 150, 50) if hovered else (255, 60, 60)

        if self.new:
            surface.fill((10, 10, 20, 180))
            pygame.draw.rect(surface, border_color, (0, 0, self.width, self.height), 2, border_radius=16)
            plus = pygame.font.Font(FONT_SPECIAL, 42).render("+", True, border_color)
            surface.blit(plus, (self.width//2 - plus.get_width()//2, 20))
            text = self.font_stat.render("Creer un compte", True, (180, 180, 220))
            surface.blit(text, (self.width//2 - text.get_width()//2, 90))
        else:
            surface.fill((10, 10, 20, 200))
            pygame.draw.rect(surface, border_color, (0, 0, self.width, self.height), 2, border_radius=16)
            # avatar
            surface.blit(self.avatar, (15, self.height//2 - 40))
            # separateur
            pygame.draw.line(surface, (60, 60, 80), (110, 15), (110, self.height - 15), 1)
            # pseudo
            text_pseudo = self.font_title.render(self.pseudo, True, (255, 215, 0))
            surface.blit(text_pseudo, (125, 12))
            pygame.draw.line(surface, (60, 60, 80), (125, 42), (self.width - 15, 42), 1)
            # money
            surface.blit(self.icon_money, (125, 52))
            surface.blit(self.font_stat.render(f"{int(self.money)} coins", True, (180, 220, 255)), (155, 55))
            # energy + pression sur meme ligne
            surface.blit(self.icon_energy, (125, 82))
            surface.blit(self.font_stat.render(f"Energy lvl {self.energy_level}", True, (100, 200, 255)), (155, 85))
            surface.blit(self.icon_pression, (350, 82))
            surface.blit(self.font_stat.render(f"Pression lvl {self.pression_level}", True, (100, 255, 180)), (380, 85))

        return surface

    def button_fontion(self, pseudo="ERREUR"):
        if self.new:
            account_number = 0
            for fichier in os.listdir(ACCOUNT_LOCATION):
                if fichier.lower().endswith(".json"):
                    account_number += 1
            inventory = {"energy": 1, "pression": 1}
            data = {"pseudo": pseudo, "money": 0, "inventory": inventory, "uuid": str(uuid_lib.uuid4())}
            save_load.save_data(file=f"{pseudo}{account_number + 1}.json", data=data)
        else:
            return self.file