import pygame
class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        self.sounds['moneda'] = pygame.mixer.Sound('assets/sounds/Moneda.wav')
        self.sounds['muerte'] = pygame.mixer.Sound('assets/sounds/Muerte.wav')
    
    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()