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

    def draw(): pass
    def break_block_at(_x, _y, _tool, _dt): pass
    def break_wall_at(_x, _y, _tool, _dt): pass
    def place_block_at(_x, _y, _item): pass
    def place_wall_at(_x, _y, _item): pass
    def update(_dt): pass

class ChunkBuffer:
    def __init__(): pass
    def draw(): pass
    def shift(_delta): pass
    def save(): pass
    def load(): pass