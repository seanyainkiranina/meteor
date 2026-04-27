""" Missle class for the Meteor game. """
import pygame

class Missle:
    """Class representing a missle in the Meteor game."""
    def __init__(self, x, y, width, height, filename, filename_right):
        self._x = x
        self._y = y+22
        self._width = width
        self._height = height
        self._image_left = pygame.image.load(filename).convert_alpha()
        self._image_right = pygame.image.load(filename_right).convert_alpha()
        self._image = self._image_right

    @property
    def image(self):
        """Get the missle's image."""
        return self._image
    def x(self):
        """Get the current x position of the missle."""
        return self._x
    def y(self):
        """Get the current y position of the missle."""
        return self._y
    
    def move(self, direction):
        """Move the missle in the specified direction."""
        if direction == "left":
            self._x -= 10  # Move left by 10 pixels
            self._image = self._image_left
            if self._x < 0:
                self._image = None  # Mark missle for removal if it goes off-screen
        elif direction == "right":
            self._x += 10  # Move right by 10 pixels
            self._image = self._image_right
            if self._x > self._width:
                self._image = None  # Mark missle for removal if it goes off-screen