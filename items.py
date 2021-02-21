from constants import *

# Item names along with their IDs

# inventory
slot             = 0

# foods
berry            = 1
apple            = 2

# woods
junglewood       = 3
oakwood          = 4
borealwood       = 5
pinewood         = 6
cactuswood       = 7
palmwood         = 8

# bow and arrow
bow              = 46
arrow            = 47

# pickaxes
wood_pickaxe     = 53
stone_pickaxe    = 54
copper_pickaxe   = 55
iron_pickaxe     = 56
gold_pickaxe     = 57
dia_pickaxe      = 58
plat_pickaxe     = 59
unob_pickaxe     = 60
hell_pickaxe     = 61
cosmo_pickaxe    = 62

# axes
wood_axe         = 63
stone_axe        = 64
copper_axe       = 65
iron_axe         = 66
gold_axe         = 67
dia_axe          = 68
plat_axe         = 69
unob_axe         = 70
hell_axe         = 71
cosmo_axe        = 72

# battle axes
wood_battleaxe   = 73
stone_battleaxe  = 74
copper_battleaxe = 75
iron_battleaxe   = 76
gold_battleaxe   = 77
dia_battleaxe    = 78
plat_battleaxe   = 79
unob_battleaxe   = 80
hell_battleaxe   = 81
cosmo_battleaxe  = 82

# swords
wood_sword       = 83
stone_sword      = 84
copper_sword     = 85
iron_sword       = 86
gold_sword       = 87
dia_sword        = 88
plat_sword       = 89
unob_sword       = 90
hell_sword       = 91
cosmo_sword      = 92

# lighter
lighter          = 93

# animal hides
deerskin         = 48
rottenleather    = 49

# meats
chicken          = 50
deermeat         = 51
rottenmeat       = 52

# door
door             = 43

# bed and bucket
bed              = 45
bucket           = 46

# items for blocks from the bedrock wastes
bedrock          = 1
obsidian         = 2
hellstone        = 3

# items for ores (not the same as the items for the block)
unobtaniumOre    = 4
diamondOre       = 5
platinumOre      = 6
goldOre          = 7
ironOre          = 8
copperOre        = 9

# items for the stones
granite          = 10
quartz           = 11
limestone        = 12
greystone        = 13
sandstone        = 14

# items for transition blocks
gravel           = 15
coke             = 16

# items for the clay blocks
clay             = 17
redClay          = 18

# item for the sand block
sand             = 19

# items for dirt and grass blocks
browndirt        = 20
grass            = 21
snowygrass       = 22

# items for snowy blocks
snow             = 23
ice              = 24

# items for all the wood blocks
junglewood       = 25
oakwood          = 26
borealwood       = 27
pinewood         = 28
cactuswood       = 29
palmwood         = 30

# items for the mineral blocks
cosmonium        = 31
adamantite       = 32
unobtanium       = 33
diamond          = 34
platinum         = 35
gold             = 36
iron             = 37
copper           = 38

# items for the mineral ingots/ pieces
cosmonium        = 31
adamantite       = 32
unobtanium       = 33
diamond          = 34
platinum         = 35
gold             = 36
iron             = 37
copper           = 38

# items for the glass blocks
glass            = 39
glasswindow      = 40

torch            = 41

ITEM_TABLE = {
    slot : pygame.image.load("Resources/Default/InventorySpace.png")
}

def loadImageTable():
    for key in ITEM_TABLE:
        ITEM_TABLE[key] = ITEM_TABLE[key].convert_alpha()
