# Elvin Mouyart
# UTF-8
import pygame
from random import randint
from config.config import *
import math

def create_simple_maps(asset_manager, maps_level):
    pygame.init()

    block_size = SIZE_BLOCK
    maps = {}

    def level_y_to_pixel_y(level_index):
        # Convertit un index de ligne en position Y en pixels
        return level_index * block_size
    def cavity_generator(maps, placed_cavities):
        import math
        
        bedrock_y = level_y_to_pixel_y(4 - PROFONDEUR_PAR_WORLD - 1)
        min_y = bedrock_y + SIZE_BLOCK * 5  # marge au-dessus de la bedrock
        
        tentatives = 0
        nb_cavites = randint(4, 8)
        
        while len(placed_cavities) < nb_cavites and tentatives < 100:
            tentatives += 1
            
            # taille aléatoire
            rayon_x = randint(5, 10)  # plus large
            rayon_y = randint(2, 4)   # moins haut
            
            # position aléatoire
            coo_x = randint(rayon_x + 1, width_in_blocks - rayon_x - 1)
            coo_y = level_y_to_pixel_y(randint(-PROFONDEUR_PAR_WORLD + rayon_y + 5, 2))
            
            # vérifie qu'on est pas trop proche de la bedrock
            if coo_y - rayon_y * SIZE_BLOCK < min_y:
                continue
            
            # vérifie qu'on chevauche pas une cavité existante
            trop_proche = False
            for (ex, ey, erx, ery) in placed_cavities:
                dist_x = abs(coo_x - ex)
                dist_y = abs(coo_y - ey) / SIZE_BLOCK
                if dist_x < rayon_x + erx + 2 and dist_y < rayon_y + ery + 2:
                    trop_proche = True
                    break
            
            if trop_proche:
                continue
            
            # contenu
            water = randint(0, 1) == 1
            
            # dessin ellipse
            for i_h in range(-rayon_y, rayon_y + 1):
                target_y = coo_y + (SIZE_BLOCK * i_h)
                if target_y not in maps:
                    continue
                if target_y < min_y:
                    continue
                
                # largeur de l'ellipse à cette hauteur
                rapport = 1 - (i_h / rayon_y) ** 2
                largeur = int(rayon_x * math.sqrt(max(0, rapport)))
                
                for i_l in range(-largeur, largeur + 1):
                    target_x = coo_x + i_l
                    if 0 <= target_x < len(maps[target_y]):
                        if i_h == -rayon_y:          # ligne du haut = full
                            maps[target_y][target_x] = "water_full" if water else "lava_full"
                        elif i_h == -rayon_y + 1:    # ligne juste en dessous = normal
                            maps[target_y][target_x] = "water" if water else "lava"
                        else:
                            maps[target_y][target_x] = "air"

            
            placed_cavities.append((coo_x, coo_y, rayon_x, rayon_y))
        
        return maps, placed_cavities
    
    def top_maps(maps):
        # --- Ciel : lignes 5 à 11 ---
        for level_y in range(5, 12):
            maps[level_y_to_pixel_y(level_y)] = ["air"] * width_in_blocks

        # --- LIGNE DE SURFACE (level 4et+) : build de départ ---
        #base lvl 4
        level = ["oak_planks"]*12+["oak_strairs_L"]+["air"]*4+["oak_strairs_R"]+["oak_planks"]*5+["crying_obsidian"]*5+["oak_planks"]*2
        maps[level_y_to_pixel_y(4)] = level
        # couche X lvl 5+
        level = ["oak_log"]+["air"]*5+["oak_log"]+["air"]*23
        maps[level_y_to_pixel_y(5)] = level
        maps[level_y_to_pixel_y(6)] = level
        maps[level_y_to_pixel_y(7)] = level
        level = ["oak_log"]*7+["air"]*23
        maps[level_y_to_pixel_y(8)] = level
        level = ["oak_strairs_R"]+["oak_planks"]*5+["oak_strairs_L"]+["air"]*23
        maps[level_y_to_pixel_y(9)] = level
        level = ["air"]+["oak_strairs_R"]+["oak_planks"]*3+["oak_strairs_L"]+["air"]*24
        maps[level_y_to_pixel_y(10)] = level
        level = ["air"]*2+["oak_strairs_R"]+["oak_planks"]+["oak_strairs_L"]+["air"]*25
        maps[level_y_to_pixel_y(11)] = level
        return maps
    
    def gen_maps(maps, maps_level):
        for i in range(1, PROFONDEUR_PAR_WORLD + 1):
            level_index = 17 - i
            if (maps_level==0):
                level_index = 4 - i
            level = []

            for _ in range(width_in_blocks):
                #100,00%
                roll = randint(0, 10000)
                bloc_choisi = None
                
                for roll_choice in range(len(WORLD_LEVEL[maps_level][2])):
                    seuil = WORLD_LEVEL[maps_level][2][roll_choice]
                    if seuil is not None and seuil >= roll:
                        bloc_choisi = WORLD_LEVEL[maps_level][1][roll_choice]

                level.append(bloc_choisi)
            if(level_index>=5):
                for breack_x in range(3):
                    level[((width_in_blocks//2)+1)-breack_x]="air"
            if(level_index>=15):
                level=["crying_obsidian"]*width_in_blocks
            maps[level_y_to_pixel_y(level_index)] = level

        # Dernière couche = level_index le plus bas - 1 bloc de plus
        bedrock_y = level_y_to_pixel_y(4 - PROFONDEUR_PAR_WORLD - 1)
        maps[bedrock_y] = ["bedrock"] * width_in_blocks
        maps[bedrock_y-1] = ["SPECIAL_BLOCK_TP"] * width_in_blocks
        print(maps)
        return maps

    # ===== CRÉATION DE LA MAP =====
    width_in_blocks = LARGER_FENETRE // block_size

    maps=gen_maps(maps,maps_level)


    # === FIN : tri de haut en bas ===
    #cavité
    placed_cavities = []
    maps, placed_cavities = cavity_generator(maps, placed_cavities)
    if maps_level==0:
        maps = top_maps(maps)
    maps = dict(sorted(maps.items(), key=lambda x: x[0], reverse=True))
    return maps


if __name__ == "__main__":
    maps = create_simple_maps()
    print(f"Niveaux générés : {len(maps)}")
    for k in list(maps.keys())[:5]:
        print(f"  Y={k} -> {maps[k][:6]}...")