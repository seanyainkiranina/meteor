"""Stargate class for the Meteor game."""

import pygame


class Stargate:
    """City class for the Meteor game."""

    def __init__(self, screen):
        self._stargates = []
        self._stargates_x = []
        self._stargates_positions = [0]
        self._screen = screen
        self._stargates.append(pygame.image.load("backgrounds\\stargate.png").convert_alpha())
        self._stargates.append(pygame.image.load("backgrounds\\stargate.png").convert_alpha())
        self._which = -1
        self._diff_x = 0
        self._max = len(self._stargates) - 1
        first = 0
        for _ in range(0, self._max):
            self._stargates_x.append(self._screen.get_width() // 2)
            self._stargates_positions.append(first)
            first += 6000
    @property
    def x(self):
        """Get the current x position of the city."""
        return self._stargates_x[self._which]

    @property
    def y(self):
        """Get the current y position of the city"""
        return self._screen.get_height() // 2
    @property
    def position(self):
        """Get the current position of the city."""
        return self._stargates_positions[self._which]

    @property
    def which(self):
        """which city"""
        return self._which

    def crash_check(self, plane, handle_shield_hit=False):
        """Check for collision with the player's plane."""
        if plane.shield_on and handle_shield_hit:
            return False  # No collision if the shield is on
        plane_rect = plane.image.get_rect(topleft=(plane.x, plane.y))
        stargate_rect = self._stargates[self._which].get_rect(topleft=(self.x, self.y))
        return plane_rect.colliderect(stargate_rect)

    def display(self, world_x, diff_x):
        """display a city"""
        self._diff_x = diff_x
        for i in range(0, self._max):
            if i >= len(self._stargates_x):
                continue
            if world_x < self._stargates_positions[i] - 2000:
                continue
            if world_x > self._stargates_positions[i] + 1000:
                continue
            self._which = i
            self.draw(i, world_x, diff_x)
            return True
        return False

    def draw(self, which_city, world_x, increment=0):
        """Draw the city layers on the screen."""
        if which_city <= self._max:
            self._which = which_city
            screen_x = self._stargates_positions[which_city] - world_x + self._screen.get_width() // 2 
            self._screen.blit(self._stargates[which_city], (screen_x, self._screen.get_height()//2))
            self._stargates_x[which_city]= screen_x
            return True
        return False
