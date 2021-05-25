# todo Need to optimize the shift left and shift right methods

import math
import pickle
import pygame
import pygame.freetype

import constants as consts


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

def generate_chunk_temp( _chunk , noise_gen ):
    # one layer of bedrock
    # one layer of obsidian
    # one layer of hellstone
    # 10 layers of stone
    # 10 layers of limestone
    # 10 layers of sandstone
    # one layer of coal
    # one layer of dirt
    # one layer of grass
    # for i in range( consts.CHUNK_WIDTH ):
    #     _chunk.blocks[0][i] = consts.tiles.bedrock
    #     _chunk.blocks[1][i] = consts.tiles.obsidian
    #     _chunk.blocks[2][i] = consts.tiles.hellstone
    #     for j in range(10):
    #         _chunk.blocks[j + 3][i] = consts.tiles.greystone
    #         _chunk.blocks[j + 13][i] = consts.tiles.limestone
    #         _chunk.blocks[j + 23][i] = consts.tiles.sandstone
    #     _chunk.blocks[32][i] = consts.tiles.coal
    #     _chunk.blocks[33][i] = consts.tiles.browndirt
    #     _chunk.blocks[34][i] = consts.tiles.grass

    # for i in range( CHUNK_WIDTH ):
    #     for j in range( CHUNK_HEIGHT ):
    #         _chunk.blocks[j][i] = tiles.bedrock

    for i in range( consts.CHUNK_WIDTH ):
        x_coor = i + ( consts.CHUNK_WIDTH * _chunk.index )
        my_height = int( ( noise_gen.noise2d( x = 0.0075 * x_coor, y = 0 ) + 1 ) * 32 ) # Value will be from 0 to 64
        for j in range( my_height ):
            _chunk.blocks[j][i] = consts.tiles.browndirt


