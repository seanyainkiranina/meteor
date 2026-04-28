"""Plane class for the parallax scrolling game."""

import pygame
from lib.missle import Missle


class Plane:
    """Class representing the player's plane in the parallax scrolling game."""

    def __init__(self, x, y, speed, width, height, filename, filename_right):
        self._x = x
        self._y = y
        self._world_x = x  # new: world position
        self._speed = speed  # Speed at which the plane moves
        self._width = width
        self._height = height
        self._right = True  # Direction the plane is facing
        self._image_left = pygame.image.load(filename).convert_alpha()
        self._image_right = pygame.image.load(
            filename_right
        ).convert_alpha()  # Pygame surface for the plane facing right
        self._image = self._image_right  # Pygame surface for the plane
        self._missle = None  # Missle object representing the plane's missle
        self._explosions = []  # List to hold explosion objects when the plane is hit
        self._explosions.append(
            pygame.image.load("player\\explosions\\1.png").convert_alpha()
        )
        self._explosions.append(
            pygame.image.load("player\\explosions\\2.png").convert_alpha()
        )
        self._explosions.append(
            pygame.image.load("player\\explosions\\3.png").convert_alpha()
        )
        self._explosions.append(
            pygame.image.load("player\\explosions\\4.png").convert_alpha()
        )
        self._explosions.append(
            pygame.image.load("player\\explosions\\5.png").convert_alpha()
        )
        self._explosions.append(
            pygame.image.load("player\\explosions\\6.png").convert_alpha()
        )
        self._explosions.append(
            pygame.image.load("player\\explosions\\7.png").convert_alpha()
        )
        self._exploding = False  # Flag to indicate if the plane is currently exploding
        self._explosion_frame = 0

    @property
    def image(self):
        """Get the plane's image."""
        return self._image

    @property
    def world_x(self):
        """Get the current world x position of the plane."""
        return self._world_x

    @property
    def x(self):
        """Get the current x position of the plane."""
        return self._x

    @property
    def y(self):
        """Get the current y position of the plane."""
        return self._y

    @property
    def direction(self):
        """Get the current direction of the plane."""
        return self._right

    @property
    def fired_missle(self):
        """Get the current missle object."""
        return self._missle

    @fired_missle.setter
    def fired_missle(self, value):
        self._missle = value

    def explode(self):
        """Trigger the explosion animation for the plane."""
        clock = pygame.time.Clock()
        self._exploding = True
        self._explosion_frame = 0  # Start at the first frame of the explosion
        while self._explosion_frame < len(self._explosions):
            clock.tick(10)  # Control the speed of the explosion animation
            self._image = self._explosions[
                self._explosion_frame
            ]  # Update to the current explosion frame
            self._explosion_frame += 1  # Move to the next frame

    def move(self):
        """Move the plane to the left by its speed."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self._y -= self._speed
        if keys[pygame.K_DOWN]:
            self._y += self._speed
        if keys[pygame.K_LEFT]:
            self._world_x -= self._speed
            self._image = self._image_right  # Change to right-facing image
        if keys[pygame.K_RIGHT]:
            self._world_x += self._speed
            self._image = self._image_left  # Change to right-facing image
        if keys[pygame.K_SPACE] and self._missle is None:
            # Fire a missle if space is pressed and there isn't already one on screen
            self._missle = Missle(
                self._x + self._image.get_width() // 2,
                self._y,
                self._width,
                self._height,
                "player\\missle.png",
                "player\\missle_right.png",
            )
            self._missle.direction = self._right  # Set missle direction to match plane
        self._x = self._width // 2 - self._image.get_width() // 2
        self._y = max(0, min(self._height - self._image.get_height(), self._y))

        if keys[pygame.K_LEFT]:
            self._right = True
        elif keys[pygame.K_RIGHT]:
            self._right = False

        if self._right and self._exploding is False:
            self._world_x -= self._speed
        if self._right is False and self._exploding is False:
            self._world_x += self._speed
