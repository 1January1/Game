import pygame
from pygame import draw, display, Vector2, Rect


from player import Player
from pygame.time import Clock
from enemy import Enemy
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
        self.enemies = []
        self.spawner = Spawner()
        self.spawn_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_event, 2000)

    def run(self):
        while not self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.pause = True
                if event.type == self.spawn_event:
                    self.enemies.append(self.spawner.spawn_enemy(WINDOW_WIDTH, WINDOW_HEIGHT))

            delta = self.clock.tick() / 1000

            self.display_surface.fill('white')

            if self.enemies:
                for x in self.enemies:
                    x.update(self.player, delta)
                    x.draw_self(self.display_surface)

            self.player.update(delta)
            self.player.draw_self(self.display_surface)

            display.flip()
            display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()