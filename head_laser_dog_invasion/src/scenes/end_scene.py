import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BG, COLOR_GREEN, COLOR_WHITE, COLOR_PINK
from src.ui.text import draw_text
from src.ui.button import Button
from src.utils.sound import play_sound

class EndScene:
    def __init__(self, game):
        self.game = game
        self.btn_menu = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100, 200, 50, "MENÚ PRINCIPAL", self.to_menu)

    def on_enter(self):
        self.win = self.game.shared_data.get("win", False)

    def to_menu(self):
        play_sound("click")
        self.game.change_scene("menu")

    def handle_event(self, event):
        self.btn_menu.handle_event(event)

    def update(self, dt):
        pass

    def draw_sad_face(self, surface):
        cx, cy = SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50
        # Rostro
        pygame.draw.circle(surface, COLOR_WHITE, (cx, cy), 80, 4)
        
        # Ojo izquierdo en X
        pygame.draw.line(surface, COLOR_GREEN, (cx - 40, cy - 30), (cx - 20, cy - 10), 4)
        pygame.draw.line(surface, COLOR_GREEN, (cx - 20, cy - 30), (cx - 40, cy - 10), 4)
        
        # Ojo derecho en X
        pygame.draw.line(surface, COLOR_GREEN, (cx + 20, cy - 30), (cx + 40, cy - 10), 4)
        pygame.draw.line(surface, COLOR_GREEN, (cx + 40, cy - 30), (cx + 20, cy - 10), 4)
        
        # Boca (línea recta o curva triste)
        pygame.draw.line(surface, COLOR_GREEN, (cx - 30, cy + 30), (cx + 30, cy + 30), 4)
        
        # Lengua afuera (elipse rosa)
        pygame.draw.ellipse(surface, COLOR_PINK, (cx + 10, cy + 30, 20, 30))

    def draw(self, screen):
        screen.fill(COLOR_BG)
        
        if self.win:
            draw_text(screen, "¡VICTORIA!", 60, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)
        else:
            self.draw_sad_face(screen)
            draw_text(screen, "GAME OVER", 50, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70)
            
        self.btn_menu.draw(screen)