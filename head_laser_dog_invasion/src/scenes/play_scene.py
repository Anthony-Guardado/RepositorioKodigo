import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BG, COLOR_GREEN
from src.entities.player import Player
from src.entities.dog import Dog
from src.ui.text import draw_text
from src.utils.sound import play_sound

class PlayScene:
    def __init__(self, game):
        self.game = game
        self.reset_level()

    def on_enter(self):
        self.lives = self.game.shared_data.get("lives", 3)
        self.level = 1
        self.reset_level()

    def reset_level(self):
        self.player = Player()
        self.lasers = []
        self.bones = []
        self.dogs = []
        
        # Formación de 8 perros
        start_x = SCREEN_WIDTH // 2 - (4 * 60)
        for i in range(8):
            self.dogs.append(Dog(start_x + i * 60, 50))
            
        self.dog_speed_x = 2 + getattr(self, 'level', 1) * 0.5
        self.dog_dir = 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                # Solo un láser visible a la vez
                if len(self.lasers) == 0:
                    laser = self.player.shoot()
                    if laser:
                        self.lasers.append(laser)

    def update(self, dt):
        self.player.update(dt)
        
        # Actualizar láseres
        for laser in self.lasers[:]:
            laser.update(dt)
            if laser.rect.bottom < 0:
                self.lasers.remove(laser)
                
        # Actualizar huesos
        for bone in self.bones[:]:
            bone.update(dt)
            if bone.rect.top > SCREEN_HEIGHT:
                self.bones.remove(bone)
                
        # Actualizar perros (Space Invaders style)
        move_down = False
        for dog in self.dogs:
            dog.rect.x += self.dog_speed_x * self.dog_dir
            if dog.rect.right > SCREEN_WIDTH or dog.rect.left < 0:
                move_down = True
                
        if move_down:
            self.dog_dir *= -1
            for dog in self.dogs:
                dog.rect.x += self.dog_speed_x * self.dog_dir
                dog.rect.y += 20
                
        # Disparo de perros
        for dog in self.dogs:
            dog.shoot_chance = 0.002 + (self.level * 0.001)
            bone = dog.shoot()
            if bone:
                self.bones.append(bone)

        self.check_collisions()
        self.check_win_loss()

    def check_collisions(self):
        player_rect = self.player.get_rect()

        # Laser vs Dog
        for laser in self.lasers[:]:
            for dog in self.dogs[:]:
                if laser.rect.colliderect(dog.rect):
                    play_sound("dog_hit")
                    self.lasers.remove(laser)
                    self.dogs.remove(dog)
                    break
                    
        # Bone vs Player
        for bone in self.bones[:]:
            if bone.rect.colliderect(player_rect):
                play_sound("player_hit")
                self.bones.remove(bone)
                self.lives -= 1

        # NUEVO: Dog vs Player o Perro llega al límite inferior de la pantalla
        for dog in self.dogs:
            if dog.rect.colliderect(player_rect) or dog.rect.bottom >= SCREEN_HEIGHT:
                play_sound("player_hit")
                self.lives = 0  # Invasión exitosa, Game Over instantáneo
                break

    def check_win_loss(self):
        if self.lives <= 0:
            self.game.shared_data["win"] = False
            self.game.change_scene("end")
        elif len(self.dogs) == 0:
            self.level += 1
            self.reset_level()

    def draw(self, screen):
        screen.fill(COLOR_BG)
        
        # Grid tenue opcional
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(screen, (0, 30, 0), (0, y), (SCREEN_WIDTH, y))
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(screen, (0, 30, 0), (x, 0), (x, SCREEN_HEIGHT))

        self.player.draw(screen)
        for dog in self.dogs:
            dog.draw(screen)
        for laser in self.lasers:
            laser.draw(screen)
        for bone in self.bones:
            bone.draw(screen)
            
        # HUD
        draw_text(screen, f"NIVEL: {self.level}", 20, 10, 10, center=False)
        draw_text(screen, f"VIDAS: {self.lives}", 20, SCREEN_WIDTH - 150, 10, center=False)