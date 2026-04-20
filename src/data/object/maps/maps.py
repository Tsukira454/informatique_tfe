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
    def _galeries(maps, placed_cavities, surface_y, min_y):
        """Creuse des tunnels de 2 blocs entre cavités voisines (triées par x)."""
        if len(placed_cavities) < 2:
            return maps

        sorted_cavites = sorted(placed_cavities, key=lambda c: c[0])

        for i in range(len(sorted_cavites) - 1):
            x1, y1 = sorted_cavites[i][0],     sorted_cavites[i][1]
            x2, y2 = sorted_cavites[i + 1][0], sorted_cavites[i + 1][1]

            dist_x        = abs(x2 - x1)
            dist_y_blocs  = abs(y2 - y1) / SIZE_BLOCK

            # Ne connecte que les voisines pas trop éloignées
            if dist_x > 14 or dist_y_blocs > 7:
                continue

            steps = max(dist_x, 1)
            for step in range(steps + 1):
                t  = step / steps
                cx = round(x1 + (x2 - x1) * t)
                cy_snap = round((y1 + (y2 - y1) * t) / SIZE_BLOCK) * SIZE_BLOCK

                if cy_snap >= surface_y or cy_snap < min_y:
                    continue

                # 2 blocs de haut (sol + plafond du tunnel)
                for dh in range(2):
                    ty = cy_snap + dh * SIZE_BLOCK
                    if ty in maps and 0 <= cx < len(maps[ty]):
                        maps[ty][cx] = "air"

        return maps

    def cavity_generator(maps, placed_cavities):
        import math

        bedrock_y = level_y_to_pixel_y(4 - PROFONDEUR_PAR_WORLD - 1)
        surface_y = level_y_to_pixel_y(3)          # premier bloc underground
        min_y     = bedrock_y + SIZE_BLOCK * 4     # marge au-dessus de la bedrock

        nb_cavites = randint(5, 9)
        tentatives = 0

        while len(placed_cavities) < nb_cavites and tentatives < 200:
            tentatives += 1

            rayon_x = randint(4, 9)
            rayon_y = randint(2, 4)

            # Plage y en index de niveau, assez loin de la surface ET de la bedrock
            max_level = -rayon_y - 2
            min_level = -PROFONDEUR_PAR_WORLD + rayon_y + 4
            if min_level > max_level:
                continue

            coo_x = randint(rayon_x + 2, width_in_blocks - rayon_x - 2)
            coo_y = level_y_to_pixel_y(randint(min_level, max_level))

            # Garde de sécurité bedrock et surface
            if coo_y - rayon_y * SIZE_BLOCK < min_y:
                continue
            if coo_y + rayon_y * SIZE_BLOCK >= surface_y:
                continue

            # Vérifie chevauchement avec cavités existantes (marge +3 blocs)
            trop_proche = False
            for (ex, ey, erx, ery) in placed_cavities:
                dist_x = abs(coo_x - ex)
                dist_y = abs(coo_y - ey) / SIZE_BLOCK
                if dist_x < rayon_x + erx + 3 and dist_y < rayon_y + ery + 2:
                    trop_proche = True
                    break

            if trop_proche:
                continue

            water = randint(0, 1) == 1

            # Dessin ellipse
            for i_h in range(-rayon_y, rayon_y + 1):
                target_y = coo_y + SIZE_BLOCK * i_h
                if target_y not in maps:
                    continue

                rapport = 1 - (i_h / rayon_y) ** 2
                largeur = int(rayon_x * math.sqrt(max(0, rapport)))

                for i_l in range(-largeur, largeur + 1):
                    target_x = coo_x + i_l
                    if 0 <= target_x < len(maps[target_y]):
                        if i_h == -rayon_y:        # fond de la cavité = liquide plein
                            maps[target_y][target_x] = "water_full" if water else "lava_full"
                        elif i_h == -rayon_y + 1:  # surface du liquide
                            maps[target_y][target_x] = "water" if water else "lava"
                        else:
                            maps[target_y][target_x] = "air"

            placed_cavities.append((coo_x, coo_y, rayon_x, rayon_y))

        maps = _galeries(maps, placed_cavities, surface_y, min_y)
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