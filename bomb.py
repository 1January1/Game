from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame import Vector2, image


class Bomb(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = image.load('assets/images/bomb_sprite.png')
        self.image = self.original_image
        self.hitbox = Rect(0, 0, 48, 48)
        self.hitbox.center = (x, y)
        self.rect = self.image.get_rect(center=(self.hitbox.x, self.hitbox.y))
        self.pos = Vector2(self.hitbox.center)

    def draw_self(self, screen, offset):
        offset_pos = self.rect.topleft - offset
        screen.blit(self.image, offset_pos)
