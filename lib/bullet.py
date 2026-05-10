"""Plane class for the parallax scrolling game."""

import pygame


class Bullet:
    """Bullet class for the Meteor game."""

    def __init__(self, screen, x, y):
        """Initialize the Bullet class."""
        self._screen = screen
        self._x = x
        self._y = y
        self._speed = 10
        self._right = False
        self._image = pygame.image.load("player\\alien_bullet.png").convert_alpha()
        self._left_image = pygame.image.load("player\\alien_bullet.png").convert_alpha()
        self._right_image = pygame.image.load("player\\alien_bullet.png").convert_alpha()
        self._direction_set = False
        self._up = False
        self._firing_up_down = False

    @property
    def direction_set(self):
        """Check if the bullet's direction has been set."""
        return self._direction_set

    @direction_set.setter
    def direction_set(self, value):
        """Set the bullet's direction."""
        self._direction_set = value 

    @property
    def firing_up_down(self):
        """Check if the bullet is firing up or down."""
        return self._firing_up_down
    @firing_up_down.setter
    def firing_up_down(self, value):
        """Set the bullet's firing direction (up or down)."""
        self._firing_up_down = value

    @property
    def x(self):
        """Get the current x position of the bullet."""
        return self._x

    @property
    def y(self):
        """Get the current y position of the bullet."""
        return self._y

    @property
    def image(self):
        """Get the current image of the bullet."""
        return self._image

    def move(self, plane):
        """Move the bullet upwards across the screen."""
        if not self._direction_set:
            if plane.x < self._x:
                self._right = True
                self._image = self._right_image
            else:
                self._right = False
                self._image = self._left_image
            self._direction_set = True
            if plane.y < self._y:
                self._up = True
            if plane.y > self._y:
                self._up = False

        if self._right:
            self._x -= self._speed
        else:
            self._x += self._speed
        if self._firing_up_down:
            if self._up:
                self._y -= self._speed
            else:
                self._y += self._speed
        self._firing_up_down = False
