"""Alien class for the Meteor game."""

import random
import pygame

from lib.meteor import Meteor  # pylint: disable=[E0611,W0611]
from lib.bullet import Bullet  # pylint: disable=[E0611,W0611]


class Alien:
    """Alien class for the Meteor game."""

    def __init__(self, screen):
        """Initialize the Alien class."""
        self._screen = screen
        self._speed = 1
        self._bullet = None
        self._right = False
        self._insights = False
        self._visible = True
        startx = random.randint(0, 300)
        self._image_left = pygame.image.load("player\\alien.png").convert_alpha()
        self._image_right = pygame.image.load("player\\alien_right.png").convert_alpha()

        r = random.randint(0, 100) % 50 == 0
        if r:
            self._image_left = pygame.image.load("player\\lander.png").convert_alpha()
            self._image_right = pygame.image.load("player\\lander.png").convert_alpha()


        self._explosion = pygame.image.load(
            "player\\alien_explosion.png"
        ).convert_alpha()
        self._explosion_frames = 6
        if random.randint(0, 100) % 2 == 0:
            self._right = True
            self._x = -100 - startx
            self._image = self._image_right
        else:
            self._x = self._screen.get_width() + 100 + startx
            self._image = self._image_left
        self._y = random.randint(
            self._image.get_height(), self._screen.get_height() // 2
        )

    @property
    def x(self):
        """Get the current x position of the alien."""
        return self._x

    @property
    def y(self):
        """Get the current y position of the alien."""
        return self._y

    @property
    def image(self):
        """Get the current image of the alien."""
        return self._image

    @property
    def bullet(self):
        """Get the current bullet of the alien."""
        return self._bullet

    def move(self, meteors, plane, aliens, missle):
        """Move the alien across the screen."""
        lookahead_distance = 50
        fire = random.randint(0, 100) < 5  # 5% chance to fire each frame
        plane_rect = plane.image.get_rect(topleft=(plane.x, plane.y))
        alien_rect = self._image.get_rect(topleft=(self._x, self._y))
        change_direction_chance = random.randint(0, 100) < 10  # 10% chance to change direction

        if plane.using_smart_bombs:
             # Check if the alien is within the smart bomb's blast radius
            smart_bomb_radius = 200  # Example radius for the smart bomb
            distance_to_alien = ((self._x - plane.x) ** 2 + (self._y - plane.y) ** 2) ** 0.5
            if distance_to_alien <= smart_bomb_radius:
                self._image = self._explosion
                self._visible = False
                plane.add_score(150)  # Award points for hitting the alien with a smart bomb
                return

        if plane_rect.colliderect(alien_rect) and self._visible:
            if plane.shield_on:
                plane.hit_on_shield()  # Reduce shield time instead of lives
                self._image = self._explosion
                self._visible = False
                plane.add_score(50)  # Award points for hitting the alien with the shield on
                return
            plane.explode()
            self._image = self._explosion
            self._visible = False
            return

        if self._bullet is not None:
            bullet_rect = self._bullet.image.get_rect(
                topleft=(self._bullet.x, self._bullet.y)
            )
            if bullet_rect.colliderect(plane_rect):
                plane.explode()
                self._bullet = None  # Remove bullet after hitting the plane

        if missle is not None:
            missle_rect = missle.image.get_rect(topleft=(missle.x(), missle.y()))
            if missle_rect.colliderect(alien_rect):
                self._image = self._explosion
                self._visible = False
                plane.add_score(100)
                return

        if not self._visible and self._explosion_frames > 0:
            self._explosion_frames -= 1
            return

        if self._explosion_frames == 0:
            self._visible = True
            self._x = random.randint(-100, self._screen.get_width() + 100)
            self._y = random.randint(
                self._image.get_height(), self._screen.get_height() // 2
            )
            if self.x < 0:
                self._x = -300
                self._right = True
            else:
                self._x = self._screen.get_width() + 300
                self._right = False
            self._image = self._image_right if self._right else self._image_left
            self._bullet = None
            self._explosion_frames = 6
            self._insights = False
            self._visible = True
            return

        if self._visible is False:
            return

        if self._x < 0 or self._x > self._screen.get_width():
            fire = False
        if fire and self._bullet is None and self._insights:
            self._bullet = Bullet(
                self._screen,
                self._x + self._image.get_width(),
                self._y + self._image.get_height() // 2,
            )
            self._bullet.firing_up_down = True
        if self._bullet is not None:
            self._bullet.move(plane)
            if (
                self._bullet.y < -50
                or self._bullet.y > self._screen.get_height() + 50
                or self._bullet.x < -50
                or self._bullet.x > self._screen.get_width() + 50
            ):
                self._bullet = None  # Remove bullet if it goes off-screen

        self._speed = random.randint(2, 10)  # Randomize speed for more dynamic movement
        if self._right:
            self._x += self._speed
            self._image = self._image_right
            if self._x < plane.x and plane.y < self._y+50 and plane.y > self._y-50:
                self._insights = True
        else:
            self._x -= self._speed
            self._image = self._image_left
            lookahead_distance = -lookahead_distance
            if self._x > plane.x and plane.y < self._y+50 and plane.y > self._y-50:
                self._insights = True

        for a in aliens:
            if a is not self:
                if alien_rect.colliderect(
                    pygame.Rect(
                        self._x + lookahead_distance,
                        self._y,
                        self._image.get_width(),
                        self._image.get_height(),
                    )
                ):
                    if a.y < self._y and change_direction_chance:
                        self._y += self._speed
                        break
                    if a.y > self._y and change_direction_chance:
                        self._y -= self._speed
                        break

        for meteor in meteors:
            meteor_rect = meteor.asteroid.get_rect(topleft=(meteor.x, meteor.y))
            if meteor_rect.colliderect(alien_rect):
                self._image = self._explosion
                self._visible = False

            if meteor_rect.colliderect(
                pygame.Rect(
                    self._x + lookahead_distance,
                    self._y,
                    self._image.get_width(),
                    self._image.get_height(),
                )
            ):
                if meteor.y < self._y:
                    self._y += 1
                    break
                if meteor.y > self._y:
                    self._y -= 1
                    break
        if change_direction_chance and self._insights:
            if plane.y < self._y:
                self._y -= 1
            if plane.y > self._y:
                self._y += 1
