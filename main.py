#!/usr/bin/env python
# Andy Luo and Matthew Simpson
# Bootleg Tetris
# Creates a multiplayer Tetris experience

# Player 1 controls
# W     : rotate CW
# A     : move down once
# S     : left
# D     : right
# T     : 180 rotation
# F     : rotate CCW
# G     : make block go brr to ground
# H     : hold block for later

# Player 2 controls (assumes numlock is off)
# NUM 8 : rotate CW
# NUM 5 : move down once
# NUM 4 : left
# NUM 6 : right
# I     : 180 rotation
# J     : rotate CCW
# K     : make block go brr to ground
# L     : hold block for later

# Hiding pygame support message
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

# import necessary modules
import pygame
from Tetris import startGame

if __name__ == '__main__':
    '''Runs the game of Tetris as well as initializing Pygame and the game display'''
    
    # Starting up PyGame
    pygame.init()
    pygame.font.init()

    # Setting up display (750 x 500px)
    display = pygame.display.set_mode((750, 500))
    pygame.display.set_caption('Tetris')

    # Running the game
    startGame(display)
