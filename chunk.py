import math
import pickle
import pygame
import pygame.freetype

import queue

import constants as consts

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
    for i in range( consts.CHUNK_WIDTH ):
        _chunk.blocks[0][i] = consts.tiles.bedrock
        _chunk.blocks[1][i] = consts.tiles.obsidian
        _chunk.blocks[2][i] = consts.tiles.hellstone
        for j in range(10):
            _chunk.blocks[j + 3][i] = consts.tiles.greystone
            _chunk.blocks[j + 13][i] = consts.tiles.limestone
            _chunk.blocks[j + 23][i] = consts.tiles.sandstone
        _chunk.blocks[32][i] = consts.tiles.coal
        _chunk.blocks[33][i] = consts.tiles.browndirt
        _chunk.blocks[34][i] = consts.tiles.grass

    # for i in range( CHUNK_WIDTH ):
    #     for j in range( CHUNK_HEIGHT ):
    #         _chunk.blocks[j][i] = tiles.bedrock

    # for i in range( consts.CHUNK_WIDTH ):
    #     x_coor = i + ( consts.CHUNK_WIDTH * _chunk.index )
    #     my_height = int( ( noise_gen.noise2d( x = 0.0075 * x_coor, y = 0 ) + 1 ) * 32 ) # Value will be from 0 to 64
    #     for j in range( my_height ):
    #         _chunk.blocks[j][i] = consts.tiles.browndirt


