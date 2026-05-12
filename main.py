import pygame
from pygame import display, Vector2, font, rect
from player import Player
from pygame.time import Clock
from enemy_spawner import Spawner
import pytmx
from enemy import Enemy
from fucking_wall import Wall
from trigger import Trigger

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tmx_data = pytmx.util_pygame.load_pygame("assets/maps/level1.tmx")
        self.clock = Clock()
        self.pause = False
        self.offset = Vector2()
        self.active_enemies = pygame.sprite.Group()
        self.passive_enemies = pygame.sprite.Group()
        self.spawner = Spawner()
        self.font = font.SysFont("comicsans", 30)
        self.walls = pygame.sprite.Group()
        self.triggers = pygame.sprite.Group()

    def draw_map(self, surface):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        pixel_x = (x * self.tmx_data.tilewidth) - self.offset.x
                        pixel_y = (y * self.tmx_data.tileheight) - self.offset.y
                        surface.blit(tile, (pixel_x, pixel_y))

    def wall_spawn(self):
        wall_layer = self.tmx_data.get_layer_by_name("walls")
        for x, y, gid in wall_layer:
            if gid != 0:
                pixel_x = x * self.tmx_data.tilewidth
                pixel_y = y * self.tmx_data.tileheight
                self.walls.add(Wall(pixel_x, pixel_y))

    def trigger_spawn(self):
        trigger_layer = self.tmx_data.get_layer_by_name("room triggers")
        for trigger in trigger_layer:
            self.triggers.add(Trigger(trigger.x, trigger.y, trigger.width, trigger.height, trigger.name))

    def start(self):
        spawn_layer = self.tmx_data.get_layer_by_name("spawn points")
        for object in spawn_layer:
            if object.name == "Player spawn":
                self.player = Player(object.x, object.y)
            if object.name == "Enemy spawn":
                self.passive_enemies.add(Enemy(object.x, object.y, object.properties["Room"]))

    def run(self):
        pygame.display.set_caption('Tallinn Miami')
        self.start()
        self.wall_spawn()
        self.trigger_spawn()
        while not self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.pause = True

            self.offset.x = self.player.rect.centerx - WINDOW_WIDTH // 2
            self.offset.y = self.player.rect.centery - WINDOW_HEIGHT // 2

            triggered_room = pygame.sprite.spritecollide(self.player, self.triggers, False)
            if triggered_room:
                for enemy in self.passive_enemies:
                    if enemy.room == triggered_room[0].name:
                        self.passive_enemies.remove(enemy)
                        self.active_enemies.add(enemy)
                        triggered_room[0].kill()

            for bullet in self.player.bullets:
                collided = pygame.sprite.spritecollide(bullet, self.active_enemies, False)
                if collided:
                    for sprite in collided:
                        sprite.hit()
                    bullet.kill()

            hit_player = pygame.sprite.spritecollide(self.player, self.active_enemies, False)
            if hit_player:
                self.pause = True

            if not self.passive_enemies and not self.active_enemies:
                self.pause = True

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

            self.player.update(delta, self.display_surface, self.offset, self.walls)
            self.display_surface.blit(text, (0, 0))
            display.flip()
            display.update()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
