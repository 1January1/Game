import pygame
from pygame import draw, display, Vector2, Rect

import player
from player import Player
from pygame.time import Clock
from enemy import Enemy

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.player = Player()
        self.clock = Clock()
        self.pause = False
        self.offset = Vector2()
        self.enemy = Enemy()

    def run(self):
        while not self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.pause = True

            delta = self.clock.tick() / 1000
            self.player.update(delta)
            self.enemy.update(self.player, delta)
                
            self.display_surface.fill('white')
            self.player.draw_self(self.display_surface)
            self.enemy.draw_self(self.display_surface)

            display.flip()
            display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()