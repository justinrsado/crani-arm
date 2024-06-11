import pygame
import os
import random
import sys
import threading as thread
from src.finger import Finger

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Game(object):

    # create all the instance variables upon creation
    def __init__(self, size):
        # create sprite groups
        self.all_sprites_list = pygame.sprite.Group()
        self.finger_list = pygame.sprite.Group()

        self.pinky = Finger(40, 100, 40, 40)
        self.ring = Finger(40, 100, 90, 40)
        self.middle = Finger(40, 100, 140, 40)
        self.pointer = Finger(40, 100, 190, 40)
        self.thumb = Finger(40, 100, 240, 40)

        self.palm = Finger(240, 180, 40, 150)

        for finger in (self.pinky, self.ring, self.middle, self.pointer, self.thumb, self.palm):
            self.all_sprites_list.add(finger)
            self.finger_list.add(finger)



    def process_events(self):
        """
        Process all of the events. Return a "True" if we need
        to close the window.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.pinky.go_down()
                if event.key == pygame.K_2:
                    self.ring.go_down()
                if event.key == pygame.K_3:
                    self.middle.go_down()
                if event.key == pygame.K_4:
                    self.pointer.go_down()
                if event.key == pygame.K_5:
                    self.thumb.go_down()

            if event.type == pygame.KEYUP:
                for finger in self.finger_list:
                    finger.go_up()


    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        self.all_sprites_list.update()

    def display_frame(self, screen):
        """ display everything to the screen for the game """
        screen.fill(WHITE)
        self.all_sprites_list.draw(screen)
        pygame.display.flip()


def main():

    # standard commands to start pygame
    pygame.init()
    # size of screen (can be adjusted)
    size = (350, 400)
    screen = pygame.display.set_mode(size)

    # control the frame rate and create game object
    clock = pygame.time.Clock()
    game = Game(size)

    # main loop
    done = False
    while not done:
        # process events
        done = game.process_events()

        # game logic
        game.run_logic()

        # drawing
        game.display_frame(screen)

        # pause for next frame
        clock.tick(25)
    pygame.quit()


if __name__ == '__main__':
    main()
