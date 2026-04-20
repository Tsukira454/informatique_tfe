import pygame
import os
from ..others.save import *
from config.config import *
from object.games.finish_menu import finish_menu
from object.others.audio_manager import *


class Robot:
    def __init__(self, compte_file, asset_manager=None, maps_level=0):
        self.maps_level = maps_level
        self.image = []
        self.asset_manager = asset_manager
        self.compte_file = compte_file
        self.compte_data = save_load.load_data(compte_file)

        if self.asset_manager is not None:
            self.image_bug = self.asset_manager.get_element("robot_bug")
            self.valeur_image = [0,1,2,3,4,5,6,7,8,20,30,40,50,75,90,100]
            for i in self.valeur_image:
                self.image.append(self.asset_manager.get_element(f"robot_{i}"))
            self.stairs = self.asset_manager.get_element("stairs")
        else:
            self.image_bug = pygame.image.load(ROOT_LOCATION / "assets/images/sprites/robots/robots_bug.png")
            self.image_bug = pygame.transform.scale(self.image_bug, (SIZE_BLOCK, SIZE_BLOCK))
            self.valeur_image = [0,1,2,3,4,5,6,7,8,20,30,40,50,75,90,100]
            for i in self.valeur_image:
                image = pygame.image.load(ROOT_LOCATION / f"assets/images/sprites/robots/robots_{i}.png")
                image = pygame.transform.scale(image, (SIZE_BLOCK, SIZE_BLOCK))
                self.image.append(image)
            self.stairs = pygame.image.load(ROOT_LOCATION / "assets/images/blocks/blocks/stairs.png")
            self.stairs = pygame.transform.scale(self.stairs, (SIZE_BLOCK, SIZE_BLOCK))

        # reste inchangé
        self.pos_x = LARGER_FENETRE//2
        self.pos_y = 696
        self.real_y = self.pos_y
        self.energy_data = self.compte_data["inventory"]["energy"]
        self.pression_data = self.compte_data["inventory"]["pression"]
        self.energy = float(SPECIAL_ITEM_DIC["energy"][1]) * (float(SPECIAL_ITEM_DIC["energy"][2]) ** self.energy_data)
        self.energy_max = self.energy
        self.pression = float(SPECIAL_ITEM_DIC["pression"][1]) * (float(SPECIAL_ITEM_DIC["pression"][2]) ** self.pression_data)
        self.rect = pygame.Rect(self.pos_x, self.pos_y, SIZE_BLOCK, SIZE_BLOCK)
        self.time = 0
        self.speed_x = SIZE_BLOCK
        self.speed_y = 0
        self.gravity = 0.6
        self.on_ground = False
        self.camera_y = 0
        self.collected_resources = {}
        self.block = {}
        self.collect_resource()
        self.liquid_blocks = LIQUID_BLOCK

    def collect_resource(self):
        extensions_images = ('.png')
        for fichier in os.listdir(ROOT_LOCATION / "assets/images/blocks/blocks/"):
            if fichier.lower().endswith(extensions_images):
                resource_name = fichier[:-4]
                if not resource_name in UNCOLECTABLE_BLOCk:
                    self.collected_resources[resource_name] = 0
                self.block[resource_name] = 0
                

    def play_sound_destroy(self):
        if 0==1:
            play_fx(ROOT_LOCATION / "assets/sounds/fx_nexus_destroy_rare.mp3")
        else:
            play_fx(ROOT_LOCATION / "assets/sounds/fx_nexus_destroy.wav")

    def end(self):
        finish_menu(self.block, self.compte_file, self.asset_manager, self.maps_level)
        
    def remove_energy(self, amount):
        self.energy -= amount
        if self.energy <= 0:
            self.end()

    def hud_valeur(self):
        return {"energy": self.energy, "energy_max": self.energy_max, "energy_pourcentage": (self.energy/self.energy_max)*100, "block_list": self.collected_resources, "pression": self.pression, "y": self.real_y//SIZE_BLOCK}

    def move_gravity(self, maps, collision_tiles):
        if not self.on_ground:
            self.speed_y += self.gravity
            self.rect.y += int(self.speed_y)

        self.on_ground = False
        for tile in collision_tiles:
            if self.rect.colliderect(tile):
                if self.speed_y > 0:
                    self.rect.bottom = tile.top
                    self.on_ground = True
                    self.speed_y = 0
                elif self.speed_y < 0:
                    self.rect.top = tile.bottom
                    self.speed_y = 0
        return maps
    
    def screen_y_to_map_key(self, screen_y_pixel):
        """
        Convertit une position Y ecran en cle de map.
        Inverse exact de : screen_y = (HAUTEUR_FENETRE - SIZE_BLOCK - map_key) - camera_y
        Donc             : map_key  =  HAUTEUR_FENETRE - SIZE_BLOCK - screen_y - camera_y
        """
        return HAUTEUR_FENETRE - SIZE_BLOCK - screen_y_pixel - self.camera_y

    def get_closest_map_y(self, maps, screen_y_pixel):
        """
        Retourne la cle de map la plus proche du pixel Y ecran donne.
        """
        target = self.screen_y_to_map_key(screen_y_pixel)
        keys = sorted(int(k) for k in maps.keys())
        closest = keys[0]
        for k in keys:
            if k <= target:
                closest = k
            else:
                break
        return closest

    def move_input(self, maps, collision_tiles):
        keys = pygame.key.get_pressed()

        block_x = self.rect.centerx // SIZE_BLOCK
        # rect.y = haut du sprite = niveau sur lequel le robot se tient
        self.real_y = self.get_closest_map_y(maps, self.rect.y)

        # --------- DEBUG : vider l'énergie ---------
        if keys[pygame.K_d]:
            self.remove_energy(100)

        # --------- GAUCHE ---------
        if keys[pygame.K_LEFT] and self.on_ground:
            self.rect.x -= self.speed_x

            for tile in collision_tiles:
                if self.rect.colliderect(tile):
                    self.rect.left = tile.right
                    target_x = block_x - 1
                    if self.real_y in maps and 0 <= target_x < len(maps[self.real_y]):
                        if self.can_destroy(maps[self.real_y][target_x]):
                            self.block[maps[self.real_y][target_x]] += 1
                            maps[self.real_y][target_x] = "air"
                            self.play_sound_destroy()
                            self.remove_energy(1)

        # --------- DROITE ---------
        elif keys[pygame.K_RIGHT] and self.on_ground:
            self.rect.x += self.speed_x

            for tile in collision_tiles:
                if self.rect.colliderect(tile):
                    self.rect.right = tile.left
                    target_x = block_x + 1
                    if self.real_y in maps and 0 <= target_x < len(maps[self.real_y]):
                        if self.can_destroy(maps[self.real_y][target_x]):
                            self.block[maps[self.real_y][target_x]] += 1
                            maps[self.real_y][target_x] = "air"
                            self.play_sound_destroy()
                            self.remove_energy(1)
        # --------- CREUSER AU-DESSUS ---------
        elif keys[pygame.K_UP] and self.on_ground:
            above = self.get_closest_map_y(maps, self.rect.y - SIZE_BLOCK)
            if above in maps and 0 <= block_x < len(maps[above]):
                if maps[above][block_x] == "air" or maps[above][block_x] in self.liquid_blocks:
                    # air OU liquide → pose des stairs
                    if self.real_y in maps:
                        maps[self.real_y][block_x] = "stairs"
                elif self.can_destroy(maps[above][block_x]):
                    bloc = maps[above][block_x]
                    if bloc in self.block:
                        self.block[bloc] += 1
                    maps[above][block_x] = "air"
                    self.play_sound_destroy()
                    self.remove_energy(1)

        # --------- CREUSER EN DESSOUS ---------
        elif keys[pygame.K_DOWN] and self.on_ground:
            bottom_snapped = (self.rect.bottom // SIZE_BLOCK) * SIZE_BLOCK
            below = self.get_closest_map_y(maps, bottom_snapped)
            if below in maps and 0 <= block_x < len(maps[below]):
                if self.can_destroy(maps[below][block_x]):  # ← below et block_x, pas target_x
                    self.block[maps[below][block_x]] += 1
                    maps[below][block_x] = "air"
                    self.play_sound_destroy()
                    self.remove_energy(1)
        if self.rect.x < 0:
            if(maps[self.real_y][int(LARGER_FENETRE/SIZE_BLOCK)-1] != "air"):
                self.energy-=1
                maps[self.real_y][int(LARGER_FENETRE/SIZE_BLOCK)-1] = "air"
                self.play_sound_destroy()
            self.rect.x = LARGER_FENETRE - SIZE_BLOCK
        elif self.rect.x >= LARGER_FENETRE:
            if(maps[self.real_y][0] != "air"):
                self.energy-=1
                maps[self.real_y][0] = "air"
                self.play_sound_destroy()
            self.rect.x = 0
        return maps

    def can_destroy(self, block_type):
        return block_type != "air" and block_type not in INDESTRUCTIBLE

    def update(self, maps, collision_tiles):
        #if abs(self.real_y // SIZE_BLOCK) >= self.pression + 2:
            #self.remove_energy(self.energy + 1) KILL METHOD
        #    return maps
        self.check_liquid(maps)
        if self.time <= pygame.time.get_ticks() - 80:
            maps = self.move_input(maps, collision_tiles)
            self.time = pygame.time.get_ticks()
        new_maps_check = self.check_new_maps(maps)
        maps = self.move_gravity(maps, collision_tiles)
        return maps, new_maps_check

    def check_new_maps(self,maps):
        block_x = self.rect.centerx // SIZE_BLOCK
        if self.real_y in maps and 0 <= block_x < len(maps[self.real_y]):
            if maps[self.real_y][block_x] == "SPECIAL_BLOCK_TP":
                return True
                
    def check_liquid(self, maps):
        block_x = self.rect.centerx // SIZE_BLOCK
        if self.real_y in maps and 0 <= block_x < len(maps[self.real_y]):
            if maps[self.real_y][block_x] in self.liquid_blocks:
                self.remove_energy(0.1)
                
    def get_pos(self):
        return (self.rect.x, self.rect.y)
    
    def drawn_robots(self):
        energy = (self.energy/self.energy_max)*100
        for i in range(len(self.valeur_image)-8):
            if self.energy == i:
                return self.image[i]
        if energy <= 20:
            return self.image[9]
        elif energy <= 30:
            return self.image[10]
        elif energy <= 40:
            return self.image[11]
        elif energy <= 50:
            return self.image[12]
        elif energy <= 75:
            return self.image[13]
        elif energy <= 90:
            return self.image[14]
        elif energy <= 100:
            return self.image[15]
        return self.image_bug

    def draw(self, screen):
        image = self.drawn_robots()
        screen.blit(image, self.rect)