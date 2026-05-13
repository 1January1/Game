from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame import Vector2, draw, image, transform
import pygame

import math

MAX_HITS = 2


class Hostage(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = image.load('assets/images/hostage_sprite.png')
        self.image = self.original_image
        self.hitbox = Rect(0, 0, 48, 48)
        self.hitbox.center = (x, y)
        self.rect = self.image.get_rect(center=(self.hitbox.x, self.hitbox.y))
        self.pos = Vector2(self.hitbox.center)
        self.hits = MAX_HITS

    def draw_self(self, screen, offset):
        offset_pos = self.rect.topleft - offset
        screen.blit(self.image, offset_pos)
        if self.hits != MAX_HITS:
            self.draw_healthbar(screen, offset)

    def rotate_to_player(self, player):
        player_pos = Vector2(player.rect.center) - self.pos
        angle = math.degrees(math.atan2(-player_pos.y, player_pos.x))
        self.image = transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def draw_healthbar(self, display_surface, offset):
        origin = self.pos - offset + Vector2(-50, -50)
        pygame.draw.rect(display_surface, "#000000", pygame.Rect(origin[0], origin[1], 100, 30))
        pygame.draw.rect(display_surface, "#FF0000", pygame.Rect(origin[0] + 5, origin[1] + 5, self.hits * 30, 20))

    def hit(self, ):
        self.hits -= 1
        if self.hits < 1:
            self.kill()

    def update(self, player):
        self.rotate_to_player(player)
