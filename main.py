#!/usr/bin/env python
# Andy Luo and Matthew Simpson
# 335776720 and 340905215, respectfully
# Bootleg Tetris
# To create a multiplayer Tetris experience

# Player 1 controls
# W     : rotate CW
# A     : move down once
# S     : left
# D     : right
# T     : 180 rotation
# F     : rotate CCW
# G     : make block go brr to ground
# H     : hold block for later

# Player 2 controls
# UP    : rotate CW
# DOWN  : move down once
# LEFT  : left
# RIGHT : right
# I     : 180 rotation
# J     : rotate CCW
# K     : make block go brr to ground
# L     : hold block for later

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