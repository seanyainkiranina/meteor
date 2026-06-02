"""Missle class for the Meteor game."""

import pygame


class Missle:
    """Class representing a missle in the Meteor game."""

    def __init__(self, x, y, width, height, filename, filename_right):
        self._x = x
        self._start_x = x
        self._y = y + 22
        self._start_y = y
        self._width = width
        self._height = height
        self._up = False
        self._down = False
        self._upward = False
        self._image_left = pygame.image.load(filename).convert_alpha()
        self._image_right = pygame.image.load(filename_right).convert_alpha()
        self._image_up = pygame.image.load("player\\missle_up.png").convert_alpha()
        self._image_right_1 = pygame.image.load(
            "player\\missle_right_1.png"
        ).convert_alpha()
        self._image_right_2 = pygame.image.load(
            "player\\missle_right_2.png"
        ).convert_alpha()
        self._image_left_1 = pygame.image.load("player\\missle_1.png").convert_alpha()
        self._image_left_2 = pygame.image.load("player\\missle_2.png").convert_alpha()

        self._image_right_1_down = pygame.image.load(
            "player\\missle_right_1_down.png"
        ).convert_alpha()
        self._image_right_2_down = pygame.image.load(
            "player\\missle_right_2_down.png"
        ).convert_alpha()
        self._image_left_1_down = pygame.image.load(
            "player\\missle_1_down.png"
        ).convert_alpha()
        self._image_left_2_down = pygame.image.load(
            "player\\missle_2_down.png"
        ).convert_alpha()
        self._image = self._image_right
        self._right = True  # Direction the missle is facing

    @property
    def upward(self):
        """staight up."""
        return self._upward

    @upward.setter
    def upward(self, value):
        """set straight up."""
        self._upward = value

    @property
    def up(self):
        """upward direction"""
        return self._up

    @up.setter
    def up(self, value):
        """set up"""
        self._up = value

    @property
    def down(self):
        """downward direction"""
        return self._up

    @down.setter
    def down(self, value):
        """set down"""
        self._down = value

    @property
    def direction(self):
        """Get the current direction of the missle."""
        return self._right

    @direction.setter
    def direction(self, value):
        """Set the direction of the missle."""
        self._right = value

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

    def hit_check(self, meteor):
        """Check if the missle has hit a meteor."""
        if self._image is None:
            return False
        missle_rect = self._image.get_rect(topleft=(self._x, self._y))
        meteor_rect = meteor.asteroid.get_rect(topleft=(meteor.x, meteor.y))
        return missle_rect.colliderect(meteor_rect)

    def move(self):
        """Move the missle in the specified direction."""
        difference = abs(self._start_x - self._x)
     #   y_difference = abs(self._y - self._start_y)
        if self._upward:
            if self._right is False:
                self._x = self._start_x + 40
            self._image = self._image_up
            self._y -= 10

        if self._up:
            if difference > 10:
                if self._right:
                    self._image = self._image_right_1
                else:
                    self._image = self._image_left_1
            if difference > 20:
                if self._right:
                    self._image = self._image_right_2
                else:
                    self._image = self._image_left_2
            if difference > 30:
                self._y -= 10
        if self._down:
            if difference > 10:
                if self._right:
                    self._image = self._image_right_1_down
                    self._x -= 10  # Move left by 10 pixels
                else:
                    self._image = self._image_left_1_down
                    self._x += 10  # Move left by 10 pixels
            if difference > 20:
                if self._right:
                    self._image = self._image_right_2_down
                else:
                    self._image = self._image_left_2_down
            if difference > 30:
                self._y += 10

        if self._right:
            if self._upward is False:
                self._x -= 10  # Move left by 10 pixels
                self._image = self._image_left

        if not self._right:
            if self._upward is False:
                self._x += 10  # Move right by 10 pixels
                self._image = self._image_right

        if self._x < -100:
            self._image = None
        if self._x > self._width + 100:
            self._image = None  # Mark missle for removal if it goes off-screen

        if self._y < -100:
            self._image = None

        if self._y > 700:
            self._image = None
