import pygame
from pygame.sprite import Sprite



class Goku(Sprite):

    def __init__(self, ai_settings, screen, stats):
        """Initialize the goku, and set its starting position."""
        super(Goku, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.stats = stats
        
        self.imageI = pygame.image.load('goku.png').convert_alpha() 
        self.imageII = pygame.image.load('ssjgoku.png')
        self.imageIII = pygame.image.load('ssjbgoku.png')
        
        # Load the goku image, and get its rect.
        if stats.level <= 5:
            self.image = pygame.image.load('goku.png').convert_alpha()
        elif stats.level > 5 and stats.level <=10:
            self.image = pygame.image.load('ssjgoku.png')
        elif stats.level > 10:
            self.image = pygame.image.load('ssjbgoku.png')
       
        self.screen_rect = screen.get_rect()
        
        self.rect = self.image.get_rect()
        
        

        # Start each new goku at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Store a decimal value for the goku's center.
        self.center = float(self.rect.centerx)
        
        # Movement flags.
        self.moving_right = False
        self.moving_left = False
        
    def center_goku(self):
        """Center the goku on the screen."""
        self.center = self.screen_rect.centerx
        
    def update(self):
        """Update the goku's position, based on movement flags."""
        # Update the goku's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.goku_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.goku_speed_factor
                    
        # Update rect object from self.center.
        self.rect.centerx = self.center
        

    def blitme(self, stats):
        """Draw the goku at its current location."""
        if stats.level <= 5:
            self.screen.blit(self.imageI, self.rect)
        elif stats.level > 5 and stats.level <=10:
            self.screen.blit(self.imageII, self.rect)
        elif stats.level > 10:    
            self.screen.blit(self.imageIII, self.rect)
        
