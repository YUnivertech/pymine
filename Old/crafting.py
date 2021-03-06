from Old import tempitems as i

PLYR_CRAFT = {
    ((i.junglewood, 1),)       : ((i.junglewood_plank, 4),),
    ((i.borealwood, 1),)       : ((i.borealwood_plank, 4),),
    ((i.oakwood, 1),)          : ((i.oakwood_plank, 4),),
    ((i.cactuswood, 1),)       : ((i.cactuswood_plank, 4),),
    ((i.pinewood, 1),)         : ((i.pinewood_plank, 4),),
    ((i.palmwood, 1),)         : ((i.palmwood_plank, 4),),
    ((i.junglewood_plank, 4),) : ((i.crafting_table, 1),),
    ((i.borealwood_plank, 4),) : ((i.crafting_table, 1),),
    ((i.oakwood_plank, 4),)    : ((i.crafting_table, 1),),
    ((i.cactuswood_plank, 4),) : ((i.crafting_table, 1),),
    ((i.pinewood_plank, 4),)   : ((i.crafting_table, 1),),
    ((i.palmwood_plank, 4),)   : ((i.crafting_table, 1),),
}
TABLE_CRAFT = {
    ((i.stick, 1), (i.junglewood_plank, 2)) : ((i.wood_sword, 1),),
    ((i.stick, 1), (i.borealwood_plank, 2)) : ((i.wood_sword, 1),),
    ((i.stick, 1), (i.oakwood_plank, 2))    : ((i.wood_sword, 1),),
    ((i.stick, 1), (i.cactuswood_plank, 2)) : ((i.wood_sword, 1),),
    ((i.stick, 1), (i.pinewood_plank, 2))   : ((i.wood_sword, 1),),
    ((i.stick, 1), (i.palmwood_plank, 2))   : ((i.wood_sword, 1),),
    ((i.stick, 1), (i.greystone, 2))        : ((i.stone_sword, 1),),
    ((i.stick, 1), (i.iron_ingot, 2))       : ((i.iron_sword, 1),),
    ((i.stick, 1), (i.copper_ingot, 2))     : ((i.copper_sword, 1),),
    ((i.stick, 1), (i.gold_brick, 2))       : ((i.gold_sword, 1),),
    ((i.stick, 1), (i.diamond_gem, 2))      : ((i.diamond_sword, 1),),
    ((i.stick, 1), (i.platinum_ingot, 2))   : ((i.platinum_sword, 1),),
    ((i.stick, 1), (i.unobtanium_ingot, 2)) : ((i.unobtanium_sword, 1),),
    ((i.stick, 1), (i.hellstone, 2))        : ((i.hellstone_sword, 1),),
    ((i.stick, 1), (i.adamantite, 2))       : ((i.adamantite_sword, 1),)
}
FURNACE = {}

def get_craftable():
    pass
