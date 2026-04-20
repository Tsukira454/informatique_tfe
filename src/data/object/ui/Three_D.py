import pygame
import threading
from pathlib import Path

class Three_D:
    def __init__(self, images, frame_delay=1):
        self.frame = 0
        self.anim_timer = 0
        self.frame_delay = frame_delay
        self.images = images
        self.file_number = len(images)
        self.loaded = True 

    def _load_images(self):
        images = []
        for i in range(1, self.file_number + 1):
            img = pygame.image.load(self.folder_images / f"{i:04d}.png")
            img = pygame.transform.scale(img, (self.width, self.height))
            images.append(img)
        self.images = images
        self.loaded = True
        print("Chargement terminé !")

    def update(self):
        if not self.loaded:
            return  # pas encore prêt
        self.anim_timer += 1
        if self.anim_timer >= self.frame_delay:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % self.file_number

    def draw(self, screen, x, y):
        if not self.loaded:
            # affiche un texte de chargement en attendant
            font = pygame.font.SysFont(None, 36)
            text = font.render("Chargement...", True, (255, 255, 255))
            screen.blit(text, (x, y))
            return
        screen.blit(self.images[self.frame], (x, y))