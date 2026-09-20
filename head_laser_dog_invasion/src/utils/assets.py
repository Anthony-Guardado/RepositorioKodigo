import pygame
from src.config import FONT_NAME

_fonts = {}

def get_font(size, bold=True):
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = pygame.font.SysFont(FONT_NAME, size, bold=bold)
    return _fonts[key]