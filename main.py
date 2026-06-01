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
from lib.mutant import Mutant
from lib.minimap import MiniMap
from lib.laserbeam import LaserBeam


class Game:
    """Main game class to handle the parallax scrolling effect."""

    def __init__(self):
        """Initialize the game and load resources."""

        pygame.init()
        self._reset = False
        # Window setup
        screen_width, screen_height = 800, 600
        self.screen = pygame.display.set_mode((screen_width, screen_height))
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
        self.camera = None
        # Parallax speeds
        self.speed1 = 1
        self.speed2 = 2
        self.speed3 = 4
        self.map_city = None

        self.displaying_map = False

        self._right = False

        self.background = None  # Will be initialized in run()
        self.aliens = []
        self.bullets = []
        self.mutants = []
        self.lasers = []
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
            self.aliens.append(Alien(self.screen, self.plane, self.planet))
        self.background = ParallaxBackground(
            [
                ParallaxLayer(self.layer1, 0.2),  # far
                ParallaxLayer(self.layer2, 0.5),  # mid
                ParallaxLayer(self.layer3, 1.0),  # foreground
            ]
        )

    @property
    def number_aliens(self):
        """return number of aliens"""
        i_max = round((3 + self.planet) // random.randint(1, 3), 0) + 1
        if i_max >= 10:
            i_max = 10
        return i_max

    def softreset(self):
        """used to change worlds"""
        color_black = (0, 0, 0)
        self.screen.fill(color_black)
        self.speed1 = 1
        self.speed2 = 2
        self.speed3 = 4
        screen_width = 800
        self.bullets.clear()
        self.lasers.clear()
        self.background = None  # Will be initialized in run()
        self.aliens = []
        self.mutants = []
        for _ in range(random.randint(1, self.number_aliens)):
            self.aliens.append(Alien(self.screen, self.plane, self.planet))

        # X positions for each layer (two copies for seamless looping)
        self.x1 = 0
        self.x2 = 0
        self.x3 = 0
        if self.map_city is not None:
            self.map_city.people.ressurection()
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
        self.screen.fill(color_black)
        self.speed1 = 1
        self.speed2 = 2
        self.speed3 = 4
        screen_width, screen_height = 800, 600
        self.bullets.clear()
        self._right = False
        self.lasers.clear()
        self.mutants = []
        self.background = None  # Will be initialized in run()
        self.aliens = []
        for _ in range(random.randint(1, self.number_aliens)):
            self.aliens.append(Alien(self.screen, self.plane, self.planet))

        # X positions for each layer (two copies for seamless looping)
        self.x1 = 0
        self.x2 = 0
        self.x3 = 0
        if self.map_city is not None:
            self.map_city.people.ressurection()

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
        self.map_city = Map(self.screen)
        meteors = [
            Meteor(
                self.screen.get_width(),
                self.screen.get_height(),
                self.plane.world_x,
                self.planet,
            )
            for _ in range(5)
        ]
        new_meteors = []
        loop = 0
        running = True
        self.bullets = []
        bullet = None
        hunting_set = False
        alarm = False
        city_shown = False
        while running:
            city_shown = False
            alarm = False
            hunting_set = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.K_ESCAPE:
                    running = False

            self.displaying_map = self.plane.display_map

            # Update positions
            if self.plane.y == 0:
                if self.plane.carrying_person:
                    self.plane.add_score(100 * self.planet)
                    self.plane.carrying_person = False
            # Draw layers (two copies each for looping)
            if self.plane.lives <= 0:
                running = False
            self.plane.move(self.lasers)
            self.plane.remove_missles()
            if self.camera is not None:
                self.camera.update(self.plane.world_x)
            if self.background is not None and self.camera is not None:
                self.background.draw(self.screen, self.camera.x)
            self._right = self.plane.direction
            # print(f"Plane direction: {'Right' if self._right else 'Left'}")
            self.screen.blit(self.plane.image, (self.plane.x, self.plane.y))

            if len(self.plane.fired_missle) > 0:
                for missle in self.plane.fired_missle:
                    if missle is not None:
                        missle.move()
                        if missle.image:
                            self.screen.blit(
                                missle.image,
                                (missle.x(), missle.y()),
                            )
            # Move meteor randomly to avoid overlap
            if random.randint(0, 100) % 20 == 0 and len(meteors) < (self.number_aliens):
                for _ in range(random.randint(0, self.number_aliens)):
                    meteors.append(
                        Meteor(
                            self.screen.get_width(),
                            self.screen.get_height(),
                            self.plane.world_x,
                            self.planet,
                        )
                    )
                if len(self.aliens) < (self.number_aliens):
                    for _ in range(random.randint(0, 1)):
                        self.aliens.append(Alien(self.screen, self.plane, self.planet))
            loop = 0
            for mutant in self.mutants:
                if mutant is not None:
                    bullet = mutant.move(
                        meteors,
                        self.plane,
                        self.aliens,
                        self.plane.fired_missle,
                        self.lasers,
                    )
                    if bullet is not None and bullet.image is not None:
                        self.bullets.append(bullet)
                    self.screen.blit(mutant.image, (mutant.x, mutant.y))
                    if mutant.x < -3000 or mutant.x > 3000 or mutant.visible is False:
                        self.mutants.remove(mutant)

            for alien in self.aliens:
                if alien is not None:
                    bullet = alien.move(
                        meteors,
                        self.plane,
                        self.aliens,
                        self.plane.fired_missle,
                        self.lasers,
                    )
                    if bullet is not None and bullet.image is not None:
                        self.bullets.append(bullet)
                    self.screen.blit(alien.image, (alien.x, alien.y))
                    if hunting_set is False:
                        if alien.hunting is True:
                            hunting_set = True
                            if self.map_city.people.visible is False:
                                alien.hunting = False
                                hunting_set = False

                    if alien.x < -3000 or alien.x > 3000:
                        self.aliens.remove(alien)
                        self.aliens.append(Alien(self.screen, self.plane, self.planet))
                    if alien.y <= 0 and alien.carrying_person:
                        self.aliens.remove(alien)
                        if len(self.mutants) < (self.planet):
                            self.mutants.append(
                                Mutant(self.screen, self.plane, self.planet)
                            )
            if self.map_city.people.visible:
                if hunting_set is False and len(self.aliens) > 0:
                    alien = random.choice(self.aliens)
                    if alien is not None:
                        hunting_set = True
                        alien.hunting = True
                        alien.target = self.map_city.people.get_person()

            for b in self.bullets[:]:
                if b is not None and b.image is not None:
                    self.screen.blit(b.image, (b.x, b.y))
                    b.move(self.plane)
                else:
                    self.bullets.remove(b)

            for meteor in meteors:
                if self.plane.using_smart_bombs:
                    meteor.explode()

                if (
                    self.plane.x > meteor.x
                    and self.plane.x < meteor.x + meteor.asteroid.get_width()
                ):
                    alarm = True
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

                self.screen.blit(meteor.asteroid, (meteor.x, meteor.y))
                meteor.move(self.plane)
                if self.map_city.city.hit_meteor_check(meteor):
                    self.plane.add_score(-100 * self.planet)
                if meteor.crash_check(self.plane, True):
                    self.plane.explode()
                    meteor.reset()
                if meteor.crash_check(self.plane, False):
                    meteor.explode()
                    self.plane.add_score(3 * self.planet)
                    self.plane.hit_on_shield()

                for lazer in self.lasers:
                    if lazer.hit_check(meteor):
                        meteor.explode()
                        self.plane.add_score(50 * self.planet)
                        if len(meteor.asteroids) > 0:
                            new_meteors.append(
                                meteor.asteroids.pop(0)
                            )  # Remove the first asteroid in the list

                            meteors.extend(new_meteors)
                            new_meteors.clear()  # Clear the list for the next frame

                if len(self.plane.fired_missle) > 0:
                    for rocket in self.plane.fired_missle:
                        if (
                            rocket is not None
                            and rocket.image is not None
                            and rocket.hit_check(meteor)
                        ):
                            meteor.explode()
                            self.plane.add_score(50 * self.planet)
                            rocket = None  # Remove missle after hit
                            if len(meteor.asteroids) > 0:
                                new_meteors.append(
                                    meteor.asteroids.pop(0)
                                )  # Remove the first asteroid in the list

                                meteors.extend(new_meteors)
                                new_meteors.clear()  # Clear the list for the next frame
            for meteor in meteors:
                if self.map_city.ptarget_shown:
                    if self.map_city.people.impact_check(meteor):
                        self.plane.add_score(-10 * self.planet)
                if meteor.y > self.screen.get_height():
                    new_meteors.append(meteor)

            for new_meteor in new_meteors:
                if new_meteor in meteors:
                    meteors.remove(new_meteor)

            new_meteors.clear()  # Clear the list for the next frame

            if self.plane.exploding:
                self.plane.explode()  # Continue explosion animation

            if loop % 20 == 0:
                self.plane.used_smart_bombs()  # Reset smart bomb usage status
            city_shown = self.map_city.draw(self.plane.world_x, lastx)
            if self.map_city.ptarget_shown:
                if self.map_city.people.crash_check(self.plane) and self.plane.inverse is False:
                    self.plane.add_score(3 * self.planet)
                    self.plane.carrying_person = True
            if self.map_city.starget_shown:
                if self.map_city.stargate.crash_check(self.plane):
                    self.planet = random.randint(1, 25)
                    self.planet = 25
                    self.layer3 = pygame.image.load(
                        f"backgrounds\\layer{self.planet}.png"
                    ).convert_alpha()
                    self.softreset()  # foreground
                    self.plane.teleport()

            if (
                self.map_city.diamond is not None
                and self.map_city.diamond.hit is False
                and self.map_city.diamond.image is not None
            ):
                self.screen.blit(
                    self.map_city.diamond.image,
                    (self.map_city.diamond.x, self.map_city.diamond.y),
                )
                self.map_city.diamond.move()
                if self.plane is not None and self.plane.image is not None:
                    if self.map_city.diamond.hit_player_check(self.plane):
                        self.plane.add_shield(100 * self.planet)
                        self.map_city.diamond.hit = True
                        self.map_city.diamond.y = 600
                        self.map_city.diamond = None

            lastx = self.plane.world_x
            score_text = (
                f"Bombs:{self.plane.smart_bombs} Energy:{self.plane.shield_time} "
            )
            score_text += f"Score:{self.plane.score} Lives:{self.plane.lives} "
            if alarm:
                score_text += " Meteor!"

            self.screen.blit(
                self.font.render(score_text, True, (255, 255, 0)), (10, 10)
            )
            score_text = f"Meteors:{len(meteors)} "
            score_text += f"Aliens:{len(self.aliens)} Planet:{self.planet} "
            score_text += f"People:{self.map_city.people.number_of_people()}"
            self.screen.blit(
                self.font.render(score_text, True, (255, 255, 255)), (10, 580)
            )

            # inside update/draw loop
            if self.displaying_map is True:
                mini_map = MiniMap(self.screen)
                mini_map.draw(
                    self.plane,
                    meteors,
                    self.aliens,
                    self.map_city.people.get_people,
                    self.map_city.stargate,
                    self.mutants,
                    city_shown
                )
            for laser in self.lasers[:]:
                laser.update()
                if not laser.alive:
                    self.lasers.remove(laser)
                else:
                    if self.camera is not None:
                        laser.draw(self.screen)

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
