import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
import game_functions as gf


def run_game():
    # Initialize  pygame, settings and  screen object.
    ai_settings = Settings()
    pygame.init()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # Make a play button
    play_button = Button(ai_settings, screen, "Play")
    # Make a ship
    ship = Ship(screen)
    # Make a Group to store the bullets in, and a group of aliens
    bullets = Group()
    aliens = Group()
    # create the stats instance
    stats = GameStats(ai_settings)
    # create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, ship, aliens, bullets,
                        play_button)
        if stats.active:
            ship.update()
            gf.update_bullets(aliens, bullets, screen, ship, ai_settings)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, ship, aliens, screen, stats, bullets,
                         play_button)
        # lets get rid of the bullets which reach the top of the screen


run_game()
