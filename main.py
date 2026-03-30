import pygame
from pygame import draw, display, Vector2, Rect
from player import Player

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.player = Player()
        self.pause = False
        self.offset = Vector2()
    

    def run(self):
        while not self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.pause = True
            
            center = self.player.rect.center
            self.offset.x = -(center[0] - WINDOW_WIDTH / 2)
            self.offset.y = -(center[1] - WINDOW_HEIGHT / 2)

            rect = self.player.rect

                
            self.display_surface.fill('white')
            draw.rect(self.display_surface, (255, 0, 0), rect=Rect(-80 + self.offset.x, -80 + self.offset.y, 160, 160))
            draw.rect(self.display_surface, (0, 255, 0), rect=Rect(rect.left + self.offset.x, rect.top + self.offset.y,
                                                                   rect.width, rect.height))
            display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()