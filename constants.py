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

