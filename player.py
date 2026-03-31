from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.key import get_pressed
from pygame import K_w, K_a, K_s, K_d, Vector2, draw

class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.rect = Rect(500, 250, 80, 80)
        # self.rect.center = (0, 0)

        self.direction = Vector2()
        self.speed = 400

    def draw_self(self, screen):
        draw.rect(screen, (225, 0, 0), self.rect)
    
    def input(self):
        keys = get_pressed()
        self.direction = Vector2(int(keys[K_d]) - int(keys[K_a]), int(keys[K_s]) - int(keys[K_w]))
        self.direction = self.direction.normalize() if self.direction else self.direction
        print(self.direction)
    
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt
    
    def update(self, dt):
        self.input()
        self.move(dt)