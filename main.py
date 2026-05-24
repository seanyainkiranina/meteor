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
        self.camera = None
        # Parallax speeds
        self.speed1 = 1
        self.speed2 = 2
        self.speed3 = 4
        self.map_city = None

        self._right = False

        self.background = None  # Will be initialized in run()
        self._aliens = []
        self._bullets = []
        self._mutants = []
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
            self._aliens.append(Alien(self._screen, self.plane,self.planet))
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
        i_max = round((3 + self.planet) // random.randint(1, 3), 0) + 1
        if i_max >= 10:
            i_max = 10
        return i_max

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
        self._mutants = []
        for _ in range(random.randint(1, self.number_aliens)):
            self._aliens.append(Alien(self._screen, self.plane,self.planet))

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
        self._screen.fill(color_black)
        self.speed1 = 1
        self.speed2 = 2
        self.speed3 = 4
        screen_width, screen_height = 800, 600
        self._bullets.clear()
        self._right = False
        self._mutants = []
        self.background = None  # Will be initialized in run()
        self._aliens = []
        for _ in range(random.randint(1, self.number_aliens)):
            self._aliens.append(Alien(self._screen, self.plane,self.planet))

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
        self.map_city = Map(self._screen)
        meteors = [
            Meteor(
                self._screen.get_width(), self._screen.get_height(), self.plane.world_x,self.planet
            )
            for _ in range(5)
        ]
        new_meteors = []
        loop = 0
        running = True
        self._bullets = []
        bullets_to_remove = []
        bullet = None
        hunting_set = False
        alarm = False
        while running:
            alarm = False
            hunting_set = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.K_ESCAPE:
                    running = False

            # Update positions
            if self.plane.y == 0:
                if self.plane.carrying_person:
                    self.plane.add_score(100 * self.planet)
                    self.plane.carrying_person = False
            # Draw layers (two copies each for looping)
            if self.plane.lives <= 0:
                running = False
            self.plane.move()
            self.plane.remove_missles()
            self.camera.update(self.plane.world_x)
            if self.background is not None:
                self.background.draw(self._screen, self.camera.x)
            self._right = self.plane.direction
            # print(f"Plane direction: {'Right' if self._right else 'Left'}")
            self._screen.blit(self.plane.image, (self.plane.x, self.plane.y))

            if len(self.plane.fired_missle) >0:
                for missle in self.plane.fired_missle:
                    if missle is not None:
                        missle.move()
                        if missle.image:
                            self._screen.blit(
                                missle.image,
                                (missle.x(), missle.y()),
                            )
            # Move meteor randomly to avoid overlap
            if random.randint(0, 100) % 20 == 0 and len(meteors) < (self.number_aliens):
                for _ in range(random.randint(0, self.number_aliens)):
                    meteors.append(
                        Meteor(
                            self._screen.get_width(),
                            self._screen.get_height(),
                            self.plane.world_x,
                            self.planet
                        )
                    )
                if len(self._aliens) < (self.number_aliens):
                    for _ in range(random.randint(0, 1)):
                        self._aliens.append(Alien(self._screen, self.plane,self.planet))
            loop = 0
            for mutant in self._mutants:
                if mutant is not None:
                    bullet = mutant.move(
                        meteors, self.plane, self._aliens, self.plane.fired_missle
                    )
                    if bullet is not None and bullet.image is not None:
                        self._bullets.append(bullet)
                    self._screen.blit(mutant.image, (mutant.x, mutant.y))
                    if mutant.x < -3000 or mutant.x > 3000 or mutant.visible is False:
                        self._mutants.remove(mutant)

            for alien in self._aliens:
                if alien is not None:
                    bullet = alien.move(
                        meteors, self.plane, self._aliens, self.plane.fired_missle
                    )
                    if bullet is not None and bullet.image is not None:
                        self._bullets.append(bullet)
                    self._screen.blit(alien.image, (alien.x, alien.y))
                    if hunting_set is False:
                        if alien.hunting is True:
                            hunting_set = True
                            if self.map_city.people.visible is False:
                                alien.hunting = False
                                hunting_set = False

                    if alien.x < -3000 or alien.x > 3000:
                        self._aliens.remove(alien)
                        self._aliens.append(Alien(self._screen, self.plane,self.planet))
                    if alien.y <= 0 and alien.carrying_person:
                        self._aliens.remove(alien)
                        if len(self._mutants) < (self.planet):
                            self._mutants.append(Mutant(self._screen, self.plane))
            if self.map_city.people.visible:
                if hunting_set is False and len(self._aliens) > 0:
                    alien = random.choice(self._aliens)
                    if alien is not None:
                        hunting_set = True
                        alien.hunting = True
                        alien.target = self.map_city.people.get_person()

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

                if self.plane.x > meteor.x and self.plane.x < meteor.x + meteor.asteroid.get_width():
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

                self._screen.blit(meteor.asteroid, (meteor.x, meteor.y))
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
                if len(self.plane.fired_missle) >0:
                    for rocket in self.plane.fired_missle:
                        if rocket is not None and rocket.image is not None and rocket.hit_check(
                            meteor
                        ):
                            meteor.explode()
                            self.plane.add_score(10 * self.planet)
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
            self.map_city.draw(self.plane.world_x, lastx)
            if self.map_city.ptarget_shown:
                if self.map_city.people.crash_check(self.plane):
                    self.plane.add_score(10 * self.planet)
                    self.plane.carrying_person = True
            if self.map_city.starget_shown:
                if self.map_city.stargate.crash_check(self.plane):
                    self.planet = random.randint(1, 15)
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
                self._screen.blit(
                    self.map_city.diamond.image,
                    (self.map_city.diamond.x, self.map_city.diamond.y),
                )
                self.map_city.diamond.move()
                if self.plane is not None and self.plane.image is not None:
                    if self.map_city.diamond.hit_player_check(self.plane):
                        self.plane.add_shield(100)
                        self.map_city.diamond.hit = True
                        self.map_city.diamond.y = 600
                        self.map_city.diamond = None

            lastx = self.plane.world_x
            score_text = (
                f"Bombs:{self.plane.smart_bombs} Shield:{self.plane.shield_time} "
            )
            score_text += f"Score:{self.plane.score} Lives:{self.plane.lives} "
            score_text += f"Meteors:{len(meteors)} "
            score_text += f"Aliens:{len(self._aliens)} Planet:{self.planet} "
            score_text += f"People:{self.map_city.people.number_of_people()}"
            if alarm:
                score_text +=" Meteor!"

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
