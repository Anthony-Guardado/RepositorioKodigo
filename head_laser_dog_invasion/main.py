import sys
import asyncio
import traceback
import pygame
from src.game import Game
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

async def main():
    try:
        # Inicialización de Pygame
        pygame.init()
        
        # En web no forzamos la frecuencia de audio, dejamos que el navegador decida
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Detectamos si estamos corriendo en el navegador (emscripten) o en escritorio
        is_web = sys.platform == "emscripten"
        
        # En web NO usamos pygame.SCALED porque Pygbag maneja su propio canvas
        flags = pygame.SCALED if not is_web else 0
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        
        pygame.display.set_caption("HEAD LASER: DOG INVASION")
        
        clock = pygame.time.Clock()
        game = Game(screen)
        
        running = True
        while running:
            dt = clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # La tecla F11 solo la permitimos en Escritorio
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    if not is_web:
                        pygame.display.toggle_fullscreen()
                        
            game.handle_event(event)
            game.update(dt)
            game.draw(screen)
            pygame.display.flip()
            
            await asyncio.sleep(0)
            
        pygame.quit()
        
    except Exception as e:
        # SI ALGO FALLA, LO PINTAMOS EN LA PANTALLA EN LUGAR DE QUEDAR EN BLANCO
        if 'screen' not in locals():
            screen = pygame.display.set_mode((640, 480))
        font = pygame.font.SysFont("couriernew", 14)
        error_text = traceback.format_exc().split('\n')
        
        while True:
            screen.fill((0, 0, 0))
            y = 20
            for line in error_text:
                # Dibujamos el texto del error en color rojo
                surf = font.render(line, True, (255, 50, 50))
                screen.blit(surf, (10, y))
                y += 20
            pygame.display.flip()
            await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())