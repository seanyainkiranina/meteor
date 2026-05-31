"""Laser Beam"""

import random
import pygame


class LaserBeam:
    """Laser Beam constuctor"""

    def __init__(self, x, y, direction=1):
        self.x = x
        self.y = y
        self.length = 600  # how far the beam reaches
        self.width = 1  # beam thickness
        self.color = (0, 255, 255)  # cyan laser
        self.direction = direction
        self.alive = True
        self.timer = 20  # frames the beam stays alive
        self.start_x = 0
        self.target_x = 0
  
    def update(self):
        """Laser beam update"""
        self.timer -= 1
        if self.timer <= 0:
            self.alive = False
    def hit_check(self, meteor):
        """Check if the missle has hit a meteor."""
        upper_x = self.start_x
        if self.target_x< upper_x:
            upper_x = self.target_x
        laser_rect = pygame.Rect(
            upper_x,
            self.y - 4,
            abs(self.start_x -self.target_x) ,
            4,
        )
        meteor_rect = meteor.asteroid.get_rect(topleft=(meteor.x, meteor.y))
        return laser_rect.colliderect(meteor_rect)

    def hit(self, target):
        """ hit detection """
        upper_x = self.start_x
        if self.target_x< upper_x:
            upper_x = self.target_x
        laser_rect = pygame.Rect(
            upper_x,
            self.y - 4,
            abs(self.start_x -self.target_x) ,
            4,
        )
        return target.colliderect(laser_rect)
    def draw(self, screen):
        """Laser beam draw"""
        start_x = self.x + (self.timer)
    
    
        if self.direction == 1:
            difference = abs(self.x - 800)
            end_x = start_x + difference + (20 - self.timer)
        else:
            difference = 0 - self.x 
            end_x = start_x + difference - (20 - self.timer)
        target_y = self.y + 4
        self.start_x = start_x
        self.target_x = end_x
        red = random.randint(0,255)
        if end_x>start_x:
            random_length = random.randint(start_x, end_x)
        else:
            random_length = random.randint(end_x, start_x)
            
        pygame.draw.line(
            screen, (red, 36, 0), (start_x, target_y+1), (end_x , target_y +1), self.width
        )
        pygame.draw.line(
            screen, (red, 0, 0), (start_x, target_y), (end_x, target_y), self.width 
        )
        pygame.draw.line(
            screen, (red, 99, 71), (start_x, target_y -2), (end_x, target_y -2), self.width
        )
        blue = random.randint(0,255)
        pygame.draw.line(
            screen, (red, 128, blue), (start_x, target_y), (random_length, target_y +1), self.width 
        )
        if end_x>start_x:
            random_length = random.randint(start_x, end_x)
        else:
            random_length = random.randint(end_x, start_x)
        blue = random.randint(0,255)
   
        pygame.draw.line(
            screen, (red, 128, blue), (start_x, target_y), (random_length, target_y +1), self.width 
        )
