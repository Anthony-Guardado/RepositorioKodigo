import pygame
from src.utils.assets import get_font
from src.config import COLOR_GREEN, COLOR_BG, COLOR_WHITE

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x - width//2, y - height//2, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                self.action()

    def draw(self, surface):
        color = COLOR_WHITE if self.is_hovered else COLOR_GREEN
        pygame.draw.rect(surface, color, self.rect, 2)
        font = get_font(24)
        text_surf = font.render(self.text, True, color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)