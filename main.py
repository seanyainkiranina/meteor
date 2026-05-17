"""Parallax Scrolling Example in Pygame
This code demonstrates how to create a parallax scrolling effect using multiple layers in Pygame.
"""

import pygame
import sys
import random
import os
from pygame import image
from pygame._camera_vidcapture import Camera
from pygame.examples import aliens
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
from lib.startscreen import StartScreen
from lib.alien import Alien


class Game:
    """Main game class to handle the parallax scrolling effect."""

    def __init__(self):
        """Initialize the game and load resources."""

        pygame.init()
        self._reset = False
        # Window setup
        screen_width, screen_height = 800, 600
        self._screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 16)
        self.planet = 1
        # Load your layers (replace with your own images)
        self.layer1 = pygame.image.load(
            "backgrounds\\layer1.png"
        ).convert_alpha()  # far background
        self.layer2 = pygame.image.load(
            "backgrounds\\layer2.png"
        ).convert_alpha()  # mid background
        self.layer3 = pygame.image.load(
            f"backgrounds\\layer{self.planet}.png"
        ).convert_alpha()  # foreground

        # Parallax speeds
        self.speed1 = 1
        self.speed2 = 2
        self.speed3 = 4

        self._right = False

        self.background = None  # Will be initialized in run()
        self._aliens = []
        self._bullets = []
        # X positions for each layer (two copies for seamless looping)
        self.x1 = 0
        self.x2 = 0
        self.x3 = 0

        self.plane = Plane(
            screen_width // 2,
            screen_height // 2,
            5,
            screen_width,
            screen_height,
            "player\\plane_right.png",
            "player\\plane.png",
        )  # Player's plane
        for _ in range(random.randint(1, 5)):
            self._aliens.append(Alien(self._screen, self.plane))
        self.camera = Camera(screen_width)
        self.background = ParallaxBackground(
            [
                ParallaxLayer(self.layer1, 0.2),  # far
                ParallaxLayer(self.layer2, 0.5),  # mid
                ParallaxLayer(self.layer3, 1.0),  # foreground
            ]
        )

    @property
    def screen(self):
        """get screen"""
        return self._screen

    @screen.setter
    def screen(self, value):
        """set screen"""
        self._screen = value

    @property
    def number_aliens(self):
        """return number of aliens"""
        return round((3 + self.planet) // random.randint(1, 3), 0) + 1

    def softreset(self):
        """used to change worlds"""
        color_black = (0, 0, 0)
        self._screen.fill(color_black)
        self.speed1 = 1
        self.speed2 = 2
        self.speed3 = 4
        screen_width, screen_height = 800, 600
        self._bullets.clear()
        self.background = None  # Will be initialized in run()
        self._aliens = []
        for _ in range(random.randint(1, self.number_aliens)):
            self._aliens.append(Alien(self._screen, self.plane))

        # X positions for each layer (two copies for seamless looping)
        self.x1 = 0
        self.x2 = 0
        self.x3 = 0
        self.camera = Camera(screen_width)
        self.background = ParallaxBackground(
            [
                ParallaxLayer(self.layer1, 0.2),  # far
                ParallaxLayer(self.layer2, 0.5),  # mid
                ParallaxLayer(self.layer3, 1.0),  # foreground
            ]
        )

    def reset(self):
        """restart game"""
        color_black = (0, 0, 0)
        self._screen.fill(color_black)
        self.speed1 = 1
        self.speed2 = 2
        self.speed3 = 4
        screen_width, screen_height = 800, 600
        self._bullets.clear()
        self._right = False

        self.background = None  # Will be initialized in run()
        self._aliens = []
        for _ in range(random.randint(1, self.number_aliens)):
            self._aliens.append(Alien(self._screen, self.plane))

        # X positions for each layer (two copies for seamless looping)
        self.x1 = 0
        self.x2 = 0
        self.x3 = 0
        self.plane = Plane(
            screen_width // 2,
            screen_height // 2,
            5,
            screen_width,
            screen_height,
            "player\\plane_right.png",
            "player\\plane.png",
        )  # Player's plane
        self.camera = Camera(screen_width)
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
        map_city = Map(self._screen)
        meteors = [
            Meteor(
                self._screen.get_width(), self._screen.get_height(), self.plane.world_x
            )
            for _ in range(5)
        ]
        new_meteors = []
        loop = 0
        running = True
        self._bullets = []
        bullets_to_remove = []
        bullet = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.K_ESCAPE:
                    running = False

            # Update positions
            if self.plane.y==0:
                if self.plane.carrying_person:
                    self.plane.add_score(200)
                    self.plane.carrying_person = False
            # Draw layers (two copies each for looping)
            if self.plane.lives <= 0:
                running = False
            self.plane.move()
            self.camera.update(self.plane.world_x)
            if self.background is not None:
                self.background.draw(self._screen, self.camera.x)
            self._right = self.plane.direction
            # print(f"Plane direction: {'Right' if self._right else 'Left'}")
            self._screen.blit(self.plane.image, (self.plane.x, self.plane.y))
            if self.plane.fired_missle:
                self.plane.fired_missle.move()
                if self.plane.fired_missle.image:
                    self._screen.blit(
                        self.plane.fired_missle.image,
                        (self.plane.fired_missle.x(), self.plane.fired_missle.y()),
                    )
                else:
                    self.plane.fired_missle = (
                        None  # Remove missle if it goes off-screen
                    )
            # Move meteor randomly to avoid overlap
            if random.randint(0, 100) % 20 == 0 and len(meteors) < (self.number_aliens):
                for _ in range(random.randint(0, self.number_aliens)):
                    meteors.append(
                        Meteor(
                            self._screen.get_width(),
                            self._screen.get_height(),
                            self.plane.world_x,
                        )
                    )
                if len(self._aliens) < (self.number_aliens):
                    for _ in range(random.randint(0, 1)):
                        self._aliens.append(Alien(self._screen, self.plane))
            loop = 0
            for alien in self._aliens:
                if alien is not None:
                    bullet = alien.move(
                        meteors, self.plane, self._aliens, self.plane.fired_missle
                    )
                    if bullet is not None and bullet.image is not None:
                        self._bullets.append(bullet)
                    self._screen.blit(alien.image, (alien.x, alien.y))
                    if alien.x < -3000 or alien.x > 3000:
                        self._aliens.remove(alien)
                        self._aliens.append(Alien(self._screen, self.plane))
            for b in self._bullets:
                if b is not None and b.image is not None:
                    self._screen.blit(b.image, (b.x, b.y))
                    b.move(self.plane)
                else:
                    bullets_to_remove.append(b)

            for b in bullets_to_remove:
                if b in self._bullets:
                    self._bullets.remove(b)

            bullets_to_remove.clear()  # Clear the list for the next frame

            for meteor in meteors:
                if self.plane.using_smart_bombs:
                    meteor.explode()

                if loop % 5 == 0:
                    for mm in meteors:
                        if mm == meteor:
                            continue
                        if mm != meteor and mm.asteroid and meteor.asteroid:
                            m_rect = mm.asteroid.get_rect(topleft=(mm.x, mm.y))
                            mm_rect = meteor.asteroid.get_rect(
                                topleft=(meteor.x, meteor.y)
                            )
                            if m_rect.colliderect(mm_rect):
                                mm.explode()

                self._screen.blit(meteor.asteroid, (meteor.x, meteor.y))
                if loop % 20 == 0:
                    map_city.people.reborn()
                meteor.move(self.plane)
                if map_city.city.hit_meteor_check(meteor):
                    self.plane.add_score(-100 * self.number_aliens)
                if meteor.crash_check(self.plane, True):
                    self.plane.explode()
                    meteor.reset()
                if meteor.crash_check(self.plane, False):
                    meteor.explode()
                    self.plane.add_score(3 * self.number_aliens)
                    self.plane.hit_on_shield()
                if self.plane.fired_missle and self.plane.fired_missle.hit_check(
                    meteor
                ):
                    meteor.explode()
                    self.plane.add_score(10 * self.number_aliens)
                    self.plane.fired_missle = None  # Remove missle after hit
                    if len(meteor.asteroids) > 0:
                        new_meteors.append(
                            meteor.asteroids.pop(0)
                        )  # Remove the first asteroid in the list

            meteors.extend(new_meteors)
            new_meteors.clear()  # Clear the list for the next frame
            for meteor in meteors:
                if map_city.ptarget_shown:
                    if map_city.people.impact_check(meteor):
                        self.plane.add_score(-200)
                if meteor.y > self._screen.get_height():
                    new_meteors.append(meteor)

            for new_meteor in new_meteors:
                if new_meteor in meteors:
                    meteors.remove(new_meteor)

            new_meteors.clear()  # Clear the list for the next frame

            if self.plane.exploding:
                self.plane.explode()  # Continue explosion animation

            if loop % 20 == 0:
                self.plane.used_smart_bombs()  # Reset smart bomb usage status
            map_city.draw(self.plane.world_x, lastx)
            if map_city.ptarget_shown:
                if map_city.people.crash_check(self.plane):
                    self.plane.add_score(100)
                    self.plane.carrying_person = True
            if map_city.starget_shown:
                if map_city.stargate.crash_check(self.plane):
                    self.planet += 1
                    if self.planet > 10:
                        self.planet = 1
                    self.layer3 = pygame.image.load(
                        f"backgrounds\\layer{self.planet}.png"
                    ).convert_alpha()
                    self.softreset()  # foreground
                    self.plane.teleport()

            if (
                map_city.diamond is not None
                and map_city.diamond.hit is False
                and map_city.diamond.image is not None
            ):
                self._screen.blit(
                    map_city.diamond.image,
                    (map_city.diamond.x, map_city.diamond.y),
                )
                map_city.diamond.move()
                if self.plane is not None and self.plane.image is not None:
                    if map_city.diamond.hit_player_check(self.plane):
                        self.plane.add_shield(100)
                        map_city.diamond.hit = True
                        map_city.diamond.y = 600
                        map_city.diamond = None

            lastx = self.plane.world_x
            score_text = (
                f"SmartBombs:{self.plane.smart_bombs} Shield:{self.plane.shield_time} "
            )
            score_text += f"Score:{self.plane.score} Lives:{self.plane.lives} "
            score_text += f"Meteors:{len(meteors)} "
            score_text += f"Aliens:{len(self._aliens)} Planet:{self.planet}"
            self._screen.blit(
                self.font.render(score_text, True, (255, 255, 0)), (10, 10)
            )

            pygame.display.flip()

            self.clock.tick(60)
            self.plane.resetting = (
                False  # Reset the plane's resetting status after handling it
            )
            loop += 1
        return self.plane.score


if __name__ == "__main__":
    game = Game()
    startup = StartScreen(game.screen)
    startup.high_score = 0
    while startup.display(game.screen) is True:
        pygame.event.clear()
        pygame.event.clear(KEYDOWN)
        game.reset()
        startup.high_score = game.run()
        pygame.event.clear(KEYDOWN)
        pygame.event.clear()
    pygame.display.quit()
    pygame.quit()
    sys.exit()
