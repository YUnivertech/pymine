import enum
import math

import pygame
import pygame.freetype

import time

log_file = open('log_file.txt', 'w')
# The debug verbosity level, can be from 0 to 4 (both inclusive)
DBG                 = 0


def dbg_debug( *args , **kwargs ):    # Messages which devs can see during debug
    dbg( 2 , *args , **kwargs )


def dbg_warning( *args , **kwargs ):  # Messages which devs can see for critical information
    dbg( 3 , *args , **kwargs )


def dbg( msg_priority , *args , **kwargs ):
    if msg_priority < DBG:
        print( *args, **kwargs )

# Utility functions to get time
get_time_us = lambda : time.time_ns() // 1_000_000
get_time_s = lambda : get_time_us() / 1_000

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

# Height at which space and overworld start
SPACE_START         = ( CHUNK_HEIGHT - 1 - 128 ) * TILE_WIDTH
OVER_START          = 128 * TILE_WIDTH

# Constant to determine the linear interpolation of the camera
LERP_C              = (10 / 3) * 3

# Constants for entity and physics (time_unit = seconds, length_unit = points)
GRAVITY_ACC         = 0.98
JUMP_VEL            = 1
SCALE_VEL           = TILE_WIDTH * 12    # 16 is number of tiles to move
AIR_FRICTION        = 0.2
DEFAULT_FRICTION    = 0.5
MAX_ACC             = 1
MAX_VEL             = 1
HITBOX_WIDTH        = TILE_WIDTH-2
HITBOX_HEIGHT       = TILE_WIDTH+6
PLYR_WIDTH          = TILE_WIDTH+2      # 36
PLYR_HEIGHT         = TILE_WIDTH+14    # 54
PLYR_RANGE          = 4 * TILE_WIDTH
INV_COLS            = 10
INV_ROWS            = 3
# HAND_DAMAGE         = 33
HAND_DAMAGE         = 10000


ALLOWED_CHARS       = [chr(ord('a') + i) for i in range(26)] + [chr(ord('A') + i) for i in range(26)] + [str(i) for i in range(10)]

pygame.freetype.init()
# # entities
# WEIGHT           = 12
INV_FONT         = pygame.freetype.SysFont('Consolas', size=16, bold=True)
INV_COLOR        = ( 0, 0, 0 )
# SC_DISPLAY_FONT  = pygame.freetype.SysFont('Consolas', size=20, bold=True)

