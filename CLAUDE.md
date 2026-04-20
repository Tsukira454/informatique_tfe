# Nexus Extraction — TFE de Elvin Mouyart

Jeu de type "extraction" en Python/Pygame. Le joueur contrôle un robot qui descend dans des mines pour collecter des ressources, gérer son énergie et sa pression, et ramener son butin.

## Lancer le jeu

```bash
# Windows
Windows_Start.bat

# Linux
./Linux_Start.sh

# Direct
cd src && python data/main.py
```

## Structure du projet

```
src/
└── data/
    ├── main.py                  # Point d'entrée — boucle principale des menus
    ├── config/
    │   └── config.py            # Toutes les constantes globales (résolution, blocs, récompenses, niveaux...)
    └── object/
        ├── games/               # Écrans / états du jeu
        │   ├── main_menu.py     # Menu principal
        │   ├── play_menu.py     # Menu de sélection de partie
        │   ├── play.py          # Boucle de jeu principale
        │   ├── compte.py        # Gestion des comptes (sélection/création)
        │   ├── boutique.py      # Boutique d'upgrades
        │   ├── option_menu.py   # Options
        │   ├── finish_menu.py   # Écran de fin de partie
        │   ├── leaderboard.py   # Classement
        │   └── load_screen.py   # Écran de chargement des assets
        ├── personnages/
        │   ├── robot.py         # Joueur principal — mouvement, collecte, HUD
        │   ├── bird.py          # Ennemi/obstacle bird
        │   └── rocket.py        # Animation d'arrivée de la fusée (niveau 0)
        ├── maps/
        │   └── maps.py          # Génération procédurale des cartes
        ├── others/
        │   ├── assets_manager.py  # Cache centralisé de tous les assets pygame
        │   ├── audio_manager.py   # Musique de fond + effets sonores
        │   ├── save.py            # Sauvegarde/chargement chiffré (Fernet/JSON)
        │   ├── logger.py          # Logger fichier
        │   ├── button_boutique.py # Boutons de la boutique
        │   ├── button_compte.py   # Boutons de gestion des comptes
        │   └── particule.py       # Système de particules
        └── ui/
            ├── menu_display.py  # Composants d'affichage des menus
            ├── moving_block.py  # Blocs animés (eau, lave)
            └── Three_D.py       # Animation 3D du robot (intro)
```

## Concepts clés

### Config globale (`config.py`)
Toutes les constantes sont importées via `from config.config import *`. Les principales :
- `ROOT_LOCATION` — chemin racine du projet (Path)
- `LARGER_FENETRE / HAUTEUR_FENETRE` — 1920×1080
- `SIZE_BLOCK` — 64px
- `REWARD_VALEUR` — dictionnaire bloc → points de récompense
- `WORLD_LEVEL` — liste des niveaux avec blocs et probabilités d'apparition
- `SPECIAL_ITEM_DIC` — items de la boutique (energy, pression) avec leurs stats
- `ACCOUNT_LOCATION` — dossier des sauvegardes comptes

### Flux de navigation
```
main_menu()
  → [Jouer]    → compte_menu() → play_menu() → play()
  → [Options]  → option_menu()
  → [Quitter]  → exit
```

### Système de sauvegarde (`save.py`)
- Format JSON chiffré avec Fernet (clé fixe dans le fichier)
- Données : `{pseudo, money, inventory: {energy: lvl, pression: lvl}}`
- Comptes stockés dans `src/data/config/accounts/*.json`

### Boucle de jeu (`play.py`)
- 60 FPS, caméra verticale descendante
- Robot spawn via animation fusée (niveau 0 seulement)
- Collecte de blocs → `robot.collected_resources`
- HUD : barre énergie (bleue) + barre pression (verte/rouge)
- Alerte sonore si pression ≥ 75%
- Inventaire : touche `E`
- Changement de niveau : `N` (dev) ou condition automatique

### Assets (`assets_manager.py`)
Tous les assets sont pré-chargés au démarrage via `ELEMENT_LOAD` / `ELEMENT_LOAD_NAME` / `ELEMENT_LOAD_SIZE` dans `config.py`. On y accède via `asset_manager.get_element("nom")`.

## Dépendances
- `pygame`
- `cryptography` (Fernet)

## Notes développeur
- Le jeu tourne dans `src/data/` — les imports sont relatifs à ce dossier
- Logger : `from object.others.logger import logger`
- Langue : français dans les logs et commentaires
