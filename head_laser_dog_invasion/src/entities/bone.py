import pygame
from src.config import COLOR_WHITE

class Bone:
    def __init__(self, x, y, speed):
        self.width = 8
        self.height = 16
        self.rect = pygame.Rect(x - self.width//2, y, self.width, self.height)
        self.speed = speed

    def update(self, dt):
        self.rect.y += self.speed

    def draw(self, surface):
        # Dibujo de un hueso simple con primitivas
        pygame.draw.rect(surface, COLOR_WHITE, (self.rect.x + 2, self.rect.y, 4, self.height))
        pygame.draw.circle(surface, COLOR_WHITE, (self.rect.x + 2, self.rect.y), 3)
        pygame.draw.circle(surface, COLOR_WHITE, (self.rect.right - 2, self.rect.y), 3)
        pygame.draw.circle(surface, COLOR_WHITE, (self.rect.x + 2, self.rect.bottom), 3)
        pygame.draw.circle(surface, COLOR_WHITE, (self.rect.right - 2, self.rect.bottom), 3)