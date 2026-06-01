"""Map class for the parallax scrolling game."""

from lib.city import City
from lib.stargate import Stargate
from lib.people import People


class Map:
    """Class representing the game map, including the parallax background and city layers."""

    def __init__(self, screen):
        self._city = City(screen)
        self._lastx = 0
        self._diamond = None
        self._stargate = Stargate(screen)
        self._stargate_shown = False
        self._people = People(screen)

    @property
    def people(self):
        """ peoples"""
        return self._people
    @property
    def stargate(self):
        """stargates are owned by the map"""
        return self._stargate

    @property
    def diamond(self):
        """Diamonds are owned by the cities"""
        return self._diamond

    @property
    def which(self):
        """city number"""
        return self.city.which

    @property
    def position(self):
        """city position"""
        return self.city.position

    @property
    def x(self):
        """x position of the city"""
        return self.city.x

    @diamond.setter
    def diamond(self, value):
        """Diamonds can be destroyed"""
        self._diamond = value

    @property
    def city(self):
        """get city"""
        return self._city

    @property
    def starget_shown(self):
        """ check if star gate is shown"""
        return self._stargate_shown

    @property
    def ptarget_shown(self):
        """ Check if person is shown """
        return self._people.visible

    def draw(self, camera_x, lastx):
        """draw city"""
        city_x=0
        if self._lastx == 0:
            self._lastx = lastx
        diff = self._lastx - lastx
        self._lastx = lastx  # Calculate the difference in camera position
        city_x=self._city.display(camera_x, diff)
        self._people.display(camera_x,diff)
        self._stargate_shown = self._stargate.display(camera_x, diff)
        self._diamond = self._city.diamond
        if self._diamond is not None:
            self._diamond.x += diff
        return city_x