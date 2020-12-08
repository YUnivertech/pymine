from constants import *

# Tile names along with their IDs

crack           =  0

# air
air             =  0

# blocks in the bedrock wastes
bedrock         =  1
obsidian        =  2
hellstone       =  3

# blocks for mineral ores
unobtaniumOre   =  4
diamondOre      =  5
platinumOre     =  6
goldOre         =  7
ironOre         =  8
copperOre       =  9

# blocks for stones
granite         =  10
quartz          =  11
limestone       =  12
greystone       =  13
sandstone       =  14

# blocks for transition blocks
gravel          =  15
coke            =  16

# blocks for clays
clay            =  17
redClay         =  18

# block for sand
sand            =  19

# blocks for dirt and grass
browndirt       =  20
grass           =  21
snowygrass      =  22

# blocks for snow
snow            =  23
ice             =  24

# tree related
# blocks for different woods
jungleWood     =  25
oakWood        =  26
borealWood     =  27
pineWood       =  28
cactusWood     =  29
palmWood       =  30

# leaves for different trees
jungleLeaves     =  25
oakLeaves        =  26
borealLeaves     =  27
pineLeaves       =  28
cactusLeaves     =  29
palmLeaves       =  30

# blocks for different woods
junglePlank     =  25
oakPlank        =  26
borealPlank     =  27
pinePlank       =  28
cactusPlank     =  29
palmPlank       =  30

# saplings for different trees
jungleSapling     =  25
oakSapling        =  26
borealSapling     =  27
pineSapling       =  28
cactusSapling     =  29
palmSapling       =  30

# mineral blocks
cosmonium  =  31
adamantite =  32
unobtanium =  33
diamond    =  34
platinum   =  35
gold       =  36
iron       =  37
copper     =  38

# blocks for glass
glass           =  39
glasswindow     =  40

# torch
torch           =  41
boreal_torch           =  41
nether_torch           =  41

# bed and door
bed             =  42
door_upper      =  42
door_lower      =  42

# Tile table with names
TILE_NAMES = {
      # air
      air            : "air",

      # bedrock wastes blocks
      bedrock        : "bedrock",
      obsidian       : " obsidian",
      hellstone      : " hellstone",

      # ores
      unobtaniumOre   : "unrefined unobtanium",
      diamondOre      : "diamond ore",
      platinumOre     : "platinum ore",
      goldOre         : "gold ore",
      ironOre         : "iron ore",
      copperOre       : "copper ore",


      # stones
      granite        : "granite",
      quartz         : "quartz",
      limestone      : "limestone",
      greystone      : "stone",
      sandstone      : "sandstone",

      # transition blocks
      gravel         : "gravel",
      coke           : "coke",

      # clays
      clay           : "clay",
      redClay        : "red clay",

      # sand
      sand           : "sand",

      # dirt, grass
      browndirt      : "dirt",
      grass          : "grass",

      # Snowy blocks
      snowygrass     : "snowy grass",
      snow           : "snow",
      ice            : "ice",

      # woods
      jungleWood    : "jungle logs",
      oakWood       : "oak logs",
      borealWood    : "boreal logs",
      pineWood      : "pine logs",
      cactusWood    : "cactus",
      palmWood      : "palm logs",

      # mineral blocks
      cosmonium : "cosmonium",
      adamantite: "adamantite",
      unobtanium: "unobtanium",
      diamond   : "diamond",
      platinum  : "platinum",
      gold      : "gold",
      iron      : "iron",
      copper    : "copper",

      glass          : " glass",
      glasswindow    : "glass window",

      torch          : "torch",
      bed            : "bed",

}

TILE_MODIFIERS = {
      crack :     [pygame.image.load("Resources/Default/break{}.png".format(i)) for i in range(0, 9)]
      #fire :     [pygame.image.load("Resources/Default/break{}.png".format(i)) for i in range(0, 9)]
      #water :     [pygame.image.load("Resources/Default/break{}.png".format(i)) for i in range(0, 9)]
      #lava :     [pygame.image.load("Resources/Default/break{}.png".format(i)) for i in range(0, 9)]
}

