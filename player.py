from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame import sprite
from pygame.key import get_pressed
from pygame import K_w, K_a, K_s, K_d, Vector2, draw, image, transform, mouse, time
import math
from bullet import Bullet

class Player(Sprite):
    def __init__(self):
        super().__init__()
        # self.rect = Rect(500, 250, 100, 100)
        self.original_image = image.load('assets/images/player_sprite.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(500, 250))
        self.direction = Vector2()
        self.speed = 400
        self.last_shot_time = 0
        self.shoot_cooldown = 200
        self.bullets = sprite.Group()

    def draw_self(self, screen):
        screen.blit(self.image, self.rect)
    
    def input(self):
        keys = get_pressed()
        self.direction = Vector2(int(keys[K_d]) - int(keys[K_a]), int(keys[K_s]) - int(keys[K_w]))
        self.direction = self.direction.normalize() if self.direction else self.direction
        if mouse.get_pressed()[0]:
            current_time = time.get_ticks()
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.shoot()
                self.last_shot_time = current_time

    def shoot(self):
        m_pos = Vector2(mouse.get_pos())
        p_pos = Vector2(self.rect.center)
        bullet_dir = (m_pos - p_pos).normalize()
        self.bullets.add(Bullet(self.rect.center, bullet_dir))
    
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

    def rotate_to_mouse(self):
        mouse_pos = mouse.get_pos()
        x, y = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(-y, x))
        self.image = transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt, screen):
        self.input()
        self.move(dt)
        self.rotate_to_mouse()
        self.draw_self(screen)
        self.bullets.update(dt, screen)