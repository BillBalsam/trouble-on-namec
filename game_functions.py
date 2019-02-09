import sys
from time import sleep

import pygame

from kame import Kame
from frieza import Frieza
import odbc


db = odbc.odbc('adventureworks2012/billb/billb90')
cursor = db.cursor()



def check_keydown_events(event, ai_settings, screen, goku, kames):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        goku.moving_right = True
    elif event.key == pygame.K_LEFT:
        goku.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_kame(ai_settings, screen, goku, kames)
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event, goku):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        goku.moving_right = False
    elif event.key == pygame.K_LEFT:
        goku.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, goku, friezas,
        kames):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, goku, kames)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, goku)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                goku, friezas, kames, mouse_x, mouse_y)
            
def check_play_button(ai_settings, screen, stats, sb, play_button, goku,
        friezas, kames, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True
        
        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_gokus()
        
        # Empty the list of friezas and kames.
        friezas.empty()
        kames.empty()
        
        # Create a new fleet and center the goku.
        create_fleet(ai_settings, screen, goku, friezas, stats)
        goku.center_goku()

def fire_kame(ai_settings, screen, goku, kames):
    """Fire a kame, if limit not reached yet."""
    # Create a new kame, add to kames group.
    if len(kames) < ai_settings.kames_allowed:
        new_kame = Kame(ai_settings, screen, goku)
        kames.add(new_kame)

def update_screen(ai_settings, screen, stats, sb, goku, friezas, kames,
        play_button):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    screen.blit(ai_settings.bg_image, [0,0])
    
    # Redraw all kames, behind goku and friezas.
    for kame in kames.sprites():
        kame.draw_kame()
   
    goku.blitme(stats)
    
    friezas.draw(screen)
    
    # Draw the score information.
    sb.show_score()
    
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()
    
def update_kames(ai_settings, screen, stats, sb, goku, friezas, kames):
    """Update position of kames, and get rid of old kames."""
    # Update kame positions.
    kames.update()

    # Get rid of kames that have disappeared.
    for kame in kames.copy():
        if kame.rect.bottom <= 0:
            kames.remove(kame)
            
    check_kame_frieza_collisions(ai_settings, screen, stats, sb, goku,
        friezas, kames)
        
def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
            
def check_kame_frieza_collisions(ai_settings, screen, stats, sb, goku,
        friezas, kames):
    """Respond to kame-frieza collisions."""
    # Remove any kames and friezas that have collided.
    collisions = pygame.sprite.groupcollide(kames, friezas, True, True)
    
    if collisions:
        for friezas in collisions.values():
            stats.score += ai_settings.frieza_points * len(friezas)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(friezas) == 0:
        # If the entire fleet is destroyed, start a new level.
        kames.empty()
        ai_settings.increase_speed()
        
        # Increase level.
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, goku, friezas, stats)
    
def check_fleet_edges(ai_settings, friezas):
    """Respond appropriately if any friezas have reached an edge."""
    for frieza in friezas.sprites():
        if frieza.check_edges():
            change_fleet_direction(ai_settings, friezas)
            break
        
def change_fleet_direction(ai_settings, friezas):
    """Drop the entire fleet, and change the fleet's direction."""
    for frieza in friezas.sprites():
        frieza.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def goku_hit(ai_settings, screen, stats, sb, goku, friezas, kames):
    """Respond to goku being hit by frieza."""
    if stats.gokus_left > 0:
        # Decrement gokus_left.
        stats.gokus_left -= 1
        
        # Update scoreboard.
        sb.prep_gokus()
        
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        cursor.execute("insert into trouble_on_namec values(?, ?)", (stats.score, stats.level))
    
    # Empty the list of friezas and kames.
    friezas.empty()
    kames.empty()
    
    # Create a new fleet, and center the goku.
    create_fleet(ai_settings, screen, goku, friezas, stats)
    goku.center_goku()
    
    # Pause.
    sleep(0.5)
    
def check_friezas_bottom(ai_settings, screen, stats, sb, goku, friezas,
        kames):
    """Check if any friezas have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for frieza in friezas.sprites():
        if frieza.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the goku got hit.
            goku_hit(ai_settings, screen, stats, sb, goku, friezas, kames)
            break
            
def update_friezas(ai_settings, screen, stats, sb, goku, friezas, kames):
    """
    Check if the fleet is at an edge,
      then update the postions of all friezas in the fleet.
    """
    check_fleet_edges(ai_settings, friezas)
    friezas.update()
    
    # Look for frieza-goku collisions.
    if pygame.sprite.spritecollideany(goku, friezas):
        goku_hit(ai_settings, screen, stats, sb, goku, friezas, kames)

    # Look for friezas hitting the bottom of the screen.
    check_friezas_bottom(ai_settings, screen, stats, sb, goku, friezas, kames)
    

    

            
def get_number_friezas_x(ai_settings, frieza_width):
    """Determine the number of friezas that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * frieza_width
    number_friezas_x = int(available_space_x / (2 * frieza_width))
    return number_friezas_x
    
def get_number_rows(ai_settings, goku_height, frieza_height, stats):
    """Determine the number of rows of friezas that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                            (3 * frieza_height) - goku_height)
    number_rows = int(available_space_y / (2 * frieza_height))
    return number_rows
    
def create_frieza(ai_settings, screen, friezas, frieza_number, row_number, stats):
    """Create an frieza, and place it in the row."""
    frieza = Frieza(ai_settings, screen, stats)
    frieza_width = frieza.rect.width
    frieza.x = frieza_width + 2 * frieza_width * frieza_number
    frieza.rect.x = frieza.x
    frieza.rect.y = frieza.rect.height + 2 * frieza.rect.height * row_number
    friezas.add(frieza)

def create_fleet(ai_settings, screen, goku, friezas, stats):
    """Create a full fleet of friezas."""
    # Create an frieza, and find number of friezas in a row.
    frieza = Frieza(ai_settings, screen, stats)
    number_friezas_x = get_number_friezas_x(ai_settings, frieza.rect.width)
    number_rows = get_number_rows(ai_settings, goku.rect.height,
        frieza.rect.height, stats)
    
    # Create the fleet of friezas.
    for row_number in range(number_rows):
        for frieza_number in range(number_friezas_x):
            create_frieza(ai_settings, screen, friezas, frieza_number,
                row_number, stats)
