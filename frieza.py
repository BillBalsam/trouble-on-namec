import pygame
from pygame.sprite import Sprite




class Frieza(Sprite):
    """A class to represent a single frieza in the fleet."""

    def __init__(self, ai_settings, screen, stats):
        """Initialize the frieza, and set its starting position."""
        super(Frieza, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.stats = stats

        # Load the frieza image, and set its rect attribute.
        if stats.level <= 5:
            self.image = pygame.image.load('friezap1.png')
        elif stats.level > 5 and stats.level <=10:
            self.image = pygame.image.load('frieza.bmp')
        elif stats.level > 10:
            self.image = pygame.image.load('golden_frieza.png')
       
        
        self.rect = self.image.get_rect()
            # Start each new frieza near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

            # Store the frieza's exact position.
        self.x = float(self.rect.x)
       

        
        
    def check_edges(self):
        """Return True if frieza is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        """Move the frieza right or left."""
        self.x += (self.ai_settings.frieza_speed_factor *
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self, stats):
        """Draw the frieza at its current location."""

        self.screen.blit(self.image, self.rect)
