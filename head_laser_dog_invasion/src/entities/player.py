import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_GREEN
from src.entities.laser import Laser
from src.utils.sound import play_sound

class Player:
    def __init__(self):
        self.radius = 20
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 40
        self.speed = 5
        self.cooldown = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        
        if self.cooldown > 0:
            self.cooldown -= dt

    def shoot(self):
        if self.cooldown <= 0:
            self.cooldown = 250  # 250 ms cooldown
            play_sound("laser")
            return Laser(self.x, self.y - self.radius, -8)
        return None

    def draw(self, surface):
        x = int(self.x)
        y = int(self.y)

        # NUEVO: Pelo de Goku Super Saiyan
        COLOR_GOLD = (255, 215, 0) # Amarillo Dorado para el pelo
        
        # Coordenadas para los picos del cabello (de izquierda a derecha)
        puntos_pelo = [
            (x - self.radius, y - 5),   # Base izquierda
            (x - 25, y - 30),           # Pico izquierdo bajo
            (x - 12, y - 20),           # Valle
            (x - 18, y - 45),           # Pico izquierdo alto
            (x, y - 25),                # Valle central
            (x + 5, y - 55),            # Pico central (el más alto)
            (x + 15, y - 20),           # Valle derecho
            (x + 25, y - 35),           # Pico derecho alto
            (x + self.radius, y - 5)    # Base derecha
        ]
        
        # Dibujar el relleno dorado del pelo
        pygame.draw.polygon(surface, COLOR_GOLD, puntos_pelo)
        # Dibujar el contorno verde para que encaje con el estilo retro
        pygame.draw.polygon(surface, COLOR_GREEN, puntos_pelo, 2)

        # Cabeza (Círculo blanco)
        pygame.draw.circle(surface, COLOR_WHITE, (x, y), self.radius)
        
        # Ojos/detalles verdes
        pygame.draw.circle(surface, COLOR_GREEN, (x - 7, y - 5), 4)
        pygame.draw.circle(surface, COLOR_GREEN, (x + 7, y - 5), 4)

    def get_rect(self):
        # El área de impacto (hitbox) ahora la hacemos un poquito más alta por el pelo
        return pygame.Rect(self.x - self.radius, self.y - self.radius - 20, self.radius*2, self.radius*2 + 20)