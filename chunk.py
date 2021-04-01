import tiles
import items

class Chunk:

    def __init__( _blocks = None , _walls = None , _local_tile_table = None , _index = None , _created = None , _active_time = None ):

        self.blocks             = _blocks
        self.walls              = _walls
        self.local_tile_table   = _local_tile_table
        self.index              = _index

        self.created            = _time
        self.active_time        = _active_time

        self.surf               = pygame.surface( ( CHUNK_WIDTH_P , CHUNK_HEIGHT_P ) )

        if not self.blocks:
            self.blocks = [[ 0 for j in range(CHUNK_WIDTH)] for i in range(CHUNK_HEIGHT)]
        if not self.walls:
            self.walls = [[ 0 for j in range(CHUNK_WIDTH)] for i in range(CHUNK_HEIGHT)]
        if not self.local_tile_table:
            self.local_tile_table = {}

    def draw( self , _rect = [ 0 , 0 , CHUNK_WIDTH , CHUNK_HEIGHT ] ): pass
        # First we blit the transparent color of air
        # Then we blit the tiles/walls
        # Then we blit the tile modifiers (cracks, glows, etc.)
        # Then we blit the liquids / fire


    def break_block_at( _x , _y , _item , _dt ): pass
        # Left click was done at the coordinates x, y for dt time using item tool at the block level
        # the behaviour of tool is acted using its corresponding function which we can get from a dictionary

    def break_wall_at( _x , _y , _item , _dt ): pass
        # Left click was done at the coordinates x, y for dt time using item tool at the wall level
        # the behaviour of tool is acted using its corresponding function which we can get from a dictionary

    def place_block_at( _x , _y , _item , _dt ): pass
        # Right click was done at the coordinates x, y for dt time using item item at the block level
        # the behaviour of item is acted using its corresponding function which we can get from a dictionary

    def place_wall_at( _x , _y , _item , _dt ): pass
        # Right click was done at the coordinates x, y for dt time using item item at the wall level
        # the behaviour of item is acted using its corresponding function which we can get from a dictionary

    def update( _dt ): pass
        # First we update the state of all the blocks using their respective function calls (growing trees, flowers, decaying blocks etc)
        # Fire spread
        # Liquid movement

class ChunkBuffer:
    def __init__(): pass
    def draw(): pass
    def shift(_delta): pass
    def save(): pass
    def load(): pass