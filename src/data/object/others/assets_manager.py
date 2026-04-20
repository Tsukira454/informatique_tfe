import pygame
import threading
from ..others.logger import *
class Assets_manager:
    def __init__(self, element, element_size, element_name):
        self.element = element
        self.element_size = element_size
        self.element_name = element_name
        self.nbr_element_load = 0
        self.element_load = {}
        self.loaded = False

        thread = threading.Thread(target=self._load_element)
        thread.daemon = True
        thread.start()
        
    def _load_element(self):
        for i in range(len(self.element)):
            images = pygame.image.load(self.element[i])
            images = pygame.transform.scale(images, self.element_size[i])
            self.element_load[self.element_name[i]] = images
            self.nbr_element_load += 1
        self.loaded = True
        
    def get_load_completion(self):
        if self.nbr_element_load == 0:
            return 0
        logger.info(f"Chargement de {self.element_name[self.nbr_element_load]}-> {self.nbr_element_load}/{len(self.element)} | {int((self.nbr_element_load / len(self.element)) * 100)}%")
        return int((self.nbr_element_load / len(self.element)) * 100)
    
    def get_element(self, element_to_get):
        return self.element_load.get(element_to_get, None)