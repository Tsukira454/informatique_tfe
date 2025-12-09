# Elvin Mouyart 6(t)b
# UTF-8

import pygame
from object.ui.main_menu import main_menu
from object.ui.play_menu import play_menu
from object.ui.option_menu import option_menu

if __name__ == "__main__":
    choice = main_menu()
    if choice == 1:
        play_menu()
    elif choice == 2:
        option_menu()
    elif choice == 3:
        ...
    else:
        ...