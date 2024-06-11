import pygame
import os
from sprite_sheet import SpriteSheet
import constants

PLAYER_HEIGHT = 64
PLAYER_WIDTH = 32


class Player(pygame.sprite.Sprite):

    def __init__(self, init_x, init_y):
        """Constructor, create the image of person"""
        super().__init__()

        # -- attributes --

        # get image of flappy_bird
        # print("flappy bird image path:", os.path.abspath(constants.base_path + "flappy_bird_sprite_sheet.png"))
        sprite_sheet = SpriteSheet(os.path.abspath(
            constants.base_path + "flappy_bird_sprite_sheet.png"))
        self.image = sprite_sheet.get_image(x=223, y=124, width=17, height=12)

        # set rect
        self.rect = self.image.get_rect()
        self.spawn(init_x, init_y)

    def spawn(self, init_x, init_y):
        self.change_x = 0  # should stay at 0
        self.change_y = 0  # y velocity
        self.accel_y = 5  # gravity
        self.max_change_y = 10
        self.rect.x = init_x
        self.rect.y = init_y

    def update(self):
        # makeshift physics
        self.calc_grav()
        self.rect.y += self.change_y

        # temporary measure until ground is implemented (prevents flappy bird from falling off screen)
        # if self.rect.y < 0:
        #     self.rect.y = 0

        # if self.rect.y > 190:
        #     self.rect.y = 190

    def calc_grav(self):
        """ Calculate gravity. """
        # TODO implement flappy bird physics

        if self.max_change_y > self.change_y:
            self.change_y += self.accel_y
            if self.max_change_y < self.change_y:
                self.change_y = self.max_change_y

    def jump(self):
        """ Called when user hits 'jump' button. """
        self.change_y = -30

    def fall(self):
        """ called when user collides with ground or pipe"""
        self.dead = True
        self.change_y = 0

    def get_dead(self):
        return self.dead
