import pygame
from pygame import display, Vector2, sprite, font
from player import Player
from pygame.time import Clock
from enemy_spawner import Spawner
import pytmx
from enemy import Enemy

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tmx_data = pytmx.util_pygame.load_pygame("assets/maps/test.tmx")
        self.clock = Clock()
        self.pause = False
        self.offset = Vector2()
        self.enemies = pygame.sprite.Group()
        self.spawner = Spawner()
        self.score = 0
        self.font = font.SysFont("comicsans", 30)


    def start(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for object in layer:
                    print(object)
                    print(object.x, object.y)
                    if object.name == "Player spawn":
                        self.player = Player(object.x, object.y)
                    if object.name == "Enemy spawn":
                        self.enemies.add(Enemy(object.x, object.y))


    def draw_map(self, surface, tmx_data):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        # Subtract offset from pixel position
                        pixel_x = (x * tmx_data.tilewidth) - self.offset.x
                        pixel_y = (y * tmx_data.tileheight) - self.offset.y
                        surface.blit(tile, (pixel_x, pixel_y))


    def run(self):
        self.start()
        while not self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.pause = True

            self.offset.x = self.player.rect.centerx - WINDOW_WIDTH // 2
            self.offset.y = self.player.rect.centery - WINDOW_HEIGHT // 2

            hits = pygame.sprite.groupcollide(self.enemies, self.player.bullets, True, True)
            for hit in hits:
                self.score += 10

            hit_player = sprite.spritecollide(self.player, self.enemies, False)
            if hit_player:
                self.pause = True

            delta = self.clock.tick() / 1000

            self.display_surface.fill('white')
            self.draw_map(self.display_surface, self.tmx_data)

            if self.enemies:
                for x in self.enemies:
                    x.update(self.player, delta)
                    x.draw_self(self.display_surface, self.offset)

            text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))

            self.player.update(delta, self.display_surface, self.offset)
            self.display_surface.blit(text, (0, 0))
            display.flip()
            display.update()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
