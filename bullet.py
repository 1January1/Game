import pygame
from pygame import draw, Vector2, sprite
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.rect = pygame.Rect(pos[0], pos[1], 5, 5)
        self.pos = Vector2(self.rect.center)
        self.direction = direction
        self.speed = 1500

    def draw_self(self, screen, offset):
        draw_pos = self.rect.center - offset
        draw.circle(screen, (255, 255, 0), draw_pos, 5)

    def wall_collision(self, walls):
        if sprite.spritecollide(self, walls, False):
            self.kill()

    def update(self, dt, screen, offset, walls):
        self.pos += self.direction * self.speed * dt
        self.wall_collision(walls)
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.draw_self(screen, offset)
        if not (-2000 <= self.rect.x <= 5000 and -2000 <= self.rect.y <= 5000):  # Map limits
            self.kill()