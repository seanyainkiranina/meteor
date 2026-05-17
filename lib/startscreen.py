"""Start up screen"""

import time
import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE
)  # pylint: disable=[E0611,W0611]
from lib.score import Score

class StartScreen:
    """Startup Screen"""

    def __init__(self, screen):
        self._screen = screen
        self._font = pygame.font.SysFont("consolas", 23)
        self._starting = 1
        self._high_score = -1000
        self._score_board = Score()

    @property
    def high_score(self):
        """ get high score"""
        return self._high_score

    @high_score.setter
    def high_score(self,value):
        """ set high score"""
        self._high_score = value
        if value > 0:
            self._score_board.value = value
            self._score_board.save()


    def instructions(self):
        """Game Instructions"""
        instruct = []
        instruct.append("Welcome to Meteor")
        instruct.append("Space bar to fire arrows to move")
        instruct.append("s for shields on d for shields off")
        instruct.append("f to toggle speed burst, g for hyper space jump")
        instruct.append("a to fire smart bomb ")
        instruct.append("Bringing a person to the top of the screen 200 pts")
        instruct.append("Extra life after every 1000 points")
        instruct.append("Esc to exit")
        instruct.append("Anykey to Start")
        return instruct

    def display_instructions(self, start_y, instructions):
        """Display Instructions"""
        display_instruct = []
        done = False
        for i in instructions:
            t = {}
            if i.split(" ")[1] == str(self._high_score) and done is False:
                t["text"] = self._font.render(i, True, (255, 0, 0))
                done = True
            else:
                t["text"] = self._font.render(i, True, (255, 255, 255))
            start_y += 16
            display_instruct.append(t)
        return display_instruct

    def display(self,screen):
        """Start up screen"""
        time.sleep(1)
        pygame.event.clear()
        pygame.event.clear(KEYDOWN)
        self._screen = screen
        black = (0, 0, 0)
        self._screen.fill(black)
        instruction_messages = self.instructions()
        self._starting=1
        start_y=16
        if self._high_score > 0:
            instruction_messages.append(f"Your Score:{self._high_score}")
        high_scores = self._score_board.get_scores()
        instruction_messages.append("High Scores")
        for h in high_scores:
            instruction_messages.append(h)
        text_messages = self.display_instructions(10, instruction_messages)
        while self._starting == 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self._starting = 0
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self._starting = 0
                    else:
                        self._starting = 2
            start_y =16
            for t in text_messages:
                t["text_rect"] = t["text"].get_rect(topleft=(10, start_y))
                self._screen.blit(t["text"], t["text_rect"])
                start_y +=20
            pygame.display.update()
        if self._starting == 2:
            pygame.event.clear(KEYDOWN)
            return True

        return False
