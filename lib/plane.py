"""Plane class for the parallax scrolling game."""

import time
import pygame
from lib.missle import Missle


class Plane:
    """Class representing the player's plane in the parallax scrolling game."""

    def __init__(self, x, y, speed, width, height, filename, filename_right):
        self._x = x
        self._y = y
        self._game_over = False
        self._score = 0
        self._lives = 3
        self._shield_on = False
        self._world_x = x  # new: world position
        self._speed = speed  # Speed at which the plane moves
        self._width = width
        self._height = height
        self._last = None
        self._shield_time = 1000
        self._right = True  # Direction the plane is facing
        self._image_left = pygame.image.load(filename).convert_alpha()
        self._shield_left = pygame.image.load(
            "player\\shield_plane.png"
        ).convert_alpha()
        self._shield_right = pygame.image.load(
            "player\\shield_plane_right.png"
        ).convert_alpha()
        self._org_width, self._org_height = self._image_left.get_size()
        self._scale_factor = 4.0  # 2x bigger
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
    def game_over(self):
        """get game over man game over"""
        return self._game_over
    
    @property
    def shield_on(self):
        """Get the shield status of the plane."""
        return self._shield_on

    @property
    def image(self):
        """Get the plane's image."""
        return self._image

    @property
    def exploding(self):
        """Get the explosion status of the plane."""
        return self._exploding

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

    def reset_missle(self):
        """Reset the missle to None."""
        self._missle = None

    def hit_on_shield(self):
        """hit on shield"""
        self._shield_time -= 10

    def add_score(self, amount):
        """Add score"""
        self._score += amount

    @property
    def lives(self):
        """get lives"""
        return self._lives

    @property
    def score(self):
        """return score"""
        return self._score

    @property
    def shield_time(self):
        """Time left for shield"""
        return self._shield_time

    def reset(self):
        """Reset the plane's position and state."""
        time.sleep(0.5)
        self._lives -= 1
        self._x = self._width // 2 - self._image.get_width() // 2
        self._y = self._height // 2 - self._image.get_height() // 2
        self._world_x = self._x
        self._right = True
        self._scale_factor = 1.0
        self._image = pygame.transform.scale(
            self._image_right,
            (
                int(self._org_width * self._scale_factor),
                int(self._org_height * self._scale_factor),
            ),
        )
        self._missle = None
        self._exploding = False
        self._explosion_frame = 0
        self._shield_on = False
        self._shield_time = 1000
        if self._lives <= 0:
            self._game_over = True

    def explode(self):
        """Trigger the explosion animation for the plane."""
        self._exploding = True
        self._y -= self._speed * 2
        self._scale_factor += 0.5  # Start with original size
        if self._explosion_frame < len(self._explosions):
            self._image = pygame.transform.scale(
                self._explosions[self._explosion_frame],
                (
                    int(self._org_width * self._scale_factor),
                    int(self._org_height * self._scale_factor),
                ),
            )
            # Update to the current explosion frame
            self._explosion_frame += 1  # Move to the next frame
            if self._explosion_frame >= 2:
                time.sleep(0.05)
        else:
            self.reset()  # Reset the plane after the explosion animation is complete

    def move(self):
        """Move the plane to the left by its speed."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.geme_over = True

        if keys[pygame.K_d]:
            if self._shield_on:
                self._y += self._shield_left.get_height() // 2
            self._shield_on = False

        if keys[pygame.K_s]:
            if self._shield_time > 0:
                if not self._shield_on:
                    self._y -= self._shield_left.get_height() // 2
                self._shield_on = True

        if self._exploding:
            self._shield_on = False
        if keys[pygame.K_ESCAPE]:
            self._lives =0
            self.explode()
            
        if keys[pygame.K_UP] and not self._exploding:
            self._y -= self._speed
        if keys[pygame.K_DOWN] and not self._exploding:
            self._y += self._speed
        if keys[pygame.K_LEFT] and not self._exploding:
            self._world_x -= self._speed
        if keys[pygame.K_RIGHT] and not self._exploding:
            self._world_x += self._speed

        if keys[pygame.K_LEFT] and not self._exploding:
            self._right = True
        elif keys[pygame.K_RIGHT] and not self._exploding:
            self._right = False

        if (
            keys[pygame.K_SPACE]
            and self._missle is None
            and not self._exploding
            and not self._shield_on
        ):
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

        if self._right and self._exploding is False:
            self._world_x -= self._speed
        if self._right is False and self._exploding is False:
            self._world_x += self._speed

        if self._shield_on:
            self._shield_time -= 1
            if self._shield_time <= 0:
                self._shield_on = False

        if self._lives <= 0:
            self._game_over = True

        if not self._exploding:
            if self._shield_on:
                if not self._right:
                    self._image = self._shield_left

                if self._right:
                    self._image = self._shield_right
            else:
                if self._right:
                    self._image = self._image_right

                if not self._right:
                    self._image = self._image_left
