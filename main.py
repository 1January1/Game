import pygame
from pygame import display, Vector2, font, time
from player import Player, RELOAD_COOLDOWN
from pygame.time import Clock
import pytmx
from enemy import Enemy
from fucking_wall import Wall
from trigger import Trigger
from hostage import Hostage
from bomb import Bomb
from elevator import Elevator

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Police Raid')
        self.tmx_data = pytmx.util_pygame.load_pygame("assets/maps/level1.tmx")
        self.clock = Clock()
        self.stopped = False
        self.offset = Vector2()
        self.active_enemies = pygame.sprite.Group()
        self.passive_enemies = pygame.sprite.Group()
        self.hostages = pygame.sprite.Group()
        self.font = font.SysFont("comicsans", 40)
        self.title_font = font.SysFont("comicsans", 80)
        self.walls = pygame.sprite.Group()
        self.room_triggers = pygame.sprite.Group()
        self.elevator_trigger = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.bomb_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.bomb_event, 1000)
        self.explosion = False
        self.explosion_size = 10
        self.explosion_sprite= pygame.image.load("assets/images/explosion_sprite.png")

        self.game_overed = False
        self.won = False

        self.load_level(self.tmx_data)

        self.level = 1


    def draw_map(self, surface):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        pixel_x = (x * self.tmx_data.tilewidth) - self.offset.x
                        pixel_y = (y * self.tmx_data.tileheight) - self.offset.y
                        surface.blit(tile, (pixel_x, pixel_y))

    def wall_spawn(self, level):
        wall_layer = level.get_layer_by_name("walls")
        for x, y, gid in wall_layer:
            if gid != 0:
                pixel_x = x * level.tilewidth
                pixel_y = y * level.tileheight
                self.walls.add(Wall(pixel_x, pixel_y))

    def room_trigger_spawn(self, level):
        trigger_layer = level.get_layer_by_name("room triggers")
        for trigger in trigger_layer:
            self.room_triggers.add(Trigger(trigger.x, trigger.y, trigger.width, trigger.height, trigger.name))

    def elevator_trigger_spawn(self, level):
        trigger_layer = level.get_layer_by_name("elevator trigger")
        for trigger in trigger_layer:
            self.elevator_trigger.add(Elevator(trigger.x, trigger.y, trigger.width, trigger.height, trigger.name))

    def spawn(self, level):
        spawn_layer = level.get_layer_by_name("spawn points")
        for object in spawn_layer:
            if object.name == "Player spawn":
                self.player = Player(object.x, object.y)
            if object.name == "Enemy spawn":
                self.passive_enemies.add(Enemy(object.x, object.y, object.properties["Room"]))
            if object.name == "Hostage spawn":
                self.hostages.add(Hostage(object.x, object.y))
                self.hostages_left += 1
            if object.name == "Bomb spawn":
                self.bombs.add(Bomb(object.x, object.y))
                self.bombs_left += 1

    def load_level(self, level):
        self.counter = 180
        self.hostages_left = 0
        self.bombs_left = 0
        self.explosion = False
        self.explosion_size = 10
        if self.walls:
            self.walls = pygame.sprite.Group()
        if self.room_triggers:
            self.room_triggers = pygame.sprite.Group()
        if self.elevator_trigger:
            self.elevator_trigger = pygame.sprite.Group()
        if self.passive_enemies:
            self.passive_enemies = pygame.sprite.Group()
        if self.active_enemies:
            self.active_enemies = pygame.sprite.Group()
        if self.hostages:
            self.hostages = pygame.sprite.Group()
        if self.bombs:
            self.bombs = pygame.sprite.Group()
        self.wall_spawn(level)
        self.room_trigger_spawn(level)
        self.elevator_trigger_spawn(level)
        self.spawn(level)
    
    def draw_hud_text(self, label, posx, posy):
        text = self.font.render(label, True, "#ffffff")
        text_size = self.font.size(label)
        pygame.draw.rect(self.display_surface, "#000000", pygame.Rect(posx, posy, text_size[0] + 10, text_size[1] + 10))
        self.display_surface.blit(text, (posx + 5, posy + 5))

    def render_hud(self):
        pygame.draw.rect(self.display_surface, "#000000", pygame.Rect(10, WINDOW_HEIGHT - 40, 190, 30))
        pygame.draw.rect(self.display_surface, "#FF0000", pygame.Rect(15, WINDOW_HEIGHT - 40 + 5, self.player.hits * 18, 20))

        label = f"Laskemoon: {self.player.active_bullets} | {self.player.available_bullets}"
        if self.player.active_bullets == 0 and self.player.available_bullets > 0:
            label += " | Vajuta R"
        self.draw_hud_text(label, 10, WINDOW_HEIGHT - 90)

        text_size = self.font.size(label)
        if self.player.reload_in_progress:
            current_time = time.get_ticks()
            pygame.draw.rect(self.display_surface, "#000000", pygame.Rect(10 + text_size[0] + 20, WINDOW_HEIGHT - 90, 190, text_size[1] + 10))
            bar_length = (current_time - self.player.last_shot_time) / RELOAD_COOLDOWN * 180
            pygame.draw.rect(self.display_surface, "#FFFFFF", pygame.Rect(10 + text_size[0] + 25, WINDOW_HEIGHT - 90 + 5, bar_length, text_size[1]))
        
        label = f"Veel vange: {self.hostages_left}"
        text_size = self.font.size(label)
        self.draw_hud_text(label, WINDOW_WIDTH - text_size[0] - 20, 10)

        offsety = text_size[1] + 30
        label = f"Veel pomme: {self.bombs_left}"
        text_size = self.font.size(label)
        self.draw_hud_text(label, WINDOW_WIDTH - text_size[0] - 20, offsety)

        label = f"{self.counter // 60}:{(self.counter % 60):02d}"
        text_size = self.font.size(label)
        self.draw_hud_text(label, WINDOW_WIDTH - text_size[0] - 20, WINDOW_HEIGHT - text_size[1] - 20)

    def game_over_menu(self):
        mouse = pygame.mouse.get_pos()
        self.display_surface.fill("#000000")

        title = "Aitäh mängimise eest!" if self.won else "Proovi uuesti!"
        button_text = "Alusta algusest"
        title_size = self.title_font.size(title)
        button_text_size = self.font.size(button_text)
        origin = (WINDOW_WIDTH // 2 - title_size[0] // 2, WINDOW_HEIGHT // 2 - (title_size[1] + button_text_size[1] + 15) // 2)
        button = pygame.Rect(WINDOW_WIDTH // 2 - button_text_size[0] // 2, origin[1] + title_size[1] + 15,
                            button_text_size[0] + 10, button_text_size[1] + 10)
        
        colliding = button.collidepoint(mouse)
        self.display_surface.blit(self.title_font.render(title, True, "#ffffff"), origin)
        pygame.draw.rect(self.display_surface, "#000000" if colliding else "#ffffff", button)
        self.display_surface.blit(self.font.render(button_text, True, "#ffffff" if colliding else "#000000"),
                                  (button.x + 5, button.y + 5))
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(mouse):
                    self.level = 1
                    self.game_overed = False
                    self.won = False

                    self.tmx_data = pytmx.util_pygame.load_pygame("assets/maps/level1.tmx")
                    self.load_level(self.tmx_data)

    def game_run(self):
        self.offset.x = self.player.rect.centerx - WINDOW_WIDTH // 2
        self.offset.y = self.player.rect.centery - WINDOW_HEIGHT // 2

        triggered_room = pygame.sprite.spritecollide(self.player, self.room_triggers, False)
        if triggered_room:
            for enemy in self.passive_enemies:
                if enemy.room == triggered_room[0].name:
                    self.passive_enemies.remove(enemy)
                    self.active_enemies.add(enemy)
                    triggered_room[0].kill()

        for bullet in self.player.bullets:
            collided_enemy = pygame.sprite.spritecollide(bullet, self.active_enemies, False)
            collided_hostage = pygame.sprite.spritecollide(bullet, self.hostages, False)
            if collided_enemy:
                for sprite in collided_enemy:
                    sprite.hit()
                bullet.kill()
            if collided_hostage:
                for sprite in collided_hostage:
                    if sprite.hit():
                        self.game_overed = True
                bullet.kill()

        hit_player = pygame.sprite.spritecollide(self.player, self.active_enemies, False)
        if hit_player:
            if self.player.try_hurt():
                self.game_overed = True

        triggered_elevator = pygame.sprite.spritecollide(self.player, self.elevator_trigger, False)
        requirements_met = self.hostages_left == 0 and self.bombs_left == 0
        if triggered_elevator and requirements_met:
            for elevator in triggered_elevator:
                if elevator.name == "lvl1-2":
                    self.level = 2
                    self.tmx_data = pytmx.util_pygame.load_pygame("assets/maps/level2.tmx")
                    self.load_level(self.tmx_data)
                if elevator.name == "lvl2-3":
                    self.level = 3
                    self.tmx_data = pytmx.util_pygame.load_pygame("assets/maps/level3.tmx")
                    self.load_level(self.tmx_data)

        saved_hostage = pygame.sprite.spritecollide(self.player, self.hostages, False)
        if saved_hostage:
            for hostage in saved_hostage:
                if hostage.active:
                    hostage.active = False
                    self.hostages_left -= 1

        defused_bomb = pygame.sprite.spritecollide(self.player, self.bombs, False)
        if defused_bomb:
            for bomb in defused_bomb:
                if bomb.active:
                    bomb.active = False
                    self.bombs_left -= 1

        delta = self.clock.tick() / 1000

        self.display_surface.fill('white')
        self.draw_map(self.display_surface)

        if self.passive_enemies:
            for x in self.passive_enemies:
                x.draw_self(self.display_surface, self.offset)

        if self.active_enemies:
            for x in self.active_enemies:
                x.update(self.player, delta, self.walls)
                x.draw_self(self.display_surface, self.offset)

        for x in self.hostages:
            x.draw_self(self.display_surface, self.offset)
            x.update(self.player)

        for x in self.bombs:
            x.draw_self(self.display_surface, self.offset)

        if self.hostages_left == 0 and self.bombs_left == 0 and self.level == 3:
            self.won = True
            self.game_overed = True

        if self.counter <= 0:
            self.player.kill()
            self.explosion = True

        self.player.update(delta, self.display_surface, self.offset, self.walls)
        self.render_hud()

        if self.explosion:
            # Leave it where it is!!!!
            # Why? - Mark
            # Or else player will render on top of explosion. Right now explosion renders on top of him.
            self.explosion_size += 2000 * delta
            scaled_explosion = pygame.transform.scale(self.explosion_sprite,(int(self.explosion_size), int(self.explosion_size)))
            draw_pos = ((WINDOW_WIDTH // 2) - (self.explosion_size // 2), (WINDOW_HEIGHT // 2) - (self.explosion_size // 2))
            self.display_surface.blit(scaled_explosion, draw_pos)
            if self.explosion_size > 2000:
                self.game_overed = True
        

    def run(self):
        while not self.stopped:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    if self.counter > 0:
                        self.counter -= 1
                if event.type == pygame.QUIT:
                    self.stopped = True
            if self.game_overed:
                self.game_over_menu()
            else:
                self.game_run()
            display.flip()
            display.update()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