# Global utility functions
get_curr_chunk     = lambda p: int( math.floor( p[0] / CHUNK_WIDTH_P ) )
get_x_pos_chunk    = lambda p: int( p[0] // TILE_WIDTH - get_curr_chunk( p ) * CHUNK_WIDTH )
get_y_pos_chunk    = lambda p: int( p[1] // TILE_WIDTH )
pos_ceil           = lambda x, y : ( x + y - 1 ) // y

# ! ----------------------------------------------------------------

class tile_attr( enum.Enum ):

    # Light related attributes
    LUMINOSITY      = 0
    LTIMPERM        = 1

    # Health related attributes
    HEALTH          = 2
    INFLAMMABLE     = 3

    # Physics related attributes
    FRICTION        = 4

    # Gameplay related attributes
    DROPS           = 5
    TYPE            = 6
    DROP_ITEM       = 7


class tile_modifs( enum.Enum ):

    # Modifier to indicate tile is cracked
    crack           = 0

    # Modifier to indicate tile is on fire
    on_fire         = 1
    fire            = 2

    # Modifier to indicate presence of fluid in tile
    water           = 3
    lava            = 4


class tiles( enum.Enum ):

    air                  = 0

    # tiles for dirt and grass blocks
    grass                = 1
    browndirt            = 2
    snowygrass           = 3
    leaves               = 4

    # wood
    junglewood           = 10
    junglewood_plank     = 11
    oakwood              = 12
    oakwood_plank        = 13
    borealwood           = 14
    borealwood_plank     = 15
    pinewood             = 16
    pinewood_plank       = 17
    cactuswood           = 18
    cactuswood_plank     = 19
    palmwood             = 20
    palmwood_plank       = 21

    # metals
    cosmonium_ore        = 30
    cosmonium            = 32
    unobtanium_ore       = 33
    unobtanium           = 35
    platinum_ore         = 36
    platinum             = 38
    gold_ore             = 39
    gold                 = 41
    iron_ore             = 42
    iron                 = 44
    copper_ore           = 45
    copper               = 47

    # non-metals
    diamond_ore          = 50
    diamond_block        = 51
    hellstone            = 52
    adamantite           = 53
    obsidian             = 54
    bedrock              = 55

    # tiles for the stones
    granite              = 60
    quartz               = 61
    limestone            = 62
    greystone            = 63
    sandstone            = 64

    # tiles for transition blocks
    gravel               = 70
    coal                 = 71

    # clay
    clay                 = 72
    red_clay             = 73

    # sand
    sand                 = 74

    # snow
    snow                 = 75
    ice                  = 76

    # glass tiles
    glasspane            = 77
    glasswindow          = 78

    # door
    wood_door_upper      = 80
    wood_door_lower      = 81
    iron_door_upper      = 82
    iron_door_lower      = 83
    gold_door_upper      = 84
    gold_door_lower      = 85
    platinum_door_upper  = 86
    platinum_door_lower  = 87

    # bed
    bed_head             = 88
    bed_tail             = 89

    # torch
    torch                = 90

    # interactive tiles
    crafting_table       = 100
    furnace              = 101
    chest                = 102


# Set of all blocks which are of wood type
wood_list           = { tiles.junglewood, tiles.junglewood_plank, tiles.oakwood, tiles.oakwood_plank,
                        tiles.borealwood, tiles.borealwood_plank, tiles.pinewood, tiles.pinewood_plank,
                        tiles.cactuswood, tiles.cactuswood_plank, tiles.palmwood, tiles.palmwood_plank }

# Set of all blocks which are of stone type
stone_list          = { tiles.granite, tiles.quartz, tiles.limestone, tiles.greystone, tiles.sandstone }

# Set of all blocks which are of metal type
metal_list          = { tiles.cosmonium_ore, tiles.cosmonium, tiles.unobtanium_ore, tiles.unobtanium,
                        tiles.platinum_ore, tiles.platinum, tiles.gold_ore, tiles.gold, tiles.iron_ore,
                        tiles.iron, tiles.copper_ore, tiles.copper }

# Set of all blocks which are of non-metal (crystalline) type
non_metal_list      = { tiles.diamond_ore, tiles.diamond_block, tiles.hellstone, tiles.adamantite,
                        tiles.obsidian, tiles.bedrock }

broken_by_pickaxe   = stone_list.union( non_metal_list )
broken_by_axe       = wood_list

class item_attr( enum.Enum ):

    MAX_STACK           = 1     # Maximum Quantity an item can stack upto in an inventory
    WEIGHT              = 2     # Weight of the item (and corresponding item entity)
    L_USE               = 3     # Function to be called when the left clicked with
    R_USE               = 4     # Function to be called when right clicked with
    DAMAGE              = 5     # Damage done to entities When attacked with


class item_modifs( enum.Enum ):
    pass


class items( enum.Enum ):

    # items for dirt and grass blocks
    grass                = 1
    browndirt            = 2
    snowygrass           = 3
    stick                = 4
    leaves               = 5

    # wood
    junglewood           = 10
    junglewood_plank     = 11
    oakwood              = 12
    oakwood_plank        = 13
    borealwood           = 14
    borealwood_plank     = 15
    pinewood             = 16
    pinewood_plank       = 17
    cactuswood           = 18
    cactuswood_plank     = 19
    palmwood             = 20
    palmwood_plank       = 21

    # metals
    cosmonium_ore        = 30
    cosmonium_ingot      = 31
    cosmonium_block      = 32
    unobtanium_ore       = 33
    unobtanium_ingot     = 34
    unobtanium_block     = 35
    platinum_ore         = 36
    platinum_ingot       = 37
    platinum_block       = 38
    gold_ore             = 39
    gold_brick           = 40
    gold_block           = 41
    iron_ore             = 42
    iron_ingot           = 43
    iron_block           = 44
    copper_ore           = 45
    copper_ingot         = 46
    copper_block         = 47

    # non-metals
    diamond_ore          = 50
    diamond_gem          = 51
    diamond_block        = 52
    hellstone            = 53
    adamantite           = 54
    adamantite_block     = 55
    obsidian             = 56
    bedrock              = 57

    # items for the stones
    granite              = 60
    quartz               = 61
    limestone            = 62
    greystone            = 63
    sandstone            = 64

    # items for transition blocks
    coal_ore             = 69
    gravel               = 70
    coal                 = 71

    # items for the clay blocks
    clay                 = 72
    red_clay             = 73

    # item for the sand block
    sand                 = 74

    # items for snowy blocks
    snow                 = 75
    ice                  = 76

    # items for the glass blocks
    glass                = 77
    glasspane            = 78
    glasswindow          = 79

    # bow and arrow
    bow                  = 80
    arrow                = 81

    # animal hides
    deerskin             = 82
    rottenleather        = 83

    # pickaxes
    wood_pickaxe         = 90
    stone_pickaxe        = 91
    copper_pickaxe       = 92
    iron_pickaxe         = 93
    gold_pickaxe         = 94
    diamond_pickaxe      = 95
    platinum_pickaxe     = 96
    unobtanium_pickaxe   = 97
    hellstone_pickaxe    = 98
    adamantite_pickaxe   = 99

    # axes
    wood_axe             = 100
    stone_axe            = 101
    copper_axe           = 102
    iron_axe             = 103
    gold_axe             = 104
    diamond_axe          = 105
    platinum_axe         = 106
    unobtanium_axe       = 107
    hellstone_axe        = 108
    adamantite_axe       = 109

    # battle axes
    wood_battleaxe       = 110
    stone_battleaxe      = 111
    copper_battleaxe     = 112
    iron_battleaxe       = 113
    gold_battleaxe       = 114
    diamond_battleaxe    = 115
    platinum_battleaxe   = 116
    unobtanium_battleaxe = 117
    hellstone_battleaxe  = 118
    adamantite_battleaxe = 119

    # swords
    wood_sword           = 120
    stone_sword          = 121
    copper_sword         = 122
    iron_sword           = 123
    gold_sword           = 124
    diamond_sword        = 125
    platinum_sword       = 126
    unobtanium_sword     = 127
    hellstone_sword      = 128
    adamantite_sword     = 129

    # door
    wood_door            = 130
    iron_door            = 131
    gold_door            = 132
    platinum_door        = 133

    # lighter
    lighter              = 140

    # bed and bucket
    bed                  = 141
    iron_bucket          = 142

    # fruits
    berry                = 143
    apple                = 144

    # meats
    chicken              = 145
    deermeat             = 146
    rottenmeat           = 147

    torch                = 148

    crafting_table       = 149
    furnace              = 150
    chest                = 151

pickaxe_list    = { items.wood_pickaxe, items.stone_pickaxe, items.copper_pickaxe, items.iron_pickaxe, items.gold_pickaxe, items.diamond_pickaxe, items.platinum_pickaxe, items.unobtanium_pickaxe, items.hellstone_pickaxe, items.adamantite_pickaxe }
axe_list        = { items.wood_axe, items.stone_axe, items.copper_axe, items.iron_axe, items.gold_axe, items.diamond_axe, items.platinum_axe, items.unobtanium_axe, items.hellstone_axe, items.adamantite_axe }
battle_axe_list = { items.wood_battleaxe, items.stone_battleaxe, items.copper_battleaxe, items.iron_battleaxe, items.gold_battleaxe, items.diamond_battleaxe, items.platinum_battleaxe, items.unobtanium_battleaxe, items.hellstone_battleaxe, items.adamantite_battleaxe }
sword_list      = { items.wood_sword, items.stone_sword, items.copper_sword, items.iron_sword, items.gold_sword, items.diamond_sword, items.platinum_sword, items.unobtanium_sword, items.hellstone_sword, items.adamantite_sword }

# Dictionary consisting of tile as key; name as a string
TILE_NAMES = {
    tiles.air                   : "air",
    tiles.grass                 : "grass",
    tiles.browndirt             : "dirt",
    tiles.snowygrass            : "snowy grass",
    tiles.leaves                : "leaves",
    tiles.junglewood            : "jungle logs",
    tiles.junglewood_plank      : "jungle planks",
    tiles.oakwood               : "oak logs",
    tiles.oakwood_plank         : "oak planks",
    tiles.borealwood            : "boreal logs",
    tiles.borealwood_plank      : "boreal planks",
    tiles.pinewood              : "pine logs",
    tiles.pinewood_plank        : "pine planks",
    tiles.cactuswood            : "cactus",
    tiles.cactuswood_plank      : "cactus flesh",
    tiles.palmwood              : "palm logs",
    tiles.palmwood_plank        : "palm planks",
    tiles.cosmonium_ore         : "cosmonium ore",
    tiles.cosmonium             : "cosmonium block",
    tiles.unobtanium_ore        : "unobtanium ore",
    tiles.unobtanium            : "unobtanium block",
    tiles.platinum_ore          : "platinum ore",
    tiles.platinum              : "platinum block",
    tiles.gold_ore              : "gold ore",
    tiles.gold                  : "gold block",
    tiles.iron_ore              : "iron ore",
    tiles.iron                  : "iron block",
    tiles.copper_ore            : "copper ore",
    tiles.copper                : "copper block",
    tiles.diamond_ore           : "diamond ore",
    tiles.diamond_block         : "diamond block",
    tiles.hellstone             : "hellstone",
    tiles.adamantite            : "adamantite block",
    tiles.obsidian              : "obsidian",
    tiles.bedrock               : "bedrock",
    tiles.granite               : "granite block",
    tiles.quartz                : "quartz block",
    tiles.limestone             : "limestone block",
    tiles.greystone             : "stone block",
    tiles.sandstone             : "sandstone block",
    tiles.gravel                : "gravel",
    tiles.coal                  : "coke",
    tiles.clay                  : "clay",
    tiles.red_clay              : "red clay",
    tiles.sand                  : "sand",
    tiles.snow                  : "snow block",
    tiles.ice                   : "ice block",
    tiles.glasspane             : "glass pane",
    tiles.glasswindow           : "glass window",
    tiles.wood_door_upper       : "wooden door up",
    tiles.wood_door_lower       : "wooden door down",
    tiles.iron_door_upper       : "iron door up",
    tiles.iron_door_lower       : "iron door low",
    tiles.gold_door_upper       : "gold door up",
    tiles.gold_door_lower       : "gold door down",
    tiles.platinum_door_upper   : "platinum door up",
    tiles.platinum_door_lower   : "platinum door down",
    tiles.bed_head              : "bed head",
    tiles.bed_tail              : "bed tail",
    tiles.torch                 : "torch",
    tiles.crafting_table        : "crafting table",
    tiles.furnace               : "furnace",
    tiles.chest                 : "chest"
}

# Dictionary consisting of tile as key; list of surfaces of modifiers as value
TILE_MODIFIERS = {
    tile_modifs.crack       : [ pygame.image.load("Resources/Default/break{}.png".format(i)) for i in range( 9 ) ],
    tile_modifs.on_fire     : [],
    tile_modifs.fire        : [],
    tile_modifs.water       : [],
    tile_modifs.lava        : []
}

# Dictionary consisting of tile as key; surface (image) as value
inventory_slot = pygame.image.load("Resources/Default/InventorySpace.png")
cave_background = pygame.image.load("Resources/Default/cave_background.png")
space_background = pygame.image.load("Resources/Default/space_background.png")

TILE_TABLE = {

    tiles.air                   : pygame.image.load("Resources/Default/tile_air.png"),
    tiles.grass                 : pygame.image.load("Resources/Default/tile_grass.png"),
    tiles.browndirt             : pygame.image.load("Resources/Default/tile_browndirt.png"),
    tiles.snowygrass            : pygame.image.load("Resources/Default/tile_snowygrass.png"),
    tiles.leaves                : pygame.image.load("Resources/Default/tile_leaves.png"),
    tiles.junglewood            : pygame.image.load("Resources/Default/tile_junglewood.png"),
    tiles.junglewood_plank      : pygame.image.load("Resources/Default/tile_junglewood_plank.png"),
    tiles.oakwood               : pygame.image.load("Resources/Default/tile_oakwood.png"),
    tiles.oakwood_plank         : pygame.image.load("Resources/Default/tile_oakwood_plank.png"),
    tiles.borealwood            : pygame.image.load("Resources/Default/tile_borealwood.png"),
    tiles.borealwood_plank      : pygame.image.load("Resources/Default/tile_borealwood_plank.png"),
    tiles.pinewood              : pygame.image.load("Resources/Default/tile_pinewood.png"),
    tiles.pinewood_plank        : pygame.image.load("Resources/Default/tile_pinewood_plank.png"),
    tiles.cactuswood            : pygame.image.load("Resources/Default/tile_cactuswood.png"),
    tiles.cactuswood_plank      : pygame.image.load("Resources/Default/tile_cactuswood_plank.png"),
    tiles.palmwood              : pygame.image.load("Resources/Default/tile_palmwood.png"),
    tiles.palmwood_plank        : pygame.image.load("Resources/Default/tile_palmwood_plank.png"),
    tiles.cosmonium_ore         : pygame.image.load("Resources/Default/tile_cosmonium_ore.png"),
    tiles.cosmonium             : pygame.image.load("Resources/Default/tile_cosmonium.png"),
    tiles.unobtanium_ore        : pygame.image.load("Resources/Default/tile_unobtanium_ore.png"),
    tiles.unobtanium            : pygame.image.load("Resources/Default/tile_unobtanium.png"),
    tiles.platinum_ore          : pygame.image.load("Resources/Default/tile_platinum_ore.png"),
    tiles.platinum              : pygame.image.load("Resources/Default/tile_platinum.png"),
    tiles.gold_ore              : pygame.image.load("Resources/Default/tile_gold_ore.png"),
    tiles.gold                  : pygame.image.load("Resources/Default/tile_gold.png"),
    tiles.iron_ore              : pygame.image.load("Resources/Default/tile_iron_ore.png"),
    tiles.iron                  : pygame.image.load("Resources/Default/tile_iron.png"),
    tiles.copper_ore            : pygame.image.load("Resources/Default/tile_copper_ore.png"),
    tiles.copper                : pygame.image.load("Resources/Default/tile_copper.png"),
    tiles.diamond_ore           : pygame.image.load("Resources/Default/tile_diamond_ore.png"),
    tiles.diamond_block         : pygame.image.load("Resources/Default/tile_diamond_block.png"),
    tiles.hellstone             : pygame.image.load("Resources/Default/tile_hellstone.png"),
    tiles.adamantite            : pygame.image.load("Resources/Default/tile_adamantite.png"),
    tiles.obsidian              : pygame.image.load("Resources/Default/tile_obsidian.png"),
    tiles.bedrock               : pygame.image.load("Resources/Default/tile_bedrock.png"),
    tiles.granite               : pygame.image.load("Resources/Default/tile_granite.png"),
    tiles.quartz                : pygame.image.load("Resources/Default/tile_quartz.png"),
    tiles.limestone             : pygame.image.load("Resources/Default/tile_limestone.png"),
    tiles.greystone             : pygame.image.load("Resources/Default/tile_greystone.png"),
    tiles.sandstone             : pygame.image.load("Resources/Default/tile_sandstone.png"),
    tiles.gravel                : pygame.image.load("Resources/Default/tile_gravel.png"),
    tiles.coal                  : pygame.image.load("Resources/Default/tile_coal_ore.png"),
    tiles.clay                  : pygame.image.load("Resources/Default/tile_clay.png"),
    tiles.red_clay              : pygame.image.load("Resources/Default/tile_red_clay.png"),
    tiles.sand                  : pygame.image.load("Resources/Default/tile_sand.png"),
    tiles.snow                  : pygame.image.load("Resources/Default/tile_snow.png"),
    tiles.ice                   : pygame.image.load("Resources/Default/tile_ice.png"),
    tiles.glasspane             : pygame.image.load("Resources/Default/tile_glasspane.png"),
    tiles.glasswindow           : pygame.image.load("Resources/Default/tile_glasswindow.png"),
    tiles.wood_door_upper       : pygame.image.load("Resources/Default/tile_wood_door_upper.png"),
    tiles.wood_door_lower       : pygame.image.load("Resources/Default/tile_wood_door_lower.png"),
    tiles.iron_door_upper       : pygame.image.load("Resources/Default/tile_iron_door_upper.png"),
    tiles.iron_door_lower       : pygame.image.load("Resources/Default/tile_iron_door_lower.png"),
    tiles.gold_door_upper       : pygame.image.load("Resources/Default/tile_gold_door_upper.png"),
    tiles.gold_door_lower       : pygame.image.load("Resources/Default/tile_gold_door_lower.png"),
    tiles.platinum_door_upper   : pygame.image.load("Resources/Default/tile_platinum_door_upper.png"),
    tiles.platinum_door_lower   : pygame.image.load("Resources/Default/tile_platinum_door_lower.png"),
    tiles.bed_head              : pygame.image.load("Resources/Default/tile_bed_head.png"),
    tiles.bed_tail              : pygame.image.load("Resources/Default/tile_bed_tail.png"),
    tiles.torch                 : pygame.image.load("Resources/Default/tile_torch.png"),
    tiles.crafting_table        : pygame.image.load("Resources/Default/tile_crafting_table.png"),
    tiles.furnace               : pygame.image.load("Resources/Default/tile_furnace.png"),
    tiles.chest                 : pygame.image.load("Resources/Default/tile_chest.png")
}

# Dictionary consisting of tile as key; dictionary consisting of tile attribute as key and attribute as value as value
TILE_ATTR = {
    # tiles.air           : {tile_attr.LUMINOSITY:255},
    # tiles.bedrock       : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:INF, tile_attr.INFLAMMABLE:None},
    # tiles.obsidian      : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:0   },
    # tiles.hellstone     : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:0   },
    # tiles.unobtaniumOre : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:160, tile_attr.HEALTH:90,  tile_attr.INFLAMMABLE:None},
    # tiles.diamondOre    : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:175, tile_attr.HEALTH:90,  tile_attr.INFLAMMABLE:None},
    # tiles.platinumOre   : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:160, tile_attr.HEALTH:80,  tile_attr.INFLAMMABLE:None},
    # tiles.goldOre       : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:160, tile_attr.HEALTH:70,  tile_attr.INFLAMMABLE:None},
    # tiles.ironOre       : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:160, tile_attr.HEALTH:70,  tile_attr.INFLAMMABLE:None},
    # tiles.granite       : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:55,  tile_attr.INFLAMMABLE:None},
    # tiles.quartz        : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:55,  tile_attr.INFLAMMABLE:None},
    # tiles.limestone     : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:55,  tile_attr.INFLAMMABLE:None},
    # tiles.copperOre     : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:160, tile_attr.HEALTH:60,  tile_attr.INFLAMMABLE:None},
    # tiles.greystone     : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:55,  tile_attr.INFLAMMABLE:None},
    # tiles.sandstone     : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:50,  tile_attr.INFLAMMABLE:None},
    # tiles.gravel        : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:50,  tile_attr.INFLAMMABLE:None},
    # tiles.coke          : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:160, tile_attr.HEALTH:50,  tile_attr.INFLAMMABLE:None},
    # tiles.clay          : {tile_attr.FRICTION:0.9,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:45,  tile_attr.INFLAMMABLE:None},
    # tiles.redClay       : {tile_attr.FRICTION:0.9,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:45,  tile_attr.INFLAMMABLE:None},
    # tiles.browndirt     : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:30,  tile_attr.INFLAMMABLE:None}

    tiles.air                 : { tile_attr.FRICTION: AIR_FRICTION, tile_attr.LUMINOSITY: 255 },
    tiles.grass               : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.grass               },
    tiles.browndirt           : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.browndirt           },
    tiles.snowygrass          : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.snowygrass          },
    tiles.leaves              : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.leaves              },
    tiles.junglewood          : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.junglewood          },
    tiles.junglewood_plank    : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.junglewood_plank    },
    tiles.oakwood             : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.oakwood             },
    tiles.oakwood_plank       : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.oakwood_plank       },
    tiles.borealwood          : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.borealwood          },
    tiles.borealwood_plank    : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.borealwood_plank    },
    tiles.pinewood            : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.pinewood            },
    tiles.pinewood_plank      : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.pinewood_plank      },
    tiles.cactuswood          : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.cactuswood          },
    tiles.cactuswood_plank    : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.cactuswood_plank    },
    tiles.palmwood            : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.palmwood            },
    tiles.palmwood_plank      : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.palmwood_plank      },
    tiles.cosmonium_ore       : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.cosmonium_ore       },
    tiles.cosmonium           : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.cosmonium_ore       },
    tiles.unobtanium_ore      : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.unobtanium_ore      },
    tiles.unobtanium          : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.unobtanium_ore      },
    tiles.platinum_ore        : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.platinum_ore        },
    tiles.platinum            : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.platinum_ore        },
    tiles.gold_ore            : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.gold_ore            },
    tiles.gold                : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.gold_ore            },
    tiles.iron_ore            : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.iron_ore            },
    tiles.iron                : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.iron_ore            },
    tiles.copper_ore          : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.copper_ore          },
    tiles.copper              : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.copper_ore          },
    tiles.diamond_ore         : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.diamond_ore         },
    tiles.diamond_block       : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.diamond_block       },
    tiles.hellstone           : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.hellstone           },
    tiles.adamantite          : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.adamantite          },
    tiles.obsidian            : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.obsidian            },
    tiles.bedrock             : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.bedrock             },
    tiles.granite             : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.granite             },
    tiles.quartz              : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.quartz              },
    tiles.limestone           : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.limestone           },
    tiles.greystone           : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.greystone           },
    tiles.sandstone           : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.sandstone           },
    tiles.gravel              : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.gravel              },
    tiles.coal                : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.coal_ore            },
    tiles.clay                : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.clay                },
    tiles.red_clay            : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.red_clay            },
    tiles.sand                : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.sand                },
    tiles.snow                : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.snow                },
    tiles.ice                 : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.ice                 },
    tiles.glasspane           : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.glasspane           },
    tiles.glasswindow         : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.glasswindow         },
    tiles.wood_door_upper     : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.wood_door           },
    tiles.wood_door_lower     : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.wood_door           },
    tiles.iron_door_upper     : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.iron_door           },
    tiles.iron_door_lower     : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.iron_door           },
    tiles.gold_door_upper     : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.gold_door           },
    tiles.gold_door_lower     : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.gold_door           },
    tiles.platinum_door_upper : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.platinum_door       },
    tiles.platinum_door_lower : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.platinum_door       },
    tiles.bed_head            : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.bed                 },
    tiles.bed_tail            : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.bed                 },
    tiles.torch               : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.torch               },
    tiles.crafting_table      : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.crafting_table      },
    tiles.furnace             : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.furnace             },
    tiles.chest               : { tile_attr.FRICTION: 0.8, tile_attr.LUMINOSITY: 255, tile_attr.HEALTH: 100, tile_attr.INFLAMMABLE: None, tile_attr.DROP_ITEM: items.chest               }
}

