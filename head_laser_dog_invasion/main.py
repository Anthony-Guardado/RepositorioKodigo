import asyncio
import pygame
from src.game import Game
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

async def main():
    # Inicialización de Pygame y el Mixer
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    
    # MODIFICADO: Agregamos pygame.SCALED para escalar la resolución nativa al monitor
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
    pygame.display.set_caption("HEAD LASER: DOG INVASION")
    
    clock = pygame.time.Clock()
    game = Game(screen)
    
    # Bucle principal compatible con pygbag
    running = True
    while running:
        dt = clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # NUEVO: Alternar pantalla completa al presionar F11
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
                
            game.handle_event(event)
            
        game.update(dt)
        game.draw(screen)
        pygame.display.flip()
        
        # OBLIGATORIO para pygbag (libera el control al navegador)
        await asyncio.sleep(0)
        
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())