#!/usr/bin/env python
# Andy Luo and Matthew Simpson
# Bootleg Tetris
# Creates a multiplayer Tetris experience

# import necessary modules
import pygame
from Grid import Grid
from Block import Block

def startGame(display):
    '''Is responsible for: parsing key inputs and redirecting them to controls within the game; for drawing and refreshing the display and grid; for checking whether a player has lost or not and prompting the respective message for such an event and; for the countdown timers of auto dropping and automatically locking the blocks to their respective grids'''
    
    frame_counter = 0

    grid_1 = Grid(100, 100, 400, display)
    grid_2 = Grid(500, 100, 400, display)

    keyPressedActions = {

        # Player 1 controls
        pygame.K_w     : grid_1.block.rotCW,
        pygame.K_a     : grid_1.block.moveLeft,
        pygame.K_s     : grid_1.block.moveDown,
        pygame.K_d     : grid_1.block.moveRight,
        pygame.K_t     : grid_1.block.rotFull,
        pygame.K_f     : grid_1.block.rotCCW,
        pygame.K_g     : grid_1.block.hardDrop,
        pygame.K_h     : grid_1.swapHold,

        # Player 2 controls
        pygame.K_KP8   : grid_2.block.rotCW,
        pygame.K_KP5   : grid_2.block.moveDown,
        pygame.K_KP4   : grid_2.block.moveLeft,
        pygame.K_KP6   : grid_2.block.moveRight,
        pygame.K_i     : grid_2.block.rotFull,
        pygame.K_j     : grid_2.block.rotCCW,
        pygame.K_k     : grid_2.block.hardDrop,
        pygame.K_l     : grid_2.swapHold

    }

    # Tracking in-game time
    clock = pygame.time.Clock()

    # Printing current event until display is exited
    while True:
        frame_counter += 1

        if grid_1.lose:
            grid_2.win = True
            font = pygame.font.SysFont(None, 30)
            new_game_text = font.render("Press Space To Restart", False, Block.WHITE)
            
            display.blit(new_game_text, (display.get_width() / 2.75, 50))
            
        elif grid_2.lose:
            grid_1.win = True
            font = pygame.font.SysFont(None, 30)
            new_game_text = font.render("Press Space To Restart", False, Block.WHITE)
            
            display.blit(new_game_text, (display.get_width() / 2.75, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit

            elif not (grid_1.win or grid_2.win):
                
                # Performing key press incurred operations
                if event.type == pygame.KEYDOWN:
                    if event.key in keyPressedActions:
                        keyPressedActions[event.key]()

                    else:
                        # Unknown key pressed
                        pass
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.draw.rect(display, Block.BLACK, pygame.Rect(display.get_width()/2.75, 50, 600, 50))

                    grid_1.resetGrid()
                    grid_2.resetGrid()
        
        if not (grid_1.win or grid_2.win):
            for g in Grid.GRIDS:
                g.drop_counter += 1

                # Delaying block movements
                if g.drop_counter >= Grid.SPEED:
                    g.drop_counter = 0

                    g.block.autoMoveDown()
                    g.drawLevel()

                # Continuing block auto-lock timer
                if g.timer_running:
                    g.timer += 1
                
                # Checking if block can move down
                elif g.block.collisionDetect(r_off=-1):
                    g.timer_running = True
        
        # Repainting grids
        for g in Grid.GRIDS:
            g.drawBlock()
            g.drawGrid()
        
        # Refreshing display at 60fps
        pygame.display.update()
        clock.tick(60)
