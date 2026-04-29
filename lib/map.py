"""Map class for the parallax scrolling game."""
from lib.city import City


class Map:
    """Class representing the game map, including the parallax background and city layers."""

    def __init__(self, screen):
        self.screen = screen
        self.city = City(screen)

    def draw(self,  camera_x , lastx):
        """Draw the map layers on the screen."""
        diff = camera_x - lastx # Calculate the difference in camera position
        if camera_x> 100 and camera_x < 1500:
            self.city.draw(1,diff)
        else:
            self.city.reset(1)  

        if camera_x> -24000 and camera_x < -27000:
            self.city.draw(2,diff)
        else:
            self.city.reset(2)

        if camera_x> 3000 and camera_x < 5000:
            self.city.draw(3,diff)
        else:
            self.city.reset(3)
