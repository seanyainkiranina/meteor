"""Meteor class for the Meteor game."""

import pygame


class City:
    """City class for the Meteor game."""

    def __init__(self, screen):
        self.screen = screen
        self.city_1 = pygame.image.load("backgrounds\\city1.png").convert_alpha()
        self.city_2 = pygame.image.load("backgrounds\\city2.png").convert_alpha()
        self.city_3 = pygame.image.load("backgrounds\\city3.png").convert_alpha()
        self.city_1_x = self.screen.get_width() // 2
        self.city_2_x = self.screen.get_width() // 2
        self.city_3_x = self.screen.get_width() // 2

    def draw(self, which_city, increment=0):
        """Draw the city layers on the screen."""
        if which_city == 1:
            self.city_1_x += increment
            self.screen.blit(
                self.city_1,
                (
                    self.city_1_x,
                    self.screen.get_height() - self.city_1.get_height() + 5,
                ),
            )
        elif which_city == 2:
            self.city_2_x += increment
            self.screen.blit(
                self.city_2,
                (
                    self.city_2_x,
                    self.screen.get_height() - self.city_2.get_height() + 5,
                ),
            )
        elif which_city == 3:
            self.city_3_x += increment
            self.screen.blit(
                self.city_3,
                (
                    self.city_3_x,
                    self.screen.get_height() - self.city_3.get_height() + 5,
                ),
            )
