from game_utilities import *

# class Shader:

#     def __init__( self, parent ):

#         self.parent = parent

#     def shadeRetro( self, index, top=True, down=True, left=True, right=True ):

#         for c in range( 0, parent.length ):
#             for i in range( 0, CHUNK_HEIGHT ):
#                 for j in range( 0, CHUNK_WIDTH ):

#                     currTileRef = parent[index][i][j]
#                     currWallRef = parent[index].walls[i][j]

#                     selfLuminousity  = 0

#                     # if(currTileRef > 0 or currWallRef == 0):    # Front tile is present or wall is absent
#                     #     selfLuminousity = TILE_ATTR[currTileRef][LUMINOSITY]
#                     # elif(currWallRef > 0):                      # Front tile is absent but wall is present
#                     #     selfLuminousity = TILE_ATTR[currWallRef][LUMINOSITY]

#                     selfLuminousity = tiles.TILE_ATTR[currTileRef][LUMINOSITY]
#                     selfIllumination = self[index].lightMap[i][j]

#                     if(selfLuminousity is not 0 and selfIllumination < selfLuminousity):
#                         parent[index].lightMap[i][j] = selfLuminousity
#                         self.propagateRetro(index, j, i)

#     def propagateRetro( self, index, x, y, top=True, right=True, bottom=True, left=True ):

#         if(index < 0): index = self.length+index

#         topVal      =  self[index].lightMap[y][x]-16
#         rightVal    =  self[index].lightMap[y][x]-16
#         bottomVal   =  self[index].lightMap[y][x]-16
#         leftVal     =  self[index].lightMap[y][x]-16

#         if(topVal < 0): top=False
#         if(rightVal < 0): right=False
#         if(bottomVal < 0): bottom=False
#         if(leftVal < 0): left=False

#         # Top side
#         if(top):
#             if(y+1 < CHUNK_HEIGHT):         #check if the next position (1 above) is valid
#                 if(topVal > self[index].lightMap[y+1][x]):
#                     self[index].lightMap[y+1][x]   =  topVal
#                     self.propogateRetro(index, x, y+1, bottom=False)

#         # Bottom side
#         if(bottom):
#             if(y-1 >= 0):                   #check if the next position (1 below) is valid
#                 if(bottomVal >= self[index].lightMap[y-1][x]):
#                     self[index].lightMap[y-1][x]   =  bottomVal
#                     self.propogateRetro(index, x, y-1, top=False)

#         # Left side
#         if(left):
#             if(x-1 >= 0):                   #check if the next position (1 to the left) is valid
#                 if(leftVal > self[index].lightMap[y][x-1]):
#                     self[index].lightMap[y][x-1]   =  leftVal
#                     self.propogateRetro(index, x-1, y, right=False)

#             elif(index-1 >= 0):             #check if previous chunk exists in the chunk buffer
#                 if(leftVal > self[index-1].lightMap[y][CHUNK_WIDTH-1]):
#                     self[index-1].lightMap[y][CHUNK_WIDTH-1]   =  leftVal
#                     self.propogateRetro(index-1, CHUNK_WIDTH-1, y, right=False)

#         # Right side
#         if(right):
#             if(x+1 < CHUNK_WIDTH):          #check if the next position (1 to the right) is valid
#                 if(rightVal > self[index].lightMap[y][x+1]):
#                     self[index].lightMap[y][x+1]   =  rightVal
#                     self.propogateRetro(index, x+1, y, left=False)

#             elif(index+1 < self.length):    #check if next chunk exists in the chunk buffer
#                 if(rightVal > self[index+1].lightMap[y][0]):
#                     self[index+1].lightMap[y][0]   =  rightVal
#                     self.propogateRetro(index+1, 0, y, left=False)

#     def shadeRadial( self ):

#         luminous = None # the luminosity of the block
#         sq2 = 1.414
#         for index in range(0, parent.length):
#             currChunkRef = self.parent[index]
#             for y in range(CHUNK_HEIGHT):
#                 for x in range(CHUNK_WIDTH):

#                     currTileRef = parent[index][y][x]
#                     currWallRef = parent[index].walls[y][x]

#                     if( currTileRef is luminous or currWallRef is luminous):

#                         propagateRadial( index, x, y, True, True, True, True)

#                         # i, j = 1, 1
#                         while( y-1-i>0 and x-1-i>0 ):   #up diagonal left
#                             propagateRadial( index, x-1-i, y-1-i, up=True, left=True)

#                         # i, j = 1, 1
#                         while( y-1-i>0 and x+1+i<CHUNK_WIDTH ): #up diagonal right
#                             propagateRadial( index, x+1+i, y-1-i, up=True, right=True)

