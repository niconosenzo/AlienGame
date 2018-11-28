import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    # Decrement ships_left.
    if stats.ships_left > 1:
        stats.ships_left -= 1

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        pygame.mouse.set_visible(True)
        stats.active = False


def check_key_down_event(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    # create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_key_up_event(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, ship, aliens, bullets,
                 play_button):
    # Watch for keyboard and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            """Respond to key press event"""
            check_key_down_event(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            """Respond to key release event"""
            check_key_up_event(event, ship)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """Start a new game_active when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset game stats
        stats.reset_stats()
        stats.active = True
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_bullets(aliens, bullets, screen, ship, ai_settings):
    bullets.update()
    for bul in bullets.copy():
        if bul.rect.bottom <= 0:
            bullets.remove(bul)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """Respond to bullet-alien collisions"""
    # check collision between bullets and aliens
    # If so, get rid the bullets and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def update_screen(ai_settings, ship, aliens, screen, stats,
                  bullets, play_button):
    """ Make the most recently drawn screen visible.
    Set the background color and redraw the screen during each
    pass through the loop """
    screen.fill(ai_settings.bg_color)
    # Re-draw all bullets behind ships and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if not stats.active:
        play_button.draw_button()
    pygame.display.flip()


def get_number_aliens_x(ai_settings, alien_width):
    """ Determine the numb of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_of_aliens = int(available_space_x / (2 * alien_width))
    return number_of_aliens


def get_number_of_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) -
                         ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create the alien and find the number of aliens in a row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """create the fleet of aliens!"""
    alien = Alien(ai_settings, screen)
    number_of_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_of_rows = get_number_of_rows(ai_settings, ship.rect.height,
                                        alien.rect.height)

    # create the first row of aliens
    for row_number in range(number_of_rows):
        for alien_number in range(number_of_aliens_x):
            # create one and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Update position of all the aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        print("Ship hit!!!")
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)


def check_aliens_bottom(ai_setting, stats, screen, ship, aliens, bullets):
    """ Check if any aliens have reached the bottom of the screen """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_setting, stats, screen, ship, aliens, bullets)
            break


def check_fleet_edges(ai_settings, aliens):
    """respond if any alien has reached the screen edge"""
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop fleet one row and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
