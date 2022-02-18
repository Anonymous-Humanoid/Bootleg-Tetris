#!/usr/bin/env python
# Andy Luo and Matthew Simpson
# Bootleg Tetris
# To create a multiplayer Tetris experience

class Block:
    ''' A collection of cells on a grid in the form of various tetrominoes in which the player can manipulate and control
    
    Static Attributes:
        - ROWS : The number of rows in a grid
        - COLS : The number of columns in a grid
        - CYAN : The rgb value for cyan
        - ORANGE : The rgb value for orange
        - BLUE : The rgb value for blue
        - MANGENTA : The rgb value for magenta
        - YELLOW : The rgb value for yellow
        - GREEN : The rgb value for green
        - RED : The rgb value for red
        - GRAY : The rgb value for gray
        - WHITE : The rgb value for white
        - BLACK : The rgb value for cyan
        - COLOURS : A dictionary matching various block types with their respective colours
        - __SHAPES : A dictionary mapping each block type to its respectively ordered rotational states
        - __STD_OFFSETS : A dictionary of block offsets used to find a valid block position near its current position immediately following the mapping of the old rotational state of the general block to its new rotation
        - __I_OFFSETS : A dictionary of block offsets used to find a valid block position near its current position immediately following the mapping of the old rotational state of the I-block to its new rotation

    Attributes:
        - __grid : The grid object that the block will be drawn on
        - __block_type : The type of tetrominoe that the block represents
        - __rot_state : The rotation state of the block
        - __row_offset : The number of rows the block is from its original starting row
        - __col_offset : The number of columns the block is from its original starting column
        - colour : The colour of the block
    '''
    
    ROWS = 20
    COLS = 10

    CYAN    = 0,   255, 255
    ORANGE  = 255, 165, 0
    BLUE    = 0,   0,   255
    MAGENTA = 255, 0,   255
    YELLOW  = 255, 255, 0
    GREEN   = 0,   255, 0
    RED     = 255, 0,   0
    GRAY    = 128, 128, 128
    WHITE   = 255, 255, 255
    BLACK   = 0,   0,   0
    
    COLOURS = {
        'i' : CYAN,
        'l' : ORANGE,
        'j' : BLUE,
        't' : MAGENTA,
        'o' : YELLOW,
        's' : GREEN,
        'z' : RED,
        '?' : GRAY
    }

    __SHAPES = {
        'i': [
            [[1, 0], [1, 1], [1, 2], [1, 3]],
            [[0, 2], [1, 2], [2, 2], [3, 2]],
            [[2, 0], [2, 1], [2, 2], [2, 3]],
            [[0, 1], [1, 1], [2, 1], [3, 1]]
        ],

        'l': [
            [[0, 2], [1, 0], [1, 2], [1, 1]],
            [[2, 2], [0, 1], [2, 1], [1, 1]],
            [[2, 0], [1, 0], [1, 2], [1, 1]],
            [[0, 0], [0, 1], [2, 1], [1, 1]]
        ],

        'j': [
            [[0, 0], [1, 0], [1, 1], [1, 2]],
            [[0, 2], [0, 1], [1, 1], [2, 1]],
            [[2, 2], [1, 0], [1, 1], [1, 2]],
            [[2, 0], [0, 1], [1, 1], [2, 1]]
        ],

        't': [
            [[1, 0], [0, 1], [1, 2], [1, 1]],
	        [[0, 1], [1, 2], [2, 1], [1, 1]],
	        [[1, 0], [2, 1], [1, 2], [1, 1]],
	        [[0, 1], [1, 0], [2, 1], [1, 1]]
        ],

        'o': [
            [[0, 0], [0, 1], [1, 0], [1, 1]]
        ],

        's': [
            [[1, 0], [0, 1], [0, 2], [1, 1]],
	        [[0, 1], [1, 2], [2, 2], [1, 1]],
	        [[2, 0], [2, 1], [1, 2], [1, 1]],
	        [[0, 0], [1, 0], [2, 1], [1, 1]]
        ],
        
        'z': [
            [[0, 0], [0, 1], [1, 2], [1, 1]],
	        [[0, 2], [1, 2], [2, 1], [1, 1]],
	        [[1, 0], [2, 1], [2, 2], [1, 1]],
	        [[0, 1], [1, 0], [2, 0], [1, 1]]
        ]
    }

    __STD_OFFSETS = {
        0 : {
            0 : ((0, 0),),
            1 : ((0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)),
            2 : ((0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)),
            3 : ((0, 0), (0, +1), (+1, +1), (-1, 1), (+1, 0), (-1, 0))
        },
        1 : {
            0 : ((0, 0), (+1, 0), (+1,-1), (0, +2), (1, +2)),
            1 : ((0, 0),),
            2 : ((0, 0), (-1, 0), (-1, 2), (-1, 1), (0, +2), (0, +1)),
            3 : ((0, 0), (+1, 0), (1, -1), (0, +2), (1, +2))
        },
        2 : {
            0 : ((0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)),
            1 : ((0, 0), (+1, 0), (+1, +2), (1, +1), (0, +2), (0, +1)),
            2 : ((0, 0),),
            3 : ((0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2))
        },
        3 : {
            0 : ((0, 0), (0, -1), (-1, -1), (1, -1), (-1, 0), (+1, 0)),
            1 : ((0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)),
            2 : ((0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)),
            3 : ((0, 0),)
        }
    }

    __I_OFFSETS = {
        0 : {
            0 : ((0, 0),),
            1 : ((0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)),
            2 : ((0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)),
            3 : ((0, 0), (0, +1), (+1, 1), (-1, +1), (+1, 0), (-1, 0))
        },
        1 : {
            0 : ((0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)),
            1 : ((0, 0),),
            2 : ((0, 0), (-1, 0), (-1, 2), (-1, +1), (0, +2), (0, +1)),
            3 : ((0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1))
        },
        2 : {
            0 : ((0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)),
            1 : ((0, 0), (+1, 0), (+1, 2), (+1, +1), (0, +2), (0, +1)),
            2 : ((0, 0),),
            3 : ((0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2))
        },
        3 : {
            0 : ((0, 0), (0, -1), (-1, -1), (1, -1), (-1, 0), (+1, 0)),
            1 : ((0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)),
            2 : ((0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)),
            3 : ((0, 0),)
        }
    }

    def __init__(self, block_type, grid, rot_state=0):
        '''Constructs a Block object whose grid is *grid*, block type is *block_type*, rotation state is *rot_state*, is offset by 3 columns and whose colour is determined by its block type'''

        self.__grid = grid

        self.resetBlock(block_type, rot_state=rot_state)
    
    def moveDown(self):
        '''Moves the block down by 1 row from player command. If the block cannot move, it instantly locks the block in place and returns False. If it can move, it restarts the lock countdown timer and turns it off and returns True'''

        self.eraseBlock()
        
        # Checking if block can move down
        if not self.__move(row=-1):
            self.__grid.instantLock()
            
            return False

        # Resetting auto-lock timers
        self.__grid.drop_counter = 0
        self.__grid.timer_running = False
        self.__grid.timer = 0

        return True
    
    def autoMoveDown(self):
        '''Moves the block down by 1 row. If the block cannot move, it starts the countdown timer and checks if the block can be locked onto the grid and returns false. If it can move, it restarts the lock countdown timer and turns it off and reurns true. This method differs from the moveDown method, as it is used by the driving Tetris class to automatically soft-drop the block'''

        self.eraseBlock()
        
        # Starting auto-lock timer if block can't move down
        if not self.__move(row=-1):
            self.__grid.timer_running = True
            self.__grid.lock()
            return False

        # Resetting auto-lock timers
        self.__grid.drop_counter = 0
        self.__grid.timer_running = False
        self.__grid.timer = 0

        return True
    
    def moveLeft(self):
        '''Moves the block to the left by 1 column using the move method. Will not do anything if the block cannot move'''

        self.eraseBlock()
        
        return self.__move(col=-1)
    
    def moveRight(self):
        '''Moves the block to the right by 1 column using the move method. Will not do anything if the block cannot move'''

        self.eraseBlock()
        
        return self.__move(col=1)
    
    def hardDrop(self):
        '''Continuously moves the block down with the moveDown method until the block cannot move down anymore and locks the block in place'''

        while self.moveDown():
            pass
    
    def rotCW(self):
        '''Rotates the block clockwise by 90 degrees if the block can rotate using the rotate method'''

        self.__rotate(1)
    
    def rotCCW(self):
        '''Rotates the block counter clockwise by 90 degrees if the block can rotate using the rotate method'''
        
        self.__rotate(3)
    
    def rotFull(self):
        '''Rotates the block by 180 degrees if the block can rotate using the rotate method'''
        
        self.__rotate(2)
    
    def __rotate(self, rot_state_change):
        '''Rotates the block in terms of the rotational state change *rot_state_change*, if possible. Also returns a boolean value based on whether rotation is possible or not.
        
        Parameters:
            - rot_state_change : The quantity by which increment the rotational state in a wraparound format
        '''
        
        # Erasing block from grid
        self.eraseBlock()

        # Cycling rotational state
        old_state = self.__rot_state
        self.__rot_state += rot_state_change
        self.__rot_state %= len(Block.__SHAPES[self.__block_type])

        # Getting block-type dependant offsets
        offsets = Block.__I_OFFSETS if self.__block_type == 'i' else Block.__STD_OFFSETS

        # Performing collision detections
        for offset in offsets[old_state][self.__rot_state]:
            if self.collisionDetect(r_off=offset[1], c_off=offset[0]):
                
                # Rotation successful; shifting block
                self.__move(row=offset[1], col=offset[0])

                self.__grid.drawBlock()
                
                return True
        
        # Rotation unsuccessful; resetting block rotation
        self.__rot_state = old_state

        self.__grid.drawBlock()

        return False
    
    def __move(self, row=0, col=0):
        ''' If the block is not colliding with another block or the grid's edges, it decreases the row offset by *row* and column offset by *col* to move the block and returns True. If the block is colliding with another or the edges, it returns False'''
        if not self.collisionDetect(r_off=row, c_off=col):
            return False
        
        # Offsetting block position (subtraction is performed to force origin cell to bottom-left hand corner)
        self.__row_offset -= row
        self.__col_offset += col

        return True
    
    def collisionDetect(self, r_off=0, c_off=0):
        '''Temporarily offsets the block by the *r_off* and *c_off* to get the coordinates at that position and checks if the coordinates of that possition are within the grid and if they overlap with existing blocks. If they overlap or are not in the grid, it returns False, otherwise it returns True'''

        # Temporarily offsetting block
        self.__row_offset -= r_off
        self.__col_offset += c_off

        # Getting new offset cell coordinates
        coordinates = self.getCoords()

        # Resetting block offset
        self.__row_offset += r_off
        self.__col_offset -= c_off
        
        # Performing collision detection with new cell coordinates
        for coords in coordinates:

            # Checking if block position is in grid boundaries
            if not (0 <= coords[0] < Block.ROWS and 0 <= coords[1] < Block.COLS):
                return False
            
            # Searching for non-empty spaces
            elif self.__grid.getCell(coords[0], coords[1])[1] != Block.BLACK:
                return False

        return True
    
    def getBlockType(self):
        '''Returns the block type
        
        Returns:
            string : This block's block type
        '''

        return self.__block_type

    def eraseBlock(self):
        '''Removes the block from the grid by changing all the cells back to black'''

        for coords in self.getCoords():
            self.__grid.setCell(coords[0], coords[1], Block.BLACK)

    def getCoords(self):
        '''Returns the current coordinates of the block'''

        return [[base_coords[0] + self.__row_offset, base_coords[1] + self.__col_offset] for base_coords in Block.__SHAPES[self.__block_type][self.__rot_state]]

    def resetBlock(self, block_type, rot_state=0):
        '''Resets the block by changing block type to *block_type*, rotation state to *rot_state* and other attributes to their base values'''

        self.__block_type = block_type.lower()
        self.__rot_state = rot_state
        self.__row_offset = 0
        self.__col_offset = 3
        self.colour = Block.COLOURS[self.__block_type]
    
    def __str__(self):
        '''str override '''
        return f'Block type: {self.block_type}, Block color: {self.__block_color}, Coordinates: {self.getCoords()}, Row offset: {self.__row_offset}, Column offset: {self.__col_offset}, Rotational state: {self.__rot_state}'

    def __repr__(self):
        '''repr override '''
        return f"Block('{self.block_type}, {self.__grid}, rot_state={self.rot_state}')"
