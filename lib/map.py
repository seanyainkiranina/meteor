"""Map class for the parallax scrolling game."""

from lib.city import City


class Map:
    """Class representing the game map, including the parallax background and city layers."""

    def __init__(self, screen):
        self._city = City(screen)
        self._lastx = 0
        self._diamond = None

    @property
    def diamond(self):
        """Diamonds are owned by the cities"""
        return self._diamond

    @property
    def which(self):
        """city number"""
        return self.city.which

    @diamond.setter
    def diamond(self, value):
        """Diamonds can be destroyed"""
        self._diamond = value

    @property
    def city(self):
        """get city"""
        return self._city

    def draw(self, camera_x, lastx):
        """draw city"""
        if self._lastx == 0:
            self._lastx = lastx
        diff = self._lastx - lastx
        self._lastx = lastx  # Calculate the difference in camera position
        self._city.display(camera_x, diff)
        self._diamond = self._city.diamond
        if self._diamond is not None:
            self._diamond.x += diff
