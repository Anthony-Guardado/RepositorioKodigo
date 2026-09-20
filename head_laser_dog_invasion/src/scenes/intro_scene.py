import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BG, COLOR_GREEN
from src.ui.text import draw_text
from src.utils.assets import get_font

class IntroScene:
    def __init__(self, game):
        self.game = game
        self.timer = 0
        self.scale = 0.1
        self.done_animating = False

    def on_enter(self):
        self.timer = 0
        self.scale = 0.1
        self.done_animating = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if self.done_animating:
                self.game.change_scene("menu")

    def update(self, dt):
        self.timer += dt
        if self.scale < 1.0:
            self.scale += 0.01
        else:
            self.done_animating = True

    def draw(self, screen):
        screen.fill(COLOR_BG)
        
        # Tamaño de fuente dinámico basado en la escala (le subí a 45 para que se vea mejor)
        current_size = max(1, int(45 * self.scale))
        font = get_font(current_size)
        
        # Separar el texto en dos líneas
        text_line1 = font.render("DESARROLLADO POR", True, COLOR_GREEN)
        text_line2 = font.render("ANTHONY GUARDADO", True, COLOR_GREEN)
        
        # Calcular el centro de la pantalla y el espaciado
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        spacing = current_size // 2 + 5
        
        # Posicionar la primera línea un poco más arriba y la segunda un poco más abajo
        rect1 = text_line1.get_rect(center=(center_x, center_y - spacing))
        rect2 = text_line2.get_rect(center=(center_x, center_y + spacing))
        
        # Dibujar en pantalla
        screen.blit(text_line1, rect1)
        screen.blit(text_line2, rect2)

        # Mostrar el mensaje de continuar solo cuando termine la animación
        if self.done_animating:
            draw_text(screen, "Presiona cualquier tecla para continuar", 20, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)