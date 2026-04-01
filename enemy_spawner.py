import pygame
import random
from enemy import Enemy


class Spawner():
    def __init__(self):
        self.sides = ['top', 'bottom', 'left', 'right']
        self.buffer = 50

    def get_coordinates(self, width, height):
        side = random.choice(self.sides)
        if side == 'top':
            x = random.randint(0, width)
            y = -self.buffer
        elif side == 'bottom':
            x = random.randint(0, width)
            y = height + self.buffer
        elif side == 'left':
            x = -self.buffer
            y = random.randint(0, height)
        elif side == 'right':
            x = width + self.buffer
            y = random.randint(0, height)
        return x, y

    def spawn_enemy(self, width, height):
        coordinates = self.get_coordinates(width, height)
        return Enemy(coordinates[0], coordinates[1])