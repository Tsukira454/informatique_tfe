import pygame
from config.config import *

class MovingBlock:
    def __init__(self, name, asset_manager=None):
        self.name = name
        self.images = []
        self.anim_speed = 12
        self.anim_timer = 0
        self.frame = 0
        i = 0
        while True:
            if asset_manager is not None:
                img = asset_manager.get_element(f"{name}_{i}")
                if img is None:
                    break
                self.images.append(img)
            else:
                path = ROOT_LOCATION / f"assets/images/blocks/blocks/{name}/{name}_{i}.png"
                if not path.exists():
                    break
                img = pygame.transform.scale(pygame.image.load(path), (SIZE_BLOCK, SIZE_BLOCK))
                self.images.append(img)
            i += 1

    def update(self):
        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(self.images)

    def get_image(self):
        return self.images[self.frame]