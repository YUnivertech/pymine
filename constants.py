import math , pygame , pygame.freetype
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
# INV_FONT            = pygame.freetype.SysFont( 'Consolas' , size = 16 , bold = True )

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


# ! ----------------------------------------------------------------

class tile_modifs( enum.Enum ):
    crack           = 0

class tiles( enum.Enum ):

    air             = 0

    bedrock         = 1
    obsidian        = 2
    hellstone       = 3

    unobtanium_ore  = 4
    diamond_ore     = 5
    platinum_ore    = 6
    gold_ore        = 7
    iron_ore        = 8
    copper_ore      = 9

    granite         = 10
    quartz          = 11
    limestone       = 12
    greystone       = 13
    sandstone       = 14

    gravel          = 15
    coke            = 16

    clay            = 17
    red_clay        = 18


    brown_dirt      = 20

class items( enum.Enum ):
    air = 0


# Tile table with names
TILE_NAMES = {
    tiles.air             : "air",
    tiles.bedrock         : "bedrock",
    tiles.obsidian        : "obsidian",
    tiles.hellstone       : "hellstone",
    tiles.unobtanium_ore  : "unrefined unobtanium",
    tiles.diamond_ore     : "diamond ore",
    tiles.platinum_ore    : "platinum ore",
    tiles.gold_ore        : "gold ore",
    tiles.iron_ore        : "iron ore",
    tiles.copper_ore      : "copper ore",
    tiles.granite         : "granite",
    tiles.quartz          : "quartz",
    tiles.limestone       : "limestone",
    tiles.greystone       : "stone",
    tiles.sandstone       : "sandstone",
    tiles.gravel          : "gravel",
    tiles.coke            : "coke",
    tiles.clay            : "clay",
    tiles.red_clay        : "red clay",
    tiles.brown_dirt      : "dirt"
}

TILE_MODIFIERS = {
    tile_modifs.crack     :     [pygame.image.load("Resources/Default/break{}.png".format(i)) for i in range(0, 9)]
    # tile_modifs.on_fire:
    # tile_modifs.fire :
    # tile_modifs.water :
    # tile_modifs.lava :
}

TILE_TABLE = {

    tiles.bedrock         : pygame.image.load("Resources/Default/bedrock.png"),
    tiles.obsidian        : pygame.image.load("Resources/Default/obsidian.png"),
    tiles.hellstone       : pygame.image.load("Resources/Default/hellstone.png"),
    tiles.unobtanium_ore  : pygame.image.load("Resources/Default/unobtaniumOre.png"),
    tiles.diamond_ore     : pygame.image.load("Resources/Default/diamondOre.png"),
    tiles.platinum_ore    : pygame.image.load("Resources/Default/ironOre.png"),
    tiles.gold_ore        : pygame.image.load("Resources/Default/goldOre.png"),
    tiles.iron_ore        : pygame.image.load("Resources/Default/ironOre.png"),
    tiles.copper_ore      : pygame.image.load("Resources/Default/copperOre.png"),
    tiles.granite         : pygame.image.load("Resources/Default/granite.png"),
    tiles.quartz          : pygame.image.load("Resources/Default/quartz.png"),
    tiles.limestone       : pygame.image.load("Resources/Default/limestone.png"),
    tiles.greystone       : pygame.image.load("Resources/Default/greystone.png"),
    tiles.sandstone       : pygame.image.load("Resources/Default/sandstone.png"),
    tiles.gravel          : pygame.image.load("Resources/Default/gravel.png"),
    tiles.coke            : pygame.image.load("Resources/Default/coalOre.png"),
    tiles.clay            : pygame.image.load("Resources/Default/clay.png"),
    tiles.red_clay        : pygame.image.load("Resources/Default/redClay.png"),
    tiles.brown_dirt      : pygame.image.load("Resources/Default/browndirt.png")
}

