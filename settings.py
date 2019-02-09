import pygame

class Settings():
    """A class to store all settings for Frieza Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_image = pygame.image.load('namec.bmp')
        
        # Goku settings.
        self.goku_limit = 3
            
        # kame settings.
        self.kame_width = 3
        self.kame_height = 15
        self.kame_color = 60, 60, 60
        self.kames_allowed = 3
        
        # Frieza settings.
        self.fleet_drop_speed = 10
            
        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quickly the frieza point values increase.
        self.score_scale = 1.5
    
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.goku_speed_factor = 5
        self.kame_speed_factor = 6
        self.frieza_speed_factor = 5
        
        # Scoring.
        self.frieza_points = 50
    
        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1
        
    def increase_speed(self):
        """Increase speed settings and frieza point values."""
        self.goku_speed_factor *= self.speedup_scale
        self.kame_speed_factor *= self.speedup_scale
        self.frieza_speed_factor *= self.speedup_scale
        
        self.frieza_points = int(self.frieza_points * self.score_scale)
