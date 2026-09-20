import sys
import pygame

# Intentamos importar numpy, pero si falla no rompemos el juego
try:
    import numpy as np
except ImportError:
    np = None

_sounds = {}

# Detectamos si estamos en el navegador
is_web = sys.platform == "emscripten"

def generate_square_wave(freq, duration, volume=0.1, wave_type='square'):
    """Genera un sonido sintetizado usando numpy y pygame.sndarray. 
    En web devuelve None para no crashear el navegador."""
    
    # Si estamos en web o numpy no cargó, cancelamos la generación
    if is_web or np is None or not pygame.mixer.get_init():
        return None
        
    sample_rate, format_id, channels = pygame.mixer.get_init()
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    
    if wave_type == 'square':
        wave = np.sign(np.sin(freq * t * 2 * np.pi))
    elif wave_type == 'descend':
        freqs = np.linspace(freq, freq/4, n_samples)
        wave = np.sign(np.sin(freqs * t * 2 * np.pi))
    elif wave_type == 'noise':
        wave = np.random.uniform(-1, 1, n_samples)
    else:
        wave = np.sin(freq * t * 2 * np.pi)
        
    wave = wave * volume
    sound_array = np.int16(wave * 32767)
    
    if channels == 2:
        sound_array = np.column_stack((sound_array, sound_array))
        
    try:
        return pygame.sndarray.make_sound(sound_array)
    except Exception as e:
        print(f"Error generando sonido: {e}")
        return None

def get_sound(name):
    """Devuelve o genera un sonido cacheado."""
    if name in _sounds:
        return _sounds[name]
        
    snd = None
    
    # Solo generamos los sonidos si NO estamos en la web
    if not is_web:
        if name == "laser":
            snd = generate_square_wave(880, 0.1, 0.1, 'square')
        elif name == "dog_hit":
            snd = generate_square_wave(440, 0.3, 0.1, 'descend')
        elif name == "bone":
            snd = generate_square_wave(220, 0.1, 0.1, 'square')
        elif name == "player_hit":
            snd = generate_square_wave(110, 0.4, 0.2, 'noise')
        elif name == "click":
            snd = generate_square_wave(1200, 0.05, 0.1, 'square')
        
    _sounds[name] = snd
    return snd

def play_sound(name):
    snd = get_sound(name)
    if snd:
        snd.play()