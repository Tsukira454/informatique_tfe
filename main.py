# Elvin Mouyart 6(t)b
# UTF-8

import pygame
import os
from object.others.logger import logger
from object.ui.main_menu import main_menu
from object.ui.play_menu import play_menu
from object.ui.option_menu import option_menu
from object.others.save import save_load
from object.ui.compte import compte_menu
from config.config import *
from object.others.audio_manager import play_bg_music



def play_music():
    try:
        play_bg_music("./assets/sounds/music_nexus_bg.wav", volume=0.4)
    except Exception:
        logger.error("Erreur lors du lancement de la musique", exc_info=True)

def check_account():
    account_extention = ".json"
    account_number=0
    for fichier in os.listdir(ACCOUNT_LOCATION):
        if fichier.lower().endswith(account_extention):
            account_number += 1
    return account_number

def start_text():
    # les +////...///+ Pour y voir plus clair pour séparée les sessions de jeux dans les logs
    logger.info("""\n\n\n
+///////////////////////////////////////////////////////////////////////////+

                Démarrage de Nexus Extraction

+///////////////////////////////////////////////////////////////////////////+
""")
    logger.info("""
+---------------------------- Bienvenue ! ----------------------------+

Bienvenue dans Nexus Extraction. Si vous lisez ceci, c’est que vous vous
trouvez actuellement dans les logs du jeu. Si vous êtes un joueur lambda,
cette fenêtre ne vous intéressera pas, mais ne la fermez pas, car cette
action entraînera la fermeture du jeu.

En cas de problème ou de plantage du jeu, merci de contacter le développeur
à l’adresse e-mail suivante : mouyelv@sjb-liege.org
en joignant les fichiers de logs qui se trouvent dans le dossier "logs/".

Merci de jouer à Nexus Extraction et bon jeu ;)

+-------------------------------- LOGS --------------------------------+
""")

if __name__ == "__main__":
    start_text()
    play_music()
    back=True
    try:
        while back:
            choice = main_menu()
            if choice == 1:
                compte_file = compte_menu()
                logger.info(f"Compte choisi -> {compte_file}")
                if isinstance(compte_file, bool):
                    back=compte_file
                elif isinstance(compte_file, str):
                    back=play_menu(compte_file[0])
            elif choice == 2:
                option_menu()
            elif choice == 3:
                back=False
        logger.info("+------ Fin du jeux -----+")
    except Exception:
        logger.error("Main erreur -> ", exc_info=True)