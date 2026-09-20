import pygame
from src.config import COLOR_GREEN, COLOR_WHITE
from src.entities.bone import Bone
from src.utils.sound import play_sound
import random

class Dog:
    def __init__(self, x, y):
        self.width = 40
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.shoot_chance = 0.002

    def update(self, dt):
        pass

    def shoot(self):
        if random.random() < self.shoot_chance:
            play_sound("bone")
            return Bone(self.rect.centerx, self.rect.bottom, 4)
        return None

    def draw(self, surface):
        # Cabeza
        pygame.draw.rect(surface, COLOR_GREEN, self.rect, 2)
        # Orejas
        pygame.draw.rect(surface, COLOR_WHITE, (self.rect.x, self.rect.y - 10, 10, 10))
        pygame.draw.rect(surface, COLOR_WHITE, (self.rect.right - 10, self.rect.y - 10, 10, 10))
        # Hocico
        pygame.draw.rect(surface, COLOR_WHITE, (self.rect.centerx - 10, self.rect.bottom - 10, 20, 10))