# Dictionary consisting of item as key; name as a string
ITEM_NAMES = {
    items.grass                : "grass block",
    items.browndirt            : "dirt block",
    items.snowygrass           : "snow block",
    items.stick                : "sticks",
    items.leaves               : "leaves",
    items.junglewood           : "jungle logs",
    items.junglewood_plank     : "jungle planks",
    items.oakwood              : "oak logs",
    items.oakwood_plank        : "oak plank",
    items.borealwood           : "boreal logs",
    items.borealwood_plank     : "boreal planks",
    items.pinewood             : "pine logs",
    items.pinewood_plank       : "pine planks",
    items.cactuswood           : "cactus",
    items.cactuswood_plank     : "cactus flesh",
    items.palmwood             : "palm logs",
    items.palmwood_plank       : "palm planks",
    items.cosmonium_ore        : "cosmonium ore",
    items.cosmonium_ingot      : "cosmonium ingot",
    items.cosmonium_block      : "cosmonium block",
    items.unobtanium_ore       : "unobtanium ore",
    items.unobtanium_ingot     : "unobtanium ingot",
    items.unobtanium_block     : "unobtanium block",
    items.platinum_ore         : "platinum ore",
    items.platinum_ingot       : "platinum ingot",
    items.platinum_block       : "platinum block",
    items.gold_ore             : "gold ore",
    items.gold_brick           : "gold brick",
    items.gold_block           : "gold block",
    items.iron_ore             : "iron ore",
    items.iron_ingot           : "iron ingot",
    items.iron_block           : "iron block",
    items.copper_ore           : "copper ore",
    items.copper_ingot         : "copper ingot",
    items.copper_block         : "copper block",
    items.diamond_ore          : "diamond ore",
    items.diamond_gem          : "diamond",
    items.diamond_block        : "diamond block",
    items.hellstone            : "hellstone",
    items.adamantite           : "adamantite",
    items.adamantite_block     : "adamantite block",
    items.obsidian             : "obsidian",
    items.bedrock              : "bedrock",
    items.granite              : "granite",
    items.quartz               : "quartz",
    items.limestone            : "limestone",
    items.greystone            : "stone",
    items.sandstone            : "sandstone",
    items.coal_ore             : "coke",
    items.gravel               : "gravel",
    items.coal                 : "coal",
    items.clay                 : "clay",
    items.red_clay             : "red clay",
    items.sand                 : "sand",
    items.snow                 : "snow",
    items.ice                  : "ice",
    items.glass                : "glass",
    items.glasspane            : "glass pane",
    items.glasswindow          : "glass window",
    items.bow                  : "bow",
    items.arrow                : "arrow",
    items.deerskin             : "deer skin",
    items.rottenleather        : "rotten leather",
    items.wood_pickaxe         : "wood pickaxe",
    items.stone_pickaxe        : "stone pickaxe",
    items.copper_pickaxe       : "copper pickaxe",
    items.iron_pickaxe         : "iron pickaxe",
    items.gold_pickaxe         : "gold pickaxe",
    items.diamond_pickaxe      : "diamond pickaxe",
    items.platinum_pickaxe     : "platinum pickaxe",
    items.unobtanium_pickaxe   : "unobtanium pickaxe",
    items.hellstone_pickaxe    : "hellstone pickaxe",
    items.adamantite_pickaxe   : "adamantite pickaxe",
    items.wood_axe             : "wood axe",
    items.stone_axe            : "stone axe",
    items.copper_axe           : "copper axe",
    items.iron_axe             : "iron axe",
    items.gold_axe             : "gold axe",
    items.diamond_axe          : "diamond axe",
    items.platinum_axe         : "platinum axe",
    items.unobtanium_axe       : "unobtanium axe",
    items.hellstone_axe        : "hellstone axe",
    items.adamantite_axe       : "adamantite axe",
    items.wood_battleaxe       : "wood battle axe",
    items.stone_battleaxe      : "stone battle axe",
    items.copper_battleaxe     : "copper battle axe",
    items.iron_battleaxe       : "iron battle axe",
    items.gold_battleaxe       : "gold battle axe",
    items.diamond_battleaxe    : "diamond battle axe",
    items.platinum_battleaxe   : "platinum battle axe",
    items.unobtanium_battleaxe : "unobtanium battle axe",
    items.hellstone_battleaxe  : "hellstone battle axe",
    items.adamantite_battleaxe : "adamantite battle axe",
    items.wood_sword           : "wood sword",
    items.stone_sword          : "stone sword",
    items.copper_sword         : "copper sword",
    items.iron_sword           : "iron sword",
    items.gold_sword           : "gold sword",
    items.diamond_sword        : "diamond sword",
    items.platinum_sword       : "platinum sword",
    items.unobtanium_sword     : "unobtanium sword",
    items.hellstone_sword      : "hellstone sword",
    items.adamantite_sword     : "adamantite sword",
    items.wood_door            : "wooden door",
    items.iron_door            : "iron door",
    items.gold_door            : "gold door",
    items.platinum_door        : "platinum door",
    items.lighter              : "lighter",
    items.bed                  : "bed",
    items.iron_bucket          : "bucket",
    items.berry                : "berry",
    items.apple                : "apple",
    items.chicken              : "chicken",
    items.deermeat             : "deer meat",
    items.rottenmeat           : "rotten meat",
    items.torch                : "torch",
    items.crafting_table       : "crafting table",
    items.furnace              : "furnace",
    items.chest                : "chest"
}

