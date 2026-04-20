import pygame
from config.config import *

class Bird:
    def __init__(self, y, direction="left", asset_manager=None):
        self.direction = direction
        self.speed_x   = 3

        if self.direction == "right":
            self.rect = pygame.Rect(-SIZE_BLOCK, y, SIZE_BLOCK, SIZE_BLOCK)
        else:
            self.rect = pygame.Rect(LARGER_FENETRE, y, SIZE_BLOCK, SIZE_BLOCK)

        # Animation
        self.images      = []
        self.images_flip = []
        self.frame       = 0
        self.anim_speed  = 12
        self.anim_timer  = 0

        # Chargement depuis asset_manager si disponible, sinon depuis le disque
        if asset_manager is not None:
            i = 0
            while True:
                img = asset_manager.get_element(f"bird_{i}")
                if img is None:
                    break
                self.images.append(img)
                self.images_flip.append(pygame.transform.flip(img, True, False))
                i += 1
        else:
            i = 0
            while True:
                path = ROOT_LOCATION / f"assets/images/sprites/bird/bird_{i}.png"
                if not path.exists():
                    break
                img = pygame.transform.scale(pygame.image.load(path), (SIZE_BLOCK, SIZE_BLOCK))
                self.images.append(img)
                self.images_flip.append(pygame.transform.flip(img, True, False))
                i += 1

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed_x
            if self.rect.left > LARGER_FENETRE:
                return False
        else:
            self.rect.x -= self.speed_x
            if self.rect.right < 0:
                return False

        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(self.images)

        return True

    def draw(self, screen):
        if self.direction == "right":
            screen.blit(self.images[self.frame], self.rect)
        else:
            screen.blit(self.images_flip[self.frame], self.rect)