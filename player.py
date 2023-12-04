import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # walking animation images
        player_walk1 = pygame.image.load('graphics/walk_1.png').convert_alpha()
        player_walk1 = pygame.transform.rotozoom(player_walk1, 0, 0.75)
        player_walk2 = pygame.image.load('graphics/walk_2.png').convert_alpha()
        player_walk2 = pygame.transform.rotozoom(player_walk2, 0, 0.75)
        player_stand = pygame.image.load('graphics/stand.png').convert_alpha()
        player_stand = pygame.transform.rotozoom(player_stand, 0, 0.75)

        self.image = pygame.image.load('graphics/walk_1.png').convert_alpha()
        self.rect = self.image.get_rect(midleft = (90, 200))
        self.player_walk = [player_walk1, player_stand, player_walk2, player_stand]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        
    def player_input(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_UP]:
            self.rect.y -= 3
        if keys[pygame.K_DOWN]:
            self.rect.y += 3
    
    def apply_bounds(self):
        if self.rect.bottom >= 310: self.rect.bottom = 310
        if self.rect.top <= 110: self.rect.top = 110

    def animation_state(self):
        # play walking animation if player is moving
        self.player_index += 0.1
        if (self.player_index >= len(self.player_walk)): self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_bounds()
        self.animation_state()