#                         # i, j = 1, 1
#                         while( y+1+i<CHUNK_HEIGHT and x-1-i>0 ):    #down diagonal left
#                             propagateRadial( index, x-1-i, y+1+i, down=True, left=True)

#                         # i, j = 1, 1
#                         while( y+1+i<CHUNK_HEIGHT and x+1+i<CHUNK_WIDTH ):  #down diagonal right
#                             propagateRadial( index, x+1+i, y+1+i, down=True, right=True)

#     def propagateRadial( self, index, x, y, up=False, down=False, left=False, right=False ):

#         currChunkRef = self.parent[index]
#         valid = True       #check if valid

#         if valid and lightval != 0:
#             if up:
#                 currChunkRef[y+1][x].lightval = 0.5    #some value
#                 propagateRadial(y+1, x, up=True)
#             if down:
#                 currChunkRef[y-1][x].lightval = 0.5    #some value
#                 propagateRadial(y-1, x, down=True)
#             if right:
#                 currChunkRef[y][x+1].lightval = 0.5    #some value
#                 propagateRadial(y, x+1, right=True)
#             if left:
#                 currChunkRef[y][x-1].lightval = 0.5     #some value
#                 propagateRadial(y, x-1, left=True)

def generate_chunk_temp( _chunk ):
    pass

class Chunk:

    def __init__( self , _blocks = None , _walls = None , _local_tile_table = None , _index = None , _created = None , _active_time = None ):

        self.blocks             = _blocks
        self.walls              = _walls
        self.local_tile_table   = _local_tile_table
        self.index              = _index

        # self.created            = _time
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
        self.positions      = [None] * 3

        # chunk and light surface data
        self.chunks         = [None] * _len
        self.light_surfs    = [None] * _len

        # References to the other managers (These must be provided in the main)
        self.entity_buffer  = None
        self.renderer       = None
        self.serializer     = None
        self.player         = None

    def initialize( self , _entity_buffer , _renderer , _serializer , _player , _camera , _screen ):

        # Set all references to main managers
        self.entity_buffer  = _entity_buffer
        self.renderer       = _renderer
        self.serializer     = _serializer
        self.player         = _player
        self.camera         = _camera
        self.screen         = _screen

    def draw( self ):

        for chunk in self.chunks: chunk.draw()

    def shift( self , _delta ):
        if _delta > 0:      self.shift_left( _delta )
        elif _delta < 0:    self.shift_right( -_delta )

    def shift_right( self , _delta ):

        for i , pos in enumerate( range( self.positions[2] , self.positions[2] - _delta , -1 ) ):

            li                      = [ self.chunks[self.len-1-i].blocks, self.chunks[self.len-1-i].walls ]
            lo                      = self.chunk[self.len-1-i].local_tile_table

            self.serializer[pos]    = li, lo

        for i in range( self.len - 1, _delta - 1, -1 ):

            self.chunks[i]          = self.chunks[i - _delta]

        loadedChunks =  [None] * _delta
        for i , pos in enumerate( range( self.positions[0] - _delta , self.positions[0] ) ):

            loadedChunks[i]         = self.serializer[pos]
            self.chunks[i]          = loadedChunks[i]
            # Process the chunks before putting it in however

        self.positions[0] -= _delta
        self.positions[1] -= _delta
        self.positions[2] -= _delta

    def shift_left( self , _delta ):

        for i , pos in enumerate( range( self.positions[0] , self.positions[0] + _delta ) ):

            li                      = [ self.chunks[i].blocks , self.chunks[i].walls ]
            lo                      = self.chunk[i].local_tile_table

            self.serializer[pos]    = li , lo

        for i in range( self.length - _delta ):

            self.chunks[i]          = self.chunks[i + _delta]

        loaded_chunks =  [None] * _delta
        for i , pos in enumerate( range( self.len - _delta , self.len ) ):

            loaded_chunks[i]        = self.serializer[self.positions[2] + i + 1]
            self.chunks[pos]        = loaded_chunks[i]
            # Process the chunks before putting it in however

        self.positions[0] += _delta
        self.positions[1] += _delta
        self.positions[2] += _delta

    def save( self ):

        for chunk in self.chunks:
            self.serializer[chunk.index] = pickle.dumps( [ chunk.blocks , chunk.walls ] ) , pickle.dumps( chunk.local_tile_table )

    def load( self ):

        for i in range( self.len ):
            self.chunks[i] = self.serializer[self.positions[0] + i]
        # Now generate and process the chunks as much as required

    def __getitem__( self , _key ): return self.chunks[_key]

    def __setitem__( self , _key , _val ): self.chunks[ _key ] = _val