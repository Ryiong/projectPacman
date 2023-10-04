import pygame

import copy

from Character import Character
from Constants import *
from Node import Node
node = Node.createNode(Node())


class Ghost(Character):
    images = [pygame.image.load("assets/img/red-ball.png"), \
              pygame.image.load("assets/img/unable-ball.png")]
    for i in range(len(images)):
        images[i].set_colorkey((0, 0, 0))
    ISBLUE_TIME = int(10 * FPS)
    ADD_TIME = int(30 * FPS)
    add_time = ADD_TIME

    def __init__(self):
        '''in - (self)'''
        self.surface = Ghost.images[0]
        self.rect = self.surface.get_rect()
        self.rect.left = 310
        self.rect.top = 275
        self.speed = 1
        self.course = [0] * (50)
        self.isBlue = False
        self.isBlue_time = 0

    def makeBlue(self):
        '''in - (self)
        Changes ghost into a blue ghost.'''
        self.isBlue = True
        self.isBlue_time = Ghost.ISBLUE_TIME  # number of frames
        self.surface = Ghost.images[1]
        self.course = []

    def makeNotBlue(self):
        '''in - (self)
        Changes blue ghost into a regular ghost.'''
        self.surface = Ghost.images[0]
        self.course = []
        self.isBlue = False
        self.isBlue_time = 0

    def checkBlue(self):
        '''in - (self)
        Checks if the ghost should return to normal, and does if necessary.'''
        self.isBlue_time -= 1
        if self.isBlue_time <= 0:
            self.makeNotBlue()

    def reset(self):
        '''in - (self)
        Resets ghost's position and makes it regular (not blue).'''
        self.makeNotBlue()
        self.rect.left = 315
        self.rect.top = 275
        self.course = [0] * (50)

    # def add(self, ghosts):
    #     '''in - (self, list of ghosts)
    #     Determines is a ghost must be added, adds it to the list, and resets the add ghost timer.
    #     Subtracts from the add ghost timer is no ghost is added.'''
    #     Ghost.add_time -= 1
    #     if len(ghosts) == 0:
    #         if Ghost.add_time > int(Ghost.ADD_TIME / 10.0):
    #             Ghost.add_time = int(Ghost.ADD_TIME / 10.0)
    #
    #     if Ghost.add_time <= 0:
    #         ghosts.append(Ghost())
    #         Ghost.add_time = Ghost.ADD_TIME

    def teleport(self):
        '''in - (self)
        Determines if pacman collided with one of teleport locations and moves him.'''
        if self.rect.colliderect(pygame.Rect((100, 256), (6, 48))):
            self.rect.left += 400
        if self.rect.colliderect(pygame.Rect((549, 256), (6, 48))):
            self.rect.left -= 400

    def canMove_distance(self, direction, walls):
        '''in - (self, direction, list of walls)
        Determines the number of steps the ghost can take in the specified direction.
        out - int'''
        test = copy.deepcopy(self)
        counter = 0
        while True:
            if not Character.canMove(test, direction, walls):
                break
            Character.move(test, direction)
            counter += 1
        return counter

    # def move(self, walls, pacman):
    #
