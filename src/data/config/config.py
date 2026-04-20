from pathlib import Path
import pygame
ROOT_LOCATION = Path(__file__).resolve().parents[2]
LARGER_FENETRE=1920
HAUTEUR_FENETRE=1080
FULLSCREEN=False
SIZE_BLOCK=64
CAMERA_SEUIL=0.6
UNDERGROUND_FOLDER= ROOT_LOCATION / "assets/images/images/underground/"
FONT_TEXT=ROOT_LOCATION / "assets/fonts/font1/ka1.ttf"
FONT_SPECIAL=ROOT_LOCATION / "assets/fonts/font2/Pixel Game.otf"
BACKGROUND = pygame.transform.scale(pygame.image.load(ROOT_LOCATION / "assets/images/images/background.png"), (LARGER_FENETRE, HAUTEUR_FENETRE))
TEXT_COLOR=(255,0,0)
ACCOUNT_LOCATION=ROOT_LOCATION / "data/config/accounts/"
REWARD_VALEUR={"dirt" : 1, "grass_block" : 1, "cobblestone": 1, "stairs" : -1, "stone": 1, "deepslate":2, "cobbled_deepslate":2, "coal_ore":2, "deepslate":2, "iron_ore": 3, "lapis_ore":4, "deepslate_coal_ore":5, "deepslate_iron_ore":5, "diamond_ore":6, "deepslate_diamond_ore":8, "raw_iron_block": 10, "emerald_ore":10, "deepslate_lapis_ore":10, "deepslate_emerald_ore":15, "coal_block": 15,"oak_planks":0, "oak_log":0, "bedrock":0, "oak_strairs_R":0, "oak_strairs_L":0}
BLOCK_LIST=["dirt", "grass_block", "stairs", "stone", "iron_ore", "diamond_ore", "emerald_ore", "oak_planks", "oak_log", "bedrock", "oak_strairs_R", "oak_strairs_L", "coal_block", "coal_ore", "cobbled_deepslate", "cobblestone", "deepslate_coal_ore", "deepslate_diamond_ore", "deepslate_emerald_ore", "deepslate_iron_ore", "deepslate_lapis_ore", "lapis_ore", "raw_iron_block", "deepslate"]
INDESTRUCTIBLE=["crying_obsidian"]
LIQUID_BLOCK=["water", "lava", "water_full", "lava_full"]
UNCOLECTABLE_BLOCk=["air", "crying_obsidian", "water", "water_full", "lava", "lava_full", "oak_planks", "oak_log", "oak_strairs_R", "oak_strairs_L", "bedrock"]
#BLOCK_CHANCE={"dirt":101, "stone":70, "iron_ore":15, "diamond_ore":3, "emerald_ore":1}
# name - lvl max - valeur start - multp par lvl - mult prix - prix base
SPECIAL_ITEM_DIC={"energy" : [-1, 10, 1.5, 2, 50], "pression" : [-1, 10, 1.2, 1.5, 40]}
BOUTIQUE_ITEM=["energy","pression"]
# WORLD LEVEL (chance = 100,00% -> 10000)
WORLD_LEVEL=[["Haut du monde",["dirt", "stone", "coal_ore", "iron_ore","grass_block", "stairs", "oak_planks", "oak_log", "bedrock", "oak_strairs_R", "oak_strairs_L", "crying_obsidian", "water_full", "lava_full"],[10001,7000,1500,500,None,None,None,None,None,None,None,None,None,None]],["Les grottes",["stone", "cobblestone", "coal_ore", "iron_ore", "deepslate", "diamond_ore", "raw_iron_block", "emerald_ore", "stairs", "crying_obsidian", "water_full", "lava_full"],[10001, 8000, 2000, 1800, 1000, 500, 250, 50, None, None, None, None]]]
PROFONDEUR_PAR_WORLD = 52
ELEMENT_LOAD = [
    # === IMAGES ===
    ROOT_LOCATION / "assets/images/images/background.png",
    ROOT_LOCATION / "assets/images/images/title.png",
    ROOT_LOCATION / "assets/images/images/creator.jpg",
    ROOT_LOCATION / "assets/images/images/music_creator.png",
    ROOT_LOCATION / "assets/images/images/underground/the_void.png",
    ROOT_LOCATION / "assets/images/images/underground/the_void_full.png",
    ROOT_LOCATION / "assets/images/images/underground/maps_level_0/background_underground_1.png",
    ROOT_LOCATION / "assets/images/images/underground/maps_level_0/background_underground_2.png",
    ROOT_LOCATION / "assets/images/images/underground/maps_level_0/background_underground_3.png",
    # === UI ===
    ROOT_LOCATION / "assets/images/UI/ui_btn_1_play.png",
    ROOT_LOCATION / "assets/images/UI/ui_btn_2_boutique.png",
    ROOT_LOCATION / "assets/images/UI/ui_btn_4_options.png",
    ROOT_LOCATION / "assets/images/UI/ui_btn_4_play.png",
    ROOT_LOCATION / "assets/images/UI/ui_btn_4_quitter.png",
    ROOT_LOCATION / "assets/images/UI/ui_btn_compte.png",
    ROOT_LOCATION / "assets/images/UI/refresh_btn.png",
    ROOT_LOCATION / "assets/images/UI/menu/barre_lateral.png",
    ROOT_LOCATION / "assets/images/UI/boutique/boutique_bg.png",
    ROOT_LOCATION / "assets/images/UI/boutique/boutique_frame.png",
    ROOT_LOCATION / "assets/images/UI/boutique/energy.png",
    ROOT_LOCATION / "assets/images/UI/boutique/pression.png",
    ROOT_LOCATION / "assets/images/UI/Inventory/inventory.png",
    ROOT_LOCATION / "assets/images/UI/play/blue_storm.png",
    ROOT_LOCATION / "assets/images/UI/play/danger.png",
    ROOT_LOCATION / "assets/images/UI/play/pression.png",
    # === BLOCS ===
    ROOT_LOCATION / "assets/images/blocks/blocks/dirt.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/grass_block.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/stone.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/stairs.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/iron_ore.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/diamond_ore.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/emerald_ore.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/oak_planks.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/oak_log.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/bedrock.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/oak_strairs_R.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/oak_strairs_L.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/coal_ore.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/deepslate_coal_ore.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/coal_block.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/raw_iron_block.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/deepslate_iron_ore.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/deepslate_diamond_ore.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/deepslate_emerald_ore.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/cobbled_deepslate.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/deepslate_lapis_ore.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/lapis_ore.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/cobblestone.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/deepslate.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/crying_obsidian.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/water_full.png",
    ROOT_LOCATION / "assets/images/blocks/blocks/lava_full.png",
    # === SPRITES ROBOTS ===
    ROOT_LOCATION / "assets/images/sprites/robots/robots_bug.png",
    *[ROOT_LOCATION / f"assets/images/sprites/robots/robots_{i}.png" for i in [0,1,2,3,4,5,6,7,8,20,30,40,50,75,90,100]],
    # === SPRITES BIRD ===
    *[ROOT_LOCATION / f"assets/images/sprites/bird/bird_{i}.png" for i in range(4)],
    # === 3D ===
    *[ROOT_LOCATION / f"assets/images/sprites/3d/robots/{i:04d}.png" for i in range(1, 241)],
    # === MOUVING BLOCK ===
    *[ROOT_LOCATION / f"assets/images/blocks/blocks/water/water_{i}.png" for i in range(8)],
    *[ROOT_LOCATION / f"assets/images/blocks/blocks/lava/lava_{i}.png" for i in range(8)],
    *[ROOT_LOCATION / f"assets/images/sprites/rocket/rocket_{i}.png" for i in range(2)],
]

