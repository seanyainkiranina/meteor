"""Camera class to follow the plane in the game."""
class Camera:
    """Simple camera class to follow the plane."""
    def __init__(self, screen_width):
        """Initialize the camera with the screen width."""
        self.x = 0
        self.screen_width = screen_width

    def update(self, target_x):
        """Update the camera's position to follow the target (plane)."""
        # Center camera on the plane
        # print(f"Camera update: target_x={target_x} screen_width={self.screen_width}")
        self.x = target_x - self.screen_width // 2
