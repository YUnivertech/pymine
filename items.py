from constants import *

# Item names along with their IDs

# inventory
slot            =  0

# foods
berry           =  1
apple           =  2

# woods
junglewood      =  3
oakwood         =  4
borealwood      =  5
pinewood        =  6
cactuswood      =  7
palmwood        =  8

# bow and arrow
bow             =  46
arrow           =  47

# pickaxes
wood_pickaxe    =  53
stone_pickaxe   =  54
copper_pickaxe  =  55
iron_pickaxe    =  56
gold_pickaxe    =  57
dia_pickaxe     =  58
plat_pickaxe    =  59
unob_pickaxe    =  60
hell_pickaxe    =  61
cosmo_pickaxe   =  62

# axes
wood_axe        =  63
stone_axe       =  64
copper_axe      =  65
iron_axe        =  66
gold_axe        =  67
dia_axe         =  68
plat_axe        =  69
unob_axe        =  70
hell_axe        =  71
cosmo_axe       =  72

# battle axes
wood_battleaxe  =  73
stone_battleaxe =  74
copper_battleaxe=  75
iron_battleaxe  =  76
gold_battleaxe  =  77
dia_battleaxe   =  78
plat_battleaxe  =  79
unob_battleaxe  =  80
hell_battleaxe  =  81
cosmo_battleaxe =  82

# swords
wood_sword      =  83
stone_sword     =  84
copper_sword    =  85
iron_sword      =  86
gold_sword      =  87
dia_sword       =  88
plat_sword      =  89
unob_sword      =  90
hell_sword      =  91
cosmo_sword     =  92

# lighter
lighter         =  93

# animal hides
deerskin        =  48
rottenleather   =  49

# meats
chicken         =  50
deermeat        =  51
rottenmeat      =  52

# door
door            =  43

# bed and bucket
bed             =  45
bucket          =  46

# items for blocks from the bedrock wastes
bedrock         =  1
obsidian        =  2
hellstone       =  3

# items for ores (not the same as the items for the block)
unobtaniumOre   =  4
diamondOre      =  5
platinumOre     =  6
goldOre         =  7
ironOre         =  8
copperOre       =  9

# items for the stones
granite         =  10
quartz          =  11
limestone       =  12
greystone       =  13
sandstone       =  14

# items for transition blocks
gravel          =  15
coke            =  16

# items for the clay blocks
clay            =  17
redClay         =  18

# item for the sand block
sand            =  19

# items for dirt and grass blocks
browndirt       =  20
grass           =  21
snowygrass      =  22

# items for snowy blocks
snow            =  23
ice             =  24

# items for all the wood blocks
junglewood     =  25
oakwood        =  26
borealwood     =  27
pinewood       =  28
cactuswood     =  29
palmwood       =  30

# items for the mineral blocks
cosmonium  =  31
adamantite =  32
unobtanium =  33
diamond    =  34
platinum   =  35
gold       =  36
iron       =  37
copper     =  38

# items for the mineral ingots/ pieces
cosmonium  =  31
adamantite =  32
unobtanium =  33
diamond    =  34
platinum   =  35
gold       =  36
iron       =  37
copper     =  38

# items for the glass blocks
glass           =  39
glasswindow     =  40

torch           =  41

ITEM_NAMES = {
    door           : "door",
    bed            : "bed",
    bucket         : "bucket",
    bow            : "bow",
    arrow          : "arrow",
    lighter        : "lighter",
    deerskin       : "deer skin",
    rottenleather  : "rotten leather",
    chicken        : "chicken",
    deermeat       : "deer meat",
    rottenmeat     : "rotten meat",
    berry          : "berry",
    apple          : "apple"
}

