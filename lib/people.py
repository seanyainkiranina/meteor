"""People class for the Meteor game."""

import random
import pygame

from lib.survivor import Survivor

class People:
    """City class for the Meteor game."""

    def __init__(self, screen):
        self._people = []
        self._people_x = []
        self._display = []
        self._survivors = []
        self._people_positions = [0]
        self._screen = screen
        for _ in range(0, 15):
            self._people.append(
                pygame.image.load("backgrounds\\people.png").convert_alpha()
            )
        self._visible = False
        self._which = -1
        self._diff_x = 0
        self._max = len(self._people) - 1
        first = -9000
        for i in range(0, self._max):
            self._display.append(True)
            self._people_x.append(self._screen.get_width() // 3)
            self._people_positions.append(first)
            self._survivors.append(Survivor(first,self._screen.get_height() - 30,i))
            first += 3000
            

    @property
    def x(self):
        """Get the current x position of the city."""
        return self._people_x[self._which]

    @property
    def visible(self):
        """Check if visible"""
        return self._visible

    @visible.setter
    def visible(self, value):
        """set visible"""
        self._display[self._which] = value
        self._visible = value

    def number_of_people(self):
        """get number of people"""
        return self._display.count(True)

    def ressurection(self):
        """bring them all back"""
        for index, _ in enumerate(self._display):
            self._display[index] = True

    @property
    def y(self):
        """Get the current y position of the city"""
        return self._screen.get_height() - 30

    @property
    def position(self):
        """Get the current position of the city."""
        return self._people_positions[self._which]

    @property
    def which(self):
        """which city"""
        return self._which

    def alien_check(self, a):
        """Check for collision with the meteor."""
        rock_rect = a.image.get_rect(topleft=(a.x, a.y))
        person_rect = self._people[self._which].get_rect(topleft=(self.x, self.y))
        checked = rock_rect.colliderect(person_rect)
        if checked:
            self._display[self._which] = False
            for survivor in  self._survivors:
                if survivor.which == self._which:
                    survivor.visible = False
        return checked

    def impact_check(self, rock):
        """Check for collision with the meteor."""
        rock_rect = rock.asteroid.get_rect(topleft=(rock.x, rock.y))
        person_rect = self._people[self._which].get_rect(topleft=(self.x, self.y))
        checked = rock_rect.colliderect(person_rect)
        if checked:
            self._display[self._which] = False
            for survivor in  self._survivors:
                if survivor.which == self._which:
                    survivor.visible = False

        return checked

    @property
    def get_people(self):
        """ return people"""
        return self._survivors

    def get_person(self):
        """return self"""
        if self._which <= self._max:
            if self._display[self._which]:
                return self
        return None

    def crash_check(self, plane):
        """Check for plane"""
        if plane.shield_on:
            return False  # No collision if the shield is on
        if plane.carrying_person: # cannot pick up two
            return False
        plane_rect = plane.image.get_rect(topleft=(plane.x, plane.y))
        person_rect = self._people[self._which].get_rect(topleft=(self.x, self.y))

        checked = plane_rect.colliderect(person_rect)
        if checked:
            self._display[self._which] = False
            for survivor in  self._survivors:
                if survivor.which == self._which:
                    survivor.visible = False

        return checked

    def reborn(self):
        """randomly show an person"""
        i = random.randint(0, self._max)
        x = random.randint(0, 1000)
        if i < len(self._display) and x < 1:
            self._display[i] = True

    def display(self, world_x, diff_x):
        """display a city"""
        self._diff_x = diff_x
        self._visible = False
        for i in range(0, self._max):
            if i >= len(self._people_x):
                continue
            if world_x < self._people_positions[i] - 2000:
                continue
            if world_x > self._people_positions[i] + 1000:
                continue
            self._which = i
            if self._display[self._which]:
                self._visible = True
                self.draw(i, world_x, diff_x)
                for s in self._survivors:
                    if s.world_x > self._people_positions[i] - 2000:
                        if s.world_x < self._people_positions[i] + 1000:
                            s.which = i
                            s.visible = True
            return True
        return False

    def draw(self, which_city, world_x, increment=0):
        """Draw the city layers on the screen."""
        if which_city <= self._max:
            self._which = which_city
            screen_x = (
                self._people_positions[which_city]
                - world_x
                + self._screen.get_width() // 3
            )
            self._screen.blit(
                self._people[which_city], (screen_x, self._screen.get_height() - 30)
            )
            self._people_x[which_city] = screen_x
            return True
        return False