TILE_TABLE = {

      bedrock         :   pygame.image.load("Resources/Default/bedrock2.png"),
      obsidian        :   pygame.image.load("Resources/Default/obsidian.png"),
      hellstone       :   pygame.image.load("Resources/Default/hellstone.png"),

      unobtaniumOre   :   pygame.image.load("Resources/Default/unobtaniumOre.png"),
      diamondOre      :   pygame.image.load("Resources/Default/diamondOre.png"),
      platinumOre     :   pygame.image.load("Resources/Default/ironOre.png"),
      goldOre         :   pygame.image.load("Resources/Default/goldOre.png"),
      ironOre         :   pygame.image.load("Resources/Default/ironOre.png"),
      copperOre       :   pygame.image.load("Resources/Default/copperOre.png"),

      granite         :   pygame.image.load("Resources/Default/granite.png"),
      quartz          :   pygame.image.load("Resources/Default/quartz.png"),
      limestone       :   pygame.image.load("Resources/Default/limestone.png"),
      greystone       :   pygame.image.load("Resources/Default/greystone.png"),
      sandstone       :   pygame.image.load("Resources/Default/sandstone.png"),

      gravel          :   pygame.image.load("Resources/Default/gravel.png"),
      coke            :   pygame.image.load("Resources/Default/coalOre.png"),

      clay            :   pygame.image.load("Resources/Default/clay.png"),
      redClay         :   pygame.image.load("Resources/Default/redClay.png"),
      browndirt       :   pygame.image.load("Resources/Default/browndirt.png"),
}

