import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BG
from src.ui.text import draw_text
from src.ui.button import Button
from src.utils.sound import play_sound

class MenuScene:
    def __init__(self, game):
        self.game = game
        self.btn_play = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50, 200, 50, "PLAY", self.play_clicked)

    def on_enter(self):
        pass

    def play_clicked(self):
        play_sound("click")
        self.game.change_scene("difficulty")

    def handle_event(self, event):
        self.btn_play.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(COLOR_BG)
        draw_text(screen, "HEAD LASER", 50, SCREEN_WIDTH//2, 100)
        draw_text(screen, "DOG INVASION", 40, SCREEN_WIDTH//2, 150)
        self.btn_play.draw(screen)