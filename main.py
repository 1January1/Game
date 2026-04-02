import pygame
from pygame import display, Vector2, sprite, font
from player import Player
from pygame.time import Clock
from enemy_spawner import Spawner

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.player = Player()
        self.clock = Clock()
        self.pause = False
        self.offset = Vector2()
        self.enemies = pygame.sprite.Group()
        self.spawner = Spawner()
        self.spawn_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_event, 2000)
        self.score = 0
        self.font = font.SysFont("comicsans", 30)

    def run(self):
        while not self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.pause = True
                if event.type == self.spawn_event:
                    self.enemies.add(self.spawner.spawn_enemy(WINDOW_WIDTH, WINDOW_HEIGHT))

            hits = pygame.sprite.groupcollide(self.enemies, self.player.bullets, True, True)
            for hit in hits:
                self.score += 10

            hit_player = sprite.spritecollide(self.player, self.enemies, False)
            if hit_player:
                self.pause = True

            delta = self.clock.tick() / 1000

            self.display_surface.fill('white')

            if self.enemies:
                for x in self.enemies:
                    x.update(self.player, delta)
                    x.draw_self(self.display_surface)

            text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))

            self.player.update(delta, self.display_surface)
            self.display_surface.blit(text, (0, 0))
            display.flip()
            display.update()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
