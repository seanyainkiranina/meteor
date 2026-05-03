"""Diamond class for the Meteor game."""
import random
import pygame


class Diamond:
    """A way to get extra points and shield points back"""

    def __init__(self, x, y):
        """create a diamond"""
        self._x = x
        self._y = y
        self._stored = pygame.image.load("player\\shield_diamond.png").convert_alpha()
        self._image = pygame.image.load("player\\shield_diamond.png").convert_alpha()
        self._width = self._image.get_width()
        self._height = self._image.get_height()
        self._hit = False

    @property
    def hit(self):
        """return hit bool"""
        return self._hit

    @hit.setter
    def hit(self, value):
        """flag a hit"""
        self._hit = value

    @property
    def image(self):
        """Get the diamonds's image."""
        return self._image

    @property
    def x(self):
        """Get the current x position of the missle."""
        return self._x

    @x.setter
    def x(self, value):
        """set x for drift"""
        self._x = value

    @property
    def y(self):
        """Get the current y position of the missle."""
        return self._y

    @y.setter
    def y(self, value):
        """set y"""
        self._y = value

    def hit_meteor_check(self, meteor):
        """Check if the diamond has hit a meteor."""
        shield_rect = self._image.get_rect(topleft=(self._x, self._y))
        meteor_rect = meteor.asteroid.get_rect(topleft=(meteor.x, meteor.y))
        return shield_rect.colliderect(meteor_rect)

    def hit_player_check(self, plane):
        """Check if diamond has hit a player"""
        if self._image is None:
            return False
        if plane.image is None:
            return False
        if plane.exploding:
            return False
        if plane.shield_on:
            return False
        shield_rect = self._image.get_rect(topleft=(self._x, self._y))
        plane_rect = plane.image.get_rect(topleft=(plane.x, plane.y))
        return shield_rect.colliderect(plane_rect)

    def move(self):
        """Move the missle in the specified direction."""
        self._y -= random.randint(3,20)  # Move left by 10 pixels
        if self._y < 0:
            self._image = None
