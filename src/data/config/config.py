from pathlib import Path
import pygame
ROOT_LOCATION = Path(__file__).resolve().parents[2]
LARGER_FENETRE=1280
HAUTEUR_FENETRE=720
FULLSCREEN=False
SIZE_BLOCK=64
FONT_TEXT=ROOT_LOCATION / "assets/fonts/font1/ka1.ttf"
FONT_SPECIAL=ROOT_LOCATION / "assets/fonts/font2/Pixel Game.otf"
BACKGROUND = pygame.transform.scale(pygame.image.load(ROOT_LOCATION / "assets/images/images/background.png"), (LARGER_FENETRE, HAUTEUR_FENETRE))
TEXT_COLOR=(255, 215, 0)
ACCOUNT_LOCATION=ROOT_LOCATION / "data/config/accounts/"
REWARD_VALEUR={"dirt" : 1, "grass_block" : 1, "stairs" : -1, "stone": 2, "iron_ore": 3}
BLOCK_LIST=["dirt", "grass_block", "stairs", "stone", "iron_ore"]
BLOCK_CHANCE={"dirt":101, "stone":70, "iron_ore":15}
# name - lvl max - type - valeur start - multp par lvl - add parr lvl
SPECIAL_ITEM={"energy": [20,"stats",10,1,2]}