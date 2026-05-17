"""People class for the Meteor game."""
import random
import pygame


class People:
    """City class for the Meteor game."""

    def __init__(self, screen):
        self._people = []
        self._people_x = []
        self._display = []
        self._people_positions = [0]
        self._screen = screen
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._people.append(pygame.image.load("backgrounds\\people.png").convert_alpha())
        self._visible = False
        self._which = -1
        self._diff_x = 0
        self._max = len(self._people) - 1
        first = -9000
        for _ in range(0, self._max):
            self._display.append(True)
            self._people_x.append(self._screen.get_width() // 3)
            self._people_positions.append(first)
            first += random.randint(2000,3000)
    @property
    def x(self):
        """Get the current x position of the city."""
        return self._people_x[self._which]

    @property
    def visible(self):
        """Check if visible"""
        return self._visible

    @property
    def y(self):
        """Get the current y position of the city"""
        return self._screen.get_height()-30
    @property
    def position(self):
        """Get the current position of the city."""
        return self._people_positions[self._which]

    @property
    def which(self):
        """which city"""
        return self._which

    def crash_check(self, plane, handle_shield_hit=False):
        """Check for collision with the player's plane."""
        if plane.shield_on and handle_shield_hit:
            return False  # No collision if the shield is on
        plane_rect = plane.image.get_rect(topleft=(plane.x, plane.y))
        person_rect = self._people[self._which].get_rect(topleft=(self.x, self.y))
        checked = plane_rect.colliderect(person_rect)
        if checked: 
            self._display[self._which] = False
        return checked

    def reborn(self):
        """ randomly show an person """
        i = random.randint(0,self._max)
        x = random.randint(0,100)
        if i<len(self._display) and x<1:
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
            return True
        return False

    def draw(self, which_city, world_x, increment=0):
        """Draw the city layers on the screen."""
        if which_city <= self._max:
            self._which = which_city
            screen_x = self._people_positions[which_city] - world_x + self._screen.get_width() // 3 
            self._screen.blit(self._people[which_city], (screen_x, self._screen.get_height()-30))
            self._people_x[which_city]= screen_x
            return True
        return False
