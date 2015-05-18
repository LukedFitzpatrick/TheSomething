from pygame.locals import *

# level/display constants
NUM_LEVEL_TILES_X = 35
NUM_LEVEL_TILES_Y = 19

TILE_WIDTH = 32
TILE_HEIGHT = 32



GAME_SCREEN_WIDTH = NUM_LEVEL_TILES_X * TILE_WIDTH
GAME_SCREEN_HEIGHT = NUM_LEVEL_TILES_Y * TILE_HEIGHT

BOTTOM_BAR_HEIGHT = 32
BOTTOM_BAR_WIDTH = NUM_LEVEL_TILES_X * TILE_WIDTH
BOTTOM_BAR_START = GAME_SCREEN_HEIGHT

SCREEN_WIDTH = NUM_LEVEL_TILES_X * TILE_WIDTH
SCREEN_HEIGHT = NUM_LEVEL_TILES_Y * TILE_HEIGHT + BOTTOM_BAR_HEIGHT

FAST_RATE = 60
SLOW_RATE = 5

# player/agent constants

RIGHT_KEY = K_d
LEFT_KEY = K_a
JUMP_KEY = K_w
DOWN_KEY = K_s

PLAYER_XV_INCREMENT = 0.5
PLAYER_XV_DASH_INCREMENT = 5
AGENT_XV_INCREMENT = 0.18

GRAVITY_INCREMENT = 0.3

JUMP_INCREMENT = 8
DOUBLE_JUMP_INCREMENT = 10
AGENT_JUMP_INCREMENT = 6

DOUBLE_TAP_FRAMES = 5


FRICTION = 0.05

COLLISION_BLOCK = 20

MAXIMUM_VELOCITY = 32

PUFF_THRESHOLD = 2

PLAYER_BOUNCE_FACTOR = 0.01

RAGE_DECREMENT = 0.03
RAGE_INCREMENT = 10

CLOSENESS_TRIGGER = 40

AGENT_LOS = 80
AGENT_FAILURE_COUNTDOWN = 150

# Graphical options
TRACE_ON = True
BOUNDING_BOX_ON = False
AI_INDICATORS_ON = False

#GLYPHS

MAGNET_DURATION = 500

# Peace
GLYPH_BULLET_TIME = False  # implemented  # passive
GLYPH_JUMPER = False       # implemented  # passive
GLYPH_DASH = False         # implemented  # double tap direction
GLYPH_MAGNET = True                       # space
GLYPH_SMOKESCREEN = False                 # space

# Rage
GLYPH_ARMOR = False                       # passive
GLYPH_INFECTION = False                   # passive
GLYPH_CHARGE = False                      # double tap direction
GLYPH_FIRE = False                        # space
GLYPH_NUKE = False                        # space 
GLYPH_VOID = False                        # space
GLYPH_GLUE = False                        # space   




