"""Meteor class for the Meteor game."""

import random
from numpy._core.defchararray import index
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
        self._cities.append(pygame.image.load("backgrounds\\city1.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city2.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city2.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city3.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city3.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city4.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city4.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city2.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city2.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city3.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city3.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city4.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city4.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city5.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city5.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city6.png").convert_alpha())
        self._cities.append(pygame.image.load("backgrounds\\city6.png").convert_alpha())
        self._diamond = None
        self._which = -1
        self._diff_x = 0
        self._max = len(self._cities) - 1
        first = -9000
        for _ in range(0, self._max):
            self._exploded.append(False)
            self._cities_x.append(self._screen.get_width() // 2)
            self._craters.append(
                pygame.image.load("backgrounds\\crater.png").convert_alpha()
            )
            self._cities_positions.append(first)
     #       print(f"City {index} position set to {first}.")
            first += 6000
        #print(f"City initialized with {len(self._cities)} cities.")
    @property
    def x(self):
        """Get the current x position of the city."""
        return self._cities_x[self._which]

    @property
    def position(self):
        """Get the current position of the city."""
        return self._cities_positions[self._which]

    @property
    def which(self):
        """which city"""
        return self._which

    @property
    def diamond(self):
        """Only one city at a time can fire a diamond"""
        return self._diamond

    @diamond.setter
    def diamond(self, value):
        """setter for diamond"""
        self._diamond = value

    def display(self, world_x, diff_x):
        """display a city"""
        self._diff_x = diff_x
        for i in range(0, self._max):
            if i >= len(self._cities_x):
                continue
            if world_x < self._cities_positions[i] - 2000:
                continue
            if world_x > self._cities_positions[i] + 1000:
                continue
            if self._exploded[i] is True:
                self.reset(i)
                continue
            # print(f"City {index} is within range of the camera at position {world_x}.")
            # print(f"city {index} at position {self._cities_positions[index]} where {world_x}.")
            self._which = i
            self.draw(i, world_x, diff_x)
            if random.randint(0, 100) % 75 == 0:
                if self._diamond is None:
                    self._diamond = Diamond(
                            self._cities_x[i],
                            800 - self._cities[i].get_height(),
                        )
        if self._diamond is not None and (self._diamond.hit or self._diamond.y < 0):
            self._diamond = None

    def reset(self, which_city):
        """Reset the city layer's position."""
        if which_city < self._max:
            self._cities_x[which_city] = self._screen.get_width() // 2

    def hit_meteor_check(self, meteor):
        """check if meteor hit"""
        if meteor.y < 600:
            return False
        if meteor.x < 0 or meteor.x > 800:
            return False
        if self._which < 0 or self._which > self._max:
            return False
        if self._exploded[self._which] is True:
            return False
        city_x = self._cities_x[self._which]
        city_y = self._screen.get_height() - self._cities[self._which].get_height() + 5
        city_rect = self._cities[self._which].get_rect(topleft=(city_x, city_y))
        meteor_rect = meteor.asteroid.get_rect(topleft=(meteor.x, meteor.y))
        boom = city_rect.colliderect(meteor_rect)
        if boom is False:
            return False
        else:
            self._exploded[self._which] = boom
            self._cities[self._which] = self._craters[self._which]
        return True

    def draw(self, which_city, world_x, increment=0):
        """Draw the city layers on the screen."""
        if which_city <= self._max:
            self._which = which_city
         #   self._cities_x[which_city] += increment
         #   print(f"Drawing city {which_city} at x position {self._cities_x[which_city]} with increment {increment}.")
            screen_x = self._cities_positions[which_city] - world_x + self._screen.get_width() // 2 
            self._screen.blit(self._cities[which_city], (screen_x, self._screen.get_height() - self._cities[which_city].get_height() + 5))
        #       print(f"City {which_city} drawn at screen x position {screen_x}.")
            self._cities_x[which_city]= screen_x
            return True
        return False
