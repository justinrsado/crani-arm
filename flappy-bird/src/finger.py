import pygame
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Finger(pygame.sprite.Sprite):

    def __init__(self, width, height, init_x, init_y):
        """Constructor, create the image of person"""
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        # set rect
        self.rect = self.image.get_rect()
        self.init_x = init_x
        self.init_y = init_y
        self.rect.x = self.init_x
        self.rect.y = self.init_y

        self.up = True

    def go_up(self):
        """ Called to make finger go up """
        self.up = True
        self.rect.x = self.init_x
        self.rect.y = self.init_y

    def go_down(self):
        """ called to make finger go down"""
        self.up = False
        self.rect.x = self.init_x
        self.rect.y = self.init_y + 100

    def get_up(self):
        return self.up
