"""Survivor"""


class Survivor:
    """class to hold a person"""

    def __init__(self, world_x, y, which):
        self._world_x = world_x
        self._y = y
        self._visible = True
        self._which = which

    @property
    def which(self):
        """which Survivor"""
        return self._which

    @property
    def visible(self):
        """get if visible"""
        return self._visible

    @visible.setter
    def visible(self, value):
        """set visible"""
        self._visible = value

    @property
    def world_x(self):
        """get world x"""
        return self._world_x

    @property
    def y(self):
        """get y"""
        return self._y
