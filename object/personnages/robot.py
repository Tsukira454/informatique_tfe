import pygame
import sys
from pathlib import Path
from math import floor
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from config.config import LARGER_FENETRE, HAUTEUR_FENETRE, SIZE_BLOCK
from object.ui.finish_menu import finish_menu


class Robot:
    def __init__(self):
        # Sprite
        self.image = []
        self.image_bug = pygame.image.load("./assets/sprites/robots/robots_bug.png")
        self.image_bug = pygame.transform.scale(self.image_bug, (SIZE_BLOCK, SIZE_BLOCK))
        self.valeur_image=[0,1,2,3,4,5,6,7,8,20,30,40,50,75,90,100]
        for i in range(len(self.valeur_image)):
            image = pygame.image.load(f"./assets/sprites/robots/robots_{self.valeur_image[i]}.png")
            image = pygame.transform.scale(image, (SIZE_BLOCK, SIZE_BLOCK))
            self.image.append(image)
        #print(self.image)
        self.stairs = pygame.image.load("./assets/blocks/blocks/stairs.png")
        self.stairs = pygame.transform.scale(self.stairs, (SIZE_BLOCK, SIZE_BLOCK))
        self.pos_x = 0
        self.pos_y = 696
        self.energy = 100
        self.energy_max = 100
        # Position rectangle
        self.rect = pygame.Rect(self.pos_x, self.pos_y, SIZE_BLOCK, SIZE_BLOCK)
        self.time = 0

        # Physique
        self.speed_x = SIZE_BLOCK
        self.speed_y = 0
        self.gravity = 0.6
        self.on_ground = False

    def end(self):
        finish_menu([0])
        
    def remove_energy(self, amount):
        self.energy-=amount
        if self.energy <= 0:
            self.end()

    def hud_valeur(self):
        return {"energy" : self.energy, "energy_max" : self.energy_max, "energy_pourcentage" : (self.energy/self.energy_max)*100}
    def move_gravity(self, maps, collision_tiles):
        if not self.on_ground:
            self.speed_y += self.gravity
            self.rect.y += int(self.speed_y)

        # Vérifier les collisions verticales
        self.on_ground = False
        for tile in collision_tiles:
            if self.rect.colliderect(tile):
                if self.speed_y > 0:  # En train de tomber
                    self.rect.bottom = tile.top
                    self.on_ground = True
                    self.speed_y = 0
                    #print(maps)
                elif self.speed_y < 0:  # En train de sauter
                    self.rect.top = tile.bottom
                    self.speed_y = 0
        return maps
    
    def get_closest_map_y(self, maps, y_pixel):
        """
        Retourne la clé de maps la plus proche de y_pixel (vers le bas),
        c'est-à-dire la ligne de la map correspondant au pixel y du robot.
        """
        keys = [int(k) for k in maps.keys()]
        keys.sort()
        closest = keys[0]
        y_pos = abs(y_pixel-1080)
        for k in keys:
            if k <= y_pos:
                closest = k
            else:
                break
        return closest


    def move_input(self, maps, collision_tiles):
        keys = pygame.key.get_pressed()

        # Calculs communs
        block_x = self.rect.centerx // SIZE_BLOCK
        real_y = self.get_closest_map_y(maps, self.rect.bottom - 1)

        # --------- GAUCHE ---------
        if keys[pygame.K_LEFT] and self.on_ground:
            self.rect.x -= self.speed_x

            for tile in collision_tiles:
                if self.rect.colliderect(tile):
                    self.rect.left = tile.right

                    target_x = block_x - 1
                    if real_y in maps and 0 <= target_x < len(maps[real_y]):
                        maps[real_y][target_x] = "air"
                        self.remove_energy(1)

        # --------- DROITE ---------
        elif keys[pygame.K_RIGHT] and self.on_ground:
            self.rect.x += self.speed_x

            for tile in collision_tiles:
                if self.rect.colliderect(tile):
                    self.rect.right = tile.left

                    target_x = block_x + 1
                    if real_y in maps and 0 <= target_x < len(maps[real_y]):
                        maps[real_y][target_x] = "air"
                        self.remove_energy(1)

        # --------- CREUSER AU-DESSUS ---------
        elif keys[pygame.K_UP] and self.on_ground:
            above = self.get_closest_map_y(maps, self.rect.top - 1)

            if above in maps and 0 <= block_x < len(maps[above]):
                if maps[above][block_x] != "air":
                    maps[above][block_x] = "air"
                    self.remove_energy(1)
                else:
                    # Pose un escalier si bloc au-dessus déjà vide
                    if real_y in maps:
                        maps[real_y][block_x] = "stairs"

        # --------- CREUSER EN DESSOUS ---------
        elif keys[pygame.K_DOWN] and self.on_ground:
            below = self.get_closest_map_y(maps, self.rect.bottom + 1)

            if below in maps and 0 <= block_x < len(maps[below]):
                maps[below][block_x] = "air"
                self.remove_energy(1)

        return maps


    def update(self, maps, collision_tiles):
        if self.time <= pygame.time.get_ticks()-80:  # Limiter la vitesse de déplacement
            maps = self.move_input(maps, collision_tiles)
            self.time = pygame.time.get_ticks()
        maps = self.move_gravity(maps, collision_tiles)
        return maps

    def get_pos(self):
        return (self.rect.x, self.rect.y)
    
    def drawn_robots(self):
        energy = (self.energy/self.energy_max)*100
        #print(energy)
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