TILE_ATTR = {
      air:{LUMINOSITY:255},
      bedrock:{ID:1,
                  WEIGHT:100,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:None,
                  HEALTH:INF,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      obsidian:{ID:2,
                  WEIGHT:99,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:100,
                  INFLAMMABLE:0,
                  LTIMPERMEABILITY:0},
      hellstone:{ID:3,
                  WEIGHT:99,
                  FRICTION:0.8,
                  LUMINOSITY:255,
                  DAMAGE:10,
                  HEALTH:100,
                  INFLAMMABLE:0,
                  LTIMPERMEABILITY:0},
      unobtaniumOre:{ID:4,
                        WEIGHT:85,
                        FRICTION:0.8,
                        LUMINOSITY:160,
                        DAMAGE:10,
                        HEALTH:90,
                        INFLAMMABLE:None,
                        LTIMPERMEABILITY:0},
      diamondOre:{ID:5,
                  WEIGHT:80,
                  FRICTION:0.8,
                  LUMINOSITY:175,
                  DAMAGE:10,
                  HEALTH:90,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      platinumOre:{ID:6,
                  WEIGHT:75,
                  FRICTION:0.8,
                  LUMINOSITY:160,
                  DAMAGE:10,
                  HEALTH:80,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      goldOre:{ID:7,
                  WEIGHT:70,
                  FRICTION:0.8,
                  LUMINOSITY:160,
                  DAMAGE:10,
                  HEALTH:70,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      ironOre:{ID:8,
                  WEIGHT:65,
                  FRICTION:0.8,
                  LUMINOSITY:160,
                  DAMAGE:10,
                  HEALTH:70,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      granite:{ID:9,
                  WEIGHT:60,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:55,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      quartz:{ID:10,
                  WEIGHT:60,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:55,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      limestone:{ID:11,
                  WEIGHT:55,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:55,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      copperOre:{ID:12,
                  WEIGHT:65,
                  FRICTION:0.8,
                  LUMINOSITY:160,
                  DAMAGE:10,
                  HEALTH:60,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      greystone:{ID:13,
                  WEIGHT:55,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:55,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      sandstone:{ID:14,
                  WEIGHT:50,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:50,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      gravel:{ID:15,
                  WEIGHT:45,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:50,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      coke:{ID:16,
            WEIGHT:40,
            FRICTION:0.8,
            LUMINOSITY:160,
            DAMAGE:10,
            HEALTH:50,
            INFLAMMABLE:None,
            LTIMPERMEABILITY:0},
      clay:{ID:17,
            WEIGHT:35,
            FRICTION:0.9,
            LUMINOSITY:0,
            DAMAGE:10,
            HEALTH:45,
            INFLAMMABLE:None,
            LTIMPERMEABILITY:0},
      redClay:{ID:18,
                  WEIGHT:35,
                  FRICTION:0.9,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:45,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      sand:{ID:19,
            WEIGHT:20,
            FRICTION:0.85,
            LUMINOSITY:0,
            DAMAGE:10,
            HEALTH:15,
            INFLAMMABLE:None,
            LTIMPERMEABILITY:0},
      browndirt:{ID:20,
                  WEIGHT:25,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:30,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      grass:{ID:21,
            WEIGHT:25,
            FRICTION:0.8,
            LUMINOSITY:0,
            DAMAGE:10,
            HEALTH:30,
            INFLAMMABLE:3,
            LTIMPERMEABILITY:0},
      snowygrass:{ID:22,
                  WEIGHT:30,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:30,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      snow:{ID:23,
            WEIGHT:30,
            FRICTION:0.85,
            LUMINOSITY:0,
            DAMAGE:10,
            HEALTH:15,
            INFLAMMABLE:None,
            LTIMPERMEABILITY:0},
      ice:{ID:24,
            WEIGHT:25,
            FRICTION:0.4,
            LUMINOSITY:0,
            DAMAGE:10,
            HEALTH:30,
            INFLAMMABLE:None,
            LTIMPERMEABILITY:150},
      glass:{ID:25,
            WEIGHT:30,
            FRICTION:0.5,
            LUMINOSITY:0,
            DAMAGE:10,
            HEALTH:30,
            INFLAMMABLE:None,
            LTIMPERMEABILITY:200},
      jungleWood:{ID:26,
                  WEIGHT:35,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:35,
                  INFLAMMABLE:4,
                  LTIMPERMEABILITY:0},
      oakWood:{ID:27,
                  WEIGHT:35,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:35,
                  INFLAMMABLE:4,
                  LTIMPERMEABILITY:0},
      borealWood:{ID:28,
                  WEIGHT:35,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:35,
                  INFLAMMABLE:4,
                  LTIMPERMEABILITY:0},
      pineWood:{ID:29,
                  WEIGHT:35,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:35,
                  INFLAMMABLE:4,
                  LTIMPERMEABILITY:0},
      cactusWood:{ID:30,
                  WEIGHT:35,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:35,
                  INFLAMMABLE:4,
                  LTIMPERMEABILITY:0},
      palmWood:{ID:31,
                  WEIGHT:35,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:35,
                  INFLAMMABLE:4,
                  LTIMPERMEABILITY:0},
      cosmonium:{ID:32,
                  WEIGHT:90,
                  FRICTION:0.8,
                  LUMINOSITY:150,
                  DAMAGE:10,
                  HEALTH:85,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      adamantite:{ID:33,
                  WEIGHT:90,
                  FRICTION:0.8,
                  LUMINOSITY:0,
                  DAMAGE:85,
                  HEALTH:85,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      unobtanium:{ID:34,
                  WEIGHT:85,
                  FRICTION:0.6,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:80,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      diamond:{ID:35,
                  WEIGHT:80,
                  FRICTION:0.6,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:80,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:150},
      platinum:{ID:36,
                  WEIGHT:75,
                  FRICTION:0.6,
                  LUMINOSITY:0,
                  DAMAGE:10,
                  HEALTH:70,
                  INFLAMMABLE:None,
                  LTIMPERMEABILITY:0},
      gold:{ID:37,
            WEIGHT:70,
            FRICTION:0.6,
            LUMINOSITY:0,
            DAMAGE:10,
            HEALTH:65,
            INFLAMMABLE:None,
            LTIMPERMEABILITY:0},
      iron:{ID:38,
            WEIGHT:70,
            FRICTION:0.6,
            LUMINOSITY:0,
            DAMAGE:10,
            HEALTH:65,
            INFLAMMABLE:None,
            LTIMPERMEABILITY:0},
      copper:{ID:39,
            WEIGHT:65,
            FRICTION:0.6,
            LUMINOSITY:0,
            DAMAGE:10,
            HEALTH:60,
            INFLAMMABLE:None,
            LTIMPERMEABILITY:0},
      torch:{ID:42,
            WEIGHT:20,
            FRICTION:None,
            LUMINOSITY:200,
            DAMAGE:10,
            HEALTH:15,
            INFLAMMABLE:None,
            LTIMPERMEABILITY:0},
      bed:{ID:44,
            WEIGHT:30,
            FRICTION:0.4,
            LUMINOSITY:0,
            DAMAGE:10,
            HEALTH:30,
            INFLAMMABLE:3,
            LTIMPERMEABILITY:0},
}


def loadImageTable():
      for key in TILE_TABLE:
            TILE_TABLE[key] = pygame.transform.smoothscale(TILE_TABLE[key], (TILE_WIDTH, TILE_WIDTH))
            TILE_TABLE[key] = TILE_TABLE[key].convert_alpha()
      for key in TILE_MODIFIERS:
            for i in range(0, len(TILE_MODIFIERS[key])):
                  TILE_MODIFIERS[key][i] = pygame.transform.smoothscale( TILE_MODIFIERS[key][i], ( TILE_WIDTH, TILE_WIDTH ) )
                  TILE_MODIFIERS[key][i] = TILE_MODIFIERS[key][i].convert_alpha()

