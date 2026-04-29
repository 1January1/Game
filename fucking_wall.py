import pygame
from pygame.sprite import Sprite


class Wall(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 64, 64)

    def draw(self, screen, offset):
        # Subtract the offset only for rendering
        offset_pos = self.rect.topleft - offset
        pygame.draw.rect(screen, (100, 100, 100), (*offset_pos, 64, 64))