class Chunk:

    def __init__( self , _blocks = None , _walls = None , _local_tile_table = None , _index = None , _active_time = None ):

        self.blocks             = _blocks
        self.walls              = _walls
        self.local_tile_table   = _local_tile_table
        self.index              = _index

        # self.created            = _time
        self.active_time        = _active_time

        # self.surf               = pygame.Surface( ( CHUNK_WIDTH_P , CHUNK_HEIGHT_P ) , flags = pygame.SRCALPHA )
        self.surf               = pygame.Surface( (consts.CHUNK_WIDTH_P , consts.CHUNK_HEIGHT_P) )

        if not self.blocks:
            self.blocks = [ [ consts.tiles.air for j in range( consts.CHUNK_WIDTH ) ] for i in range( consts.CHUNK_HEIGHT ) ]
        if not self.walls:
            self.walls = [ [ consts.tiles.air for j in range( consts.CHUNK_WIDTH ) ] for i in range( consts.CHUNK_HEIGHT ) ]
        if not self.local_tile_table:
            self.local_tile_table = {}

    def draw( self, _rect = [ 0 , 0 , consts.CHUNK_WIDTH , consts.CHUNK_HEIGHT ] ):

        x_start = consts.TILE_WIDTH * ( _rect[0 ])
        y_start = consts.TILE_WIDTH * (consts.CHUNK_HEIGHT - _rect[3 ])

        x_span  = consts.TILE_WIDTH * (_rect[2 ] - _rect[0 ])
        y_span  = consts.TILE_WIDTH * (_rect[3 ] - _rect[1 ])

        # make the region transparent
        self.surf.fill( ( 0 , 0 , 0 , 0 ), [ x_start , y_start , x_span, y_span])

        # loop for blitting the tiles and walls
        for i in range( _rect[1] , _rect[3] ):

            coors = [ 0 , consts.TILE_WIDTH * (consts.CHUNK_HEIGHT - i - 1) ]

            for j in range( _rect[0] , _rect[2] ):

                coors[0]            = consts.TILE_WIDTH * j
                tile_ref , wall_ref = self.blocks[i][j] , self.walls[i][j]

                if tile_ref != consts.tiles.air :

                    self.surf.blit( consts.TILE_TABLE[tile_ref ], coors )
                    if ( i , j , 1 ) in self.local_tile_table : pass

                elif wall_ref != consts.tiles.air :

                    self.surf.blit( consts.TILE_TABLE[wall_ref ], coors )
                    if ( i , j , 0 ) in self.local_tile_table : pass

        # Then we blit the tile modifiers (cracks, glows, etc.)
        # Then we blit the liquids / fire


    def break_block_at( self , _x , _y , _item , _dt ):
        # Left click was done at the coordinates x, y for dt time using item tool at the block level
        # the behaviour of tool is acted using its corresponding function which we can get from a dictionary
        if( ( _x, _y, True ) not in self.local_tile_table ):
            self.local_tile_table[ ( _x, _y, True ) ] = { }

        if( consts.tile_attr.HEALTH not in self.local_tile_table[ ( _x, _y, True) ] ):
            self.local_tile_table[ ( _x, _y, True ) ][ consts.tile_attr.HEALTH ] = 100

        self.local_tile_table[ ( _x, _y, True ) ][ consts.tile_attr.HEALTH ] -= (25 * _dt)

        if(self.local_tile_table[ ( _x, _y, True ) ][ consts.tile_attr.HEALTH ] <= 0):
            del self.local_tile_table[ ( _x, _y, True ) ]
            self.blocks[_y][_x] = consts.tiles.air
            return True

        return False

    def break_wall_at( self , _x , _y , _item , _dt ): pass
        # Left click was done at the coordinates x, y for dt time using item tool at the wall level
        # the behaviour of tool is acted using its corresponding function which we can get from a dictionary

    def place_block_at( self , _x , _y , _tile, _local_entry = None ):
        # Place _tile at (_x, _y) and put an entry for it in the local tile table if _local_entry is a valid dictionary
        # Right click was done at the coordinates x, y for dt time using item item at the block level
        # the behaviour of item is acted using its corresponding function which we can get from a dictionary
        if self.blocks[_y][_x] != consts.tiles.air: return False
        self.blocks[_y][_x] = _tile

        if _local_entry: self.local_tile_table[ ( _x, _y, True) ] = _local_entry.copy()

        return True

    def place_wall_at( self , _x , _y , _item , _dt ): pass
        # Right click was done at the coordinates x, y for dt time using item item at the wall level
        # the behaviour of item is acted using its corresponding function which we can get from a dictionary

    def update( self , _dt ): pass
        # First we update the state of all the blocks using their respective function calls (growing trees, flowers, decaying blocks etc)
        # Fire spread
        # Liquid movement

