from game_utilities import *

class Chunk:

    def __init__( self , _blocks = None , _walls = None , _local_tile_table = None , _index = None , _created = None , _active_time = None ):

        self.blocks             = _blocks
        self.walls              = _walls
        self.local_tile_table   = _local_tile_table
        self.index              = _index

        self.created            = _time
        self.active_time        = _active_time

        self.surf               = pygame.surface( ( CHUNK_WIDTH_P , CHUNK_HEIGHT_P ) , flags = pygame.SRCALPHA )

        if not self.blocks:
            self.blocks = [[ 0 for j in range(CHUNK_WIDTH)] for i in range(CHUNK_HEIGHT)]
        if not self.walls:
            self.walls = [[ 0 for j in range(CHUNK_WIDTH)] for i in range(CHUNK_HEIGHT)]
        if not self.local_tile_table:
            self.local_tile_table = {}

    def draw( self , _rect = [ 0 , 0 , CHUNK_WIDTH , CHUNK_HEIGHT ] ):

        x_start = TILE_WIDTH * ( _rect[0] )
        y_start = TILE_WIDTH * ( CHUNK_HEIGHT - _rect[3] )

        x_span  = TILE_WIDTH * ( _rect[2] - _rect[0] )
        y_span  = TILE_WIDTH * ( _rect[3] - _rect[1] )

        # make the region transparent
        self.surface.fill( ( 0 , 0 , 0 , 0 ), [ x_start , y_start , x_span, y_span])

        # loop for blitting the tiles and walls
        for i in range( _rect[1] , _rect[3] ):

            coors = [ 0 , TILE_WIDTH * ( CHUNK_HEIGHT - i - 1 ) ]

            for j in range( _rect[0] , _rect[2] ):

                coors[0]            = TILE_WIDTH * j
                tile_ref , wall_ref = self.blocks[i][j] , self.walls[i][j]

                if tile_ref > 0 :

                    self.surface.blit( TILE_TABLE[tile_ref] , coors )
                    if ( i , j , 1 ) in self.local_tile_table : pass

                elif wall_ref > 0 :

                    self.surface.blit( TILE_TABLE[wall_ref] , coors )
                    if ( i , j , 0 ) in self.local_tile_table : pass

        # Then we blit the tile modifiers (cracks, glows, etc.)
        # Then we blit the liquids / fire


    def break_block_at( self , _x , _y , _item , _dt ): pass
        # Left click was done at the coordinates x, y for dt time using item tool at the block level
        # the behaviour of tool is acted using its corresponding function which we can get from a dictionary

    def break_wall_at( self , _x , _y , _item , _dt ): pass
        # Left click was done at the coordinates x, y for dt time using item tool at the wall level
        # the behaviour of tool is acted using its corresponding function which we can get from a dictionary

    def place_block_at( self , _x , _y , _item , _dt ): pass
        # Right click was done at the coordinates x, y for dt time using item item at the block level
        # the behaviour of item is acted using its corresponding function which we can get from a dictionary

    def place_wall_at( self , _x , _y , _item , _dt ): pass
        # Right click was done at the coordinates x, y for dt time using item item at the wall level
        # the behaviour of item is acted using its corresponding function which we can get from a dictionary

    def update( self , _dt ): pass
        # First we update the state of all the blocks using their respective function calls (growing trees, flowers, decaying blocks etc)
        # Fire spread
        # Liquid movement

class ChunkBuffer:

    def __init__( self , _len , _middle = 0 ):

        # size and positions of chunks in the world
        self.len            = _len
        self.positions      = [None] * _len

        # chunk and light surface data
        self.chunks         = [None] * _len
        self.light_surfs    = [None] * _len

        # References to the other managers (These must be provided in the main)
        self.entity_buffer  = None
        self.renderer       = None
        self.serializer     = None
        self.player         = None

    def draw( self ):

        for chunk in self.chunks: chunk.draw()

    def shift( self , _delta ): pass
    def save( self ): pass
    def load( self ): pass