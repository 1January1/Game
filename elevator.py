import pygame
from pygame.sprite import Sprite


class Elevator(Sprite):
    def __init__(self, x, y, width, height, name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
