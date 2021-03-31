from constants import *

class tiles( enum.Enum ):
    air = 0

class items( enum.Enum ):
    pass

# liquids will be modifiers which will be
# used as overlays on top of existing blocks
# an empty slot can have a certain liquid level but no more