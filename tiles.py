from constants import *

# Tile names along with their IDs
crack         = 0

# air
air           = 0

# blocks in the bedrock wastes
bedrock       = 1
obsidian      = 2
hellstone     = 3

# blocks for mineral ores
unobtaniumOre = 4
diamondOre    = 5
platinumOre   = 6
goldOre       = 7
ironOre       = 8
copperOre     = 9

# blocks for stones
granite       = 10
quartz        = 11
limestone     = 12
greystone     = 13
sandstone     = 14

# blocks for transition blocks
gravel        = 15
coke          = 16

# blocks for clays
clay          = 17
redClay       = 18

# blocks for dirt and grass
browndirt     = 20

# Tile table with names
TILE_NAMES = {
    # air
    air           : "air",
    bedrock       : "bedrock",
    obsidian      : " obsidian",
    hellstone     : " hellstone",
    unobtaniumOre : "unrefined unobtanium",
    diamondOre    : "diamond ore",
    platinumOre   : "platinum ore",
    goldOre       : "gold ore",
    ironOre       : "iron ore",
    copperOre     : "copper ore",
    granite       : "granite",
    quartz        : "quartz",
    limestone     : "limestone",
    greystone     : "stone",
    sandstone     : "sandstone",
    gravel        : "gravel",
    coke          : "coke",
    clay          : "clay",
    redClay       : "red clay",
    browndirt     : "dirt"

}

TILE_MODIFIERS = {
    crack :     [pygame.image.load("Resources/Default/break{}.png".format(i)) for i in range(0, 9)]

}

TILE_TABLE = {

    bedrock       : pygame.image.load("Resources/Default/bedrock.png"),
    obsidian      : pygame.image.load("Resources/Default/obsidian.png"),
    hellstone     : pygame.image.load("Resources/Default/hellstone.png"),
    unobtaniumOre : pygame.image.load("Resources/Default/unobtaniumOre.png"),
    diamondOre    : pygame.image.load("Resources/Default/diamondOre.png"),
    platinumOre   : pygame.image.load("Resources/Default/ironOre.png"),
    goldOre       : pygame.image.load("Resources/Default/goldOre.png"),
    ironOre       : pygame.image.load("Resources/Default/ironOre.png"),
    copperOre     : pygame.image.load("Resources/Default/copperOre.png"),
    granite       : pygame.image.load("Resources/Default/granite.png"),
    quartz        : pygame.image.load("Resources/Default/quartz.png"),
    limestone     : pygame.image.load("Resources/Default/limestone.png"),
    greystone     : pygame.image.load("Resources/Default/greystone.png"),
    sandstone     : pygame.image.load("Resources/Default/sandstone.png"),
    gravel        : pygame.image.load("Resources/Default/gravel.png"),
    coke          : pygame.image.load("Resources/Default/coalOre.png"),
    clay          : pygame.image.load("Resources/Default/clay.png"),
    redClay       : pygame.image.load("Resources/Default/redClay.png"),
    browndirt     : pygame.image.load("Resources/Default/browndirt.png")
}

TILE_ATTR = {
    air           :{LUMINOSITY:255},
    bedrock       :{ID:1,  FRICTION:0.8,  LUMINOSITY:0,   HEALTH:INF, INFLAMMABLE:None},
    obsidian      :{ID:2,  FRICTION:0.8,  LUMINOSITY:0,   HEALTH:100, INFLAMMABLE:0   },
    hellstone     :{ID:3,  FRICTION:0.8,  LUMINOSITY:255, HEALTH:100, INFLAMMABLE:0   },
    unobtaniumOre :{ID:4,  FRICTION:0.8,  LUMINOSITY:160, HEALTH:90,  INFLAMMABLE:None},
    diamondOre    :{ID:5,  FRICTION:0.8,  LUMINOSITY:175, HEALTH:90,  INFLAMMABLE:None},
    platinumOre   :{ID:6,  FRICTION:0.8,  LUMINOSITY:160, HEALTH:80,  INFLAMMABLE:None},
    goldOre       :{ID:7,  FRICTION:0.8,  LUMINOSITY:160, HEALTH:70,  INFLAMMABLE:None},
    ironOre       :{ID:8,  FRICTION:0.8,  LUMINOSITY:160, HEALTH:70,  INFLAMMABLE:None},
    granite       :{ID:9,  FRICTION:0.8,  LUMINOSITY:0,   HEALTH:55,  INFLAMMABLE:None},
    quartz        :{ID:10, FRICTION:0.8,  LUMINOSITY:0,   HEALTH:55,  INFLAMMABLE:None},
    limestone     :{ID:11, FRICTION:0.8,  LUMINOSITY:0,   HEALTH:55,  INFLAMMABLE:None},
    copperOre     :{ID:12, FRICTION:0.8,  LUMINOSITY:160, HEALTH:60,  INFLAMMABLE:None},
    greystone     :{ID:13, FRICTION:0.8,  LUMINOSITY:0,   HEALTH:55,  INFLAMMABLE:None},
    sandstone     :{ID:14, FRICTION:0.8,  LUMINOSITY:0,   HEALTH:50,  INFLAMMABLE:None},
    gravel        :{ID:15, FRICTION:0.8,  LUMINOSITY:0,   HEALTH:50,  INFLAMMABLE:None},
    coke          :{ID:16, FRICTION:0.8,  LUMINOSITY:160, HEALTH:50,  INFLAMMABLE:None},
    clay          :{ID:17, FRICTION:0.9,  LUMINOSITY:0,   HEALTH:45,  INFLAMMABLE:None},
    redClay       :{ID:18, FRICTION:0.9,  LUMINOSITY:0,   HEALTH:45,  INFLAMMABLE:None},
    browndirt     :{ID:20, FRICTION:0.8,  LUMINOSITY:0,   HEALTH:30,  INFLAMMABLE:None}

}


def loadImageTable():
    for key in TILE_TABLE:
        TILE_TABLE[key] = pygame.transform.smoothscale(TILE_TABLE[key], (TILE_WIDTH, TILE_WIDTH))
        TILE_TABLE[key] = TILE_TABLE[key].convert_alpha()
    for key in TILE_MODIFIERS:
        for i in range(0, len(TILE_MODIFIERS[key])):
            TILE_MODIFIERS[key][i] = pygame.transform.smoothscale( TILE_MODIFIERS[key][i], ( TILE_WIDTH, TILE_WIDTH ) )
            TILE_MODIFIERS[key][i] = TILE_MODIFIERS[key][i].convert_alpha()