# Dictionary consisting of item as key; surface list of surfaces of modifiers as value
ITEM_MODIFIERS = {}

# Dictionary consisting of item as key; surface (image) as value
ITEM_TABLE = {
    # items for dirt and grass blocks
    items.grass                : pygame.image.load("Resources/Default/item_grass.png"),
    items.browndirt            : pygame.image.load("Resources/Default/item_browndirt.png"),
    items.snowygrass           : pygame.image.load("Resources/Default/item_snowygrass.png"),
    items.stick                : pygame.image.load("Resources/Default/item_stick.png"),
    items.leaves               : pygame.image.load("Resources/Default/item_leaves.png"),

    # wood
    items.junglewood           : pygame.image.load("Resources/Default/item_junglewood.png"),
    items.junglewood_plank     : pygame.image.load("Resources/Default/item_junglewood_plank.png"),
    items.oakwood              : pygame.image.load("Resources/Default/item_oakwood.png"),
    items.oakwood_plank        : pygame.image.load("Resources/Default/item_oakwood_plank.png"),
    items.borealwood           : pygame.image.load("Resources/Default/item_borealwood.png"),
    items.borealwood_plank     : pygame.image.load("Resources/Default/item_borealwood_plank.png"),
    items.pinewood             : pygame.image.load("Resources/Default/item_pinewood.png"),
    items.pinewood_plank       : pygame.image.load("Resources/Default/item_pinewood_plank.png"),
    items.cactuswood           : pygame.image.load("Resources/Default/item_cactuswood.png"),
    items.cactuswood_plank     : pygame.image.load("Resources/Default/item_cactuswood_plank.png"),
    items.palmwood             : pygame.image.load("Resources/Default/item_palmwood.png"),
    items.palmwood_plank       : pygame.image.load("Resources/Default/item_palmwood_plank.png"),

    # metals
    items.cosmonium_ore        : pygame.image.load("Resources/Default/item_cosmonium_ore.png"),
    items.cosmonium_ingot      : pygame.image.load("Resources/Default/item_cosmonium_ingot.png"),
    items.cosmonium_block      : pygame.image.load("Resources/Default/item_cosmonium_block.png"),
    items.unobtanium_ore       : pygame.image.load("Resources/Default/item_unobtanium_ore.png"),
    items.unobtanium_ingot     : pygame.image.load("Resources/Default/item_unobtanium_ingot.png"),
    items.unobtanium_block     : pygame.image.load("Resources/Default/item_unobtanium_block.png"),
    items.platinum_ore         : pygame.image.load("Resources/Default/item_platinum_ore.png"),
    items.platinum_ingot       : pygame.image.load("Resources/Default/item_platinum_ingot.png"),
    items.platinum_block       : pygame.image.load("Resources/Default/item_platinum_block.png"),
    items.gold_ore             : pygame.image.load("Resources/Default/item_gold_ore.png"),
    items.gold_brick           : pygame.image.load("Resources/Default/item_gold_brick.png"),
    items.gold_block           : pygame.image.load("Resources/Default/item_gold_block.png"),
    items.iron_ore             : pygame.image.load("Resources/Default/item_iron_ore.png"),
    items.iron_ingot           : pygame.image.load("Resources/Default/item_iron_ingot.png"),
    items.iron_block           : pygame.image.load("Resources/Default/item_iron_block.png"),
    items.copper_ore           : pygame.image.load("Resources/Default/item_copper_ore.png"),
    items.copper_ingot         : pygame.image.load("Resources/Default/item_copper_ingot.png"),
    items.copper_block         : pygame.image.load("Resources/Default/item_copper_block.png"),

    # non-metals
    items.diamond_ore          : pygame.image.load("Resources/Default/item_diamond_ore.png"),
    items.diamond_gem          : pygame.image.load("Resources/Default/item_diamond_gem.png"),
    items.diamond_block        : pygame.image.load("Resources/Default/item_diamond_block.png"),
    items.hellstone            : pygame.image.load("Resources/Default/item_hellstone.png"),
    items.adamantite           : pygame.image.load("Resources/Default/item_adamantite.png"),
    items.adamantite_block     : pygame.image.load("Resources/Default/item_adamantite_block.png"),
    items.obsidian             : pygame.image.load("Resources/Default/item_obsidian.png"),
    items.bedrock              : pygame.image.load("Resources/Default/item_bedrock.png"),

    # items for the stones
    items.granite              : pygame.image.load("Resources/Default/item_granite.png"),
    items.quartz               : pygame.image.load("Resources/Default/item_quartz.png"),
    items.limestone            : pygame.image.load("Resources/Default/item_limestone.png"),
    items.greystone            : pygame.image.load("Resources/Default/item_greystone.png"),
    items.sandstone            : pygame.image.load("Resources/Default/item_sandstone.png"),

    # items for transition blocks
    items.coal_ore             : pygame.image.load("Resources/Default/item_coal_ore.png"),
    items.gravel               : pygame.image.load("Resources/Default/item_gravel.png"),
    items.coal                 : pygame.image.load("Resources/Default/item_coal.png"),

    # items for the clay blocks
    items.clay                 : pygame.image.load("Resources/Default/item_clay.png"),
    items.red_clay             : pygame.image.load("Resources/Default/item_red_clay.png"),

    # item for the sand block
    items.sand                 : pygame.image.load("Resources/Default/item_sand.png"),

    # items for snowy blocks
    items.snow                 : pygame.image.load("Resources/Default/item_snow.png"),
    items.ice                  : pygame.image.load("Resources/Default/item_ice.png"),

    # items for the glass blocks
    items.glass                : pygame.image.load("Resources/Default/item_glass.png"),
    items.glasspane            : pygame.image.load("Resources/Default/item_glasspane.png"),
    items.glasswindow          : pygame.image.load("Resources/Default/item_glasswindow.png"),

    # bow and arrow
    items.bow                  : pygame.image.load("Resources/Default/item_bow.png"),
    items.arrow                : pygame.image.load("Resources/Default/item_arrow.png"),

    # animal hides
    items.deerskin             : pygame.image.load("Resources/Default/item_deerskin.png"),
    items.rottenleather        : pygame.image.load("Resources/Default/item_rottenleather.png"),

    # pickaxes
    items.wood_pickaxe         : pygame.image.load("Resources/Default/item_wood_pickaxe.png"),
    items.stone_pickaxe        : pygame.image.load("Resources/Default/item_stone_pickaxe.png"),
    items.copper_pickaxe       : pygame.image.load("Resources/Default/item_copper_pickaxe.png"),
    items.iron_pickaxe         : pygame.image.load("Resources/Default/item_iron_pickaxe.png"),
    items.gold_pickaxe         : pygame.image.load("Resources/Default/item_gold_pickaxe.png"),
    items.diamond_pickaxe      : pygame.image.load("Resources/Default/item_diamond_pickaxe.png"),
    items.platinum_pickaxe     : pygame.image.load("Resources/Default/item_platinum_pickaxe.png"),
    items.unobtanium_pickaxe   : pygame.image.load("Resources/Default/item_unobtanium_pickaxe.png"),
    items.hellstone_pickaxe    : pygame.image.load("Resources/Default/item_hellstone_pickaxe.png"),
    items.adamantite_pickaxe   : pygame.image.load("Resources/Default/item_adamantite_pickaxe.png"),

    # axes
    items.wood_axe             : pygame.image.load("Resources/Default/item_wood_axe.png"),
    items.stone_axe            : pygame.image.load("Resources/Default/item_stone_axe.png"),
    items.copper_axe           : pygame.image.load("Resources/Default/item_copper_axe.png"),
    items.iron_axe             : pygame.image.load("Resources/Default/item_iron_axe.png"),
    items.gold_axe             : pygame.image.load("Resources/Default/item_gold_axe.png"),
    items.diamond_axe          : pygame.image.load("Resources/Default/item_diamond_axe.png"),
    items.platinum_axe         : pygame.image.load("Resources/Default/item_platinum_axe.png"),
    items.unobtanium_axe       : pygame.image.load("Resources/Default/item_unobtanium_axe.png"),
    items.hellstone_axe        : pygame.image.load("Resources/Default/item_hellstone_axe.png"),
    items.adamantite_axe       : pygame.image.load("Resources/Default/item_adamantite_axe.png"),

    # battle axes
    items.wood_battleaxe       : pygame.image.load("Resources/Default/item_wood_battleaxe.png"),
    items.stone_battleaxe      : pygame.image.load("Resources/Default/item_stone_battleaxe.png"),
    items.copper_battleaxe     : pygame.image.load("Resources/Default/item_copper_battleaxe.png"),
    items.iron_battleaxe       : pygame.image.load("Resources/Default/item_iron_battleaxe.png"),
    items.gold_battleaxe       : pygame.image.load("Resources/Default/item_gold_battleaxe.png"),
    items.diamond_battleaxe    : pygame.image.load("Resources/Default/item_diamond_battleaxe.png"),
    items.platinum_battleaxe   : pygame.image.load("Resources/Default/item_platinum_battleaxe.png"),
    items.unobtanium_battleaxe : pygame.image.load("Resources/Default/item_unobtanium_battleaxe.png"),
    items.hellstone_battleaxe  : pygame.image.load("Resources/Default/item_hellstone_battleaxe.png"),
    items.adamantite_battleaxe : pygame.image.load("Resources/Default/item_adamantite_battleaxe.png"),

    # swords
    items.wood_sword           : pygame.image.load("Resources/Default/item_wood_sword.png"),
    items.stone_sword          : pygame.image.load("Resources/Default/item_stone_sword.png"),
    items.copper_sword         : pygame.image.load("Resources/Default/item_copper_sword.png"),
    items.iron_sword           : pygame.image.load("Resources/Default/item_iron_sword.png"),
    items.gold_sword           : pygame.image.load("Resources/Default/item_gold_sword.png"),
    items.diamond_sword        : pygame.image.load("Resources/Default/item_diamond_sword.png"),
    items.platinum_sword       : pygame.image.load("Resources/Default/item_platinum_sword.png"),
    items.unobtanium_sword     : pygame.image.load("Resources/Default/item_unobtanium_sword.png"),
    items.hellstone_sword      : pygame.image.load("Resources/Default/item_hellstone_sword.png"),
    items.adamantite_sword     : pygame.image.load("Resources/Default/item_adamantite_sword.png"),

    # door
    items.wood_door            : pygame.image.load("Resources/Default/item_wood_door.png"),
    items.iron_door            : pygame.image.load("Resources/Default/item_iron_door.png"),
    items.gold_door            : pygame.image.load("Resources/Default/item_gold_door.png"),
    items.platinum_door        : pygame.image.load("Resources/Default/item_platinum_door.png"),

    # lighter
    items.lighter              : pygame.image.load("Resources/Default/item_lighter.png"),

    # bed and bucket
    items.bed                  : pygame.image.load("Resources/Default/item_bed.png"),
    items.iron_bucket          : pygame.image.load("Resources/Default/item_iron_bucket.png"),

    # fruits
    items.berry                : pygame.image.load("Resources/Default/item_berry.png"),
    items.apple                : pygame.image.load("Resources/Default/item_apple.png"),

    # meats
    items.chicken              : pygame.image.load("Resources/Default/item_chicken.png"),
    items.deermeat             : pygame.image.load("Resources/Default/item_deermeat.png"),
    items.rottenmeat           : pygame.image.load("Resources/Default/item_rottenmeat.png"),

    items.torch                : pygame.image.load("Resources/Default/item_torch.png"),

    items.crafting_table       : pygame.image.load("Resources/Default/item_crafting_table.png"),
    items.furnace              : pygame.image.load("Resources/Default/item_furnace.png"),
    items.chest                : pygame.image.load("Resources/Default/item_chest.png")
}

