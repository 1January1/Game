import pygame
from pygame.sprite import Sprite


class Wall(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 64, 64)
