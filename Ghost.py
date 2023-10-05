import pygame
import copy
import heapq

from Character import Character
from Constants import *
from Node import Node
node = Node.createNode(Node())


class Ghost(Character):
    images = [pygame.image.load("assets/img/red-ball.png"),
              pygame.image.load("assets/img/unable-ball.png")]
    for i in range(len(images)):
        images[i].set_colorkey((0, 0, 0))
    ISBLUE_TIME = int(10 * FPS)
    ADD_TIME = int(30 * FPS)
    add_time = ADD_TIME

    def __init__(self):
        self.surface = Ghost.images[0]
        self.rect = self.surface.get_rect()
        self.rect.left = 315
        self.rect.top = 275
        self.speed = 1
        self.course = [0] * (50)
        self.isBlue = False
        self.isBlue_time = 0

    def makeBlue(self):
        self.isBlue = True
        self.isBlue_time = Ghost.ISBLUE_TIME  # number of frames
        self.surface = Ghost.images[1]
        self.course = []

    def makeNotBlue(self):
        self.surface = Ghost.images[0]
        self.course = []
        self.isBlue = False
        self.isBlue_time = 0

    def checkBlue(self):
        self.isBlue_time -= 1
        if self.isBlue_time <= 0:
            self.makeNotBlue()

    def reset(self):
        self.makeNotBlue()
        self.rect.left = 315
        self.rect.top = 275
        self.course = [0] * (50)

    def add(self, ghosts):
        Ghost.add_time -= 1
        if len(ghosts) == 0:
            if Ghost.add_time > int(Ghost.ADD_TIME / 10.0):
                Ghost.add_time = int(Ghost.ADD_TIME / 10.0)

        if Ghost.add_time <= 0:
            ghosts.append(Ghost())
            Ghost.add_time = Ghost.ADD_TIME

    def teleport(self):
        if self.rect.colliderect(pygame.Rect((100, 256), (6, 48))):
            self.rect.left += 400
        if self.rect.colliderect(pygame.Rect((549, 256), (6, 48))):
            self.rect.left -= 400

    def canMove_distance(self, direction, walls):
        test = copy.deepcopy(self)
        counter = 0
        while True:
            if not Character.canMove(test, direction, walls):
                break
            Character.move(test, direction)
            counter += 1
        return counter

    @staticmethod
    def heuristic(node, goal):
        return abs(node.rect.centerx - goal.rect.centerx) + abs(node.rect.centery - goal.rect.centery)

    def a_star(self, graph, start, goal):
        open_list = [(0, start)]
        closed_list = set()
        while open_list:
            _, current = heapq.heappop(open_list)
            if current == goal:
                path = []
                while current.parent:
                    path.append(current.parent.direction)
                    current = current.parent
                return path[::-1]
            closed_list.add(current)
            for neighbor in graph.neighbors(current):
                if neighbor in closed_list:
                    continue
                tentative_g_score = current.g_score + 1
                if neighbor not in open_list or tentative_g_score < neighbor.g_score:
                    neighbor.parent = current
                    neighbor.g_score = tentative_g_score
                    neighbor.f_score = tentative_g_score + self.heuristic(neighbor, goal)
                    if neighbor not in open_list:
                        heapq.heappush(open_list, (neighbor.f_score, neighbor))
        return []

    def find_shortest_path(self, ghost, pacman, walls):
        start_node = node.from_ghost(ghost)
        goal_node = node.from_pacman(pacman)
        return self.a_star(walls, start_node, goal_node)

    def move(self, walls, pacman):
        if len(self.course) > 0:
            if self.canMove(self.course[0], walls) or self.rect.colliderect(pygame.Rect((268, 248), (112, 64))):
                Character.move(self, self.course[0])
                del self.course[0]
            else:
                self.course = []
        else:
            path = self.find_shortest_path(self, pacman, walls)
            if path:
                self.course = path