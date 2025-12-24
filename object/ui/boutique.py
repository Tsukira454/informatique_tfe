# Elvin Mouyart
# UTF-8
import pygame
import sys
from pathlib import Path
from .option_menu import option_menu
from .play import play
from ..others.button_boutique import ButtonBoutique


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, FULLSCREEN

def boutique():
    pygame.init()

    if FULLSCREEN:
        screen = pygame.display.set_mode((LARGER_FENETRE, HAUTEUR_FENETRE), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((LARGER_FENETRE, HAUTEUR_FENETRE))

    pygame.display.set_caption("Menu Play")

    # === Chargement images bg ===
    background = pygame.image.load("./assets/images/background.png")
    background = pygame.transform.scale(background, (LARGER_FENETRE, HAUTEUR_FENETRE))

    # === Boutique ===
    boutique_bg = pygame.image.load("./assets/UI/boutique/boutique_bg.png")
    boutique_frame = pygame.image.load("./assets/UI/boutique/boutique_frame.png")
    boutique_bg = pygame.transform.scale(boutique_bg, (int((LARGER_FENETRE/7)*5), HAUTEUR_FENETRE))
    boutique_frame = pygame.transform.scale(boutique_frame, (150,150))

    def load_boutique():
        frame_list=[]
        for h in range(4):
            for l in range(6):
                frame_list.append(boutique_frame)
        return frame_list
    
    frame_list = load_boutique()
    running = True

    while running:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                running = False


        screen.blit(background, (0,0))
        screen.blit(boutique_bg, (0,0))
        h=0
        l=0
        for i in range(len(frame_list)):
            if i%6==0:
                h+=1
                l=0
            screen.blit(frame_list[i], (100+(200*l),(200*h)))
            l+=1
        h=0
        


        pygame.display.flip()
