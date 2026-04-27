"""Meteor class for the Meteor game."""

import random
import pygame


class Meteor:
    """Class representing the main game logic for the Meteor game."""

    def __init__(self, width, height):
        self._x = random.randint(0, width)
        self._y = random.randint(-100, -40)  # Start above the screen
        self._width = width
        self._height = height
        self._prefixs = ["J6_", "C6_", "A1_", "J5_"]
        self._prefix = random.choice(self._prefixs)
        self._asteroid = pygame.image.load(f"images\\{self._prefix}0.png").convert_alpha()
        self._r =0
    @property
    def asteroid(self):
        """Get the asteroid's image."""
        self._r += 1
        if self._r > 360:
            self._r = 0
        if self._r % 20 == 0:
            self._asteroid = pygame.image.load(f"images\\{self._prefix}{self._r}.png").convert_alpha()
        return self._asteroid

    @property
    def x(self):
        """Get the current x position of the asteroid."""
        return self._x

    @property
    def y(self):
        """Get the current y position of the asteroid."""
        return self._y

    def move(self):
        """Move the asteroid downwards."""
        self._y += random.randint(1, 5)  # Move down by a random speed
     
        if self._y > self._height:
            self._prefix = random.choice(self._prefixs)
            self._x = random.randint(0, self._width)  # Reset to a new random x position
            self._y = random.randint(-100, -40)  # Reset to start above the screen
