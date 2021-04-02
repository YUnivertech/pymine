import math
import pygame
import pygame.freetype
import enum

# Infinity
INF                 = math.inf

# Width of a tile in points (1 point = 1 pixel on display)
TILE_WIDTH          = 16

# Width and height of a chunk (in tiles)
CHUNK_WIDTH         = 16
CHUNK_HEIGHT        = 512

# Width and height of a chunk (in points)
CHUNK_WIDTH_P       = TILE_WIDTH * CHUNK_WIDTH
CHUNK_HEIGHT_P      = TILE_WIDTH * CHUNK_HEIGHT

# Constant to determine the linear interpolation of the camera
LERP_C              = 0.025

# Font for displaying item names in inventory
INV_FONT            = pygame.freetype.SysFont( 'Consolas' , size = 16 , bold = True )

# import math, pygame.freetype
#
# # Initalize pygame and start the clock
# pygame.init()
# clock = pygame.time.Clock()
#
# # Width of an individual tile unit (in points)
# TILE_WIDTH       = 16
#
# # Width, height of chunk (in tiles)
# CHUNK_WIDTH      = 16
# CHUNK_HEIGHT     = 512
#
# # Width, height of chunk (in points)
# CHUNK_HEIGHT_P   = CHUNK_HEIGHT * TILE_WIDTH
# CHUNK_WIDTH_P    = CHUNK_WIDTH * TILE_WIDTH
#
# # Constants for chunk generation
# BEDROCK_LOWER_X  = 0.1
# BEDROCK_LOWER_Y  = 0.2
# BEDROCK_UPPER_X  = 0.1
# BEDROCK_UPPER_Y  = 0.2
# CAVE_X           = 0.05
# CAVE_Y           = 0.1
# UNDERGROUND_X    = 0.05
# UNDERGROUND_Y    = 0.1
#
# # Infinity
# INF = math.inf
#
# # Constants for camera
# LERP_C           = 0.025
#
# # Constants for entity and physics (time_unit = seconds, length_unit = points)
# GRAVITY_ACC      = 0.98
# JUMP_VEL         = 1
# SCALE_VEL        = TILE_WIDTH * 12    # 16 is number of tiles to move
# AIR_FRICTION     = 0.2
# DEFAULT_FRICTION = 0.5
# MAX_ACC          = 1
# MAX_VEL          = 1
# HITBOX_WIDTH     = TILE_WIDTH-2
# HITBOX_HEIGHT    = TILE_WIDTH+6
# PLYR_WIDTH       = TILE_WIDTH+2      # 36
# PLYR_HEIGHT      = TILE_WIDTH+14    # 54
# PLYR_RANGE       = 4*TILE_WIDTH
# INV_COLS         = 10
# INV_ROWS         = 3
#
# # Tiles, items, entities
# ID               = 0
#
# # Tiles
# LUMINOSITY       = 1
# FRICTION         = 2
# BREAKTIME        = 3
# HEALTH           = 4
# INFLAMMABLE      = 5
# LTIMPERMEABILITY = 6
# DROPS            = 7
#
# # items
# PLACEABLE        = 8
# PLACES           = 9
# DAMAGE           = 10
# MAX_STACK        = 11
#
# # entities
# WEIGHT           = 12
# INV_FONT         = pygame.freetype.SysFont('Consolas', size=16, bold=True)
# SC_DISPLAY_FONT  = pygame.freetype.SysFont('Consolas', size=20, bold=True)