# TILE_ATTR = {
#     air           :{LUMINOSITY:255},
#     bedrock       :{ID:1,  FRICTION:0.8,  LUMINOSITY:0,   HEALTH:INF, INFLAMMABLE:None},
#     obsidian      :{ID:2,  FRICTION:0.8,  LUMINOSITY:0,   HEALTH:100, INFLAMMABLE:0   },
#     hellstone     :{ID:3,  FRICTION:0.8,  LUMINOSITY:255, HEALTH:100, INFLAMMABLE:0   },
#     unobtaniumOre :{ID:4,  FRICTION:0.8,  LUMINOSITY:160, HEALTH:90,  INFLAMMABLE:None},
#     diamondOre    :{ID:5,  FRICTION:0.8,  LUMINOSITY:175, HEALTH:90,  INFLAMMABLE:None},
#     platinumOre   :{ID:6,  FRICTION:0.8,  LUMINOSITY:160, HEALTH:80,  INFLAMMABLE:None},
#     goldOre       :{ID:7,  FRICTION:0.8,  LUMINOSITY:160, HEALTH:70,  INFLAMMABLE:None},
#     ironOre       :{ID:8,  FRICTION:0.8,  LUMINOSITY:160, HEALTH:70,  INFLAMMABLE:None},
#     granite       :{ID:9,  FRICTION:0.8,  LUMINOSITY:0,   HEALTH:55,  INFLAMMABLE:None},
#     quartz        :{ID:10, FRICTION:0.8,  LUMINOSITY:0,   HEALTH:55,  INFLAMMABLE:None},
#     limestone     :{ID:11, FRICTION:0.8,  LUMINOSITY:0,   HEALTH:55,  INFLAMMABLE:None},
#     copperOre     :{ID:12, FRICTION:0.8,  LUMINOSITY:160, HEALTH:60,  INFLAMMABLE:None},
#     greystone     :{ID:13, FRICTION:0.8,  LUMINOSITY:0,   HEALTH:55,  INFLAMMABLE:None},
#     sandstone     :{ID:14, FRICTION:0.8,  LUMINOSITY:0,   HEALTH:50,  INFLAMMABLE:None},
#     gravel        :{ID:15, FRICTION:0.8,  LUMINOSITY:0,   HEALTH:50,  INFLAMMABLE:None},
#     coke          :{ID:16, FRICTION:0.8,  LUMINOSITY:160, HEALTH:50,  INFLAMMABLE:None},
#     clay          :{ID:17, FRICTION:0.9,  LUMINOSITY:0,   HEALTH:45,  INFLAMMABLE:None},
#     redClay       :{ID:18, FRICTION:0.9,  LUMINOSITY:0,   HEALTH:45,  INFLAMMABLE:None},
#     browndirt     :{ID:20, FRICTION:0.8,  LUMINOSITY:0,   HEALTH:30,  INFLAMMABLE:None}
#
# }
#
#
# def loadImageTable():
#     for key in TILE_TABLE:
#         TILE_TABLE[key] = pygame.transform.smoothscale(TILE_TABLE[key], (TILE_WIDTH, TILE_WIDTH))
#         TILE_TABLE[key] = TILE_TABLE[key].convert_alpha()
#     for key in TILE_MODIFIERS:
#         for i in range(0, len(TILE_MODIFIERS[key])):
#             TILE_MODIFIERS[key][i] = pygame.transform.smoothscale( TILE_MODIFIERS[key][i], ( TILE_WIDTH, TILE_WIDTH ) )
#             TILE_MODIFIERS[key][i] = TILE_MODIFIERS[key][i].convert_alpha()

# ! ----------------------------------------------------------------------

