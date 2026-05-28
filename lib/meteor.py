"""Meteor class for the Meteor game."""

import time
import re
import random
import pygame


class Meteor:
    """Class representing the main game logic for the Meteor game."""

    def __init__(self, width, height, world_x=0, planet=1,prefix=None, x=None, y=None):
        self._asteroids = []
        self._planet = planet
        self._speed =  random.randint(1, self._planet +3)
        if x is None or y is None:
            self._x = random.randint(0, width)
            self._y = random.randint(-2000, -200)  # Start above the screen
        else:
            self._x = x
            self._y = y
        self._world_x = self.screen_to_world_x(self._x, world_x, width)
        self._width = width
        self._height = height
        self.rotation_speed = random.randint(
            1, 20
        )  # Random rotation speed for the meteor
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
            "K1",
            "K2",
            "K3",
            "K4",
            "K5",
            "L1_"
        ]
        self._prefix = random.choice(self._prefixs)
        if self._prefix[0] == "K":
            self._speed = random.randint(self._planet,self._planet+5)
        self._id = self._prefix + str(
            random.randint(1, 1000000)
        )  # Unique ID for the meteor

        if prefix is not None:
            self._asteroid = pygame.image.load(
                f"images\\rot\\{prefix}.png"
            ).convert_alpha()
        else:
            if  self.prefix[0] != "K":
                self._asteroid = pygame.image.load(
                    f"images\\rot\\{self._prefix}0.png"
                ).convert_alpha()
            else:
                self._asteroid = pygame.image.load(
                    f"images\\{self._prefix}.png"
                ).convert_alpha()
        self._r = 0

    def screen_to_world_x(self, screen_x, camera_x, screen_width):
        """Convert screen x coordinate to world x coordinate based on camera position and screen width."""
        return screen_x + camera_x - screen_width // 2
    @property
    def world_x(self):
        """ get world x"""
        return self._world_x

    @property
    def id(self):
        """Get the unique ID of the meteor."""
        return self._id

    @property
    def asteroid(self):
        """Get the asteroid's image."""

        if self.rotation_speed % 50 == 0:
            self._r += 1
            if self._r > 360:
                self._r = 0
            if self.prefix[0] !="K":
                self._asteroid = pygame.image.load(
                    f"images\\rot\\{self._prefix}{self._r}.png"
                ).convert_alpha()
            else:
                self._asteroid = pygame.image.load(
                    f"images\\{self._prefix}.png"
                ).convert_alpha()

        self.rotation_speed -= 1
        if self.rotation_speed < 0:
            self.rotation_speed = random.randint(1, 100)
        return self._asteroid

    @property
    def x(self):
        """Get the current x position of the asteroid."""
        return self._x

    @x.setter
    def x(self, value):
        """Set the x position of the asteroid."""
        self._x = value

    @property
    def y(self):
        """Get the current y position of the asteroid."""
        return self._y

    @y.setter
    def y(self, value):
        """Set the y position of the asteroid."""
        self._y = value

    @property
    def asteroids(self):
        """Get the asteroids."""
        return self._asteroids

    @property
    def prefix(self):
        """Get the current prefix of the asteroid."""
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        """Set the prefix of the asteroid."""
        self._prefix = value

    def explode(self):
        """Trigger the explosion animation for the asteroid."""
        self._asteroid = self.next()  # Get the next explosion frame

    def next(self):
        """Get the next image for the asteroid's animation."""
        next_step = "X"
        last_width = self.asteroid.get_width()
        last_height = self.asteroid.get_height()
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
        if newprefix in self._prefixs:
            self.prefix = next_step + self.prefix[1:]
            if self.prefix[0] !="K":
                self._asteroid = pygame.image.load(
                    f"images\\rot\\{self._prefix}{self._r}.png"
                ).convert_alpha()
            if (
                last_width < self.asteroid.get_width()
                or last_height < self.asteroid.get_height()
            ):
                self._asteroid = pygame.transform.scale(
                    self.asteroid,
                    (
                        int(last_width * 0.75),
                        int(last_height * 0.75),
                    ),
                )
            self.new_direction(f"{self._prefix}{self._r}")
        else:
            self._asteroid = pygame.image.load("images\\explode.png").convert_alpha()
            self.reset()  # Mark for removal if explosion is complete
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

    def collide(self, other):
        """Check for collision with another meteor."""
        rect1 = self.asteroid.get_rect(topleft=(self.x, self.y))
        rect2 = other.asteroid.get_rect(topleft=(other.x, other.y))
        return rect1.colliderect(rect2)

    def bounce(self, other):
        """Bounce off another meteor by swapping their velocities."""
        # Simple bounce logic: swap x and y positions
        self.x += random.randint(1, 5)  # Add some randomness to the bounce
        other.x += random.randint(-5, 1)

    def move(self, plane, rotate=False):
        """Move the asteroid downwards."""

        self._y += self._speed  # Move down by a random speed
        # Convert world → screen for drawing
        self._x = self._world_x - plane.world_x + self._width // 2
        if self._y > self._height:
            if not rotate:
                self._prefix = random.choice(self._prefixs)
        #    self._x = random.randint(0, self._width)  # Reset to a new random x position

    def crash_check(self, plane, handle_shield_hit=False):
        """Check for collision with the player's plane."""
        if plane.shield_on and handle_shield_hit:
            return False  # No collision if the shield is on
        plane_rect = plane.image.get_rect(topleft=(plane.x, plane.y))
        meteor_rect = self.asteroid.get_rect(topleft=(self.x, self.y))
        return plane_rect.colliderect(meteor_rect)

    def new_direction(self, file_name):
        """Change the direction of the meteor."""
        start_y = self._y - self._asteroid.get_height()
        end_y = self._y + self._asteroid.get_height()
        if start_y == 0:
            return
        array_y = [start_y, end_y]
        new_x = self._x + random.randint(-4, 4)
        self._asteroids.append(
            Meteor(
                self._width,
                self._height,
                self._world_x + random.randint(-4, 4),
                self._planet,
                file_name,
                new_x,
                random.choice(array_y),
            )
        )
        # Move in a random direction

    def reset(self):
        """Reset the meteor's position and prefix."""
        self._prefix = random.choice(self._prefixs)
        self._x = random.randint(0, self._width)  # Reset to a new random x position
        self._y = random.randint(-2000, -200)  # Reset to start above the screen