class ChunkBuffer:

    def __init__( self , _len ):

        # size and positions of chunks in the world
        self.len            = _len
        # self.positions      = [None] * 3
        self.positions      = [ 0, 0, 0 ]

        # chunk and light surface data
        self.chunks         = [None] * _len
        self.light_surfs    = [None] * _len

        # References to the other managers (These must be provided in the main)
        self.entity_buffer  = None
        self.renderer       = None
        self.serializer     = None
        self.player         = None

    def initialize( self , _entity_buffer , _renderer , _serializer , _player , _camera , _screen , _noise_gen ):

        # Set all references to main managers
        self.entity_buffer  = _entity_buffer
        self.renderer       = _renderer
        self.serializer     = _serializer
        self.player         = _player
        self.camera         = _camera
        self.screen         = _screen
        self.noise_gen      = _noise_gen

        self.positions[1]   = math.floor( self.player.pos[0] / consts.CHUNK_WIDTH_P )

        self.positions[0]   = self.positions[1] - ( self.len // 2 )
        self.positions[2]   = self.positions[1] + ( self.len // 2 )

        self.load()

    def draw( self ):

        for chunk in self.chunks: chunk.draw()

    def shift( self , _delta ):

        flag ,_delta = (True, _delta) if _delta > 0 else (False, -_delta)
        num_times , extra = _delta // self.len , _delta % self.len

        side = self.shift_left if flag else self.shift_right

        for i in range( num_times ): side( self.len )
        if extra: side( extra )

        if num_times: return ( 0 , self.len )
        elif flag:    return ( self.len - extra, extra )
        else:         return ( 0, extra)

    def shift_right( self , _delta ):

        for i , pos in enumerate( range( self.positions[2] , self.positions[2] - _delta , -1 ) ):

            li                      = [ self.chunks[self.len-1-i].blocks, self.chunks[self.len-1-i].walls ]
            lo                      = self.chunks[self.len-1-i].local_tile_table

            self.serializer[pos]    = pickle.dumps( li ), pickle.dumps( lo )

        for i in range( self.len - 1, _delta - 1, -1 ):

            self.chunks[i]          = self.chunks[i - _delta]

        loaded_chunks =  [None] * _delta
        for i , pos in enumerate( range( self.positions[0] - _delta , self.positions[0] ) ):

            loaded_chunks[i]         = self.serializer[pos]

            if loaded_chunks[i] is None:
                loaded_chunks[i] = Chunk( _index = pos )
                generate_chunk_temp( loaded_chunks[i] , self.noise_gen )
            else:
                li = pickle.loads( loaded_chunks[i][0] )
                lo = pickle.loads( loaded_chunks[i][1] )
                loaded_chunks[i] = Chunk( _blocks = li[0] , _walls = li[1] , _local_tile_table = lo , _index = pos )

            self.chunks[i]          = loaded_chunks[i]

        self.positions[0] -= _delta
        self.positions[1] -= _delta
        self.positions[2] -= _delta

        return self.positions[0]

    def shift_left( self , _delta ):

        for i , pos in enumerate( range( self.positions[0] , self.positions[0] + _delta ) ):

            li                      = [ self.chunks[i].blocks , self.chunks[i].walls ]
            lo                      = self.chunks[i].local_tile_table

            self.serializer[pos]    = pickle.dumps( li ), pickle.dumps( lo )

        for i in range( self.len - _delta ):

            self.chunks[i]          = self.chunks[i + _delta]

        loaded_chunks =  [None] * _delta
        for i , pos in enumerate( range( self.len - _delta , self.len ) ):

            loaded_chunks[i]        = self.serializer[self.positions[2] + i + 1]

            if loaded_chunks[i] is None:
                loaded_chunks[i] = Chunk( _index = self.positions[2] + i + 1 )
                generate_chunk_temp( loaded_chunks[i] , self.noise_gen )
            else:
                li = pickle.loads( loaded_chunks[i][0] )
                lo = pickle.loads( loaded_chunks[i][1] )
                loaded_chunks[i] = Chunk( _blocks = li[0] , _walls = li[1] , _local_tile_table = lo , _index = self.positions[2] + i + 1 )

            self.chunks[pos]        = loaded_chunks[i]

        self.positions[0] += _delta
        self.positions[1] += _delta
        self.positions[2] += _delta

        return self.positions[2]

    def save( self ):

        for chunk in self.chunks:
            self.serializer[chunk.index] = pickle.dumps( [ chunk.blocks , chunk.walls ] ) , pickle.dumps( chunk.local_tile_table )

    def load( self ):

        for i in range( self.len ):
            self.chunks[i] = self.serializer[self.positions[0] + i]

        for i in range( self.len ):

            if( self.chunks[i] is None ):

                self.chunks[i] = Chunk( _index = self.positions[0] + i )
                generate_chunk_temp( self.chunks[i] , self.noise_gen )

            else:

                li = pickle.loads( self.chunks[i][0] )
                lo = pickle.loads( self.chunks[i][1] )

                self.chunks[i] = Chunk( _blocks = li[0] , _walls = li[1] , _local_tile_table = lo , _index = self.positions[0] + i )

            self.chunks[i].draw()

    def show_indices( self ):
        for c in self.chunks: print(c.index, end=' ')
        print()

    def __getitem__( self , _key ): return self.chunks[_key]

    def __setitem__( self , _key , _val ): self.chunks[ _key ] = _val