import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in a freet!"""

    def __init__(self, ai_setting, screen):
        """Initialize the alien and its starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_setting = ai_setting

        # load alien image and set rect attributes
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # start new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store alien position
        self.x = float(self.rect.x)

    def blitme(self):
        """ draw the alien at its current position"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= screen_rect.left:
            return True

    def update(self):
        """Move alien to the right or left"""
        self.x += (self.ai_setting.alien_speed_factor *
                   self.ai_setting.fleet_direction)
        self.rect.x = self.x