TILE_NAMES = {

    # bedrock wastes blocks
    bedrock        : "bedrock",
    obsidian       : "block of obsidian",
    hellstone      : "block of hellstone",

    # ores
    unobtaniumOre   : "unrefined unobtanium",
    diamondOre      : "diamond ore",
    platinumOre     : "platinum ore",
    goldOre         : "gold ore",
    ironOre         : "iron ore",
    copperOre       : "copper ore",


    # stones
    granite        : "block of granite",
    quartz         : "block of quartz",
    limestone      : "block of limestone",
    greystone      : "block of stone",
    sandstone      : "block of sandstone",

    # transition blocks
    gravel         : "block of gravel",
    coke           : "block of coke",

    # clays
    clay           : "block of clay",
    redClay        : "block of red clay",

    # sand
    sand           : "block of sand",

    # dirt, grass
    browndirt      : "block of dirt",
    grass          : "block of grass",

    # Snowy blocks
    snowygrass     : "block of snowy grass",
    snow           : "block of snow",
    ice            : "block of ice",

    # woods
    junglewood    : "jungle logs",
    oakwood       : "oak logs",
    borealwood    : "boreal logs",
    pinewood      : "pine logs",
    cactuswood    : "cactus",
    palmwood      : "palm logs",

    # mineral blocks
    cosmonium : "block of cosmonium",
    adamantite: "block of adamantite",
    unobtanium: "unobtanium block",
    diamond   : "diamond block",
    platinum  : "platinum block",
    gold      : "gold block",
    iron      : "iron block",
    copper    : "copper block",

    glass          : "block of glass",
    glasswindow    : "glass window",

    torch          : "torch",
    bed            : "bed",

}

ITEM_TABLE = {
    slot : pygame.image.load("Resources/Default/InventorySpace.png")
}

