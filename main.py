"""Parallax Scrolling Example in Pygame
This code demonstrates how to create a parallax scrolling effect using multiple layers in Pygame.
"""

import pygame
import sys
import random
import os
from pygame import image
from pygame._camera_vidcapture import Camera
from pygame.locals import (  # pylint: disable=[E0611,W0611]
    QUIT,  # pylint: disable=[E0611,W0611]
    KEYDOWN,  # pylint: disable=[E0611,W0611]
    K_UP,  # pylint: disable=[E0611,W0611]
    K_DOWN,  # pylint: disable=[E0611,W0611]
    K_LEFT,  # pylint: disable=[E0611,W0611]
    K_RIGHT,  # pylint: disable=[E0611,W0611]
)

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from lib.camera import Camera  # pylint: disable=[E0611,W0611]
from lib.meteor import Meteor  # pylint: disable=[E0611,W0611]
from lib.pb import ParallaxBackground
from lib.parallaxlayer import ParallaxLayer
from lib.plane import Plane  # pylint: disable=[E0611,W0611]
from lib.map import Map


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

        self.background = None  # Will be initialized in run()

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
        self.camera = Camera(WIDTH)
        self.background = ParallaxBackground(
            [
                ParallaxLayer(self.layer1, 0.2),  # far
                ParallaxLayer(self.layer2, 0.5),  # mid
                ParallaxLayer(self.layer3, 1.0),  # foreground
            ]
        )

    def run(self):
        """Main game loop."""
        lastx = self.plane.world_x
        map_city = Map(self.screen)
        meteors = [
            Meteor(self.screen.get_width(), self.screen.get_height()) for _ in range(10)
        ]
        new_meteors= []
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Update positions

            # Draw layers (two copies each for looping)

            self.plane.move()
            self.camera.update(self.plane.world_x)
            self.background.draw(self.screen, self.camera.x)
            self._right = self.plane.direction
            # print(f"Plane direction: {'Right' if self._right else 'Left'}")
            self.screen.blit(self.plane.image, (self.plane.x, self.plane.y))
            if self.plane.fired_missle:
                self.plane.fired_missle.move()
                if self.plane.fired_missle.image:
                    self.screen.blit(
                        self.plane.fired_missle.image,
                        (self.plane.fired_missle.x(), self.plane.fired_missle.y()),
                    )
                else:
                    self.plane.fired_missle = (
                        None  # Remove missle if it goes off-screen
                    )
            for meteor in meteors:
                self.screen.blit(meteor.asteroid, (meteor.x, meteor.y))
                meteor.move(self.plane.world_x, lastx)
                if meteor.crash_check(self.plane):
                    self.plane.explode()
                    meteor.reset()
                if self.plane.fired_missle and self.plane.fired_missle.hit_check(meteor):
                    meteor.explode()
                    self.plane.fired_missle = None  # Remove missle after hit
                    if len(meteor.asteroids) >0:
                        new_meteors.append(meteor.asteroids.pop(0))  # Remove the first asteroid in the list
                        for new_meteor in new_meteors:
                            print(f"old meteor added at position: ({meteor.x}, {meteor.y})")
                            print(f"New meteor added at position: ({new_meteor.x}, {new_meteor.y})")
            meteors.extend(new_meteors)
            new_meteors.clear()  # Clear the list for the next frame
            if self.plane.exploding:
                self.plane.explode()  # Continue explosion animation

            map_city.draw(lastx, self.plane.world_x)

            lastx = self.plane.world_x
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
