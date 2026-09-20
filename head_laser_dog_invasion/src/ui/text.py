import pygame
from src.utils.assets import get_font
from src.config import COLOR_GREEN

def draw_text(surface, text, size, x, y, color=COLOR_GREEN, center=True):
    font = get_font(size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(text_surface, rect)