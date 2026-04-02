import pygame
from pygame import draw
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.rect = pygame.Rect(pos[0], pos[1], 10, 10)
        self.direction = direction
        self.speed = 800

    def draw_self(self,screen):
        draw.circle(screen, (255,255,0), self.rect.center, 10)

    def update(self, dt, screen):
        self.rect.center += self.direction * self.speed * dt
        self.draw_self(screen)
        if not (0 <= self.rect.x <= 1280 and 0 <= self.rect.y <= 720):
            self.kill()