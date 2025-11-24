# Elvin Mouyart 6(t)b
# UTF-8
import pygame
from object.ui.main_menu import main_menu
if __name__ == "__main__":
    choice = main_menu()
    if choice == 1:
        print("Jouer")
    elif choice == 2:
        print("Settings")
    elif choice == 3:
        print("Quitter")
    else:
        print("Fermé")