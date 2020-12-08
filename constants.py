import pygame
import math

# Width of an individual tile unit (in points)
TILE_WIDTH          =  16

# Width, height of chunk (in tiles)
CHUNK_WIDTH         =  16
CHUNK_HEIGHT        =  512

# Width, height of chunk (in points)
CHUNK_HEIGHT_P      =  CHUNK_HEIGHT * TILE_WIDTH
CHUNK_WIDTH_P       =  CHUNK_WIDTH * TILE_WIDTH

# Constants for chunk generation
BEDROCK_LOWER_X     =  0.1
BEDROCK_LOWER_Y     =  0.2

BEDROCK_UPPER_X     =  0.1
BEDROCK_UPPER_Y     =  0.2

CAVE_X              =  0.05
CAVE_Y              =  0.1

UNDERGROUND_X       =  0.05
UNDERGROUND_Y       =  0.1

# Infinity
#generateBigNum = lambda numBits : 1<<(numBits-1)|generateBigNum(numBits-1) if(numBits >= 1) else 1
INF = math.inf #generateBigNum(64)

## Constants for camera
LERP_C              =  0.025

## Constants for entity and physics (time_unit = seconds, length_unit = points)
GRAVITY_ACC         =  0.98
JUMP_VEL            =  0.6
SCALE_VEL           =  TILE_WIDTH * 16    # 16 is number of tiles to move
AIR_FRICTION        =  0.2
UP_ACC              =  0.8
DOWN_ACC            =  0.8
DEFAULT_FRICTION    =  1
MAX_ACC             =  1
MAX_VEL             =  1
PLYR_WIDTH          =  TILE_WIDTH       # 36
PLYR_HEIGHT         =  TILE_WIDTH<<1    # 54
INV_COLS            =  10
INV_ROWS            =  3

# List of attributes (constants)

# Tiles, items, entities
ID                  = 0

# Tiles
LUMINOSITY          = 1
FRICTION            = 2
BREAKTIME           = 3
HEALTH              = 4
INFLAMMABLE         = 5
LTIMPERMEABILITY    = 6
DROPS               = 7

# items
PLACEABLE           = 8
PLACES              = 9
DAMAGE              = 10
MAX_STACK           = 11

# entities
WEIGHT              = 12
