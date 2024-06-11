import pygame
import constants

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet """

    def __init__(self, file_name):
        print(file_name)
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # create a new blank image
        image = pygame.Surface([width, height]).convert_alpha()

        # copy the sprite from large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming white is the transparent color
        image.set_colorkey(constants.WHITE)

        image = pygame.transform.scale(image, (width * constants.sf, height * constants.sf))
        # Return image
        return image
