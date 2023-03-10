import pygame.sprite


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/doodle_r.png')
        self.rect = self.image.get_rect()

        self.gunshoot_sound = pygame.mixer.Sound('sounds/lasser.wav')

    def shoot(self):
        self.gunshoot_sound.play()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
