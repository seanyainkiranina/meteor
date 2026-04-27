""" Parallax background management for the Meteor game."""
class ParallaxBackground:
    def __init__(self, layers):
        """Initialize the parallax background with a list of layers."""
        self.layers = layers

    def update(self):
        """Update the background layers based on the plane's direction."""
        pass  # no direction logic

    def draw(self, screen, camera_x):
        """Draw the background layers on the screen."""
        for layer in self.layers:
            layer.draw(screen, camera_x)

