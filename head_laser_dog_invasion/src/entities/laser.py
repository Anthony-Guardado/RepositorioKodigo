import pygame
from src.config import COLOR_GREEN

class Laser:
    def __init__(self, x, y, speed):
        self.width = 6
        self.height = 20
        self.rect = pygame.Rect(x - self.width//2, y, self.width, self.height)
        self.speed = speed

    def update(self, dt):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_GREEN, self.rect)