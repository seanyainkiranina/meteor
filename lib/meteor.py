"""Meteor class for the Meteor game."""

import random
import pygame
import re


class Meteor:
    """Class representing the main game logic for the Meteor game."""

    def __init__(self, width, height):
        self._x = random.randint(0, width)
        self._y = random.randint(-4000, -200)  # Start above the screen
        self._width = width
        self._height = height
        self._prefixs = [
            "A1_",
            "A2_",
            "A3_",
            "A4_",
            "A5_",
            "B10_",
            "B11_",
            "B12_",
            "B13_",
            "B14_",
            "B15_",
            "B16_",
            "B17_",
            "B1_",
            "B2_",
            "B3_",
            "B4_",
            "B5_",
            "B6_",
            "B7_",
            "B8_",
            "B9_",
            "C10_",
            "C11_",
            "C12_",
            "C13_",
            "C14_",
            "C15_",
            "C16_",
            "C17_",
            "C1_",
            "C2_",
            "C3_",
            "C4_",
            "C5_",
            "C6_",
            "C7_",
            "C8_",
            "C9_",
            "D10_",
            "D11_",
            "D1_",
            "D2_",
            "D3_",
            "D4_",
            "D5_",
            "D7_",
            "D8_",
            "D9_",
            "E1_",
            "E2_",
            "E3_",
            "E4_",
            "E5_",
            "F1_",
            "G1_",
            "G2_",
            "G3_",
            "G4_",
            "G5_",
            "G7_",
            "H1_",
            "H2_",
            "H3_",
            "H4_",
            "H5_",
            "H6_",
            "I1_",
            "I2_",
            "I3_",
            "I4_",
            "I5_",
            "I6_",
            "J1_",
            "J2_",
            "J3_",
            "J4_",
            "J5_",
            "J6_",
        ]
        self._prefix = random.choice(self._prefixs)
        self._asteroid = pygame.image.load(
            f"images\\rot\\{self._prefix}0.png"
        ).convert_alpha()
        self._r = 0

    @property
    def asteroid(self):
        """Get the asteroid's image."""
        self._r += 1
        if self._r > 360:
            self._r = 0
        if self._r % 20 == 0:
            self._asteroid = pygame.image.load(
                f"images\\rot\\{self._prefix}{self._r}.png"
            ).convert_alpha()
        return self._asteroid

    @property
    def x(self):
        """Get the current x position of the asteroid."""
        return self._x

    @property
    def y(self):
        """Get the current y position of the asteroid."""
        return self._y

    @property
    def prefix(self):
        """Get the current prefix of the asteroid."""
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        """Set the prefix of the asteroid."""
        self._prefix = value

    def next(self):
        """Get the next image for the asteroid's animation."""
        next_step = "X"
        if self.prefix[0] == "A":
            next_step = "B"
        elif self.prefix[0] == "B":
            next_step = "C"
        elif self.prefix[0] == "C":
            next_step = "D"
        elif self.prefix[0] == "D":
            next_step = "E"
        elif self.prefix[0] == "E":
            next_step = "F"
        elif self.prefix[0] == "F":
            next_step = "G"
        elif self.prefix[0] == "G":
            next_step = "H"
        elif self.prefix[0] == "H":
            next_step = "I"
        elif self.prefix[0] == "I":
            next_step = "J"
        newprefix = next_step + self.prefix[1:]
        if self._prefixs.index(newprefix) >-1:
            self.prefix = next_step + self.prefix[1:]
        self._asteroid = pygame.image.load(
            f"images\\rot\\{self._prefix}{self._r}.png"
        ).convert_alpha()
        return self._asteroid

    def remove_non_numeric(self, s):
        """
        Remove all non-numeric characters from a string.
        Returns only digits as a string.
        """
        if not isinstance(s, str):
            raise TypeError("Input must be a string.")

        # Replace any character that is not a digit with an empty string
        return re.sub(r"[^0-9]", "", s)

    def move(self, currentx, lastx):
        """Move the asteroid downwards."""
        self._y += random.randint(1, 5)  # Move down by a random speed
        if lastx < currentx:
            self._x -= random.randint(0, 2)  # Move right slightly
        elif lastx > currentx:
            self._x += random.randint(0, 2)  # Move left slightly
        if self._y > self._height:
            self._prefix = random.choice(self._prefixs)
            self._x = random.randint(0, self._width)  # Reset to a new random x position
            self._y = random.randint(-4000, -200)  # Reset to start above the screen
