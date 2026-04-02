from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.key import get_pressed
from pygame import K_w, K_a, K_s, K_d, Vector2, draw, image, transform, mouse
import math

class Player(Sprite):
    def __init__(self):
        super().__init__()
        # self.rect = Rect(500, 250, 100, 100)
        self.original_image = image.load('assets/images/player_sprite.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(500, 250))
        self.direction = Vector2()
        self.speed = 400

    def draw_self(self, screen):
        screen.blit(self.image, self.rect)
    
    def input(self):
        keys = get_pressed()
        self.direction = Vector2(int(keys[K_d]) - int(keys[K_a]), int(keys[K_s]) - int(keys[K_w]))
        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

    def rotate_to_mouse(self):
        mouse_pos = mouse.get_pos()
        x, y = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(-y, x))
        self.image = transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt):
        self.input()
        self.move(dt)
        self.rotate_to_mouse()