# Elvin Mouyart 6(t)b
# UTF-8

import pygame
from object.ui.main_menu import main_menu
from object.ui.play_menu import play_menu
from object.ui.option_menu import option_menu
import pygame

def play_music():
    pygame.mixer.init()
    bg_sound = pygame.mixer.Sound("./assets/sounds/music_bg.mp3")
    bg_sound.set_volume(0.2)
    bg_sound.play(-1)


if __name__ == "__main__":
    play_music()
    back=True
    while back:
        choice = main_menu()
        if choice == 1:
            back=play_menu()
        elif choice == 2:
            option_menu()
        elif choice == 3:
            back=False