"""Mutant class for the Meteor game."""

import random
import pygame

from lib.meteor import Meteor  # pylint: disable=[E0611,W0611]
from lib.bullet import Bullet  # pylint: disable=[E0611,W0611]
from lib.laserbeam import LaserBeam  # pylint: disable=[E0611,W0611]
# from lib.people import People


class Mutant:
    """Mutant class represents an Mutant that moves across the screen and can fire bullets at the player's plane."""

    def __init__(self, screen, plane,planet):
        filenames = ["mutant.png","defender_mutant.png"]
        filename = random.choice(filenames)
        self._screen = screen
        self._speed = 3
        self._planet = planet
        self._hunting = False
        self._bullet = None
        self._right = False
        self._insights = False
        self._visible = True
        self._speed = random.randint(2, 10)
        self._image_left = pygame.image.load(f"player\\{filename}").convert_alpha()
        self._image_right = pygame.image.load(f"player\\{filename}").convert_alpha()
        self._explosion = pygame.image.load(
            "player\\alien_explosion.png"
        ).convert_alpha()
        self._explosion_frames = 6
        self._person = None
        self._carrying_person = False

        # Random start direction and world position
        if random.randint(0, 100) % 2 == 0:
            self._right = True
            self._world_x = -20 + plane.world_x
            self._image = self._image_right
        else:
            self._world_x = 20 + plane.world_x
            self._image = self._image_left

        self._y = self._image.get_height() +2
        self._x = self._world_x  # initial screen projection
  
    @property
    def visible(self):
        """Get if Mutant is visible"""
        return self._visible
  
    @property
    def target(self):
        """Get target"""
        return self._person

    @target.setter
    def target(self, value):
        """set target"""
        self._person = value

    @property
    def world_x(self):
        """get world x"""
        return self._world_x

    @property
    def hunting(self):
        """return if hunting"""
        return self._hunting

    @hunting.setter
    def hunting(self, value):
        """Hunting for people"""
        self._hunting = value

    @property
    def x(self):
        """Get the current x position of the Mutant."""
        return self._x

    @property
    def y(self):
        """Get the current y position of the Mutant."""
        return self._y

    @property
    def image(self):
        """Get the current image of the Mutant."""
        return self._image

    @property
    def bullet(self):
        """Get the current bullet of the Mutant."""
        return self._bullet

    @bullet.setter
    def bullet(self, value):
        """Set the bullet of the Mutant."""
        self._bullet = value

    def move(self, meteors, plane, Mutants, missle, lasers):
        """Move the Mutant using world coordinates."""
        lookahead_distance = 100
        plane_rect = plane.image.get_rect(topleft=(plane.x, plane.y))
        mutant_rect = self._image.get_rect(topleft=(self._x, self._y))
        change_direction_chance = (
            random.randint(0, 100) < 1
        )  # 4% chance to change direction
        # Fire logic and collisions use world coordinates
        fire = random.randint(0, 100) < 50

        # Convert world position to screen position
        self._x = self._world_x - plane.world_x + self._screen.get_width() // 2

        # Skip drawing if off-screen
        if (
            self._x < -self._image.get_width()
            or self._x > self._screen.get_width() + self._image.get_width()
        ):
            return

        if len(lasers)>0:
            for l in lasers[:]:
                if l.hit(mutant_rect):
                    self._image = self._explosion
                    self._visible = False
                    plane.add_score(200 * self._planet)
                    return


        if plane.using_smart_bombs:
            # Check if the Mutant is within the smart bomb's blast radius
            smart_bomb_radius = 200  # Example radius for the smart bomb
            distance_to_mutant = (
                (self._x - plane.x) ** 2 + (self._y - plane.y) ** 2
            ) ** 0.5
            if distance_to_mutant <= smart_bomb_radius:
                self._image = self._explosion
                self._visible = False
                plane.add_score(
                    200 * self._planet
                )  # Award points for hitting the Mutant with a smart bomb
                return

        if plane_rect.colliderect(mutant_rect) and self._visible:
            if plane.shield_on:
                plane.hit_on_shield()  # Reduce shield time instead of lives
                self._image = self._explosion
                self._visible = False
                plane.add_score(
                    100 * self._planet
                )  # Award points for hitting the Mutant with the shield on
                return
            plane.explode()
            self._image = self._explosion
            self._visible = False
            return

        if change_direction_chance and self._right:
            self._right = False
        else:
            if change_direction_chance and not self._right:
                self._right = True

        # Fire logic and collisions use world coordinates

        # Movement in world space
        if self._right:
            self._world_x += self._speed
            self._image = self._image_right
            if abs(plane.x - self._x) < 200 and plane.invisible is False:
                self._insights = True
        else:
            self._world_x -= self._speed
            self._image = self._image_left
            if abs(plane.x - self._x) < 200 and plane.invisible is False:
                self._insights = True


        # Bullet creation uses world coordinates
        if fire and self._bullet is None and self._insights:
            self._bullet = Bullet(
                self._screen,
                self._x,
                self._y + self._image.get_height() // 2,
            )
            self._bullet.firing_up_down = True
            if self._bullet is not None:
                if self._bullet.image is not None:
                    self._bullet.fire(plane)
                    return self._bullet

        if self._bullet is not None and self._bullet.image is None:
            self._bullet = None  # Remove bullet if it goes off-screen


        if len(missle)>0:
            for m in missle:
                if m is None or m.image is None:
                    continue
                missle_rect = m.image.get_rect(topleft=(m.x(), m.y()))
                if missle_rect.colliderect(mutant_rect):
                    self._image = self._explosion
                    self._visible = False
                    plane.add_score(200 * self._planet)
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
                self._x = -3000
                self._right = True
            else:
                self._x = self._screen.get_width() + 3000
                self._right = False
            self._image = self._image_right if self._right else self._image_left
            self._bullet = None
            self._explosion_frames = 6
            self._insights = False
            self._visible = True
            return

        #    if self._visible is False:
        #        return

        if self._bullet is not None and plane.resetting is True:
            self._bullet = None  # Remove bullet after hitting the plane

        self._speed = random.randint(2, 10)  # Randomize speed for more dynamic movement
        if self._right:
            self._x += self._speed
            self._image = self._image_right
            if self._x < plane.x and plane.y < self._y + 100 and plane.y > self._y - 100:
                self._insights = True
        else:
            self._x -= self._speed
            self._image = self._image_left
            lookahead_distance = -lookahead_distance
            if (
                self._x > plane.x
                and plane.y < self._y + 50
                and plane.y > self._y - 50
            ):
                self._insights = True

        if self._y < plane.y:
            self._y += self._speed

        if self._y > plane.y:
            self._y -= self._speed


        for meteor in meteors:
            meteor_rect = meteor.asteroid.get_rect(topleft=(meteor.x, meteor.y))
            if meteor_rect.colliderect(mutant_rect):
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
                if (
                    meteor.y < self._y
                    and change_direction_chance
                ):
                    self._y += self._speed
                    break
                if (
                    meteor.y > self._y
                    and change_direction_chance
                ):
                    self._y -= self._speed
                    break
        if change_direction_chance and self._insights:
            if plane.y < self._y:
                self._y -= self._speed
            if plane.y > self._y:
                self._y += self._speed

        # Draw Mutant
        if self._visible:
            self._screen.blit(self._image, (self._x, self._y))

        return None