# from Old.constants import *
#
# HAND_DAMAGE = 30
# USE = 13
#
# slot                 = 0
#
# # items for dirt and grass blocks
# grass                = 1
# browndirt            = 2
# snowygrass           = 3
# stick                = 4
#
# # wood
# junglewood           = 10
# junglewood_plank     = 11
# oakwood              = 12
# oakwood_plank        = 13
# borealwood           = 14
# borealwood_plank     = 15
# pinewood             = 16
# pinewood_plank       = 17
# cactuswood           = 18
# cactuswood_plank     = 19
# palmwood             = 20
# palmwood_plank       = 21
#
# # metals
# cosmonium_ore        = 30
# cosmonium_ingot      = 31
# cosmonium_block      = 32
# unobtanium_ore       = 33
# unobtanium_ingot     = 34
# unobtanium_block     = 35
# platinum_ore         = 36
# platinum_ingot       = 37
# platinum_block       = 38
# gold_ore             = 39
# gold_brick           = 40
# gold_block           = 41
# iron_ore             = 42
# iron_ingot           = 43
# iron_block           = 44
# copper_ore           = 45
# copper_ingot         = 46
# copper_block         = 47
#
# # non-metals
# diamond_ore          = 50
# diamond_gem          = 51
# diamond_block        = 52
# hellstone            = 53
# adamantite           = 54
# adamantite_block     = 55
# obsidian             = 56
# bedrock              = 57
#
# # items for the stones
# granite              = 60
# quartz               = 61
# limestone            = 62
# greystone            = 63
# sandstone            = 64
#
# # items for transition blocks
# gravel               = 70
# coal                 = 71
#
# # items for the clay blocks
# clay                 = 72
# redClay              = 73
#
# # item for the sand block
# sand                 = 74
#
# # items for snowy blocks
# snow                 = 75
# ice                  = 76
#
# # items for the glass blocks
# glass                = 77
# # glasspane          = 78
# glasswindow          = 78
#
# # bow and arrow
# bow                  = 80
# arrow                = 81
#
# # animal hides
# deerskin             = 82
# rottenleather        = 83
#
# # pickaxes
# wood_pickaxe         = 90
# stone_pickaxe        = 91
# copper_pickaxe       = 92
# iron_pickaxe         = 93
# gold_pickaxe         = 94
# diamond_pickaxe      = 95
# platinum_pickaxe     = 96
# unobtanium_pickaxe   = 97
# hellstone_pickaxe    = 98
# adamantite_pickaxe   = 99
#
# # axes
# wood_axe             = 100
# stone_axe            = 101
# copper_axe           = 102
# iron_axe             = 103
# gold_axe             = 104
# diamond_axe          = 105
# platinum_axe         = 106
# unobtanium_axe       = 107
# hellstone_axe        = 108
# adamantite_axe       = 109
#
# # battle axes
# wood_battleaxe       = 110
# stone_battleaxe      = 111
# copper_battleaxe     = 112
# iron_battleaxe       = 113
# gold_battleaxe       = 114
# diamond_battleaxe    = 115
# platinum_battleaxe   = 116
# unobtanium_battleaxe = 117
# hellstone_battleaxe  = 118
# adamantite_battleaxe = 119
#
# # swords
# wood_sword           = 120
# stone_sword          = 121
# copper_sword         = 122
# iron_sword           = 123
# gold_sword           = 124
# diamond_sword        = 125
# platinum_sword       = 126
# unobtanium_sword     = 127
# hellstone_sword      = 128
# adamantite_sword     = 129
#
# # door
# wood_door            = 130
# iron_door            = 131
# gold_door            = 132
# platinum_door        = 133
#
# # lighter
# lighter              = 140
#
# # bed and bucket
# bed                  = 141
# iron_bucket          = 142
#
# # fruits
# berry                = 143
# apple                = 144
#
# # meats
# chicken              = 145
# deermeat             = 146
# rottenmeat           = 147
#
# torch                = 148
#
# crafting_table       = 149
# furnace              = 150
#
# ITEM_NAMES = {
#     grass                : "grass",
#     browndirt            : "dirt",
#     snowygrass           : "snowy grass",
#     stick                : "stick",
#     junglewood           : "jungle wood",
#     junglewood_plank     : "plank of jungle wood",
#     oakwood              : "oak wood",
#     oakwood_plank        : "plank of oak wood",
#     borealwood           : "boreal wood",
#     borealwood_plank     : "plank of boreal wood",
#     pinewood             : "pine wood",
#     pinewood_plank       : "plank of pine wood",
#     cactuswood           : "cactus wood",
#     cactuswood_plank     : "plank of cactus wood",
#     palmwood             : "palm wood",
#     palmwood_plank       : "plank of palm wood",
#     cosmonium_ore        : "ore of cosmonium",
#     cosmonium_ingot      : "cosmonium ingot",
#     cosmonium_block      : "block of cosmonium",
#     unobtanium_ore       : "ore of unobtanium",
#     unobtanium_ingot     : "unobtanium ingot",
#     unobtanium_block     : "block of unobtanium",
#     platinum_ore         : "ore of platinum",
#     platinum_ingot       : "platinum ingot",
#     platinum_block       : "block of platinum",
#     gold_ore             : "ore of gold",
#     gold_brick           : "gold brick",
#     gold_block           : "block of gold",
#     iron_ore             : "ore of iron",
#     iron_ingot           : "iron ingot",
#     iron_block           : "block of iron",
#     copper_ore           : "ore of copper",
#     copper_ingot         : "copper ingot",
#     copper_block         : "block of copper",
#     diamond_ore          : "ore of diamond",
#     diamond_gem          : "diamond gem",
#     diamond_block        : "block of diamond",
#     hellstone            : "hellstone",
#     adamantite           : "adamantite",
#     adamantite_block     : "block of ",
#     obsidian             : "obsidian",
#     bedrock              : "bedrock",
#     granite              : "granite",
#     quartz               : "quartz",
#     limestone            : "limestone",
#     greystone            : "grey stone",
#     sandstone            : "sandstone",
#     gravel               : "gravel",
#     coal                 : "coal",
#     clay                 : "clay",
#     redClay              : "red clay",
#     sand                 : "sand",
#     snow                 : "snow",
#     ice                  : "ice",
#     glass                : "glass",
#     glasswindow          : "glass window",
#     bow                  : "wooden bow",
#     arrow                : "arrow",
#     deerskin             : "skin of deer",
#     rottenleather        : "rotten leather",
#     wood_pickaxe         : "wooden pickaxe",
#     stone_pickaxe        : "stone pickaxe",
#     copper_pickaxe       : "copper pickaxe",
#     iron_pickaxe         : "iron pickaxe",
#     gold_pickaxe         : "gold pickaxe",
#     diamond_pickaxe      : "diamond pickaxe",
#     platinum_pickaxe     : "platinum pickaxe",
#     unobtanium_pickaxe   : "unobtanium pickaxe",
#     hellstone_pickaxe    : "hellstone pickaxe",
#     adamantite_pickaxe   : "adamantite pickaxe",
#     wood_axe             : "wooden axe",
#     stone_axe            : "stone axe",
#     copper_axe           : "copper axe",
#     iron_axe             : "iron axe",
#     gold_axe             : "gold axe",
#     diamond_axe          : "diamond axe",
#     platinum_axe         : "platinum axe",
#     unobtanium_axe       : "unobtanium axe",
#     hellstone_axe        : "hellstone axe",
#     adamantite_axe       : "adamantite axe",
#     wood_battleaxe       : "wooden battle axe",
#     stone_battleaxe      : "stone battle axe",
#     copper_battleaxe     : "copper battle axe",
#     iron_battleaxe       : "iron battle axe",
#     gold_battleaxe       : "gold battle axe",
#     diamond_battleaxe    : "diamond battle axe",
#     platinum_battleaxe   : "platinum battle axe",
#     unobtanium_battleaxe : "unobtanium battle axe",
#     hellstone_battleaxe  : "hellstone battle axe",
#     adamantite_battleaxe : "adamantite battle axe",
#     wood_sword           : "wooden sword",
#     stone_sword          : "stone sword",
#     copper_sword         : "copper sword",
#     iron_sword           : "iron sword",
#     gold_sword           : "gold sword",
#     diamond_sword        : "diamond sword",
#     platinum_sword       : "platinum sword",
#     unobtanium_sword     : "unobtanium sword",
#     hellstone_sword      : "hellstone sword",
#     adamantite_sword     : "adamantite sword",
#     wood_door            : "wooden door",
#     iron_door            : "iron door",
#     gold_door            : "gold door",
#     platinum_door        : "platinum door",
#     lighter              : "lighter",
#     bed                  : "bed",
#     iron_bucket          : "iron bucket",
#     berry                : "berry",
#     apple                : "apple",
#     chicken              : "chicken",
#     deermeat             : "meat of deer",
#     rottenmeat           : "rotten meat",
#     torch                : "torch",
#     crafting_table       : "crafting table",
#     furnace              : "furnace"
# }
#
# ITEM_TABLE = {
#     slot : pygame.image.load( "../Resources/Default/InventorySpace.png" )
# }
#
# ITEM_ATTR = {
#     grass                : {ID:grass               , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     browndirt            : {ID:browndirt           , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     snowygrass           : {ID:snowygrass          , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     stick                : {ID:stick               , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     junglewood           : {ID:junglewood          , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     junglewood_plank     : {ID:junglewood_plank    , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     oakwood              : {ID:oakwood             , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     oakwood_plank        : {ID:oakwood_plank       , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     borealwood           : {ID:borealwood          , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     borealwood_plank     : {ID:borealwood_plank    , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     pinewood             : {ID:pinewood            , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     pinewood_plank       : {ID:pinewood_plank      , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     cactuswood           : {ID:cactuswood          , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     cactuswood_plank     : {ID:cactuswood_plank    , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     palmwood             : {ID:palmwood            , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     palmwood_plank       : {ID:palmwood_plank      , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     cosmonium_ore        : {ID:cosmonium_ore       , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     cosmonium_ingot      : {ID:cosmonium_ingot     , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     cosmonium_block      : {ID:cosmonium_block     , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     unobtanium_ore       : {ID:unobtanium_ore      , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     unobtanium_ingot     : {ID:unobtanium_ingot    , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     unobtanium_block     : {ID:unobtanium_block    , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     platinum_ore         : {ID:platinum_ore        , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     platinum_ingot       : {ID:platinum_ingot      , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     platinum_block       : {ID:platinum_block      , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     gold_ore             : {ID:gold_ore            , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     gold_brick           : {ID:gold_brick          , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     gold_block           : {ID:gold_block          , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     iron_ore             : {ID:iron_ore            , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     iron_ingot           : {ID:iron_ingot          , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     iron_block           : {ID:iron_block          , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     copper_ore           : {ID:copper_ore          , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     copper_ingot         : {ID:copper_ingot        , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     copper_block         : {ID:copper_block        , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     diamond_ore          : {ID:diamond_ore         , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     diamond_gem          : {ID:diamond_gem         , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     diamond_block        : {ID:diamond_block       , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     hellstone            : {ID:hellstone           , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     adamantite           : {ID:adamantite          , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     adamantite_block     : {ID:adamantite_block    , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     obsidian             : {ID:obsidian            , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     bedrock              : {ID:bedrock             , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     granite              : {ID:granite             , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     quartz               : {ID:quartz              , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     limestone            : {ID:limestone           , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     greystone            : {ID:greystone           , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     sandstone            : {ID:sandstone           , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     gravel               : {ID:gravel              , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     coal                 : {ID:coal                , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     clay                 : {ID:clay                , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     redClay              : {ID:redClay             , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     sand                 : {ID:sand                , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     snow                 : {ID:snow                , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     ice                  : {ID:ice                 , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     glass                : {ID:glass               , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     glasswindow          : {ID:glasswindow         , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     bow                  : {ID:bow                 , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     arrow                : {ID:arrow               , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     deerskin             : {ID:deerskin            , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     rottenleather        : {ID:rottenleather       , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     wood_pickaxe         : {ID:wood_pickaxe        , WEIGHT:100, DAMAGE: 100        , USE:None },
#     stone_pickaxe        : {ID:stone_pickaxe       , WEIGHT:100, DAMAGE: 100        , USE:None },
#     copper_pickaxe       : {ID:copper_pickaxe      , WEIGHT:100, DAMAGE: 100        , USE:None },
#     iron_pickaxe         : {ID:iron_pickaxe        , WEIGHT:100, DAMAGE: 100        , USE:None },
#     gold_pickaxe         : {ID:gold_pickaxe        , WEIGHT:100, DAMAGE: 100        , USE:None },
#     diamond_pickaxe      : {ID:diamond_pickaxe     , WEIGHT:100, DAMAGE: 100        , USE:None },
#     platinum_pickaxe     : {ID:platinum_pickaxe    , WEIGHT:100, DAMAGE: 100        , USE:None },
#     unobtanium_pickaxe   : {ID:unobtanium_pickaxe  , WEIGHT:100, DAMAGE: 100        , USE:None },
#     hellstone_pickaxe    : {ID:hellstone_pickaxe   , WEIGHT:100, DAMAGE: 100        , USE:None },
#     adamantite_pickaxe   : {ID:adamantite_pickaxe  , WEIGHT:100, DAMAGE: 100        , USE:None },
#     wood_axe             : {ID:wood_axe            , WEIGHT:100, DAMAGE: 100        , USE:None },
#     stone_axe            : {ID:stone_axe           , WEIGHT:100, DAMAGE: 100        , USE:None },
#     copper_axe           : {ID:copper_axe          , WEIGHT:100, DAMAGE: 100        , USE:None },
#     iron_axe             : {ID:iron_axe            , WEIGHT:100, DAMAGE: 100        , USE:None },
#     gold_axe             : {ID:gold_axe            , WEIGHT:100, DAMAGE: 100        , USE:None },
#     diamond_axe          : {ID:diamond_axe         , WEIGHT:100, DAMAGE: 100        , USE:None },
#     platinum_axe         : {ID:platinum_axe        , WEIGHT:100, DAMAGE: 100        , USE:None },
#     unobtanium_axe       : {ID:unobtanium_axe      , WEIGHT:100, DAMAGE: 100        , USE:None },
#     hellstone_axe        : {ID:hellstone_axe       , WEIGHT:100, DAMAGE: 100        , USE:None },
#     adamantite_axe       : {ID:adamantite_axe      , WEIGHT:100, DAMAGE: 100        , USE:None },
#     wood_battleaxe       : {ID:wood_battleaxe      , WEIGHT:100, DAMAGE: 100        , USE:None },
#     stone_battleaxe      : {ID:stone_battleaxe     , WEIGHT:100, DAMAGE: 100        , USE:None },
#     copper_battleaxe     : {ID:copper_battleaxe    , WEIGHT:100, DAMAGE: 100        , USE:None },
#     iron_battleaxe       : {ID:iron_battleaxe      , WEIGHT:100, DAMAGE: 100        , USE:None },
#     gold_battleaxe       : {ID:gold_battleaxe      , WEIGHT:100, DAMAGE: 100        , USE:None },
#     diamond_battleaxe    : {ID:diamond_battleaxe   , WEIGHT:100, DAMAGE: 100        , USE:None },
#     platinum_battleaxe   : {ID:platinum_battleaxe  , WEIGHT:100, DAMAGE: 100        , USE:None },
#     unobtanium_battleaxe : {ID:unobtanium_battleaxe, WEIGHT:100, DAMAGE: 100        , USE:None },
#     hellstone_battleaxe  : {ID:hellstone_battleaxe , WEIGHT:100, DAMAGE: 100        , USE:None },
#     adamantite_battleaxe : {ID:adamantite_battleaxe, WEIGHT:100, DAMAGE: 100        , USE:None },
#     wood_sword           : {ID:wood_sword          , WEIGHT:100, DAMAGE: 100        , USE:None },
#     stone_sword          : {ID:stone_sword         , WEIGHT:100, DAMAGE: 100        , USE:None },
#     copper_sword         : {ID:copper_sword        , WEIGHT:100, DAMAGE: 100        , USE:None },
#     iron_sword           : {ID:iron_sword          , WEIGHT:100, DAMAGE: 100        , USE:None },
#     gold_sword           : {ID:gold_sword          , WEIGHT:100, DAMAGE: 100        , USE:None },
#     diamond_sword        : {ID:diamond_sword       , WEIGHT:100, DAMAGE: 100        , USE:None },
#     platinum_sword       : {ID:platinum_sword      , WEIGHT:100, DAMAGE: 100        , USE:None },
#     unobtanium_sword     : {ID:unobtanium_sword    , WEIGHT:100, DAMAGE: 100        , USE:None },
#     hellstone_sword      : {ID:hellstone_sword     , WEIGHT:100, DAMAGE: 100        , USE:None },
#     adamantite_sword     : {ID:adamantite_sword    , WEIGHT:100, DAMAGE: 100        , USE:None },
#     wood_door            : {ID:wood_door           , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     iron_door            : {ID:iron_door           , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     gold_door            : {ID:gold_door           , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     platinum_door        : {ID:platinum_door       , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     lighter              : {ID:lighter             , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     bed                  : {ID:bed                 , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     iron_bucket          : {ID:iron_bucket         , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     berry                : {ID:berry               , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     apple                : {ID:apple               , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     chicken              : {ID:chicken             , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     deermeat             : {ID:deermeat            , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     rottenmeat           : {ID:rottenmeat          , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     torch                : {ID:torch               , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     crafting_table       : {ID:crafting_table      , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None },
#     furnace              : {ID:furnace             , WEIGHT:100, DAMAGE: HAND_DAMAGE, USE:None }
# }
#
#
# def loadImageTable():
#     for key in ITEM_TABLE:
#         ITEM_TABLE[key] = ITEM_TABLE[key].convert_alpha()