class Chunk:

    def __init__( self , _blocks = None , _walls = None , _local_tile_table = None , _index = None , _active_time = None ):

        self.blocks             = _blocks
        self.walls              = _walls
        self.liquid_lvls        = [[[None, 0] for i in range( consts.CHUNK_WIDTH )] for j in range( consts.CHUNK_HEIGHT )]

        self.local_tile_table   = _local_tile_table
        self.index              = _index

        # self.created            = _time
        self.active_time        = _active_time

        self.surf               = pygame.Surface( ( consts.CHUNK_WIDTH_P , consts.CHUNK_HEIGHT_P ) , flags = pygame.SRCALPHA )

        if not self.blocks:
            self.blocks = [ [ consts.tiles.air for j in range( consts.CHUNK_WIDTH ) ] for i in range( consts.CHUNK_HEIGHT ) ]
        if not self.walls:
            self.walls = [ [ consts.tiles.air for j in range( consts.CHUNK_WIDTH ) ] for i in range( consts.CHUNK_HEIGHT ) ]
        if not self.local_tile_table:
            self.local_tile_table = [ {}, {} ]

    def draw( self, _rect = [ 0 , 0 , consts.CHUNK_WIDTH , consts.CHUNK_HEIGHT ] ):

        x_start = consts.TILE_WIDTH * ( _rect[0])
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
                    if ( i , j ) in self.local_tile_table[1] : pass

                elif wall_ref != consts.tiles.air :

                    self.surf.blit( consts.TILE_TABLE[wall_ref ], coors )
                    if ( i , j ) in self.local_tile_table[0] : pass

                if self.liquid_lvls[i][j][0]:
                    which_liquid, my_level = self.liquid_lvls[i][j]
                    self.surf.blit( consts.TILE_MODIFIERS[consts.tile_modifs.water][int( my_level )], coors )

        # Blitting modifiers on walls
        for key in self.local_tile_table[0]:
            x, y        = key
            wall        = self.walls[y][x]
            wall_attr   = self.local_tile_table[0][key]

            coors       = [ x * consts.TILE_WIDTH, ( consts.CHUNK_HEIGHT - y - 1) * consts.TILE_WIDTH ]

            if consts.tile_attr.HEALTH in wall_attr:
                break_state = int( ( wall_attr[consts.tile_attr.HEALTH] * 8 ) / consts.TILE_ATTR[wall][consts.tile_attr.HEALTH] )
                self.surf.blit( consts.TILE_MODIFIERS[consts.tile_attr.crack][8 - break_state], coors )

        # Blitting modifiers on tiles
        for key in self.local_tile_table[1]:
            x, y        = key
            blck        = self.blocks[y][x]
            blck_attr   = self.local_tile_table[1][key]

            coors       = [ x * consts.TILE_WIDTH, ( consts.CHUNK_HEIGHT - y - 1) * consts.TILE_WIDTH ]

            if consts.tile_attr.HEALTH in blck_attr:
                break_state = int( ( blck_attr[consts.tile_attr.HEALTH] * 8 ) / consts.TILE_ATTR[blck][consts.tile_attr.HEALTH] )
                self.surf.blit( consts.TILE_MODIFIERS[consts.tile_modifs.crack][8 - break_state], coors )

        # Then we blit the tile modifiers (cracks, glows, etc.)
        # Then we blit the liquids / fire

    def update( self, _dt ):

        # Go through every block in this table
        to_remove = queue.Queue( maxsize = consts.CHUNK_WIDTH * consts.CHUNK_HEIGHT )
        for key in self.local_tile_table[0]:

            to_remove_local = queue.Queue( maxsize = 256 )
            x, y = key

            flag = 0

            # Go through every attribute of this block
            for attr in self.local_tile_table[0][key]:

                if attr == consts.tile_attr.HEALTH:

                    blck = self.walls[y][x]
                    health_tot = consts.TILE_ATTR[blck][consts.tile_attr.HEALTH]
                    self.local_tile_table[0][key][attr] += ( health_tot // 5 ) * _dt

                    # If this is of no significance, then put it to a queue to be removed
                    if self.local_tile_table[0][key][attr] >= health_tot:
                        to_remove_local.put( attr )

                    flag = 1

            # Go through the queue and remove all redundant key-value pairs
            while to_remove_local.qsize():
                del self.local_tile_table[0][key][to_remove_local.get()]

            if len( self.local_tile_table[0][key] ) <= 0:
                to_remove.append( key )

            if flag and self.blocks[y][x] == consts.tiles.air:
                self.draw( [x, y, x + 1, y + 1] )

        while to_remove.qsize():
            del self.local_tile_table[0][to_remove.get()]

        # Go through every block in this table
        for key in self.local_tile_table[1]:

            to_remove_local = queue.Queue( maxsize = consts.CHUNK_WIDTH * consts.CHUNK_HEIGHT )
            x, y = key

            flag = 0

            # Go through every attribute of this block
            for attr in self.local_tile_table[1][key]:

                if attr == consts.tile_attr.HEALTH:

                    blck = self.blocks[y][x]
                    health_tot = consts.TILE_ATTR[blck][consts.tile_attr.HEALTH]
                    self.local_tile_table[1][key][attr] += ( health_tot // 5 ) * _dt

                    # If this is of no significance, then put it to a queue to be removed
                    if self.local_tile_table[1][key][attr] >= health_tot:
                        to_remove_local.put( attr )

                    flag = 1

            # Go through the queue and remove all redundant key-value pairs
            while to_remove_local.qsize():
                del self.local_tile_table[1][key][to_remove_local.get()]

            if len( self.local_tile_table[1][key] ) <= 0:
                to_remove.put( key )

            if flag:
                self.draw( [x, y, x + 1, y + 1] )

        while to_remove.qsize():
            del self.local_tile_table[1][to_remove.get()]

        for i in range( consts.CHUNK_HEIGHT ):
            for j in range( consts.CHUNK_WIDTH ):
                if self.liquid_lvls[i][j][0]:
                    which_liquid, my_level = self.liquid_lvls[i][j]

    def get_surf( self ):
        return self.surf

class ChunkBuffer:

    def __init__( self , _len ):

        # size and positions of chunks in the world
        self.len            = _len
        self.mid            = 0

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

        self.mid            = math.floor( _player.get_pos()[0] / consts.CHUNK_WIDTH_P )

        self.load()

    def get_start_chunk_ind( self ):
        return self.mid - ( self.len >> 1 )

    def get_middle_chunk_ind( self ):
        return self.mid

    def get_end_chunk_ind( self ):
        return self.mid + ( self.len >> 1 )

    def draw( self ):
        for chunk in self.chunks:
            chunk.draw()

    def update( self, _dt ):
        for chunk in self.chunks:
            chunk.update( _dt )

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

        for i , pos in enumerate( range( self.get_end_chunk_ind() , self.get_end_chunk_ind() - _delta , -1 ) ):

            li                      = [ self.chunks[self.len-1-i].blocks, self.chunks[self.len-1-i].walls ]
            lo                      = self.chunks[self.len-1-i].local_tile_table

            self.serializer.set_chunk( pos, pickle.dumps( li ), pickle.dumps( lo ) )

        for i in range( self.len - 1, _delta - 1, -1 ):

            self.chunks[i]          = self.chunks[i - _delta]

        loaded_chunks =  [None] * _delta
        for i , pos in enumerate( range( self.get_start_chunk_ind() - _delta , self.get_start_chunk_ind() ) ):

            loaded_chunks[i]         = self.serializer.get_chunk( pos )

            if loaded_chunks[i] is None:
                loaded_chunks[i] = Chunk( _index = pos )
                generate_chunk_temp( loaded_chunks[i] , self.noise_gen )
            else:
                li = pickle.loads( loaded_chunks[i][0] )
                lo = pickle.loads( loaded_chunks[i][1] )
                loaded_chunks[i] = Chunk( _blocks = li[0] , _walls = li[1] , _local_tile_table = lo , _index = pos )

            self.chunks[i]          = loaded_chunks[i]

        self.mid -= _delta

    def shift_left( self , _delta ):

        for i , pos in enumerate( range( self.get_start_chunk_ind() , self.get_start_chunk_ind() + _delta ) ):

            li                      = [ self.chunks[i].blocks , self.chunks[i].walls ]
            lo                      = self.chunks[i].local_tile_table

            self.serializer.set_chunk( pos, pickle.dumps( li ), pickle.dumps( lo ) )

        for i in range( self.len - _delta ):

            self.chunks[i]          = self.chunks[i + _delta]

        loaded_chunks =  [None] * _delta
        for i , pos in enumerate( range( self.len - _delta , self.len ) ):

            loaded_chunks[i]        = self.serializer.get_chunk( self.get_end_chunk_ind() + i + 1 )

            if loaded_chunks[i] is None:
                loaded_chunks[i] = Chunk( _index = self.get_end_chunk_ind() + i + 1 )
                generate_chunk_temp( loaded_chunks[i] , self.noise_gen )
            else:
                li = pickle.loads( loaded_chunks[i][0] )
                lo = pickle.loads( loaded_chunks[i][1] )
                loaded_chunks[i] = Chunk( _blocks = li[0] , _walls = li[1] , _local_tile_table = lo , _index = self.get_end_chunk_ind() + i + 1 )

            self.chunks[pos]        = loaded_chunks[i]

        self.mid += _delta

    def calc_light( self ):
        pass

    def save( self ):

        for chunk in self.chunks:
            self.serializer.set_chunk( chunk.index, pickle.dumps( [ chunk.blocks , chunk.walls ] ) , pickle.dumps( chunk.local_tile_table ) )

    def load( self ):

        left = self.mid - ( self.len >> 1 )
        right = self.mid + ( self.len >> 1 )

        for i in range( self.len ):
            self.chunks[i] = self.serializer.get_chunk( left + i )

            if self.chunks[i] is None:

                self.chunks[i] = Chunk( _index = left + i )
                generate_chunk_temp( self.chunks[i] , self.noise_gen )

            else:

                li = pickle.loads( self.chunks[i][0] )
                lo = pickle.loads( self.chunks[i][1] )

                self.chunks[i] = Chunk( _blocks = li[0] , _walls = li[1] , _local_tile_table = lo , _index = left + i )

            self.chunks[i].draw()


    def show_indices( self ):
        for c in self.chunks: print(c.index, end=' ')
        print()

    # def shadeRetro( self, index, top=True, down=True, left=True, right=True ):

    #     for c in range( self.len ):
    #         for i in range( consts.CHUNK_HEIGHT ):
    #             for j in range( consts.CHUNK_WIDTH ):

    #                 currTileRef = parent[index][i][j]
    #                 currWallRef = parent[index].walls[i][j]

    #                 selfLuminousity  = 0

    #                 # if(currTileRef > 0 or currWallRef == 0):    # Front tile is present or wall is absent
    #                 #     selfLuminousity = TILE_ATTR[currTileRef][LUMINOSITY]
    #                 # elif(currWallRef > 0):                      # Front tile is absent but wall is present
    #                 #     selfLuminousity = TILE_ATTR[currWallRef][LUMINOSITY]

    #                 selfLuminousity = tiles.TILE_ATTR[currTileRef][LUMINOSITY]
    #                 selfIllumination = self[index].lightMap[i][j]

    #                 if(selfLuminousity is not 0 and selfIllumination < selfLuminousity):
    #                     parent[index].lightMap[i][j] = selfLuminousity
    #                     self.propagateRetro(index, j, i)

    # def propagateRetro( self, index, x, y, top=True, right=True, bottom=True, left=True ):

    #     if(index < 0): index = self.length+index

    #     topVal      =  self[index].lightMap[y][x]-16
    #     rightVal    =  self[index].lightMap[y][x]-16
    #     bottomVal   =  self[index].lightMap[y][x]-16
    #     leftVal     =  self[index].lightMap[y][x]-16

    #     if(topVal < 0): top=False
    #     if(rightVal < 0): right=False
    #     if(bottomVal < 0): bottom=False
    #     if(leftVal < 0): left=False

    #     # Top side
    #     if(top):
    #         if(y+1 < CHUNK_HEIGHT):         #check if the next position (1 above) is valid
    #             if(topVal > self[index].lightMap[y+1][x]):
    #                 self[index].lightMap[y+1][x]   =  topVal
    #                 self.propogateRetro(index, x, y+1, bottom=False)

    #     # Bottom side
    #     if(bottom):
    #         if(y-1 >= 0):                   #check if the next position (1 below) is valid
    #             if(bottomVal >= self[index].lightMap[y-1][x]):
    #                 self[index].lightMap[y-1][x]   =  bottomVal
    #                 self.propogateRetro(index, x, y-1, top=False)

    #     # Left side
    #     if(left):
    #         if(x-1 >= 0):                   #check if the next position (1 to the left) is valid
    #             if(leftVal > self[index].lightMap[y][x-1]):
    #                 self[index].lightMap[y][x-1]   =  leftVal
    #                 self.propogateRetro(index, x-1, y, right=False)

    #         elif(index-1 >= 0):             #check if previous chunk exists in the chunk buffer
    #             if(leftVal > self[index-1].lightMap[y][CHUNK_WIDTH-1]):
    #                 self[index-1].lightMap[y][CHUNK_WIDTH-1]   =  leftVal
    #                 self.propogateRetro(index-1, CHUNK_WIDTH-1, y, right=False)

    #     # Right side
    #     if(right):
    #         if(x+1 < CHUNK_WIDTH):          #check if the next position (1 to the right) is valid
    #             if(rightVal > self[index].lightMap[y][x+1]):
    #                 self[index].lightMap[y][x+1]   =  rightVal
    #                 self.propogateRetro(index, x+1, y, left=False)

    #         elif(index+1 < self.length):    #check if next chunk exists in the chunk buffer
    #             if(rightVal > self[index+1].lightMap[y][0]):
    #                 self[index+1].lightMap[y][0]   =  rightVal
    #                 self.propogateRetro(index+1, 0, y, left=False)

    # def shadeRadial( self ):

    #     luminous = None # the luminosity of the block
    #     sq2 = 1.414
    #     for index in range(0, parent.length):
    #         currChunkRef = self.parent[index]
    #         for y in range(CHUNK_HEIGHT):
    #             for x in range(CHUNK_WIDTH):

    #                 currTileRef = parent[index][y][x]
    #                 currWallRef = parent[index].walls[y][x]

    #                 if( currTileRef is luminous or currWallRef is luminous):

    #                     propagateRadial( index, x, y, True, True, True, True)

    #                     # i, j = 1, 1
    #                     while( y-1-i>0 and x-1-i>0 ):   #up diagonal left
    #                         propagateRadial( index, x-1-i, y-1-i, up=True, left=True)

    #                     # i, j = 1, 1
    #                     while( y-1-i>0 and x+1+i<CHUNK_WIDTH ): #up diagonal right
    #                         propagateRadial( index, x+1+i, y-1-i, up=True, right=True)

    #                     # i, j = 1, 1
    #                     while( y+1+i<CHUNK_HEIGHT and x-1-i>0 ):    #down diagonal left
    #                         propagateRadial( index, x-1-i, y+1+i, down=True, left=True)

    #                     # i, j = 1, 1
    #                     while( y+1+i<CHUNK_HEIGHT and x+1+i<CHUNK_WIDTH ):  #down diagonal right
    #                         propagateRadial( index, x+1+i, y+1+i, down=True, right=True)

    # def propagateRadial( self, index, x, y, up=False, down=False, left=False, right=False ):

    #     currChunkRef = self.parent[index]
    #     valid = True       #check if valid

    #     if valid and lightval != 0:
    #         if up:
    #             currChunkRef[y+1][x].lightval = 0.5    #some value
    #             propagateRadial(y+1, x, up=True)
    #         if down:
    #             currChunkRef[y-1][x].lightval = 0.5    #some value
    #             propagateRadial(y-1, x, down=True)
    #         if right:
    #             currChunkRef[y][x+1].lightval = 0.5    #some value
    #             propagateRadial(y, x+1, right=True)
    #         if left:
    #             currChunkRef[y][x-1].lightval = 0.5     #some value
    #             propagateRadial(y, x-1, left=True)