import pygame
from config.config import *

class Animation_rocket:
    def __init__(self, folder_image, asset_manager):
        self.images = []
        self.folder_image = folder_image
        self.pos_x = (LARGER_FENETRE//10)*8
        self.pos_y = -200  # démarre hors écran en haut
        self.speed = 8
        self.actuel_frame = 0
        self.anim_timer = 0
        self.anim_speed = 6  # frames entre chaque image

        # phases : "descend", "wait", "remonte", "done"
        self.phase = "descend"
        self.wait_timer = 0
        self.wait_duration = 60  # frames d'attente avant de remonter
        self.target_y = HAUTEUR_FENETRE // 2 - 200  # position d'arrêt

        if asset_manager is not None:
            i = 0
            while True:
                img = asset_manager.get_element(f"{self.folder_image}_{i}")
                if img is None:
                    break
                self.images.append(img)
                i += 1

    def update(self):
        # animation frames
        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.actuel_frame = (self.actuel_frame + 1) % len(self.images)

        # phases de mouvement
        if self.phase == "descend":
            self.pos_y += self.speed
            if self.pos_y >= self.target_y:
                self.pos_y = self.target_y
                self.phase = "wait"

        elif self.phase == "wait":
            self.wait_timer += 1
            if self.wait_timer >= self.wait_duration:
                self.phase = "remonte"

        elif self.phase == "remonte":
            self.pos_y -= self.speed * 2  # remonte plus vite
            if self.pos_y < -300:
                self.phase = "done"

    def is_done(self):
        return self.phase == "done"

    def show_robot(self):
        # affiche le robot pendant la phase wait et remonte
        return self.phase in ("wait", "remonte")

    def draw(self, screen):
        if not self.images:
            return
        img = self.images[self.actuel_frame]
        screen.blit(img, (self.pos_x - img.get_width() // 2, self.pos_y))
    def get_pos(self):
        return (self.pos_x, self.pos_y)