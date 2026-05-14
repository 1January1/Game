from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame import sprite
from pygame.key import get_pressed
from pygame import K_w, K_a, K_s, K_d, K_r, Vector2, image, transform, mouse, time
import math
from bullet import Bullet

MAX_HITS = 10
SPEED = 400
SHOOT_COOLDOWN = 200
HURT_COOLDOWN = 500
RELOAD_COOLDOWN = 2000

STARTING_BULLETS = 150
MAGAZINE_MAX_BULLETS = 30

class Player(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = image.load('assets/images/player_sprite.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = Rect(0, 0, 48, 48)
        self.hitbox.center = (x, y)
        self.direction = Vector2()
        self.bullets = sprite.Group()

        self.hits = MAX_HITS
        self.last_hurt_time = 0

        self.active_bullets = MAGAZINE_MAX_BULLETS
        self.available_bullets = STARTING_BULLETS
        self.last_shot_time = 0
        self.last_reload_time = 0
        self.reload_in_progress = False

    def draw_self(self, screen, offset):
        offset_pos = self.rect.topleft - offset
        screen.blit(self.image, offset_pos)
        # draw.rect(screen, "red", self.hitbox.move(-offset.x, -offset.y), 2) # debug hitbox
    
    def input(self, offset):
        current_time = time.get_ticks()

        keys = get_pressed()
        self.direction = Vector2(int(keys[K_d]) - int(keys[K_a]), int(keys[K_s]) - int(keys[K_w]))
        self.direction = self.direction.normalize() if self.direction else self.direction

        if keys[K_r] and not self.reload_in_progress and self.available_bullets > 0 and self.active_bullets != MAGAZINE_MAX_BULLETS:
            self.reload_in_progress = True
            self.last_reload_time = current_time

        if mouse.get_pressed()[0] and not self.reload_in_progress:
            if current_time - self.last_shot_time > SHOOT_COOLDOWN and self.active_bullets > 0:
                self.shoot(offset)
                self.active_bullets -= 1
                self.last_shot_time = current_time
    
    def check_reload(self):
        if self.reload_in_progress:
            current_time = time.get_ticks()
            if current_time - self.last_shot_time > RELOAD_COOLDOWN:
                self.reload_in_progress = False
                bullets_needed = MAGAZINE_MAX_BULLETS - self.active_bullets
                if bullets_needed <= self.available_bullets:
                    self.active_bullets = MAGAZINE_MAX_BULLETS
                    self.available_bullets -= bullets_needed
                else:
                    self.active_bullets = self.available_bullets
                    self.available_bullets = 0


    def shoot(self, offset):
        m_pos = Vector2(mouse.get_pos()) + offset
        p_pos = Vector2(self.hitbox.center)
        bullet_dir = (m_pos - p_pos).normalize() if (m_pos - p_pos).length() > 0 else Vector2(1, 0)
        self.bullets.add(Bullet(self.rect.center, bullet_dir))

    def try_hurt(self):
        current_time = time.get_ticks()
        if current_time - self.last_hurt_time > HURT_COOLDOWN:
            self.hits -= 1
            self.last_hurt_time = current_time
        return self.hits <= 0

    def collision(self, walls, direction):
        for wall in walls:
            if self.hitbox.colliderect(wall.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = wall.rect.left
                    if self.direction.x < 0:
                        self.hitbox.left = wall.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox.bottom = wall.rect.top
                    if self.direction.y < 0:
                        self.hitbox.top = wall.rect.bottom
    
    def move(self, dt, walls):
        self.hitbox.x += self.direction.x * SPEED * dt
        self.collision(walls, 'horizontal')
        self.hitbox.y += self.direction.y * SPEED * dt
        self.collision(walls, 'vertical')

    def rotate_to_mouse(self, offset):
        mouse_pos = mouse.get_pos()
        screen_player_pos = Vector2(self.hitbox.center) - offset
        dx = mouse_pos[0] - screen_player_pos.x
        dy = mouse_pos[1] - screen_player_pos.y
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self, dt, screen, offset, walls):
        self.input(offset)
        self.check_reload()
        self.move(dt, walls)
        self.rotate_to_mouse(offset)
        self.draw_self(screen, offset)
        self.bullets.update(dt, screen, offset, walls)