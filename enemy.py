from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame import Vector2, draw, image, transform, sprite
import math


class Enemy(Sprite):
    def __init__(self, x, y, room):
        super().__init__()
        self.original_image = image.load('assets/images/enemy_sprite.png')
        self.image = self.original_image
        self.hitbox = Rect(0, 0, 48, 48)
        self.hitbox.center = (x, y)
        self.rect = self.image.get_rect(center=(self.hitbox.x, self.hitbox.y))
        self.pos = Vector2(self.hitbox.center)
        self.direction = Vector2()
        self.speed = 300
        self.room = room
        print(self.room)

    def draw_self(self, screen, offset):
        offset_pos = self.rect.topleft - offset
        screen.blit(self.image, offset_pos)

    def find_player(self, player):
        target_vector = Vector2(player.rect.center) - self.pos
        self.direction = target_vector.normalize()

    def check_collision(self, walls, direction):
        for wall in walls:
            if self.hitbox.colliderect(wall.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox.right = wall.rect.left
                    if self.direction.x < 0: self.hitbox.left = wall.rect.right
                    self.pos.x = self.hitbox.centerx

                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox.bottom = wall.rect.top
                    if self.direction.y < 0: self.hitbox.top = wall.rect.bottom
                    self.pos.y = self.hitbox.centery

    def move(self, dt, walls):
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.check_collision(walls, 'horizontal')
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.check_collision(walls, 'vertical')
        self.rect.center = self.hitbox.center

    def rotate_to_player(self, player):
        player_pos = Vector2(player.rect.center) - self.pos
        angle = math.degrees(math.atan2(-player_pos.y, player_pos.x))
        self.image = transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self, player, dt, walls):
        self.find_player(player)
        self.move(dt, walls)
        self.rotate_to_player(player)
