import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BG
from src.ui.text import draw_text
from src.ui.button import Button
from src.utils.sound import play_sound

class DifficultyScene:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button(SCREEN_WIDTH//2, 200, 200, 50, "FÁCIL", lambda: self.select(5)),
            Button(SCREEN_WIDTH//2, 280, 200, 50, "MEDIO", lambda: self.select(3)),
            Button(SCREEN_WIDTH//2, 360, 200, 50, "DIFÍCIL", lambda: self.select(1))
        ]

    def on_enter(self):
        pass

    def select(self, lives):
        play_sound("click")
        self.game.shared_data["lives"] = lives
        self.game.change_scene("play")

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(COLOR_BG)
        draw_text(screen, "SELECCIONA DIFICULTAD", 40, SCREEN_WIDTH//2, 100)
        for btn in self.buttons:
            btn.draw(screen)