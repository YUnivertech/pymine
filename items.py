from constants import *

# inventory
slot             = 0

ITEM_TABLE = {
    slot : pygame.image.load("Resources/Default/InventorySpace.png")
}

def loadImageTable():
    for key in ITEM_TABLE:
        ITEM_TABLE[key] = ITEM_TABLE[key].convert_alpha()