# # l_use and r_use functions for various items
# _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt
# player = _entity_buffer.player
# inventory = player.inventory

# Entity hitting behaviour has not been implemented yet
# -1 returned indicates there was nothing to break
# 0 indicates that nothing has been broken
# 1 indicates that something has been broken

#! Only redraw a portion of the chunk

# Function only to be called if not colliding with the player or any other entity
def place_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, _block ):

    chunk = _chunk_buffer.chunks[_chunk]
    blocks= chunk.blocks
    walls = chunk.walls

    if blocks[_y][_x] != tiles.air: return 0
    blocks[_y][_x] = _block
    chunk.draw()

    return 1

    # if _local_entry: self.local_tile_table[ ( _x, _y, True) ] = _local_entry.copy()
    # Lightmaps

# Function only to be called if no entity is being attacked
def break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, _damage ):

    # -1 returned indicates there was nothing to break
    # 0 indicates that nothing has been broken
    # 1 indicates that something has been broken

    chunk = _chunk_buffer.chunks[_chunk]
    layer = chunk.blocks
    table = chunk.local_tile_table[1]

    if chunk.blocks[_y][_x] == tiles.air:
        if chunk.walls[_y][_x] == tiles.air:
            return -1
        layer = chunk.walls
        table = chunk.local_tile_table[0]

    if (_x, _y) not in table:
        table[(_x, _y)] = {}
    if tile_attr.HEALTH not in table[(_x, _y)]:
        table[(_x, _y)][tile_attr.HEALTH] = TILE_ATTR[layer[_y][_x]][tile_attr.HEALTH]

    table[(_x, _y)][tile_attr.HEALTH] -= ( _damage * _dt )

    if table[(_x, _y)][tile_attr.HEALTH] <= 0:
        which_block   = layer[_y][_x]
        layer[_y][_x] = tiles.air

        del table[(_x, _y)][tile_attr.HEALTH]
        if table[(_x, _y)]:
            del table[(_x, _y)]
        chunk.draw()

        pos = [_x, _y, chunk.index]
        _entity_buffer.add_item_entity( TILE_ATTR[which_block][tile_attr.DROP_ITEM], pos )

        return 1

    else:
        chunk.draw()

    return 0

