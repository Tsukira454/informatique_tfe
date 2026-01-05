import pygame
import pygame
import os
import json
from config.config import *
from object.ui.finish_menu import finish_menu


class ButtonCompte:
    def __init__(self, new, file, data):
        self.new = new
        self.compte_loc = ACCOUNT_LOCATION
        if self.new:
            ...
        else:
            self.file = file
            self.data = data
            self.money = self.data["money"]
            self.pseudo = self.data["pseudo"]
        self.font = pygame.font.Font(FONT_TEXT, 24)
        self.image = pygame.image.load("./assets/ui/ui_btn_compte.png")
        self.image = pygame.transform.scale(self.image, (500,150))

    def button_img(self):
        if self.new:
            text_new=self.font.render("Cree un compte", True, TEXT_COLOR)
            surface = pygame.Surface((500,150), pygame.SRCALPHA)
            surface.blit(self.image, (0,0))
            surface.blit(text_new, ((500//2)-(text_new.get_width()//2), (150//2)-(text_new.get_height()//2)))
        else:
            text_pseudo=self.font.render(f"{self.pseudo}", True, TEXT_COLOR)
            text_money=self.font.render(f"money - {self.money}", True, TEXT_COLOR)
            surface = pygame.Surface((500,150), pygame.SRCALPHA)
            surface.blit(self.image, (0,0))
            surface.blit(text_pseudo, ((500//2)-(text_pseudo.get_width()//2), ((150//10)*3)-(text_pseudo.get_height()//2)))
            surface.blit(text_money, ((500//2)-(text_money.get_width()//2), ((150//10)*7)-(text_money.get_height()//2)))
        return surface
    
    def button_fontion(self, pseudo="ERREUR"):
        if self.new:
            account_number=0
            for fichier in os.listdir(ACCOUNT_LOCATION):
                if fichier.lower().endswith(".json"):
                    account_number += 1
            data={"pseudo" : pseudo, "money" : 0}
            with open(f'{self.compte_loc}{pseudo}{account_number+1}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        else:
            return self.file
