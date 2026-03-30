from pygame.rect import Rect
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.rect = Rect(0, 0, 80, 80)
        self.rect.center = (0, 0)