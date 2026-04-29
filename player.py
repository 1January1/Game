from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame import sprite
from pygame.key import get_pressed
from pygame import K_w, K_a, K_s, K_d, Vector2, draw, image, transform, mouse, time
import math
from bullet import Bullet
import pytmx


class Player(Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.rect = Rect(500, 250, 100, 100)
        self.original_image = image.load('assets/images/player_sprite.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = Vector2()
        self.speed = 400
        self.last_shot_time = 0
        self.shoot_cooldown = 200
        self.bullets = sprite.Group()

    def draw_self(self, screen, offset):
        offset_pos = self.rect.topleft - offset
        screen.blit(self.image, offset_pos)
    
    def input(self, offset):
        keys = get_pressed()
        self.direction = Vector2(int(keys[K_d]) - int(keys[K_a]), int(keys[K_s]) - int(keys[K_w]))
        self.direction = self.direction.normalize() if self.direction else self.direction
        if mouse.get_pressed()[0]:
            print("Clicked")
            current_time = time.get_ticks()
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.shoot(offset)
                self.last_shot_time = current_time

    def shoot(self, offset):
        m_pos = Vector2(mouse.get_pos()) + offset
        p_pos = Vector2(self.rect.center)
        bullet_dir = (m_pos - p_pos).normalize() if (m_pos - p_pos).length() > 0 else Vector2(1, 0)
        self.bullets.add(Bullet(self.rect.center, bullet_dir))
    
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

    def rotate_to_mouse(self, offset):
        mouse_pos = mouse.get_pos()
        screen_player_pos = Vector2(self.rect.center) - offset
        dx = mouse_pos[0] - screen_player_pos.x
        dy = mouse_pos[1] - screen_player_pos.y
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt, screen, offset):
        self.input(offset)
        self.move(dt)
        self.rotate_to_mouse(offset)
        self.draw_self(screen, offset)
        self.bullets.update(dt, screen, offset)