ITEM_ATTR = {
    bed:{ID:45,
        WEIGHT:30,
        LUMINOSITY:0,
        DAMAGE:10,
        HEALTH:30,
        INFLAMMABLE:3,
        LTIMPERMEABILITY:0},
    bucket:{ID:46,
            WEIGHT:15,
            LUMINOSITY:0,
            DAMAGE:10,
            HEALTH:None,
            INFLAMMABLE:None,
            LTIMPERMEABILITY:0},
    bow:{ID:47,
        WEIGHT:10,
        LUMINOSITY:0,
        DAMAGE:10,
        HEALTH:None,
        INFLAMMABLE:None,
        LTIMPERMEABILITY:0},
    arrow:{ID:48,
            WEIGHT:5,
            LUMINOSITY:0,
            DAMAGE:10,
            HEALTH:None,
            INFLAMMABLE:None,
            LTIMPERMEABILITY:0},
    wood_pickaxe:{ID:53,
                WEIGHT:15,
                LUMINOSITY:0,
                DAMAGE:15,
                HEALTH:None,
                INFLAMMABLE:None,
                LTIMPERMEABILITY:0},
    stone_pickaxe:{ID:54,
                   WEIGHT:17,
                   LUMINOSITY:0,
                   DAMAGE:20,
                   HEALTH:None,
                   INFLAMMABLE:None,
                   LTIMPERMEABILITY:0},
    copper_pickaxe:{ID:55,
                    WEIGHT:19,
                    LUMINOSITY:0,
                    DAMAGE:25,
                    HEALTH:None,
                    INFLAMMABLE:None,
                    LTIMPERMEABILITY:0},
    iron_pickaxe:{ID:56,
                  WEIGHT:21,
                  LUMINOSITY:0,
                  DAMAGE:35,
                  HEALTH:None,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
    gold_pickaxe:{ID:57,
                  WEIGHT:23,
                  LUMINOSITY:0,
                  DAMAGE:30,
                  HEALTH:None,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
    dia_pickaxe:{ID:58,
                 WEIGHT:27,
                 LUMINOSITY:0,
                 DAMAGE:45,
                 HEALTH:None,
                 INFLAMMABLE:None,
                 LTIMPERMEABILITY:0},
    plat_pickaxe:{ID:59,
                  WEIGHT:25,
                  LUMINOSITY:0,
                  DAMAGE:40,
                  HEALTH:None,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
    unob_pickaxe:{ID:60,
                  WEIGHT:29,
                  LUMINOSITY:0,
                  DAMAGE:50,
                  HEALTH:None,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
    cosmo_pickaxe:{ID:62,
                   WEIGHT:31,
                   LUMINOSITY:0,
                   DAMAGE:55,
                   HEALTH:None,
                   INFLAMMABLE:None,
                   LTIMPERMEABILITY:0},
    hell_pickaxe:{ID:61,
                  WEIGHT:33,
                  LUMINOSITY:0,
                  DAMAGE:60,
                  HEALTH:None,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
    wood_axe:{ID:63,
              WEIGHT:15,
              LUMINOSITY:0,
              DAMAGE:25,
              HEALTH:None,
              INFLAMMABLE:None,
              LTIMPERMEABILITY:0},
    stone_axe:{ID:64,
               WEIGHT:20,
               LUMINOSITY:0,
               DAMAGE:30,
               HEALTH:None,
               INFLAMMABLE:None,
               LTIMPERMEABILITY:0},
    copper_axe:{ID:65,
                WEIGHT:25,
                LUMINOSITY:0,
                DAMAGE:35,
                HEALTH:None,
                INFLAMMABLE:None,
                LTIMPERMEABILITY:0},
    iron_axe:{ID:66,
              WEIGHT:30,
              LUMINOSITY:0,
              DAMAGE:45,
              HEALTH:None,
              INFLAMMABLE:None,
              LTIMPERMEABILITY:0},
    gold_axe:{ID:67,
              WEIGHT:30,
              LUMINOSITY:0,
              DAMAGE:40,
              HEALTH:None,
              INFLAMMABLE:None,
              LTIMPERMEABILITY:0},
    dia_axe:{ID:68,
             WEIGHT:35,
             LUMINOSITY:0,
             DAMAGE:50,
             HEALTH:None,
             INFLAMMABLE:None,
             LTIMPERMEABILITY:0},
    plat_axe:{ID:69,
              WEIGHT:30,
              LUMINOSITY:0,
              DAMAGE:45,
              HEALTH:None,
              INFLAMMABLE:None,
              LTIMPERMEABILITY:0},
    unob_axe:{ID:70,
              WEIGHT:35,
              LUMINOSITY:0,
              DAMAGE:55,
              HEALTH:None,
              INFLAMMABLE:None,
              LTIMPERMEABILITY:0},
    cosmo_axe:{ID:72,
               WEIGHT:40,
               LUMINOSITY:0,
               DAMAGE:55,
               HEALTH:None,
               INFLAMMABLE:None,
               LTIMPERMEABILITY:0},
    hell_axe:{ID:71,
              WEIGHT:45,
              LUMINOSITY:0,
              DAMAGE:60,
              HEALTH:None,
              INFLAMMABLE:None,
              LTIMPERMEABILITY:0},
    wood_battleaxe:{ID:73,
                    WEIGHT:15,
                    LUMINOSITY:0,
                    DAMAGE:30,
                    HEALTH:None,
                    INFLAMMABLE:None,
                    LTIMPERMEABILITY:0},
    stone_battleaxe:{ID:74,
                     WEIGHT:20,
                     LUMINOSITY:0,
                     DAMAGE:35,
                     HEALTH:None,
                     INFLAMMABLE:None,
                     LTIMPERMEABILITY:0},
    copper_battleaxe:{ID:75,
                      WEIGHT:25,
                      LUMINOSITY:0,
                      DAMAGE:40,
                      HEALTH:None,
                      INFLAMMABLE:None,
                      LTIMPERMEABILITY:0},
    iron_battleaxe:{ID:76,
                    WEIGHT:30,
                    LUMINOSITY:0,
                    DAMAGE:50,
                    HEALTH:None,
                    INFLAMMABLE:None,
                    LTIMPERMEABILITY:0},
    gold_battleaxe:{ID:77,
                    WEIGHT:30,
                    LUMINOSITY:0,
                    DAMAGE:45,
                    HEALTH:None,
                    INFLAMMABLE:None,
                    LTIMPERMEABILITY:0},
    dia_battleaxe:{ID:78,
                   WEIGHT:35,
                   LUMINOSITY:0,
                   DAMAGE:60,
                   HEALTH:None,
                   INFLAMMABLE:None,
                   LTIMPERMEABILITY:0},
    plat_battleaxe:{ID:79,
                    WEIGHT:30,
                    LUMINOSITY:0,
                    DAMAGE:55,
                    HEALTH:None,
                    INFLAMMABLE:None,
                    LTIMPERMEABILITY:0},
    unob_battleaxe:{ID:80,
                    WEIGHT:35,
                    LUMINOSITY:0,
                    DAMAGE:60,
                    HEALTH:None,
                    INFLAMMABLE:None,
                    LTIMPERMEABILITY:0},
    cosmo_battleaxe:{ID:82,
                     WEIGHT:35,
                     LUMINOSITY:0,
                     DAMAGE:60,
                     HEALTH:None,
                     INFLAMMABLE:None,
                     LTIMPERMEABILITY:0},
    hell_battleaxe:{ID:81,
                    WEIGHT:40,
                    LUMINOSITY:0,
                    DAMAGE:65,
                    HEALTH:None,
                    INFLAMMABLE:None,
                    LTIMPERMEABILITY:0},
    wood_sword:{ID:83,
                WEIGHT:15,
                LUMINOSITY:0,
                DAMAGE:30,
                HEALTH:None,
                INFLAMMABLE:None,
                LTIMPERMEABILITY:0},
    stone_sword:{ID:84,
                 WEIGHT:20,
                 LUMINOSITY:0,
                 DAMAGE:35,
                 HEALTH:None,
                 INFLAMMABLE:None,
                 LTIMPERMEABILITY:0},
    copper_sword:{ID:85,
                  WEIGHT:25,
                  LUMINOSITY:0,
                  DAMAGE:40,
                  HEALTH:None,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
    iron_sword:{ID:86,
                WEIGHT:30,
                LUMINOSITY:0,
                DAMAGE:50,
                HEALTH:None,
                INFLAMMABLE:None,
                LTIMPERMEABILITY:0},
    gold_sword:{ID:87,
                WEIGHT:30,
                LUMINOSITY:0,
                DAMAGE:45,
                HEALTH:None,
                INFLAMMABLE:None,
                LTIMPERMEABILITY:0},
    dia_sword:{ID:88,
               WEIGHT:35,
               LUMINOSITY:0,
               DAMAGE:60,
               HEALTH:None,
               INFLAMMABLE:None,
               LTIMPERMEABILITY:0},
    plat_sword:{ID:89,
                WEIGHT:30,
                LUMINOSITY:0,
                DAMAGE:55,
                HEALTH:None,
                INFLAMMABLE:None,
                LTIMPERMEABILITY:0},
    unob_sword:{ID:90,
                WEIGHT:35,
                LUMINOSITY:0,
                DAMAGE:60,
                HEALTH:None,
                INFLAMMABLE:None,
                LTIMPERMEABILITY:0},
    cosmo_sword:{ID:92,
                 WEIGHT:35,
                 LUMINOSITY:0,
                 DAMAGE:40,
                 HEALTH:None,
                 INFLAMMABLE:None,
                 LTIMPERMEABILITY:0},
    hell_sword:{ID:91,
                WEIGHT:40,
                LUMINOSITY:0,
                DAMAGE:65,
                HEALTH:None,
                INFLAMMABLE:None,
                LTIMPERMEABILITY:0},
    lighter:{ID:93,
             WEIGHT:5,
             LUMINOSITY:0,
             DAMAGE:10,
             HEALTH:None,
             INFLAMMABLE:None,
             LTIMPERMEABILITY:0},
    deerskin:{ID:48,
              WEIGHT:5,
              LUMINOSITY:0,
              DAMAGE:10,
              HEALTH:None,
              INFLAMMABLE:None,
              LTIMPERMEABILITY:0},
    rottenleather:{ID:49,
                   WEIGHT:5,
                   LUMINOSITY:0,
                   DAMAGE:10,
                   HEALTH:None,
                   INFLAMMABLE:None,
                   LTIMPERMEABILITY:0},
    chicken:{ID:50,
             WEIGHT:5,
             LUMINOSITY:0,
             DAMAGE:10,
             HEALTH:None,
             INFLAMMABLE:None,
             LTIMPERMEABILITY:0},
    deermeat:{ID:51,
              WEIGHT:5,
              LUMINOSITY:0,
              DAMAGE:10,
              HEALTH:None,
              INFLAMMABLE:None,
              LTIMPERMEABILITY:0},
    rottenmeat:{ID:52,
                WEIGHT:5,
                LUMINOSITY:0,
                DAMAGE:10,
                HEALTH:None,
                INFLAMMABLE:None,
                LTIMPERMEABILITY:0},
    berry:{ID:1,
           WEIGHT:2,
           LUMINOSITY:0,
           DAMAGE:10,
           HEALTH:None,
           INFLAMMABLE:None,
           LTIMPERMEABILITY:0},
    apple:{ID:2,
           WEIGHT:2,
           LUMINOSITY:0,
           DAMAGE:10,
           HEALTH:None,
           INFLAMMABLE:None,
           LTIMPERMEABILITY:0}
}

def loadImageTable():
    for key in ITEM_TABLE:
        ITEM_TABLE[key] = ITEM_TABLE[key].convert_alpha()