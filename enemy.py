from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame import Vector2, draw, image, transform
import math


class Enemy(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = image.load('assets/images/enemy_sprite.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = Vector2(self.rect.center)
        self.direction = Vector2()
        self.speed = 300

    def draw_self(self, screen):
        screen.blit(self.image, self.rect)

    def find_player(self, player):
        target_vector = Vector2(player.rect.center) - self.pos
        self.direction = target_vector.normalize()

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def rotate_to_player(self, player):
        player_pos = player.rect.center - self.pos
        angle = math.degrees(math.atan2(-player_pos[1], player_pos[0]))
        self.image = transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, player, dt):
        self.find_player(player)
        self.move(dt)
        self.rotate_to_player(player)