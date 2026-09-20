from src.scenes.intro_scene import IntroScene
from src.scenes.menu_scene import MenuScene
from src.scenes.difficulty_scene import DifficultyScene
from src.scenes.play_scene import PlayScene
from src.scenes.end_scene import EndScene

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.shared_data = {}  # Para pasar datos entre escenas (ej. vidas, victoria)
        self.scenes = {
            "intro": IntroScene(self),
            "menu": MenuScene(self),
            "difficulty": DifficultyScene(self),
            "play": PlayScene(self),
            "end": EndScene(self)
        }
        self.current_scene = self.scenes["intro"]
        
    def change_scene(self, scene_name):
        self.current_scene = self.scenes[scene_name]
        self.current_scene.on_enter()
        
    def handle_event(self, event):
        self.current_scene.handle_event(event)
        
    def update(self, dt):
        self.current_scene.update(dt)
        
    def draw(self, screen):
        self.current_scene.draw(screen)