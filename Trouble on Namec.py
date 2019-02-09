import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from goku import Goku
import game_functions as gf

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Frieza Invasion")
    
    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")
    
    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # Set the background color.
    bg_color = (230, 230, 230)
    
    
    # Make a goku, a group of kames, and a group of friezas.
    goku = Goku(ai_settings, screen, stats)
    kames = Group()
    friezas = Group()
    
    # Create the fleet of friezas.
    gf.create_fleet(ai_settings, screen, goku, friezas, stats)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, goku,
            friezas, kames)
        
        if stats.game_active:
            
            goku.update()
            gf.update_kames(ai_settings, screen, stats, sb, goku, friezas,
                kames)
            gf.update_friezas(ai_settings, screen, stats, sb, goku, friezas,
                kames)
        
        gf.update_screen(ai_settings, screen, stats, sb, goku, friezas,
            kames, play_button)

run_game()
