"""Parallax Scrolling Example in Pygame
This code demonstrates how to create a parallax scrolling effect using multiple layers in Pygame.
"""

import pygame
import sys
import random
import os
from pygame.locals import (  # pylint: disable=[E0611,W0611]
    QUIT,  # pylint: disable=[E0611,W0611]
    KEYDOWN,  # pylint: disable=[E0611,W0611]
    K_UP,  # pylint: disable=[E0611,W0611]
    K_DOWN,  # pylint: disable=[E0611,W0611]
    K_LEFT,  # pylint: disable=[E0611,W0611]
    K_RIGHT,  # pylint: disable=[E0611,W0611]
)

from lib.meteor import Meteor  # pylint: disable=[E0611,W0611]
from lib.plane import Plane  # pylint: disable=[E0611,W0611]

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))


class Game:
    """Main game class to handle the parallax scrolling effect."""

    def __init__(self):
        """Initialize the game and load resources."""

        pygame.init()

        # Window setup
        WIDTH, HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # Load your layers (replace with your own images)
        self.layer1 = pygame.image.load(
            "backgrounds\\layer1.png"
        ).convert_alpha()  # far background
        self.layer2 = pygame.image.load(
            "backgrounds\\layer2.png"
        ).convert_alpha()  # mid background
        self.layer3 = pygame.image.load(
            "backgrounds\\layer3.png"
        ).convert_alpha()  # foreground

        # Parallax speeds
        self.speed1 = 1
        self.speed2 = 2
        self.speed3 = 4

        self._right = False

        # X positions for each layer (two copies for seamless looping)
        self.x1 = 0
        self.x2 = 0
        self.x3 = 0
        self.plane = Plane(
            WIDTH // 2,
            HEIGHT // 2,
            5,
            WIDTH,
            HEIGHT,
            "player\\plane_right.png",
            "player\\plane.png",
        )  # Player's plane

    def scroll_layer(self, image, x, speed, right=True):
        """Scroll a layer and return updated x."""
        if right:
            x -= speed
        else:
            x += speed
        if right and x <= -image.get_width():
            x = 0
        if not right and x >= image.get_width():
            x = 0
        return x

    def run(self):
        """Main game loop."""
        x_far = x_mid = x_fore = 0
        meteors = [Meteor(self.screen.get_width(), self.screen.get_height()) for _ in range(5)]
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            x_far = self.scroll_layer(self.layer1, x_far, self.speed1, self._right)
            x_mid = self.scroll_layer(self.layer2, x_mid, self.speed2, self._right)
            x_fore = self.scroll_layer(self.layer3, x_fore, self.speed3, self._right)
            # Update positions

            # Draw layers (two copies each for looping)
            self.screen.blit(self.layer1, (self.x1, 0))
            xdifference1 = self.layer1.get_width()
            xdifference2 = self.layer2.get_width()
            xdifference3 = self.layer3.get_width()

            if not self._right:
                xdifference1 = -xdifference1
                xdifference2 = -xdifference2
                xdifference3 = -xdifference3

            self.screen.blit(self.layer1, (x_far + xdifference1, 0))
            self.screen.blit(self.layer1, (x_far, 0))
            self.screen.blit(self.layer2, (x_mid + xdifference2, 0))
            self.screen.blit(self.layer2, (x_mid, 0))
            self.screen.blit(self.layer3, (x_fore + xdifference3, 0))
            self.screen.blit(self.layer3, (x_fore, 0))
            self.plane.move()
            self._right = self.plane.direction
            self.screen.blit(self.plane.image, (self.plane.x, self.plane.y))
            if self.plane.fired_missle:
                self.plane.fired_missle.move("right" if self._right else "left")
                if self.plane.fired_missle.image:
                    self.screen.blit(
                        self.plane.fired_missle.image,
                        (self.plane.fired_missle.x(), self.plane.fired_missle.y()),
                    )
                else:
                    self.plane.fired_missle = None  # Remove missle if it goes off-screen
            for meteor in meteors:
                self.screen.blit(meteor.asteroid, (meteor.x, meteor.y))
                meteor.move()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
