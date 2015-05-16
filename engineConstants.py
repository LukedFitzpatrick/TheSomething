from pygame.locals import *

# level/display constants
NUM_LEVEL_TILES_X = 35
NUM_LEVEL_TILES_Y = 19

TILE_WIDTH = 32
TILE_HEIGHT = 32

BOTTOM_BAR_HEIGHT = 128
BOTTOM_BAR_WIDTH = NUM_LEVEL_TILES_X * TILE_WIDTH

SCREEN_WIDTH = NUM_LEVEL_TILES_X * TILE_WIDTH
SCREEN_HEIGHT = NUM_LEVEL_TILES_Y * TILE_HEIGHT + BOTTOM_BAR_HEIGHT

GAME_SCREEN_WIDTH = NUM_LEVEL_TILES_X * TILE_WIDTH
GAME_SCREEN_HEIGHT = NUM_LEVEL_TILES_Y * TILE_HEIGHT

FRAME_RATE = 60

# player constants

RIGHT_KEY = K_d
LEFT_KEY = K_a
JUMP_KEY = K_w

PLAYER_XV_INCREMENT = 0.5
GRAVITY_INCREMENT = 0.3
JUMP_INCREMENT = 8

MAXIMUM_VELOCITY = 32

PLAYER_BOUNCE_FACTOR = 0.1

# Debugging/Utility Constants
TRACE_ON = True
