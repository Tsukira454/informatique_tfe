import pygame
from config.config import *
from ..others.save import *
from ..others.audio_manager import *
class ButtonBoutique:
    def __init__(self, image, name, compte_file):
        self.image = pygame.image.load(ROOT_LOCATION / f"assets/images/UI/boutique/{image}.png")
        self.image = pygame.transform.scale(self.image, (100,100))
        self.boutique_frame = pygame.image.load(ROOT_LOCATION / "assets/images/UI/boutique/boutique_frame.png")
        self.boutique_frame = pygame.transform.scale(self.boutique_frame, (150,150))
        self.compte_file = compte_file
        self.name = name
    
    def get_hud(self):
        data = SPECIAL_ITEM_DIC[self.name]
        data_player = save_load.load_data(self.compte_file)
        price = data[4] * (float(data_player["inventory"][self.name]) * data[3])
        level = data_player["inventory"][self.name]

        font = pygame.font.Font(FONT_TEXT, 20)
        if(price>=1000):
            font_price = pygame.font.Font(FONT_TEXT, 16)
        else:
            font_price = pygame.font.Font(FONT_TEXT, 20)
        text_name  = font.render(f"{self.name}", True, TEXT_COLOR)
        text_level = font.render(f"lvl {level}", True, TEXT_COLOR)
        text_price = font_price.render(f"{int(price)} Coins", True, TEXT_COLOR)

        surface = pygame.Surface((150, 270), pygame.SRCALPHA)
        surface.blit(text_name,  (75 - text_name.get_width()//2, 5))    # nom en haut
        surface.blit(self.boutique_frame, (0, 30))     # frame décalée vers le bas
        surface.blit(self.image, (25, 55))             # image suit la frame
        surface.blit(text_level, (75 - text_level.get_width()//2, 195))
        surface.blit(text_price, (75 - text_price.get_width()//2, 220))

        return surface
    
    def buy(self):
        data = SPECIAL_ITEM_DIC[self.name]
        data_player = save_load.load_data(self.compte_file)
        price = data[4] * (float(data_player["inventory"][self.name]) * data[3])
        if int(data_player["money"]) >= price:
            play_fx(ROOT_LOCATION / "assets/sounds/buy.mp3")
            new_inventory = data_player["inventory"]
            new_inventory[self.name] += 1
            print(f"new_inventory avant save: {new_inventory}")  # ← ajoute ça
            new_data = save_load.build_data(file=self.compte_file, pseudo=data_player["pseudo"], money=(data_player["money"] - price), inventory=new_inventory)
            print(f"new_data: {new_data}")  # ← et ça
            save_load.save_data(file=self.compte_file, data=new_data)
            return True
        play_fx(ROOT_LOCATION / "assets/sounds/denied.mp3")
        return False