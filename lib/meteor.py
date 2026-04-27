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
        self._prefixs = ["A1_","A2_","A3_", "A4_", "A5_",
                          "B10_","B11_", "B12_", "B13_", "B14_",
                          "B15_","B16_", "B17_", "B1_", "B2_",
                          "B3_", "B4_", "B5_", "B6_", "B7_", "B8_", "B9_",
                          "C1_", "C2_", "C3_", "C4_", "C5_", "C6_", "C7_", "C8_", "C9_",
                          "C10_", "C11_", "C12_", "C13_", "C14_", "C15_", "C16_", "C17_",
                          "D10_", "D11_", "D1_", "D2_", "D3_", "D4_", "D5_", "D7_",
                          "D8_","E1_", "E2_", "E3_", "E4_", "E5_", "F1_", "G1_", "G2_", "G3_",
                          "G4_", "G5_", "I1_", "G7_", "H1_", "H2_"]
        self._prefix = random.choice(self._prefixs)
        self._asteroid = pygame.image.load(f"images\\rot\\{self._prefix}0.png").convert_alpha()
        self._r =0
    @property
    def asteroid(self):
        """Get the asteroid's image."""
        self._r += 1
        if self._r > 360:
            self._r = 0
        if self._r % 20 == 0:
            self._asteroid = pygame.image.load(f"images\\rot\\{self._prefix}{self._r}.png").convert_alpha()
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
