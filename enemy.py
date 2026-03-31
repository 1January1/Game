from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame import Vector2, draw


class Enemy(Sprite):
    def __init__(self):
        super().__init__()
        self.rect = Rect(100, 250, 80, 80)
        self.pos = Vector2(self.rect.center)
        self.direction = Vector2()
        self.speed = 300

    def draw_self(self, screen):
        draw.rect(screen, (0, 0, 225), self.rect)

    def find_player(self, player):
        target_vector = Vector2(player.rect.center) - self.pos
        self.direction = target_vector.normalize()

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self, player, dt):
        self.find_player(player)
        self.move(dt)