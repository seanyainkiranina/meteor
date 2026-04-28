"""ParallaxLayer class for the parallax scrolling game."""
import pygame

class ParallaxLayer:
    """Class representing a single layer in the parallax background."""
    def __init__(self, image, parallax_factor):
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.factor = parallax_factor
        self.font = pygame.font.SysFont("consolas", 16)

    def update(self):
        """Update the layer's position based on the parallax factor."""
        pass  # no movement logic needed

    def draw(self, screen, camera_x):
        """Draw the layer on the screen, applying parallax scrolling based on camera position."""
        # Compute parallax offset
        x = -(camera_x * self.factor) % self.width

        # Draw three copies to guarantee coverage
        screen.blit(self.image, (x, 0))
        screen.blit(self.image, (x - self.width, 0))
        screen.blit(self.image, (x + self.width, 0))
       # cities = City(screen)
       # cities.draw()
        # Debug text
        # debug_text = f"cam={camera_x:.1f} x={x:.1f} factor={self.factor}"
        # screen.blit(self.font.render(debug_text, True, (255, 255, 0)), (10, 10))
