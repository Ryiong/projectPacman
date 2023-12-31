# Set up pygame and modules
import pygame
from pygame.locals import *

pygame.init()

from Constants import *

# Create window
screen = pygame.display.set_mode(WINDOWSIZE, 0, 32)
pygame.display.set_caption("Pacman Game")

import random, copy

from Character import Character
from Pacman import Pacman
from Ghost import Ghost
from Walls import Walls
from Pellets import Pellets
from Sound import Sound
from Node import Node

# Create game objects
background = pygame.image.load("assets/img/bg.png").convert()
pacman = Pacman()
ghosts = [Ghost()]
walls = Walls.createList(Walls())
pellets_small = Pellets.createListSmall(Pellets())
pellets_large = Pellets.createListLarge(Pellets())
node = Node.createNode((Node()))
clock = pygame.time.Clock()
pygame.mixer.music.load("assets/sound/bg_music.mp3")
pygame.mixer.music.set_volume(1.5)


# Opening screen and music
Sound.channel.play(Sound.opening)
screen.fill((0, 0, 0))
screen.blit(background, (100, 0))
screen.blit(pacman.getScoreScreen(), (10, 10))
for p in pellets_small:
    screen.blit(Pellets.images[0], (p[0] + Pellets.shifts[0][0], p[1] + Pellets.shifts[0][1]))
for p in pellets_large:
    screen.blit(Pellets.images[1], (p[0] + Pellets.shifts[1][0], p[1] + Pellets.shifts[1][1]))
for g in ghosts:
    screen.blit(g.surface, g.rect)
screen.blit(pacman.surface, pacman.rect)
pygame.display.update()
while True:
    if not pygame.mixer.get_busy():
        break

# Game loop
keepGoing_game = True
while keepGoing_game:
    # Round loop
    keepGoing_round = True
    pygame.mixer.music.play(-1, 0.0)
    while keepGoing_round:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            # Quitting
            if event.type == QUIT:
                keepGoing_game = keepGoing_round = False

            # Arrow key down
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    pacman.moveUp = True
                    pacman.moveLeft = pacman.moveDown = pacman.moveRight = False
                    pacman.direction = 0
                elif event.key == K_LEFT:
                    pacman.moveLeft = True
                    pacman.moveUp = pacman.moveDown = pacman.moveRight = False
                    pacman.direction = 1
                elif event.key == K_DOWN:
                    pacman.moveDown = True
                    pacman.moveUp = pacman.moveLeft = pacman.moveRight = False
                    pacman.direction = 2
                elif event.key == K_RIGHT:
                    pacman.moveRight = True
                    pacman.moveUp = pacman.moveLeft = pacman.moveDown = False
                    pacman.direction = 3

            # Arrow key up
            elif event.type == KEYUP:
                pacman.moveUp = pacman.moveLeft = pacman.moveDown = pacman.moveRight = False

        # Move pacman rectangle
        pacman.move(walls)

        # Check if pacman must teleport to the other side
        pacman.teleport()

        # Animate and rotate pacman sprite
        pacman.getScreen()

        # Check if pacman has eaten any pellets and delete them
        Pellets.check(Pellets(), pellets_small, pellets_large, pacman, ghosts)




        # Check if blue ghosts must return to normal
        for g in ghosts:
            if g.isBlue:
                g.checkBlue()

        # Move ghosts
        for g in ghosts:
            g.move(walls, pacman)
            # Check if ghost must teleport to the other side
            g.teleport()



        # Draw screen
        screen.fill((0, 0, 0))
        screen.blit(background, (100, 0))
        screen.blit(pacman.getScoreScreen(), (10, 10))
        for p in pellets_small:
            screen.blit(Pellets.images[0], (p[0] + Pellets.shifts[0][0], p[1] + Pellets.shifts[0][1]))
        for p in pellets_large:
            screen.blit(Pellets.images[1], (p[0] + Pellets.shifts[1][0], p[1] + Pellets.shifts[1][1]))
        for g in ghosts:
            screen.blit(g.surface, g.rect)
        screen.blit(pacman.surface, pacman.rect)
        pygame.display.update()

        # Check if pacman collided with a ghost
        for g in ghosts[:]:
            if pacman.rect.colliderect(g.rect):
                if not g.isBlue:
                    keepGoing_round = False
                    pacman.lives -= 1
                    if pacman.lives == 0:
                        keepGoing_game = False
                    else:
                        Sound.channel.play(Sound.death)
                    break
                else:  # Ghost is blue
                    del ghosts[ghosts.index(g)]
                    pacman.score += 100
                    Sound.channel.play(Sound.eatGhost)


        # Check if pacman has eaten all the pellets
        else:
            if len(pellets_small) == 0 and len(pellets_large) == 0:
                keepGoing_game = keepGoing_round = False

    # Reset round
    pygame.mixer.music.stop()
    pacman.reset()
    for g in ghosts:
        g.reset()
    while True:
        if not pygame.mixer.get_busy():
            break

# End of game screen
screen.fill((0, 0, 0))
screen_temp = None


if pacman.lives == 0:  # Player loses
    Sound.channel.play(Sound.lose)
    screen_temp = pacman.getLosingScreen()

elif len(pellets_small) == 0 and len(pellets_large) == 0:  # Player wins
    Sound.channel.play(Sound.win)
    screen_temp = pacman.getWinningScreen()

if screen_temp != None:  # Player loses or wins (does not quit)
    rect_temp = screen_temp.get_rect()
    rect_temp.center = screen.get_rect().center
    screen.blit(screen_temp, rect_temp)
    pygame.display.update()

while True:
    if not pygame.mixer.get_busy():
        pygame.quit()
        break