# l_use and r_use functions for various items
def l_use_grass(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_grass(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    player = _entity_buffer.player
    state = place_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, tiles.grass )
    if state != 0:
        player.inventory.rem_item_pos( player.get_held_index() )

def l_use_browndirt(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_browndirt(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    player = _entity_buffer.player
    state = place_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, tiles.browndirt )
    if state != 0:
        player.inventory.rem_item_pos( player.get_held_index() )

def l_use_snowygrass(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_snowygrass(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    player = _entity_buffer.player
    state = place_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, tiles.snowygrass )
    if state != 0:
        player.inventory.rem_item_pos( player.get_held_index() )

# Dictionary consisting of item as key; dictionary consisting of item attribute as key and attribute as value as value
ITEM_ATTR = {
    items.grass                : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:l_use_grass, item_attr.R_USE:r_use_grass},
    items.browndirt            : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:l_use_browndirt, item_attr.R_USE:r_use_browndirt},
    items.snowygrass           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.stick                : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.leaves               : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.junglewood           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.junglewood_plank     : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.oakwood              : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.oakwood_plank        : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.borealwood           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.borealwood_plank     : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.pinewood             : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.pinewood_plank       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.cactuswood           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.cactuswood_plank     : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.palmwood             : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.palmwood_plank       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.cosmonium_ore        : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.cosmonium_ingot      : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.cosmonium_block      : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.unobtanium_ore       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.unobtanium_ingot     : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.unobtanium_block     : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.platinum_ore         : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.platinum_ingot       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.platinum_block       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.gold_ore             : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.gold_brick           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.gold_block           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.iron_ore             : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.iron_ingot           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.iron_block           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.copper_ore           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.copper_ingot         : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.copper_block         : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.diamond_ore          : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.diamond_gem          : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.diamond_block        : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.hellstone            : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.adamantite           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.adamantite_block     : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.obsidian             : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.bedrock              : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.granite              : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.quartz               : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.limestone            : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.greystone            : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.sandstone            : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.coal_ore             : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.gravel               : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.coal                 : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.clay                 : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.red_clay             : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.sand                 : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.snow                 : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.ice                  : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.glass                : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.glasspane            : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.glasswindow          : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.bow                  : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.arrow                : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.deerskin             : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.rottenleather        : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.wood_pickaxe         : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.stone_pickaxe        : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.copper_pickaxe       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.iron_pickaxe         : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.gold_pickaxe         : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.diamond_pickaxe      : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.platinum_pickaxe     : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.unobtanium_pickaxe   : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.hellstone_pickaxe    : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.adamantite_pickaxe   : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.wood_axe             : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.stone_axe            : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.copper_axe           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.iron_axe             : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.gold_axe             : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.diamond_axe          : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.platinum_axe         : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.unobtanium_axe       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.hellstone_axe        : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.adamantite_axe       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.wood_battleaxe       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.stone_battleaxe      : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.copper_battleaxe     : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.iron_battleaxe       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.gold_battleaxe       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.diamond_battleaxe    : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.platinum_battleaxe   : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.unobtanium_battleaxe : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.hellstone_battleaxe  : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.adamantite_battleaxe : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.wood_sword           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.stone_sword          : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.copper_sword         : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.iron_sword           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.gold_sword           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.diamond_sword        : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.platinum_sword       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.unobtanium_sword     : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.hellstone_sword      : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.adamantite_sword     : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.wood_door            : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.iron_door            : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.gold_door            : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.platinum_door        : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.lighter              : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.bed                  : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.iron_bucket          : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.berry                : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.apple                : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.chicken              : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.deermeat             : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.rottenmeat           : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.torch                : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.crafting_table       : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.furnace              : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.chest                : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None}
}

