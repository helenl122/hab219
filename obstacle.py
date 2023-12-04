import pygame
from random import randint, choice

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/skull.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(randint(800,1100), 110 + randint(0,25)*5))
        velocs = [0,0,0,1,-1, 0, 0]
        self.velocity = choice(velocs)

    def apply_velocity(self):
        if self.rect.y <= 116  or self.rect.y >= 270: self.velocity = -self.velocity
        self.rect.y -= self.velocity
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.rect.x -= 3
        self.apply_velocity()
        self.destroy()