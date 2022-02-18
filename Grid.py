#!/usr/bin/env python
# Andy Luo and Matthew Simpson
# Bootleg Tetris
# To create a multiplayer Tetris experience

# import necessary modules
import pygame
from Block import Block
from random import randint

class Grid:
    """ A coloured grid of square cells in which player interactions with the game are possible.

    Static attributes:
        - COLS : The number of columns in the grid
        - ROWS : The number of rows in the grid
        - GRIDS : A list of each instance of Grid
        - BLOCKS : A list of the possible block types (e.g., I-block)
        - NEXT_BLOCKS : The list used in the generation of future blocks, obeying bag-like rules
        - LEVEL : The game's current level
        - SPEED : The game's current soft drop rate
        - __SCORE : The scoring increment values based on the quantity of lines immediately cleared
        
    Attributes:
        - __x : The x-coordinate of grid in the surface
        - __y : The y-coordinate of grid in the surface
        - __width : The width of the grid in pixels
        - __height : The height of the grid in pixels
        - __cellLength : The length of each square cell in pixel
        - __surface : The pygame surface that the grid will be drawn on
        - __grid_index : The index of this grid object in the static list GRIDS
        - block : The controllable block of this grid
        - hold : The block type of the block being held
        - __block_index : The The index of the current block in the static list NEXT_BLOCKS
        - timer_running : The boolean indicator of wether the timer is running
        - timer : The countdown timer for the block locking mechanism
        - drop_counter : A counter used to slow down the block's automatic drop rate
        - flag : An indicator for whether a method has been called atleast once or not
        - lose : The boolean value signifying the defeat of the player in control of this grid
        - win : A boolean indicator of whether the player has won or not
        - __is_held : The boolean value used to disable block holding more than once before a block locks into place
        - __lines_cleared : The quantity of lines cleared by the player
        - lines_received : The quantity of lines awaiting receival into the grid  
        - score : This player's current score
        - __grid_colours : 
        - __grid : A matrix of rectangles representing the grid
    """

    COLS = 10
    ROWS = 20
    
    GRIDS = []

    BLOCKS = ['i', 'j', 'l', 's', 'z', 't', 'o']
    NEXT_BLOCKS = []

    LEVEL = 0
    SPEED = 35

    __SCORE = {
        0 : 0, # 0 score, just in case
        1 : 40,
        2 : 100,
        3 : 300,
        4 : 1200
    }

    def __init__(self, x:int, y:int, height:int, surface):
        '''The constructor/initialization method of the grid and its attributes

        Parameters:
            - x : The x-coordinate of where the grid's top-left corner should be drawn
            - y : The y-coordinate of where the grid's top-left corner should be drawn
            - height : The drawn grid's height in pixels
            - surface : The surface to draw the grid on
        '''

        self.__x = x
        self.__y = y
        self.__width = height // 2
        self.__height = height
        self.__cellLength = height // Grid.ROWS
        self.__surface = surface
        self.__grid_index = len(Grid.GRIDS)

        Grid.GRIDS.append(self)
        
        # Temporary initialization
        self.block = Block('?', self)
        self.hold = Block('?', self)
        self.__block_index = 0

        self.resetGrid()
    
    def resetGrid(self):
        '''Resets the Grid attributes, excluding unchanged attributes, such as __surface'''

        # Temporarily reinitializing block 
        self.block.resetBlock('?')
        self.hold.resetBlock('?')
        self.__block_index = 0

        # Resetting timers
        self.timer_running = False
        self.timer = 0
        self.drop_counter = 0
        
        # Resetting win/loss flags
        self.flag = False
        self.lose = False
        self.win = False

        # Resetting statistics
        self.__is_held = False
        self.__lines_cleared = 0
        self.lines_received = 0
        self.score = 0

        # Resetting grid cell colours
        self.__grid_colours = [
            [Block.BLACK for j in range(Grid.COLS)]
            for i in range(Grid.ROWS)
        ]

        # Resetting grid cells
        self.__grid = [
            [
                pygame.Rect(
                    self.__x + j * self.__cellLength,
                    self.__y + i * self.__cellLength,
                    self.__cellLength,
                    self.__cellLength
                )
                for j in range(10)
            ]
        for i in range(20)
        ]

        Grid.LEVEL = 0
        Grid.SPEED = 35
        
        # Resetting drawn statistics
        self.drawLevel()
        self.drawHold()
        self.drawScore()
        self.drawLinesCleared()
        
        # Generating new block if there are none
        if len(Grid.NEXT_BLOCKS) > len(Grid.GRIDS):
            Grid.NEXT_BLOCKS = [Grid.BLOCKS[randint(0, len(Grid.BLOCKS) - 1)]]
        
        self.__getNextBlock()

    def drawHold(self):
        '''Draws text displaying the player's currently held block'''
        
        pygame.draw.rect(self.__surface, Block.BLACK, pygame.Rect(self.__x - 100, self.__y, 100, 100))
        font = pygame.font.SysFont(None, 20)
        hold_text = font.render(f'Holding {self.hold.getBlockType()}-block' if self.hold.getBlockType() != '?' else f'Holding nothing', False, Block.WHITE)
        self.__surface.blit(hold_text, (self.__x - 100, self.__y))
    
    def drawLevel(self):
        '''Draws text displaying the current level'''

        pygame.draw.rect(self.__surface, Block.BLACK, pygame.Rect(self.__x - 100, self.__y + self.__height // 1.5, 100, 30))
        font = pygame.font.SysFont(None, 20)
        level_text = font.render(f'level {Grid.LEVEL + 1}', False, Block.WHITE)
        self.__surface.blit(level_text, (self.__x - 100, self.__y + self.__height // 1.5))
    
    def drawLinesCleared(self):
        '''Draws text displaying the player's current quantity of cleared lines'''

        pygame.draw.rect(self.__surface, Block.BLACK, pygame.Rect(self.__x - 100, self.__y + self.__height - 40, 100, 30))
        font = pygame.font.SysFont(None, 20)
        lines_text = font.render('Lines:', False, Block.WHITE)
        lines_value = font.render(str(self.__lines_cleared), False, Block.WHITE)
        self.__surface.blit(lines_text, (self.__x - 100, self.__y + self.__height - 40))
        self.__surface.blit(lines_value, (self.__x - 100, self.__y + self.__height - 20))
    
    def drawScore(self):
        '''Draws text displaying the player's current score'''

        pygame.draw.rect(self.__surface, Block.BLACK, pygame.Rect(self.__x - 100, self.__y + self.__height // 1.25, 100, 30))
        font = pygame.font.SysFont(None, 20)
        score_text = font.render('Score:', False, Block.WHITE)
        score_value = font.render(str(self.score), False, Block.WHITE)
        self.__surface.blit(score_text, (self.__x - 100, self.__y + self.__height // 1.25))
        self.__surface.blit(score_value, (self.__x - 100, self.__y + self.__height // 1.25 + 20))

    def swapHold(self):
        '''Swaps the current block with the currently held block; a process called holding. Can only occur once a "turn" before it's locked in place for the remainder of this player's "turn"'''

        if not self.__is_held:
            self.__is_held = True

            self.block.eraseBlock()

            if self.hold.getBlockType() == '?':
                self.flag = False

                self.hold.resetBlock(self.block.getBlockType())

                self.__getNextBlock()
            else:
                temp = self.hold.getBlockType()
                
                self.hold.resetBlock(self.block.getBlockType())
                self.block.resetBlock(temp)
            
            self.drawHold()
    
    def getX(self):
        '''Returns the grid's x-coordinate '''

        return self.__x

    def setX(self, x):
        '''Sets the grid's x-coordinate to *x* if x is within the bounds of the surface'''

        if 0 <= x <= self.__surface.get_width() - self.__width:
            self.__x = x
    
    def getY(self):
        '''Returns the grid's y-coordinate'''

        return self.__y

    def setY(self, y):
        '''Sets the grid's y-coordiante to *y* if y is within the bounds of the surface'''
        if 0 <= y <= self.__surface.get_height() - self.__height:
            self.__y = y
    
    def getWidth(self):
        '''Returns the grid's width in pixels'''
        return self.__width

    def setWidth(self, width):
        '''Sets the grid's width to *width* if it is within the bounds of the surface'''
        if 0 <= width <= self.__surface.get_width():
            self.__width = width
            self.__height = width * 2
            self.__cellLength = width // Grid.COLS
    
    def getHeight(self):
        '''Returnes the grid's height in pixels'''
        return self.__height

    def setHeight(self, height):
        '''Sets the grid's height to *height* if it is within the bounds of the surface'''
        if 0 <= height <= self.__surface.get_height():
            self.__height = height
            self.__width = height // 2
            self.__cellLength = height // Grid.ROWs

    def drawGrid(self):
        '''If the the player has not won or lost, it draws the matrix of rectangles called __grid and draws the gridlines. If the player has lost, draws a big red rectangle with a label on it saying "You Lose". If the player has won, draws a big green rectangle with a label on it saying "You Win". '''
        
        # Checking if the game is still in progress
        if not (self.lose or self.win):
            for row in range(len(self.__grid)):
                for col in range(len(self.__grid[row])):
                    pygame.draw.rect(self.__surface, self.__grid_colours[row][col], self.__grid[row][col])

            for row in range(len(self.__grid) + 1):
                pygame.draw.rect(self.__surface, Block.WHITE, pygame.Rect(self.__x, self.__y + row * self.__cellLength, self.__width, 1))

            for col in range(len(self.__grid[0]) + 1):
                pygame.draw.rect(self.__surface, Block.WHITE, pygame.Rect(int(self.__x + col * self.__cellLength), self.__y, 1, self.__height))
        
        # Checking if this player lost
        elif self.lose:
            pygame.draw.rect(self.__surface, Block.RED, pygame.Rect(self.__x, self.__y, self.__width, self.__height))
            font = pygame.font.SysFont(None, 65)
            loss_text = font.render('You Lose', True, Block.WHITE)
            self.__surface.blit(loss_text, (self.__x , self.__y + self.__height // 2))
        
        # Checking if this player won
        elif self.win:
            pygame.draw.rect(self.__surface, Block.GREEN, pygame.Rect(self.__x, self.__y, self.__width, self.__height))
            font = pygame.font.SysFont(None, 65)
            win_text = font.render('You Win', True, Block.WHITE)
            self.__surface.blit(win_text, (self.__x , self.__y + self.__height // 2))
        
        # Updating window
        pygame.display.update()

    def getCell(self, row, col):
        '''Returns the grid's indexed cell and colour
        
        Parameters:
            - row : The row index of the cell
            - col : The column index of the cell
        
        Returns:
            tuple : The grid's indexed cell followed by its colour
        '''
        return self.__grid[row][col], self.__grid_colours[row][col]

    def setCell(self, row, col, colour):
        '''Sets the grid's indexed cell colour to *colour*
        
        Parameters:
            - row : The row index of the cell
            - col : The column index of the cell
            - colour : The colour the cell is to be coloured
        '''

        self.__grid_colours[row][col] = colour

    def drawBlock(self):
        '''Draws the current block on the grid'''

        for coords in self.block.getCoords():
            self.setCell(coords[0], coords[1], self.block.colour)
    
    def lock(self):
        '''Manages a timer for when the current block should be either movable or immovable ("locked") when on the ground. Generates a new block if this block is locked'''

        if self.timer >= Grid.SPEED * 3 and not self.block.collisionDetect(r_off=-1):
            
            # Clearing lines and generating block
            self.__getNextBlock()
            self.__clearLines()

            # Resetting affected attributes
            self.timer_running = False
            self.__is_held = False
            self.timer = 0

        else:
            # Starting lock timer
            self.timer_running = True
    
    def instantLock(self):
        '''Instantly locks the current block to the grid; clears and sends any complete lines. Generates a new block if this block is locked'''

        self.__getNextBlock()
        self.__clearLines()

        # Resetting affected attributes
        self.timer_running = False
        self.__is_held = False
        self.timer = 0
    
    def __receiveLines(self):
        '''Detects and collects which rows in the grid will be moved and moves them up by the number of line sent. The empty space will be replaced by gray blocks which represent garbage lines. There will be a randomly selected column in which there will be no garbage lines to represent messiness. If the sum of the number of rows moved and the number of lines recieved exeeds or equals the number of rows on the grid, the player loses.'''
        moved_rows = []

        self.lines_received = abs(self.lines_received) # TODO Further investigate debugging potential

        for i in range(Grid.ROWS):
            moveable = False
            
            for cell in self.__grid_colours[i]:
                if cell != Block.BLACK:
                    moveable = True
            
            if moveable:
                moved_rows.append(i)
        
        if moved_rows:
            random_col = randint(0, Grid.COLS - 1)

            if self.lines_received + len(moved_rows) >= Grid.ROWS:
                self.lose = True
            else:
                
                # Filling bottom area with garbage lines
                for row in range(moved_rows[0], moved_rows[0] + len(moved_rows)):
                    for col in range(Grid.COLS):
                        self.setCell(row - self.lines_received, col, self.__grid_colours[row][col])

                        if col != random_col:
                            self.setCell(row, col, Block.GRAY)
                        else:
                            self.setCell(row, col, Block.BLACK)

    def __clearLines(self):
        '''Finds and stores the rows which can be cleared and clears them while moving the rows above them down by the number of rows cleared. If rows were cleared, the __lines_cleared, score, LEVEL, and SPEED increase and visually update accordingly. Finally, reduces the lines recieved by the number of lines cleared. If the lines recieved attribute becomes negative, it sends lines back to the other grid using the GRIDS static list if the lines recieved are still positive, it calls the recieveLines method to recieve the lines and resets the lines recieved attribute'''
        cleared_rows = []
        
        for i in range(Grid.ROWS):
            clearable = True

            # Checking if row is clearable
            for cell in self.__grid_colours[i]:
                if cell == Block.BLACK:
                    clearable = False
            
            if clearable:
                cleared_rows.append(i)
        
        if cleared_rows:

            # Changing scoring attributes
            self.__lines_cleared += len(cleared_rows)
            Grid.LEVEL = self.__lines_cleared // 10

            # len(cleared_rows) <= 4, but similarly to tetr.io, we're protected if not
            self.score += (len(cleared_rows) // 5) * Grid.__SCORE[4] + Grid.__SCORE[len(cleared_rows) % 5]
            
            # Changing speed; capped at 1 fps
            if Grid.LEVEL <= 17:
                Grid.SPEED = 35 - 2 * Grid.LEVEL

            if cleared_rows[0] > 0:
                for row in range(cleared_rows[0] - 1, -1, -1):
                    for col in range (Block.COLS):
                        self.setCell(row + len(cleared_rows), col, self.__grid_colours[row][col])
                        self.setCell(row, col, Block.BLACK)

            # Visually updating scoring attributes
            self.drawLevel()
            self.drawScore()
            self.drawLinesCleared()

            # Reducing incoming lines
            self.lines_received -= len(cleared_rows)

            # Sending lines to other grid
            if self.lines_received < -1:
                Grid.GRIDS[1 - self.__grid_index].lines_received -= self.lines_received # Lines received is negative, remember

        elif self.lines_received > 0:
            self.__receiveLines()
            self.lines_received = 0

    def __getNextBlock(self):
        '''Replaces the current block with next block in NEXT_BLOCKS static list. If there are no blocks ahead in queue generates no blocks using the generateBlock method. Increases the block index attribute by 1.
        '''
        
        if self.flag:
            self.drawBlock()

        self.flag = True

        # Generating new block if necessary
        if self.__block_index == len(Grid.NEXT_BLOCKS):
            Grid.__generateBlock()

        # Setting block
        self.block.resetBlock(Grid.NEXT_BLOCKS[self.__block_index])

        for coords in self.block.getCoords():
            if self.__grid_colours[coords[0]][coords[1]] != Block.BLACK:
                self.lose = True

        self.__block_index += 1
    
    def __generateBlock():
        '''Based on certain conditions involving previously generated blocks, generates a new block and appends it to the static list BLOCKS'''
        
        blocks = Grid.BLOCKS.copy()

        try:
            
            # Allowing no 5 same blocks to be queued consecutively
            if len({Grid.NEXT_BLOCKS[i] for i in range(-4, 0)}) == 1:
                blocks.remove(Grid.NEXT_BLOCKS[-1])
            
            # Forcing at least one I-block within 12 queues of one another
            if [Grid.NEXT_BLOCKS[i] for i in range(-11, 0)].count('i') == 0:
                blocks = ['i']
            
        except IndexError:

            # Haven't generated enough blocks for these rules to apply yet
            pass
        
        # Appending generated block to queue
        Grid.NEXT_BLOCKS.append(blocks[randint(0, len(blocks) - 1)])
    
    def __str__(self):
        '''str override'''
        return f'Grid: ({self.__grid}), Grid colours: ({self.__gridColours}))'

    def __repr__(self):
        '''repr overide'''
        return f'Grid({self.__x}, {self.__y}, {self.__height})'