# Textures for entities

player_running = [pygame.image.load("Resources/Default/running{}.png".format(1-i)) for i in range(2)] + [pygame.image.load("Resources/Default/static.png")] + [pygame.image.load("Resources/Default/running{}.png".format(i)) for i in range(2)]
player_running[0] = pygame.transform.flip(player_running[0], True, False)
player_running[1] = pygame.transform.flip(player_running[1], True, False)

def l_use_hand( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_hand( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return 0

def l_use_stick(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_stick(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return 0

def l_use_leaves(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_leaves(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return 0

def l_use_junglewood(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_junglewood(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_junglewood_plank(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_junglewood_plank(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_oakwood(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_oakwood(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_oakwood_plank(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_oakwood_plank(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_borealwood(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_borealwood(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_borealwood_plank(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_borealwood_plank(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_pinewood(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_pinewood(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_pinewood_plank(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_pinewood_plank(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_palmwood(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_palmwood(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_palmwood_plank(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_palmwood_plank(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_cosmonium_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_cosmonium_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_cosmonium_ingot(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_cosmonium_ingot(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_cosmonium_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_cosmonium_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_unobtanium_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_unobtanium_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_unobtanium_ingot(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_unobtanium_ingot(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_cosmonium_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_cosmonium_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_platinum_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_platinum_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_platinum_ingot(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_platinum_ingot(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_platinum_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_platinum_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_gold_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_gold_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_gold_brick(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_gold_brick(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_gold_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_gold_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_copper_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_copper_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_copper_ingot(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_copper_ingot(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_copper_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_copper_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_diamond_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_diamond_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_diamond_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_diamond_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_diamond_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_diamond_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_hellstone(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_hellstone(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_adamantite(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_adamantite(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_adamantite_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_adamantite_block(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_obsidian(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_obsidian(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_bedrock(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_bedrock(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_granite(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_granite(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_quartz(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_quartz(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_limestone(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_limestone(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_greystone(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_greystone(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_sandstone(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_sandstone(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_coal_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_coal_ore(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_gravel(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_gravel(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_coal(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_coal(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_clay(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_clay(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_red_clay(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_red_clay(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_sand(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_sand(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_snow(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_snow(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_ice(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_ice(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_glass(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_glass(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_glasspane(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_glasspane(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_glasswindow(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_glasswindow(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_bow(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_bow(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_arrow(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_arrow(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_deerskin(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_deerskin(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_rottenleather(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_rottenleather(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_wood_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_wood_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_stone_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_stone_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_copper_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_copper_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_iron_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_iron_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_gold_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_gold_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_diamond_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_diamond_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_platinum_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_platinum_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_unobtanium_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_unobtanium_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_hellstone_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_hellstone_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_adamantite_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_adamantite_pickaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_wood_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_wood_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_stone_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_stone_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_copper_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_copper_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_iron_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_iron_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_gold_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_gold_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_diamond_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_diamond_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_platinum_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_platinum_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_unobtanium_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_unobtanium_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_hellstone_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_hellstone_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_adamantite_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_adamantite_axe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_wood_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_wood_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_stone_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_stone_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_copper_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_copper_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_iron_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_iron_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_gold_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_gold_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_diamond_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_diamond_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_platinum_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_platinum_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_unobtanium_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_unobtanium_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_hellstone_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_hellstone_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_adamantite_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_adamantite_battleaxe(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_wood_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_wood_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_stone_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_stone_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_copper_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_copper_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_iron_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_iron_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_gold_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_gold_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_diamond_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_diamond_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_platinum_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_platinum_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_unobtanium_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_unobtanium_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_hellstone_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_hellstone_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_adamantite_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_adamantite_sword(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_wood_door(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_wood_door(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_iron_door(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_iron_door(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_gold_door(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_gold_door(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_platinum_door(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_platinum_door(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_lighter(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_lighter(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_bed(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_bed(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_bed(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_bed(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_iron_bucket(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_iron_bucket(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_berry(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_berry(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_apple(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_apple(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_chicken(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_chicken(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_deermeat(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_deermeat(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_rottenmeat(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_rottenmeat(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_torch(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_torch(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_crafting_table(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_crafting_table(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_furnace(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_furnace(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def l_use_chest(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    return break_block_generic( _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt, HAND_DAMAGE )

def r_use_chest(  _x, _y, _chunk, _chunk_buffer, _entity_buffer, _dt ):
    pass

def loadImageTable():

    for key in TILE_TABLE:

        TILE_TABLE[key] = pygame.transform.smoothscale(TILE_TABLE[key], (TILE_WIDTH, TILE_WIDTH))
        TILE_TABLE[key] = TILE_TABLE[key].convert_alpha()

    for key in TILE_MODIFIERS:

        for i in range( len(TILE_MODIFIERS[key]) ):

            TILE_MODIFIERS[key][i] = pygame.transform.smoothscale( TILE_MODIFIERS[key][i], ( TILE_WIDTH, TILE_WIDTH ) )
            TILE_MODIFIERS[key][i] = TILE_MODIFIERS[key][i].convert_alpha()

    for key in ITEM_TABLE:

        ITEM_TABLE[key] = ITEM_TABLE[key].convert_alpha()


# Initialize pygame and start the clock
pygame.init()
clock = pygame.time.Clock()
