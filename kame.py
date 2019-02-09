import pygame
from pygame.sprite import Sprite

class Kame(Sprite):
    """A class to manage kames fired from the goku."""

    def __init__(self, ai_settings, screen, goku):
        """Create a kame object, at the goku's current position."""
        super(Kame, self).__init__()
        self.screen = screen

        # Create kame rect at (0, 0), then set correct position.
        self.image = pygame.image.load('kame.bmp')
        self.rect = self.image.get_rect()
        self.rect.centerx = goku.rect.centerx
        self.rect.top = goku.rect.top
        
        # Store a decimal value for the kame's position.
        self.y = float(self.rect.y)

        self.color = ai_settings.kame_color
        self.speed_factor = ai_settings.kame_speed_factor

    def update(self):
        """Move the kame up the screen."""
        # Update the decimal position of the kame.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_kame(self):
        """Draw the kame to the screen."""
        #pygame.draw.rect(self.screen, self.color, self.rect, self.image)
        self.screen.blit(self.image, self.rect)
