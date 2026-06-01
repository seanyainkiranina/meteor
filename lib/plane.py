"""Plane class for the parallax scrolling game."""

import random
import time
import pygame
from lib.missle import Missle
from lib.laserbeam import LaserBeam


class Plane:
    """Class representing the player's plane in the parallax scrolling game."""

    def __init__(self, x, y, speed, width, height, filename, filename_right):
        self._x = x
        self._y = y
        self._saved_speed = speed
        self._smart_bombs = 3
        self._using_smart_bombs = False
        self._counter = 0
        self._carrying_person = False
        self._step = 0
        self._game_over = False
        self._score = 0
        self._free_guy = 50000
        self._free_energy = 1000
        self._lives = 3
        self._jumped = False
        self._shield_on = False
        self._world_x = x  # new: world position
        self._speed = speed  # Speed at which the plane moves
        self._width = width
        self._height = height
        self._inverse = False
        self._last = None
        self._last_laser_y = -1
        self._shield_time = 1000
        self._right = True  # Direction the plane is facing
        self._image_left = pygame.image.load(filename).convert_alpha()
        self._shield_left = pygame.image.load(
            "player\\shield_plane.png"
        ).convert_alpha()
        self._shield_right = pygame.image.load(
            "player\\shield_plane_right.png"
        ).convert_alpha()

        self._invisible_right = pygame.image.load(
            "player\\plane_inverse.png"
        ).convert_alpha()
        self._invisible = pygame.image.load(
            "player\\plane_right_inverse.png"
        ).convert_alpha()

        self._org_width, self._org_height = self._image_left.get_size()
        self._scale_factor = 4.0  # 2x bigger
        self._image_right = pygame.image.load(
            filename_right
        ).convert_alpha()  # Pygame surface for the plane facing right
        self._image_right_person = pygame.image.load(
            "player\\plane_right_person.png"
        ).convert_alpha()
        self._image_person = pygame.image.load(
            "player\\plane_person.png"
        ).convert_alpha()
        self._image = self._image_right  # Pygame surface for the plane
        self._missle = None  # Missle object representing the plane's missle
        self._missles = []
        self._explosions = []  # List to hold explosion objects when the plane is hit
        for x in range(1, 7):
            self._explosions.append(
                pygame.image.load(f"player\\explosions\\{x}.png").convert_alpha()
            )
        self._exploding = False  # Flag to indicate if the plane is currently exploding
        self._explosion_frame = 0
        self._reset = False
        self._display_map = False

    @property
    def invisible(self):
        """get inverse"""
        return self._inverse

    @property
    def inverse(self):
        """get inverse"""
        return self._inverse

    @inverse.setter
    def inverse(self, value):
        """set inverse"""
        self._inverse = value

    @property
    def display_map(self):
        """get display map"""
        return self._display_map

    def fire_laser(self, lasers):
        """fire a laser"""
        direction = 1
        if self._shield_time < 20:
            return
        half_plane = self._image.get_width() * direction
        if self._shield_on:
            return
        if self._exploding:
            lasers.clear()
            return
        if len(lasers) > 2:
            return
        if self._last_laser_y > -1 and self._last_laser_y != self.y and len(lasers) > 0:
            return
        self._shield_time -= 20
        self._last_laser_y = self.y

        if self._right:
            direction = -1
            half_plane = 0

        nose_y = self.y + self._image.get_height() // 2
        nose_x = self.x + half_plane
        lasers.append(LaserBeam(nose_x, nose_y, direction))

    @property
    def step(self):
        """ get step"""
        return self._step
    @step.setter
    def step(self,value):
        """ set step"""
        self._step = value

    @property
    def carrying_person(self):
        """get carrying person"""
        return self._carrying_person

    @carrying_person.setter
    def carrying_person(self, value):
        """set carrying person"""
        self._carrying_person = value

    @property
    def counter(self):
        """Get the counter value."""
        return self._counter

    @property
    def resetting(self):
        """Check if the plane needs to be reset after an explosion."""
        return self._reset

    @resetting.setter
    def resetting(self, value):
        """Set the resetting status of the plane."""
        self._reset = value

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
        return self._missles

    def remove_missles(self):
        """remove missles"""
        if isinstance(self._missles, list) is False:
            self._missles = []

        if len(self._missles) == 0:
            return
        self._missles = [
            m
            for m in self._missles
            if m is not None and getattr(m, "image", None) is not None
        ]

    @property
    def smart_bombs(self):
        """Get the number of smart bombs available."""
        return self._smart_bombs

    @property
    def using_smart_bombs(self):
        """Check if a smart bomb is being used."""
        return self._using_smart_bombs

    def used_smart_bombs(self):
        """Reset the smart bomb usage status."""
        self._using_smart_bombs = False

    def reset_missle(self):
        """Reset the missle to None."""
        self._missle = None

    def hit_on_shield(self):
        """hit on shield"""
        self._shield_time -= 10

    def add_score(self, amount):
        """Add score"""
        if self._step < (self._score + amount):
            amt = amount
            if amount > self._free_energy and self._shield_on is False:
                self._shield_time += (round((amount) / self._free_energy)) * 10
                amt -= round((amount) / self._free_energy) * self._free_energy
            if self._score + amt > self._free_energy:
                self._shield_time += 10
        if self._step < (self._score + amount):
            amt = amount
            if amount > self._free_guy:
                self._lives += round((amount) / self._free_guy)
                amt -= round((amount) / self._free_guy) * self._free_guy
            if self._score + amt > self._free_guy:
                self._lives += 1
        self._score += amount
        if amount>0:
            self._step = self._score

    def add_shield(self, amount):
        """Add shield"""
        self._shield_time += amount

    @property
    def speed(self):
        """Speed the plane is flying."""
        return self._speed

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
        self._reset = True
        self._lives -= 1
        self._x = self._width // 2 - self._image.get_width() // 2
        self._y = self._height // 2 - self._image.get_height() // 2
        self._world_x = self._x
        self._right = True
        self._counter = 0
        self._jumped = False
        self._shield_on = False
        self._scale_factor = 1.0
        self._carrying_person = False
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
        self._inverse = False
        self._missles = []
        if self._lives <= 0:
            self._game_over = True

    def explode(self):
        """Trigger the explosion animation for the plane."""
        if self.shield_on:
            self.hit_on_shield()  # Reduce shield time instead of lives
            return
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

    def teleport(self):
        """Jump the plane"""
        self._y = random.randint(
            self._image.get_height(), 600 - self._image.get_height()
        )
        self._world_x = random.randint(
            self._world_x - self._width - 3000, self._world_x + self._width + 30000
        )

    def move(self, lasers):
        """Move the plane to the left by its speed."""
        keys = pygame.key.get_pressed()
        self._counter += 1
        if self._counter > 50:
            self._counter = 0
            if self._jumped:
                self._jumped = False

        if keys[pygame.K_q] and self._jumped is False:
            if (
                self._shield_time > 0
                and self._carrying_person is False
                and self._shield_on is False
            ):
                if self._inverse is True:
                    self._inverse = False
                else:
                    self._inverse = True
            self._jumped = True

        if keys[pygame.K_m] and self._jumped is False:
            if self._display_map is True:
                self._display_map = False
            else:
                self._display_map = True
            self._jumped = True

        if keys[pygame.K_ESCAPE]:
            self.geme_over = True

        if keys[pygame.K_d]:
            if self._shield_on:
                self._y += self._shield_left.get_height() // 2
            self._shield_on = False

        if keys[pygame.K_z]:
            self.fire_laser(lasers)

        if keys[pygame.K_s]:
            if (
                self._shield_time > 0
                and self._carrying_person is False
                and self._inverse is False
            ):
                if not self._shield_on:
                    self._y -= self._shield_left.get_height() // 2
                self._shield_on = True

        if keys[pygame.K_a] and not self._jumped:
            if self._smart_bombs > 0 and not self._using_smart_bombs:
                self._smart_bombs -= 1
                self._jumped = True
                # print(f"Smart bombs left: {self._smart_bombs}")
                self._using_smart_bombs = True

        if self._exploding:
            self._shield_on = False
        if keys[pygame.K_ESCAPE]:
            self._lives = 0
            self.explode()

        if keys[pygame.K_g] and self._jumped is False and not self._exploding:
            self._jumped = True
            self._y = random.randint(
                self._image.get_height(), 600 - self._image.get_height()
            )
            self._world_x = random.randint(
                self._world_x - self._width, self._world_x + self._width
            )

        if keys[pygame.K_UP] and not self._exploding:
            self._y -= self._speed
        if keys[pygame.K_DOWN] and not self._exploding:
            self._y += self._speed
        if keys[pygame.K_LEFT] and not self._exploding:
            self._world_x -= self._speed
        if keys[pygame.K_RIGHT] and not self._exploding:
            self._world_x += self._speed

        if self._world_x < -12000:
            self._world_x = 12000
        if self._world_x > 12000:
            self._world_x = -12000

        if (
            keys[pygame.K_f]
            and not self._exploding
            and self._missle is None
            and not self._jumped
        ):
            self._jumped = True
            if self._speed == 20:
                self._speed = self._saved_speed
            else:
                self._saved_speed = self._speed
                self._speed = 20

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
            if len(self._missles) > 2:
                return
            fired_rocket_x = (self._image.get_width() // 2)
            if self._right:
                fired_rocket_x = 0  
            self._missle = Missle(
                self._x + fired_rocket_x,
                self._y,
                self._width,
                self._height,
                "player\\missle.png",
                "player\\missle_right.png",
            )
            if len(self._missles) == 0 and self._y>100:
                self._missle.up = True
            if len(self._missles) == 1 and self.y<700:
                self._missle.up = False
                self._missle.down = True


            self._missle.direction = self._right
            if self._missles is None:
                self._missles = []
            self._missles.append(self._missle)  # type: ignore
            self._missle = None  # Set missle direction to match plane
        self._x = self._width // 2 - self._image.get_width() // 2
        self._y = max(0, min(self._height - self._image.get_height(), self._y))

        if self._right and self._exploding is False:
            self._world_x -= self._speed
        if self._right is False and self._exploding is False:
            self._world_x += self._speed

        if self._inverse:
            self._shield_time -= 1
            if self._shield_time <= 0:
                self._inverse = False

        if self._shield_on:
            self._shield_time -= 1
            if self._shield_time <= 0:
                self._y += self._shield_left.get_height() // 2
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
                    if self._carrying_person:
                        self._image = self._image_right_person
                    else:
                        self._image = self._image_right

                if not self._right:
                    if self._carrying_person:
                        self._image = self._image_person
                    else:
                        self._image = self._image_left

                if self.inverse:
                    if not self._right:
                        self._image = self._invisible
                    else:
                        self._image = self._invisible_right
