"""Mini map"""

import pygame


class MiniMap:
    """constuctor"""

    def __init__(self, screen):
        self._screen = screen
        self._width = 200
        self._height = 120
        self._surface = pygame.Surface((self._width, self._height))
        self._surface.set_alpha(180)
        self._bg = (15, 15, 15)
        self._border = (80, 80, 80)

    def draw(self, plane, meteors, aliens, people, stargate, mutants):
        """draw map"""
        screen_w = self._screen.get_width()
        screen_h = self._screen.get_height()

        # CAMERA WINDOW IN WORLD COORDINATES
        camera_left = plane.world_x - screen_w // 2
        camera_right = plane.world_x + screen_w // 2
        camera_width = camera_right - camera_left

        # Clear mini-map
        self._surface.fill(self._bg)
        pygame.draw.rect(
            self._surface, self._border, (0, 0, self._width, self._height), 2
        )

        def world_to_map(wx, wy):
            """calc the map"""
            # Only X is scaled (side-scroller)
            mx = int(((wx - camera_left) / camera_width) * self._width)
            my = int((wy / screen_h) * self._height)
            return mx, my

        # --- PLANE ---
        px, py = world_to_map(plane.world_x, plane.y)
        pygame.draw.circle(self._surface, (0, 255, 0), (px, py), 3)
        if plane.carrying_person:
            pygame.draw.circle(self._surface, (0, 150, 255), (px, py+4), 5)

        if camera_left <= stargate.world_x <= camera_right:
            mx, my = world_to_map(stargate.world_x, stargate.y)
            pygame.draw.circle(self._surface, (255, 255, 0), (mx, my), 3)

        for mt in mutants:
            if camera_left <= mt.world_x <= camera_right:
                mx, my = world_to_map(mt.world_x, mt.y)
                pygame.draw.circle(self._surface, (120, 120, 255), (mx, my), 2)

        # --- METEORS ---
        for m in meteors:
            if camera_left <= m.world_x <= camera_right:
                mx, my = world_to_map(m.world_x, m.y)
                pygame.draw.circle(self._surface, (255, 120, 0), (mx, my), 2)

        # --- ALIENS ---
        for a in aliens:
            if camera_left <= a._world_x <= camera_right:
                mx, my = world_to_map(a.world_x, a.y)
                color = (255, 0, 0) if a.hunting else (150, 0, 0)
                pygame.draw.circle(self._surface, color, (mx, my), 2)

        # --- PEOPLE ---
        for p in people:
            if p.visible is True:
                if camera_left <= p.world_x <= camera_right:
                    mx, my = world_to_map(p.world_x, p.y)
                    pygame.draw.circle(self._surface, (0, 150, 255), (mx, my), 5)

        # Draw mini-map in top-right corner
        self._screen.blit(
            self._surface, (self._screen.get_width() - self._width - 10, 10)
        )
