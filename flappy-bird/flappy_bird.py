import pygame
import os
import random
import sys
import threading as thread
from serial_arduino import Serial_Arduino
from src.constants import PIPE_FREQUENCY
from src.player import Player
from src.stage import TopPipe, BottomPipe, Ground
from src.sprite_sheet import SpriteSheet
import src.constants as constants


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

PIPE_GAP = 50


STATES = ["PLAYING", "DEAD"]

# TODO
"""
    Pooja: game counter, pipe height  
    (Note: internal game counter completed by Conner in order to speed up pipes: self.pipe_counter)
    Leon: game state handler logic (start screen, death)
    Conner: speed up and first pipe delay: COMPLETE
    
"""


class Game(object):

    # create all the instance variables upon creation
    def __init__(self, size, initial_delay, serial_arduino):
        self.hand_closed_p = False
        self.serial_arduino = serial_arduino
        # set instance variables
        self.state = "PLAYING"
        self.size = size
        # Initialize start time
        self.last_pipe = initial_delay
        self.initial_pipe_vel = 3
        self.max_pipe_vel = 5
        # a high number correlates to a slower increase in difficulty
        self.difficulty_increase_rate = 8

        # create sprite groups
        self.all_sprites_list = pygame.sprite.Group()
        self.stage_sprites_list = pygame.sprite.Group()

        # Create player
        self.player = Player(10, 10)
        self.player.rect.x, self.player.rect.y = 10, 10
        self.all_sprites_list.add(self.player)

        # create stage sprites
        # top pipe
        self.pipe_a_top = TopPipe(
            change_x=5, screen_width=size[0], screen_height=size[1], game=self)
        self.pipe_a_top.rect.x, self.pipe_a_top.rect.y = 20, 0
        self.all_sprites_list.add(self.pipe_a_top)
        self.stage_sprites_list.add(self.pipe_a_top)

        # bottom pipe
        self.pipe_a_bottom = BottomPipe(
            change_x=5, screen_width=size[0], screen_height=size[1])
        self.pipe_a_bottom.rect.x, self.pipe_a_bottom.rect.y = 20, 180
        self.all_sprites_list.add(self.pipe_a_bottom)
        self.stage_sprites_list.add(self.pipe_a_bottom)

        # ground
        self.ground = Ground(screen_width=size[0], screen_height=size[1])
        self.ground.rect.x, self.ground.rect.y = 0, size[1] - \
            self.ground.rect.height
        self.all_sprites_list.add(self.ground)
        self.stage_sprites_list.add(self.ground)

        #  self.pipe_b # focus on one pipe for now

        # Draw backgound
        self.sprite_sheet = SpriteSheet(os.path.abspath(
            constants.base_path + "flappy_bird_sprite_sheet.png"))
        self.bg = self.sprite_sheet.get_image(x=0, y=0, width=144, height=256)

        self.pipe_counter = 0

    def process_events(self):
        """
        Process all of the events. Return a "True" if we need
        to close the window.
        """

        if self.state == "PLAYING":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
            self.serial_arduino.get_on_lock().acquire()
            hand_closed = self.serial_arduino.get_on()
            self.serial_arduino.get_on_lock().release()

            if hand_closed != self.hand_closed_p:
                if hand_closed == False:
                    self.player.jump()
                self.hand_closed_p = hand_closed
                # if event.type == pygame.KEYDOWN:  # Key is pressed Event
                #     if event.key == pygame.K_SPACE:
                #         self.player.jump()

            # check for collisions
            stage_collision_list = pygame.sprite.spritecollide(
                self.player, self.stage_sprites_list, False)
            if len(stage_collision_list) > 0:
                self.state = "DEAD"
                for sprite in stage_collision_list:
                    print(sprite)
                self.player.fall()
                for sprite in self.stage_sprites_list:
                    sprite.stop()
            else:
                pass
        elif self.state == "DEAD":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.state = "PLAYING"
                        self.player.spawn(10, 10)
                        self.pipe_counter = 0

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if self.state == "PLAYING":
            # increase change_x by one every 4 pipes (max out at 10)
            pipe_change_x = min(self.max_pipe_vel,
                                (self.initial_pipe_vel + (self.pipe_counter // self.difficulty_increase_rate)))

            time_now = pygame.time.get_ticks()
            if time_now - self.last_pipe > (pipe_change_x * 500 * constants.sf):
                top_height = random.randint(-100 * constants.sf, 0)
                bottom_pipe = BottomPipe(
                    pipe_change_x, screen_width=self.size[0], screen_height=self.size[1])
                top_pipe = TopPipe(pipe_change_x, screen_width=self.size[0],
                                   screen_height=self.size[1], game=self)
                bottom_pipe.rect.x = self.size[0]
                top_pipe.rect.x = self.size[0]

                top_pipe.rect.y = top_height
                bottom_pipe.rect.y = 185 * constants.sf + top_height
                self.all_sprites_list.add(bottom_pipe)
                self.all_sprites_list.add(top_pipe)
                self.stage_sprites_list.add(top_pipe)
                self.stage_sprites_list.add(bottom_pipe)
                self.last_pipe = time_now
            # time_now = pygame.time.get_ticks()
            # if time_now - self.last_pipe > (pipe_change_x * 500):
            #     top_height = random.randint(-100, 0)
            #     bottom_pipe = BottomPipe(
            #         pipe_change_x, screen_width=144, screen_height=128)
            #     top_pipe = TopPipe(pipe_change_x, screen_width=144,
            #                        screen_height=128, game=self)
            #     bottom_pipe.rect.x = 144
            #     top_pipe.rect.x = 144

            #     top_pipe.rect.y = top_height
            #     bottom_pipe.rect.y = 185 + top_height
            #     self.all_sprites_list.add(bottom_pipe)
            #     self.all_sprites_list.add(top_pipe)
            #     self.stage_sprites_list.add(top_pipe)
            #     self.stage_sprites_list.add(bottom_pipe)
            #     self.last_pipe = time_now

            self.all_sprites_list.update()
        else:
            if pygame.time.get_ticks() > 300 and pygame.time.get_ticks() < 2000:
                self.state = "PLAYING"

    def display_frame(self, screen):
        """ display everything to the screen for the game """
        screen.fill(WHITE)
        screen.blit(self.bg, (0, 0))
        self.all_sprites_list.remove(self.ground)
        self.all_sprites_list.add(self.ground)
        self.all_sprites_list.draw(screen)

        pygame.display.flip()


def main():
    # create new Serial object
    serial_arduino = Serial_Arduino()
    try:
        thread1 = thread.Thread(
            target=serial_arduino.read_loop_begin, args=())
        thread1.start()
    except ValueError as err:
        print(err)
        quit()

    # standard commands to start pygame
    pygame.init()
    # size of screen (can be adjusted)
    size = (144 * constants.sf, 256 * constants.sf)
    screen = pygame.display.set_mode(size)

    # control the frame rate and create game object
    clock = pygame.time.Clock()
    game = Game(size, 2000, serial_arduino)

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
