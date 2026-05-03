"""Meteor class for the Meteor game."""

import random
import pygame
from lib.diamond import Diamond


class City:
    """City class for the Meteor game."""

    def __init__(self, screen):
        self._cities = []
        self._craters = []
        self._cities_x = []
        self._diamonds = []
        self._exploded = []
        self._cities_positions = [0]
        self._screen = screen
        self._cities.append(pygame.image.load("backgrounds\\city1.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city2.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city3.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city1.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city2.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city3.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city1.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city2.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city3.png").convert_alpha())
        self._diamond = None
        self._which = -1
        index = 0
        while index < len(self._cities):
            self._exploded.append(False)
            self._cities_x.append(self._screen.get_width() // 2)
            self._craters.append(pygame.image.load("backgrounds\\crater.png").convert_alpha())
            self._cities_positions.append(random.randint(-30000, 30000))
            index += 1

    @property
    def diamond(self):
        """Only one city at a time can fire a diamond"""
        return self._diamond

    @diamond.setter
    def diamond(self,value):
        """setter for diamond"""
        self._diamond = value

    def display(self, where_city, diff_x):
        """display a city"""
        index = 0
        while index < len(self._cities_positions):
            if index >= len(self._cities):
                return
            if index >= len(self._cities_x):
                self._cities_x.append(self._screen.get_width() // 2)
            if where_city > self._cities_positions[index] - 5000 and where_city < (
                    self._cities_positions[index] + 5000
             ):
                if self.draw(index, diff_x) and  random.randint(0, 100) % 50 == 0:
                    if self._diamond is None:
                        self._diamond = Diamond(
                                self._cities_x[index],
                                800 - self._cities[index].get_height(),
                        )
                    else:
                        if self._diamond.hit or self._diamond.y<0:
                            self._diamond = None
            else:
                self.reset(index)
            index += 1

    def reset(self, which_city):
        """Reset the city layer's position."""
        if 0 >= which_city < len(self._cities_x):
            self._cities_x[which_city] = self._screen.get_width() // 2

    def hit_meteor_check(self,meteor):
        """ check if meteor hit """
        if self._which <0:
            return False
        if self._which >= len(self._cities):
            return False
        if self._which >= len(self._cities_x):
            return False
        if self._which >= len(self._exploded):
            return False
        if self._exploded[self._which]:
            return False
        city_x = self._cities_x[self._which]
        city_y = 800-self._cities[self._which].get_height()
        city_rect = self._cities[self._which].get_rect(
            topleft=(city_x, city_y))
        meteor_rect = meteor.asteroid.get_rect(topleft=(meteor.x, meteor.y))
        boom = city_rect.colliderect(meteor_rect)
        if boom is False:
            return False
        self._exploded[self._which] =  boom
        self._cities[self._which] = self._craters[self._which]

        return True

        

    def draw(self, which_city, increment=0):
        """Draw the city layers on the screen."""
        if 0 >= which_city < len(self._cities_x):
            self._which = which_city
            self._cities_x[which_city] += increment
            self._screen.blit(
                self._cities[which_city],
                (
                    self._cities_x[which_city],
                    self._screen.get_height()
                    - self._cities[which_city].get_height()
                    + 5,
                ),
            )
            return True
        self._which = -1
        return False
