import pygame
from sprite_sheet import SpriteSheet
import os
import constants


class Pipe(pygame.sprite.Sprite):
    def __init__(self, change_x, screen_width, screen_height):
        super().__init__()

        # instance variables
        self.change_x = change_x  # velocity
        self.screen_width = screen_width
        self.screen_height = screen_height

    def stop(self):
        """ called when flappy bird collides with stage """
        # TODO kill
        self.change_x = 0
        self.kill()

    def reset(self):
        """ reposition pipe at right side of screen and randomize height"""
        # set to right side of screen
        self.rect.x = self.screen_width

        # TODO randomize pipe height and coordinate pipe height between top and bottom pipe
        # might need to add in flappy_bird.py to accomplish this


    def update(self):
        self.rect.x -= self.change_x

        if self.rect.x < -26:
            self.stop()

    def speed_up(self):
        # TODO
        pass


class TopPipe(Pipe):
    def __init__(self, change_x, screen_width, screen_height, game):
        super().__init__(change_x, screen_width, screen_height)

        # get image of top pipe
        # print("top pipe image path:", os.path.abspath(constants.base_path + "flappy_bird_sprite_sheet.png"))
        sprite_sheet = SpriteSheet(os.path.abspath(constants.base_path + "flappy_bird_sprite_sheet.png"))
        self.image = sprite_sheet.get_image(x=302, y=0, width=26, height=135)

        self.rect = self.image.get_rect()

        self.game = game

    def update(self):
        self.rect.x -= self.change_x

        if self.rect.x < -26:
            self.stop()
            self.game.pipe_counter += 1


class BottomPipe(Pipe):
    def __init__(self, change_x, screen_width, screen_height):
        super().__init__(change_x, screen_width, screen_height)

        # get image of top pipe
        # print("bottom pipe image path:", os.path.abspath(constants.base_path + "flappy_bird_sprite_sheet.png"))
        sprite_sheet = SpriteSheet(os.path.abspath(constants.base_path + "flappy_bird_sprite_sheet.png"))
        self.image = sprite_sheet.get_image(x=331, y=0, width=26, height=121)

        self.rect = self.image.get_rect()

# TODO implement ground sprite
class Ground(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height

        # TODO grab image from sprite sheet
        # print("ground image path:", os.path.abspath(constants.base_path + "flappy_bird_sprite_sheet.png"))
        sprite_sheet = SpriteSheet(os.path.abspath(constants.base_path + "flappy_bird_sprite_sheet.png"))
        self.image = sprite_sheet.get_image(x=145, y=0, width=154, height=55)

        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0

    def stop(self):
        pass

    def update(self):
        # ground shouldn't do anything
        pass