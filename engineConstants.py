from pygame.locals import *

# level/display constants
NUM_LEVEL_TILES_X = 50
NUM_LEVEL_TILES_Y = 30

TILE_WIDTH = 16
TILE_HEIGHT = 16

GAME_SCREEN_WIDTH = NUM_LEVEL_TILES_X * TILE_WIDTH
GAME_SCREEN_HEIGHT = NUM_LEVEL_TILES_Y * TILE_HEIGHT

GLYPH_WIDTH = 32
GLYPH_HEIGHT = 32

BOTTOM_BAR_HEIGHT = 32
BOTTOM_BAR_WIDTH = NUM_LEVEL_TILES_X * TILE_WIDTH
BOTTOM_BAR_START = GAME_SCREEN_HEIGHT

GLYPHLOCATIONX = 60
GLYPHLOCATIONY = GAME_SCREEN_HEIGHT+BOTTOM_BAR_HEIGHT + 5
GLYPHBARHEIGHT = 32 + 5

SCREEN_WIDTH = NUM_LEVEL_TILES_X * TILE_WIDTH
SCREEN_HEIGHT = NUM_LEVEL_TILES_Y * TILE_HEIGHT + BOTTOM_BAR_HEIGHT + GLYPHBARHEIGHT

FAST_RATE = 60
SLOW_RATE = 16

# player/agent constants

RIGHT_KEY = K_d
LEFT_KEY = K_a
JUMP_KEY = K_w
DOWN_KEY = K_s
GLYPH_NEXT_KEY = K_e
GLYPH_PREVIOUS_KEY = K_q

PLAYER_XV_INCREMENT = 0.15
PLAYER_XV_DASH_INCREMENT = 3

AGENT_XV_INCREMENT = 0.05
AGENT_XV_VARIATION = 10

GRAVITY_INCREMENT = 0.3

JUMP_INCREMENT = 5
DOUBLE_JUMP_INCREMENT = 8
AGENT_JUMP_INCREMENT = 8

DOUBLE_TAP_FRAMES = 5

FRICTION = 0.03

COLLISION_BLOCK = 20

MAXIMUM_VELOCITY = 32

PUFF_THRESHOLD = 2

PLAYER_BOUNCE_FACTOR = 0.01

RAGE_DECREMENT = 0.03
RAGE_INCREMENT = 10

CLOSENESS_TRIGGER = 40

AGENT_LOS = 100
AGENT_FAILURE_COUNTDOWN = 150

AGENT_WIDTH = 8
AGENT_HEIGHT = 16

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16

AGENT_SPAWN_FRAMES = 1000

# Graphical options
TRACE_ON = False
BOUNDING_BOX_ON = False
AI_INDICATORS_ON = False
SUBTLE_AI_INDICATORS_ON = True

# GLYPHS
MAGNET_DURATION = 400
SMOKE_SCREEN_DURATION = 100

ARMOUR_KILL_FREQUENCY = 3 # means 1 in 3 enemies are killed by armour
ARMOUR_KILL_RAGE_INCREMENT = 4

INFECTION_DURATION = 400
INFECTION_KILL_RAGE_INCREMENT = 3

CHARGE_DURATION = 20 # how long you are lethal for
CHARGE_KILL_RAGE_INCREMENT = 2

FIRE_DURATION = 50
FIRE_KILL_RAGE_INCREMENT = 1

NUKE_KILL_RAGE_INCREMENT = 5

VOID_DURATION = 400
VOID_KILL_RAGE_INCREMENT = 5

# Peace
GLYPH_BULLET_TIME = 0  # implemented  # passive
GLYPH_JUMPER = 1      # implemented  # passive
GLYPH_DASH = 2      # implemented  # double tap direction
GLYPH_MAGNET = 3       # implemented  # space
GLYPH_SMOKESCREEN = 4 # implemented     # space

# Rage
GLYPH_ARMOUR = 5    #implemented     # passive
GLYPH_INFECTION = 6    #implemented     # passive
GLYPH_CHARGE = 7        #implemented     # double tap direction
GLYPH_FIRE = 8   #implemented              # space
GLYPH_NUKE = 9   #implemented              # space 
GLYPH_VOID = 10    #implemented              # space   


#Hello!
