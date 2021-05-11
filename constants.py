import math , pygame , pygame.freetype
import pygame
import pygame.freetype
import enum
import pickle
import opensimplex

import pygame_gui, os
from pygame_gui.elements import UIButton, UIPanel, UITextBox, UITextEntryLine
from pygame_gui.elements.ui_selection_list import UISelectionList

# The debug verbosity level, can be from 0 to 4 (both inclusive)
DBG                 = 0

def dbg_verbose( *args , **kwargs ):  # Messages which the commong users can see (always printed)
    dbg_generic( 0 , *args , **kwargs )

def dbg_info( *args , **kwargs ):     # Messages which more technical users can see
    dbg_generic( 1 , *args , **kwargs )

def dbg_debug( *args , **kwargs ):    # Messages which devs can see during debug
    dbg_generic( 2 , *args , **kwargs )

def dbg_warning( *args , **kwargs ):  # Messages which devs can see for critical information
    dbg_generic( 3 , *args , **kwargs )

def dbg_generic( msg_priority , *args , **kwargs ):
    if( msg_priority <= DBG ): print( *args , **kwargs )

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
LERP_C              = 0.02

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
PLYR_RANGE          = 4*TILE_WIDTH
INV_COLS            = 10
INV_ROWS            = 3
HAND_DAMAGE         = 30

pygame.freetype.init()
# # entities
# WEIGHT           = 12
INV_FONT         = pygame.freetype.SysFont('Consolas', size=16, bold=True)
INV_COLOR        = ( 0 , 0 , 0 )
# SC_DISPLAY_FONT  = pygame.freetype.SysFont('Consolas', size=20, bold=True)


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

    # interactable tiles
    crafting_table       = 100
    furnace              = 101
    chest                = 102

class item_attr( enum.Enum ):

    MAX_STACK           = 1
    WEIGHT              = 2
    L_USE               = 3
    R_USE               = 4
    DAMAGE              = 5

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

inventory_slot = pygame.image.load("Resources/Default/InventorySpace.png")
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

    tiles.air                 : {tile_attr.FRICTION:AIR_FRICTION, tile_attr.LUMINOSITY:255},
    tiles.grass               : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.browndirt           : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.snowygrass          : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.leaves              : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.junglewood          : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.junglewood_plank    : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.oakwood             : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.oakwood_plank       : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.borealwood          : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.borealwood_plank    : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.pinewood            : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.pinewood_plank      : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.cactuswood          : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.cactuswood_plank    : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.palmwood            : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.palmwood_plank      : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.cosmonium_ore       : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.cosmonium           : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.unobtanium_ore      : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.unobtanium          : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.platinum_ore        : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.platinum            : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.gold_ore            : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.gold                : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.iron_ore            : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.iron                : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.copper_ore          : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.copper              : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.diamond_ore         : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.diamond_block       : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.hellstone           : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.adamantite          : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.obsidian            : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.bedrock             : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.granite             : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.quartz              : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.limestone           : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.greystone           : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.sandstone           : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.gravel              : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.coal                : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.clay                : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.red_clay            : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.sand                : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.snow                : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.ice                 : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.glasspane           : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.glasswindow         : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.wood_door_upper     : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.wood_door_lower     : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.iron_door_upper     : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.iron_door_lower     : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.gold_door_upper     : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.gold_door_lower     : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.platinum_door_upper : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.platinum_door_lower : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.bed_head            : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.bed_tail            : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.torch               : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.crafting_table      : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.furnace             : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None},
    tiles.chest               : {tile_attr.FRICTION:0.8, tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:None}
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

# Dictionary consisting of item as key; dictionary consisting of item attribute as key and attribute as value as value
ITEM_ATTR = {
    items.grass                : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
    items.browndirt            : {item_attr.WEIGHT:100, item_attr.DAMAGE:HAND_DAMAGE, item_attr.L_USE:None, item_attr.R_USE:None},
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