ELEMENT_LOAD_NAME = [
    "background", "title", "creator", "music_creator", "the_void", "the_void_full",
    "underground_1", "underground_2", "underground_3",
    "btn_play_menu", "btn_boutique_menu", "btn_option_menu",
    "btn_play", "btn_quitter", "btn_compte", "refresh_btn",
    "barre_laterale", "boutique_bg", "boutique_frame",
    "boutique_energy", "boutique_pression", "inventory",
    "blue_storm", "danger", "pression_icon",
    "dirt", "grass_block", "stone", "stairs", "iron_ore", "diamond_ore", "emerald_ore",
    "oak_planks", "oak_log", "bedrock", "oak_strairs_R", "oak_strairs_L", "coal_ore",
    "deepslate_coal_ore", "coal_block", "raw_iron_block", "deepslate_iron_ore", "deepslate_diamond_ore",
    "deepslate_emerald_ore", "cobbled_deepslate", "deepslate_lapis_ore", "lapis_ore", "cobblestone", "deepslate",
    "crying_obsidian", "water_full", "lava_full",
    "robot_bug",
    *[f"robot_{i}" for i in [0,1,2,3,4,5,6,7,8,20,30,40,50,75,90,100]],
    *[f"bird_{i}" for i in range(4)],
    *[f"robot_3d_{i:04d}" for i in range(1, 241)],
    *[f"water_{i}" for i in range(8)],
    *[f"lava_{i}" for i in range(8)],
    *[f"rocket_{i}" for i in range(2)],
]

ELEMENT_LOAD_SIZE = [
    # === IMAGES ===
    (LARGER_FENETRE, HAUTEUR_FENETRE),          # background
    (1200, 125),                                 # title
    (300, 300),                                  # creator
    (300, 300),                                  # music_creator
    (1920, 1080),                                # The void
    (1920, 1080),                                # The void full
    (1920, 1080),                                # underground_1
    (1920, 1080),                                # underground_2
    (1920, 1080),                                # underground_3
    # === UI ===
    (300, 140),                                  # btn_play_menu
    (300, 140),                                  # btn_boutique_menu
    (300, 140),                                  # btn_option_menu
    (300, 140),                                  # btn_play
    (300, 140),                                  # btn_quitter
    (500, 150),                                  # btn_compte
    (96, 96),                                    # refresh_btn
    (250, HAUTEUR_FENETRE),                      # barre_laterale
    (int((LARGER_FENETRE/7)*5), HAUTEUR_FENETRE),# boutique_bg
    (150, 150),                                  # boutique_frame
    (100, 100),                                  # boutique_energy
    (100, 100),                                  # boutique_pression
    (600, 400),                                  # inventory
    (25, 25),                                    # blue_storm
    (35, 35),                                    # danger
    (25, 25),                                    # pression_icon
    # === BLOCS ===
    *[(SIZE_BLOCK, SIZE_BLOCK) for _ in range(27)],
    # === SPRITES ROBOTS ===
    (SIZE_BLOCK, SIZE_BLOCK),                    # robot_bug
    *[(SIZE_BLOCK, SIZE_BLOCK) for _ in [0,1,2,3,4,5,6,7,8,20,30,40,50,75,90,100]],
    # === SPRITES BIRD ===
    *[(SIZE_BLOCK, SIZE_BLOCK) for _ in range(4)],
    # === 3D ===
    *[(300, 300) for _ in range(1, 241)],
    # === MOUVING BLOCK ===
    *[(SIZE_BLOCK, SIZE_BLOCK) for _ in range(8)],
    *[(SIZE_BLOCK, SIZE_BLOCK) for _ in range(8)],
    *[(SIZE_BLOCK*2, SIZE_BLOCK*4) for _ in range(2)],
]