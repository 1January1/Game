from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame import Vector2, image
import pygame


class Bomb(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = image.load('assets/images/bomb_sprite.png')
        self.image = self.original_image
        self.hitbox = Rect(0, 0, 48, 48)
        self.hitbox.center = (x, y)
        self.rect = self.image.get_rect(center=(self.hitbox.x, self.hitbox.y))
        self.pos = Vector2(self.hitbox.center)
        self.active = True

    def draw_self(self, screen, offset):
        offset_pos = self.rect.topleft - offset
        screen.blit(self.image, offset_pos)
        self.draw_attention(screen, offset)
    
    def draw_attention(self, screen, offset):
        if self.active:
            origin = self.pos - offset + Vector2(25, -75)
            pygame.draw.rect(screen, "#000000", pygame.Rect(origin[0], origin[1], 15, 60))
            pygame.draw.rect(screen, "#FF0000", pygame.Rect(origin[0] + 5, origin[1] + 5, 5, 50))
            pygame.draw.rect(screen, "#000000", pygame.Rect(origin[0], origin[1] + 70, 15, 15))
            pygame.draw.rect(screen, "#FF0000", pygame.Rect(origin[0] + 5, origin[1] + 75, 5, 5))
