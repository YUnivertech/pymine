import math , pygame , pygame.freetype
import pygame
import pygame.freetype
import enum
import pickle

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

# # entities
# WEIGHT           = 12
# INV_FONT         = pygame.freetype.SysFont('Consolas', size=16, bold=True)
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

class tiles( enum.Enum ):

    air             = 0

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
    L_USE               = 2
    R_USE               = 3
    DAMAGE              = 4

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

'''
# Dictionary consisting of tile as key; name as a string
TILE_NAMES = {
    tiles.air                   : "air",

    # tiles for dirt and grass blocks
    tiles.grass                 : "grass",
    tiles.browndirt             : "dirt",
    tiles.snowygrass            : "snowy grass",
    tiles.leaves                : "leaves",

    # wood
    tiles.junglewood            : "jungle logs",
    tiles.junglewood_plank      : "jungle planks",
    tiles.oakwood               : "oak logs",
    tiles.oakwood_plank         : "oak planks",
    tiles.borealwood            : "boreal logs",
    tiles.borealwood_plank      : "boreal planks",
    tiles.pinewood              :
    tiles.pinewood_plank        :
    tiles.cactuswood            :
    tiles.cactuswood_plank      :
    tiles.palmwood              :
    tiles.palmwood_plank        :

    # metals
    tiles.cosmonium_ore         :
    tiles.cosmonium             :
    tiles.unobtanium_ore        :
    tiles.unobtanium            :
    tiles.platinum_ore          :
    tiles.platinum              :
    tiles.gold_ore              :
    tiles.gold                  :
    tiles.iron_ore              :
    tiles.iron                  :
    tiles.copper_ore            :
    tiles.copper                :

    # non-metals
    tiles.diamond_ore           :
    tiles.diamond_block         :
    tiles.hellstone             :
    tiles.adamantite            :
    tiles.obsidian              :
    tiles.bedrock               :

    # tiles for the stones
    tiles.granite               :
    tiles.quartz                :
    tiles.limestone             :
    tiles.greystone             :
    tiles.sandstone             :

    # tiles for transition blocks
    tiles.gravel                :
    tiles.coal                  :

    # clay
    tiles.clay                  :
    tiles.red_clay              :

    # sand
    tiles.sand                  :

    # snow
    tiles.snow                  :
    tiles.ice                   :

    # glass tiles
    tiles.glasspane             :
    tiles.glasswindow           :

    # door
    tiles.wood_door_upper       :
    tiles.wood_door_lower       :
    tiles.iron_door_upper       :
    tiles.iron_door_lower       :
    tiles.gold_door_upper       :
    tiles.gold_door_lower       :
    tiles.platinum_door_upper   :
    tiles.platinum_door_lower   :

    # bed
    tiles.bed_head              :
    tiles.bed_tail              :

    # torch
    tiles.torch                 :

    # interactable tiles
    tiles.crafting_table        :
    tiles.furnace               :
    tiles.chest                 :
}
'''

# Dictionary consisting of tile as key; list of surfaces of modifiers as value
TILE_MODIFIERS = {
    tile_modifs.crack     :     [pygame.image.load("Resources/Default/break{}.png".format(i)) for i in range(0, 9)]
    # tile_modifs.on_fire:
    # tile_modifs.fire :
    # tile_modifs.water :
    # tile_modifs.lava :
}

# Dictionary consisting of tile as key; surface (image) as value
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

# Dictionary consisting of tile as key; dictionary consisting of tile attribute as key and attribute as value as value
TILE_ATTR = {
    tiles.air           : {tile_attr.LUMINOSITY:255},
    tiles.bedrock       : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:INF, tile_attr.INFLAMMABLE:None},
    tiles.obsidian      : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:0   },
    tiles.hellstone     : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:255, tile_attr.HEALTH:100, tile_attr.INFLAMMABLE:0   },
    tiles.unobtaniumOre : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:160, tile_attr.HEALTH:90,  tile_attr.INFLAMMABLE:None},
    tiles.diamondOre    : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:175, tile_attr.HEALTH:90,  tile_attr.INFLAMMABLE:None},
    tiles.platinumOre   : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:160, tile_attr.HEALTH:80,  tile_attr.INFLAMMABLE:None},
    tiles.goldOre       : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:160, tile_attr.HEALTH:70,  tile_attr.INFLAMMABLE:None},
    tiles.ironOre       : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:160, tile_attr.HEALTH:70,  tile_attr.INFLAMMABLE:None},
    tiles.granite       : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:55,  tile_attr.INFLAMMABLE:None},
    tiles.quartz        : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:55,  tile_attr.INFLAMMABLE:None},
    tiles.limestone     : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:55,  tile_attr.INFLAMMABLE:None},
    tiles.copperOre     : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:160, tile_attr.HEALTH:60,  tile_attr.INFLAMMABLE:None},
    tiles.greystone     : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:55,  tile_attr.INFLAMMABLE:None},
    tiles.sandstone     : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:50,  tile_attr.INFLAMMABLE:None},
    tiles.gravel        : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:50,  tile_attr.INFLAMMABLE:None},
    tiles.coke          : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:160, tile_attr.HEALTH:50,  tile_attr.INFLAMMABLE:None},
    tiles.clay          : {tile_attr.FRICTION:0.9,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:45,  tile_attr.INFLAMMABLE:None},
    tiles.redClay       : {tile_attr.FRICTION:0.9,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:45,  tile_attr.INFLAMMABLE:None},
    tiles.browndirt     : {tile_attr.FRICTION:0.8,  tile_attr.LUMINOSITY:0,   tile_attr.HEALTH:30,  tile_attr.INFLAMMABLE:None}
}

# # Dictionary consisting of item as key; name as a string
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

# Dictionary consisting of item as key; surface (image) as value
# ITEM_TABLE = {
#     slot : pygame.image.load( "../Resources/Default/InventorySpace.png" )
# }

# Dictionary consisting of item as key; dictionary consisting of item attribute as key and attribute as value as value
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

# def loadImageTable():
#     for key in TILE_TABLE:
#         TILE_TABLE[key] = pygame.transform.smoothscale(TILE_TABLE[key], (TILE_WIDTH, TILE_WIDTH))
#         TILE_TABLE[key] = TILE_TABLE[key].convert_alpha()
#     for key in TILE_MODIFIERS:
#         for i in range(0, len(TILE_MODIFIERS[key])):
#             TILE_MODIFIERS[key][i] = pygame.transform.smoothscale( TILE_MODIFIERS[key][i], ( TILE_WIDTH, TILE_WIDTH ) )
#             TILE_MODIFIERS[key][i] = TILE_MODIFIERS[key][i].convert_alpha()
#     for key in ITEM_TABLE:
#         ITEM_TABLE[key] = ITEM_TABLE[key].convert_alpha()