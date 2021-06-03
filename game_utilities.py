import bz2
import math
import os
import pygame
import pygame.freetype
import sqlite3

import constants as consts


def populate_key_states( _key_states , _button_states ):
    for i in range( pygame.K_a , pygame.K_z + 1 ):
        _key_states[i] = 0
    for i in range( pygame.K_0 , pygame.K_9 + 1 ):
        _key_states[i] = 0

    _key_states[pygame.K_UP ]    = 0
    _key_states[pygame.K_DOWN ]  = 0
    _key_states[pygame.K_LEFT ]  = 0
    _key_states[pygame.K_RIGHT ] = 0

    _key_states[pygame.K_SPACE ] = 0

    # 0 is for left, 1 is for middle and 2 is for right
    _button_states[ pygame.BUTTON_LEFT ]   = 0
    _button_states[ pygame.BUTTON_MIDDLE ] = 0
    _button_states[ pygame.BUTTON_RIGHT ]  = 0


# Translations
#     From                        To
# 1   array-space                 chunk-space
#     coordinates in the array    coordinates in the chunk
# 2   chunk-space                 world-space
#     coordinates in the chunk    coordinates in the world (absolute coordinates)
# 3   world-space                 camera-space
#     coordinates in the world    coordinates relative to camera
# 4   camera-space                screen-space
#     coordinates in the array    coordinates on the display

class Renderer:

    def __init__( self ):

        # References to other managers (must be provided in main)
        self.entity_buffer  = None
        self.chunk_buffer   = None
        self.serializer     = None
        self.player         = None

        # Reference to camera and screen surface
        self.camera         = None
        self.screen         = None

        # Reference to window size
        self.window_size    = None

        # Index of the middle chunk (the chunk the camera is in)
        # self.middle         = None
        self.middle = 0

        # Indexes of the top and bottom most pixels of the chunk to be rendered
        self.up_index       = None
        self.down_index     = None

        # Number of pixels on the top and bottom half of the screen
        self.num_hor        = None
        self.num_ver        = None

        self.camera_upper   = None

    def initialize( self , _chunk_buffer , _entity_buffer , _player , _serializer , _camera , _screen , _window_size ):

        # Set all references to main managers
        self.chunk_buffer   = _chunk_buffer
        self.entity_buffer  = _entity_buffer
        self.player         = _player
        self.serializer     = _serializer
        self.camera         = _camera
        self.screen         = _screen

        self.window_size    = _window_size

        self.update_size()
        self.update_camera()

    def paint_screen( self ):

        # First we need to put the background picture
        # This remains constant if you are very high or very low
        # In the overworld, it changes from day to night

        # right_walker    = self.middle
        # left_walker     = self.middle - 1

        flag            = False

        for right_walker in range( self.middle , self.chunk_buffer.len ):

            slice_ind       = self.chunk_buffer[right_walker].index * consts.CHUNK_WIDTH       # Absolute index of current vertical slice
            slice_pos       = [ 0 , 0 ]                                                 # List containing coordinates of the location where the slice must be blit
            slice_rect      = [ 0 , self.up_index , consts.TILE_WIDTH , self.down_index ]      # Rectangular region containing the "visible" area of the chunk's surface

            for tile_walker in range( 0 , consts.CHUNK_WIDTH ):

                slice_pos[0]    = ( slice_ind + tile_walker ) * consts.TILE_WIDTH - self.camera[0 ] + self.num_hor
                slice_rect[0]   = tile_walker * consts.TILE_WIDTH

                slice_surf      = self.chunk_buffer[ right_walker ].surf.subsurface( slice_rect )            # Mini-surface containing the visible region of the chunk's surface

                if slice_pos[0] > self.window_size[0] :
                    flag = True
                    break

                self.screen.blit( slice_surf, slice_pos )

                # if(cls.isShader):
                #     light_surf      = self.chunk_buffer.light_surfs[ right_walker ].subsurface( slice_rect )
                #     cls.screen.blit( light_surf, slice_pos, special_flags = pygame.BLEND_RGBA_MULT )

            if flag : break

        flag = False

        for left_walker in range( self.middle - 1, -1 , -1 ):

            slice_ind       = self.chunk_buffer[left_walker].index * consts.CHUNK_WIDTH        # Absolute index of current vertical slice
            slice_pos       = [ 0 , 0 ]                                                 # List containing coordinates of the location where the slice must be blit
            slice_rect      = [ 0 , self.up_index , consts.TILE_WIDTH , self.down_index ]      # Rectangular region containing the "visible" area of the chunk's surface

            for tile_walker in range( consts.CHUNK_WIDTH - 1 , -1 , -1 ):

                slice_pos[0]    = ( slice_ind + tile_walker ) * consts.TILE_WIDTH - self.camera[0 ] + self.num_hor
                slice_rect[0]   = tile_walker * consts.TILE_WIDTH

                slice_surf      = self.chunk_buffer[ left_walker ].surf.subsurface( slice_rect )            # Mini-surface containing the visible region of the chunk's surface

                if slice_pos[0] < -consts.TILE_WIDTH :
                    flag = True
                    break

                self.screen.blit( slice_surf, slice_pos )

                # if(cls.isShader):
                #     cls.screen.blit( light_surf, slice_pos, special_flags = pygame.BLEND_RGBA_MULT )
                #     light_surf      = self.chunk_buffer.light_surfs[ left_walker ].subsurface( slice_rect )


            if flag : break

        # Temporary rendering of camera
        camera_coors = [self.camera[0], self.camera[1]]
        plyr_coors    = [self.player.pos[0], self.player.pos[1]]

        # Translate to camera's space
        camera_coors[0] -= self.camera[0]
        camera_coors[1] -= self.camera[1]

        plyr_coors[0] -= self.camera[0]
        plyr_coors[1] -= self.camera[1]

        # Translate to screen's space
        camera_coors[0] += self.num_hor
        camera_coors[1] = self.num_ver - camera_coors[1]

        plyr_coors[0] += self.num_hor
        plyr_coors[1] = self.num_ver - plyr_coors[1]

        # Blit a small rectangle
        self.screen.blit( self.player.texture_strct.texture, ( plyr_coors[0] - 8, plyr_coors[1] - 8))
        # pygame.draw.rect( self.screen, (50, 50, 255), pygame.Rect( plyr_coors[0] - 8, plyr_coors[1] - 8, 17, 17 ) )
        # pygame.draw.rect( self.screen, (255, 50, 50), pygame.Rect( camera_coors[0] - 2, camera_coors[1] - 2, 5, 5 ) )

        # item = cls.player.inventory.getSelectedItem()
        # name, quantity = 'Nothing', cls.player.inventory.getSelectedQuantity()
        # if(tiles.TILE_NAMES.get( item, None )):
        #     name = tiles.TILE_NAMES[item]
        # elif(items.ITEM_NAMES.get( item, None )):
        #     name = items.ITEM_NAMES[item]

        # if(name != 'Nothing'): name += '  ' + str(quantity)
        # toShow, rect = SC_DISPLAY_FONT.render( name , (0, 0, 0) )
        # xVal = cls.screen.get_width() - toShow.get_width() - 8
        # cls.screen.blit(toShow, [xVal, 16])

        # cls.entityBuffer.draw()
        # for group in cls.entityBuffer.entities:
        #     for entity in group:
        #         coors = entity.surfPos()
        #         coors[1] -= cls.camera[1]
        #         coors[1] = cls.numVer - coors[1]
        #         coors[0] += cls.numHor - cls.camera[0]
        #         cls.screen.blit( entity.surf, coors )

    def paint_inventory( self ):
        self.player.inventory.draw()
        self.screen.blit( self.player.inventory.surf , (20 , 20) )

    def paint_inventory_top( self ):
        self.player.inventory.draw_top()
        self.screen.blit( self.player.inventory.surf, (20, 20) )

    def update_size( self ):

        # Number of pixels to paint on either side of the camera (centred on the screen) after screen has been resized
        self.num_hor        = self.window_size[0] // 2
        self.num_ver        = self.window_size[1] // 2


        self.camera_upper   = consts.CHUNK_HEIGHT_P - self.num_ver

    def update_camera( self ):

        # Index of the highest point to be rendered
        self.up_index       = max( consts.CHUNK_HEIGHT_P - (self.camera[1 ] + self.num_ver), 0 )

        # Index of the lowest point to be rendered
        self.down_index     = min( consts.CHUNK_HEIGHT_P - self.up_index, self.window_size[1 ] )


class Serializer:
    def __init__( self, target ):
        self.name = "Worlds/" + target + '.db'
        if not os.path.isdir("Worlds"): os.mkdir("Worlds")
        self.conn = sqlite3.connect( self.name )
        c = self.conn.cursor()
        try:
            # Create Table
            c.execute( '''CREATE TABLE terrain(keys INTEGER NOT NULL PRIMARY KEY, list TEXT, local TEXT, chunk_time TEXT, entity TEXT)''' )
            self.conn.commit()
            c.execute( '''CREATE TABLE player(playername TEXT NOT NULL PRIMARY KEY, pickledplayer TEXT)''' )
            self.conn.commit()
            c.execute( '''CREATE TABLE info(world_time TEXT)''' )
            self.conn.commit()
        except Exception as e:
            consts.dbg(1, "EXCEPTION IN SERIALIZER INIT:", e)

    def set_chunk( self, key, t0, t1 ):
        t = t0, t1
        c = self.conn.cursor()
        try:
            # Save string at new key location
            c.execute( '''INSERT INTO terrain (keys, list, local) VALUES (?,?,?)''', ( key, bz2.compress( t[0] ), bz2.compress( t[1] ) ) )
            self.conn.commit()
        except Exception as e:
            # Update string at existing key
            consts.dbg( 1, "EXCEPTION IN SERIALIZER SETITEM:", e )
            c.execute( 'UPDATE terrain SET list =?, local =?  WHERE keys=?', ( bz2.compress( t[0] ), bz2.compress( t[1] ), key ) )
            self.conn.commit()

    def get_chunk(self, key):
        c = self.conn.cursor()
        c.execute( '''SELECT list FROM terrain WHERE keys=?''', ( key, ) )
        li = c.fetchone()
        c.execute( '''SELECT local FROM terrain WHERE keys=?''', ( key, ) )
        lo = c.fetchone()
        self.conn.commit()
        try:
            li = bz2.decompress( li[0] )
            lo = bz2.decompress( lo[0] )
            return li, lo
        except Exception as e:
            consts.dbg( 1, "EXCEPTION IN SERIALIZER GETITEM:", e )
            return None

    def set_chunk_time( self, _key, _time ):
        c = self.conn.cursor()
        try:
            # Set world time for the first time
            c.execute( '''INSERT INTO terrain (chunk_time) VALUES (?) WHERE keys=?''', ( bz2.compress( _time ), _key) )
            self.conn.commit()
        except Exception as e:
            # Update world time
            consts.dbg( 1, "EXCEPTION IN SERIALIZER SET_CHUNK_TIME:", e )
            c.execute( '''UPDATE terrain SET chunk_time=? WHERE keys=?''', ( bz2.compress( _time ), _key) )
            self.conn.commit()

    def get_chunk_time( self, _key ):
        c = self.conn.cursor()
        c.execute( '''SELECT chunk_time FROM terrain WHERE keys=?''', ( _key, ))
        res = c.fetchone()
        self.conn.commit()
        try:
            return bz2.decompress( res[0] )
        except Exception as e:
            consts.dbg( 1, "EXCEPTION IN SERIALIZER GET_CHUNK_TIME:", e )
            return res

    def set_entity(self, key, li):
        c = self.conn.cursor( )
        try:
            # Save string at new key location
            c.execute( '''INSERT INTO terrain (entity, keys) VALUES (?,?)''', (bz2.compress( li ), key) )
            self.conn.commit( )
        except Exception as e:
            consts.dbg(1, "EXCEPTION IN SERIALIZER SET_ENTITY:", e )
            # Update string at existing key
            c.execute( '''UPDATE terrain SET entity =? WHERE keys=?''', (bz2.compress( li ), key) )
            self.conn.commit( )

    def get_entity(self, key):
        c = self.conn.cursor()
        c.execute( '''SELECT entity FROM terrain WHERE keys=?''', ( key, ) )
        li = c.fetchone()
        self.conn.commit()
        try:
            li = bz2.decompress( li[0] )
            return li
        except Exception as e:
            consts.dbg( 1, "EXCEPTION IN SERIALIZER GET_ENTITY:", e )
            return None

    def save_player( self, name, pickled ):
        c = self.conn.cursor()
        try:
            # Save pickledplayer at new playername
            c.execute( '''INSERT INTO player (playername, pickledplayer) VALUES (?,?)''', ( name, bz2.compress( pickled ) ) )
            self.conn.commit()
        except Exception as e:
            # Update pickledplayer at existing playername
            consts.dbg( 1, "EXCEPTION IN SERIALIZER SAVE_PLAYER:", e )
            c.execute( '''UPDATE player SET pickledplayer =?  WHERE playername=?''', ( bz2.compress( pickled ), name ) )
            self.conn.commit()

    def load_player( self, name ):
        c = self.conn.cursor()
        c.execute( '''SELECT pickledplayer FROM player WHERE playername=?''', ( name, ) )
        res = c.fetchone()
        self.conn.commit()
        try:
            return bz2.decompress( res[0] )
        except Exception as e:
            consts.dbg( 1, "EXCEPTION IN SERIALIZER LOAD_PLAYER:", e )
            return res

    def set_world_time( self, _time ):
        c = self.conn.cursor()
        try:
            # Set world time for the first time
            c.execute( '''INSERT INTO info (world_time) VALUES (?)''', ( bz2.compress( _time ), ) )
            self.conn.commit()
        except Exception as e:
            # Update world time
            consts.dbg( 1, "EXCEPTION IN SERIALIZER SET_WORLD_TIME:", e )
            c.execute( '''UPDATE info SET world_time=?''', ( bz2.compress( _time ), ) )
            self.conn.commit()

    def get_world_time( self ):
        c = self.conn.cursor()
        c.execute( '''SELECT world_time FROM info''' )
        res = c.fetchone()
        self.conn.commit()
        try:
            return bz2.decompress( res[0] )
        except Exception as e:
            consts.dbg( 1, "EXCEPTION IN SERIALIZER GET_WORLD_TIME:", e )
            return res

    def stop( self ):
        self.conn.close( )


vector = [
    -0.763874, -0.596439, -0.246489, 0.0, 0.396055, 0.904518, -0.158073, 0.0,
    -0.499004, -0.8665, -0.0131631, 0.0, 0.468724, -0.824756, 0.316346, 0.0,
    0.829598, 0.43195, 0.353816, 0.0, -0.454473, 0.629497, -0.630228, 0.0,
    -0.162349, -0.869962, -0.465628, 0.0, 0.932805, 0.253451, 0.256198, 0.0,
    -0.345419, 0.927299, -0.144227, 0.0,    -0.715026, -0.293698, -0.634413, 0.0,
    -0.245997, 0.717467, -0.651711, 0.0,    -0.967409, -0.250435, -0.037451, 0.0,
    0.901729, 0.397108, -0.170852, 0.0,    0.892657, -0.0720622, -0.444938, 0.0,
    0.0260084, -0.0361701, 0.999007, 0.0,    0.949107, -0.19486, 0.247439, 0.0,
    0.471803, -0.807064, -0.355036, 0.0,    0.879737, 0.141845, 0.453809, 0.0,
    0.570747, 0.696415, 0.435033, 0.0,    -0.141751, -0.988233, -0.0574584, 0.0,
    -0.58219, -0.0303005, 0.812488, 0.0,    -0.60922, 0.239482, -0.755975, 0.0,
    0.299394, -0.197066, -0.933557, 0.0,    -0.851615, -0.220702, -0.47544, 0.0,
    0.848886, 0.341829, -0.403169, 0.0,    -0.156129, -0.687241, 0.709453, 0.0,
    -0.665651, 0.626724, 0.405124, 0.0,    0.595914, -0.674582, 0.43569, 0.0,
    0.171025, -0.509292, 0.843428, 0.0,    0.78605, 0.536414, -0.307222, 0.0,
    0.18905, -0.791613, 0.581042, 0.0,    -0.294916, 0.844994, 0.446105, 0.0,
    0.342031, -0.58736, -0.7335, 0.0,    0.57155, 0.7869, 0.232635, 0.0,
    0.885026, -0.408223, 0.223791, 0.0,    -0.789518, 0.571645, 0.223347, 0.0,
    0.774571, 0.31566, 0.548087, 0.0,    -0.79695, -0.0433603, -0.602487, 0.0,
    -0.142425, -0.473249, -0.869339, 0.0,    -0.0698838, 0.170442, 0.982886, 0.0,
    0.687815, -0.484748, 0.540306, 0.0,    0.543703, -0.534446, -0.647112, 0.0,
    0.97186, 0.184391, -0.146588, 0.0,    0.707084, 0.485713, -0.513921, 0.0,
    0.942302, 0.331945, 0.043348, 0.0,    0.499084, 0.599922, 0.625307, 0.0,
    -0.289203, 0.211107, 0.9337, 0.0,    0.412433, -0.71667, -0.56239, 0.0,
    0.87721, -0.082816, 0.47291, 0.0,    -0.420685, -0.214278, 0.881538, 0.0,
    0.752558, -0.0391579, 0.657361, 0.0,    0.0765725, -0.996789, 0.0234082, 0.0,
    -0.544312, -0.309435, -0.779727, 0.0,    -0.455358, -0.415572, 0.787368, 0.0,
    -0.874586, 0.483746, 0.0330131, 0.0,    0.245172, -0.0838623, 0.965846, 0.0,
    0.382293, -0.432813, 0.81641, 0.0,    -0.287735, -0.905514, 0.311853, 0.0,
    -0.667704, 0.704955, -0.239186, 0.0,    0.717885, -0.464002, -0.518983, 0.0,
    0.976342, -0.214895, 0.0240053, 0.0,    -0.0733096, -0.921136, 0.382276, 0.0,
    -0.986284, 0.151224, -0.0661379, 0.0,    -0.899319, -0.429671, 0.0812908, 0.0,
    0.652102, -0.724625, 0.222893, 0.0,    0.203761, 0.458023, -0.865272, 0.0,
    -0.030396, 0.698724, -0.714745, 0.0,    -0.460232, 0.839138, 0.289887, 0.0,
    -0.0898602, 0.837894, 0.538386, 0.0,    -0.731595, 0.0793784, 0.677102, 0.0,
    -0.447236, -0.788397, 0.422386, 0.0,    0.186481, 0.645855, -0.740335, 0.0,
    -0.259006, 0.935463, 0.240467, 0.0,    0.445839, 0.819655, -0.359712, 0.0,
    0.349962, 0.755022, -0.554499, 0.0,    -0.997078, -0.0359577, 0.0673977, 0.0,
    -0.431163, -0.147516, -0.890133, 0.0,    0.299648, -0.63914, 0.708316, 0.0,
    0.397043, 0.566526, -0.722084, 0.0,    -0.502489, 0.438308, -0.745246, 0.0,
    0.0687235, 0.354097, 0.93268, 0.0,    -0.0476651, -0.462597, 0.885286, 0.0,
    -0.221934, 0.900739, -0.373383, 0.0,    -0.956107, -0.225676, 0.186893, 0.0,
    -0.187627, 0.391487, -0.900852, 0.0,    -0.224209, -0.315405, 0.92209, 0.0,
    -0.730807, -0.537068, 0.421283, 0.0,    -0.0353135, -0.816748, 0.575913, 0.0,
    -0.941391, 0.176991, -0.287153, 0.0,    -0.154174, 0.390458, 0.90762, 0.0,
    -0.283847, 0.533842, 0.796519, 0.0,    -0.482737, -0.850448, 0.209052, 0.0,
    -0.649175, 0.477748, 0.591886, 0.0,    0.885373, -0.405387, -0.227543, 0.0,
    -0.147261, 0.181623, -0.972279, 0.0,    0.0959236, -0.115847, -0.988624, 0.0,
    -0.89724, -0.191348, 0.397928, 0.0,    0.903553, -0.428461, -0.00350461, 0.0,
    0.849072, -0.295807, -0.437693, 0.0,    0.65551, 0.741754, -0.141804, 0.0,
    0.61598, -0.178669, 0.767232, 0.0,    0.0112967, 0.932256, -0.361623, 0.0,
    -0.793031, 0.258012, 0.551845, 0.0,    0.421933, 0.454311, 0.784585, 0.0,
    -0.319993, 0.0401618, -0.946568, 0.0,    -0.81571, 0.551307, -0.175151, 0.0,
    -0.377644, 0.00322313, 0.925945, 0.0,    0.129759, -0.666581, -0.734052, 0.0,
    0.601901, -0.654237, -0.457919, 0.0,    -0.927463, -0.0343576, -0.372334, 0.0,
    -0.438663, -0.868301, -0.231578, 0.0,    -0.648845, -0.749138, -0.133387, 0.0,
    0.507393, -0.588294, 0.629653, 0.0,    0.726958, 0.623665, 0.287358, 0.0,
    0.411159, 0.367614, -0.834151, 0.0,    0.806333, 0.585117, -0.0864016, 0.0,
    0.263935, -0.880876, 0.392932, 0.0,    0.421546, -0.201336, 0.884174, 0.0,
    -0.683198, -0.569557, -0.456996, 0.0,    -0.117116, -0.0406654, -0.992285, 0.0,
    -0.643679, -0.109196, -0.757465, 0.0,    -0.561559, -0.62989, 0.536554, 0.0,
    0.0628422, 0.104677, -0.992519, 0.0,    0.480759, -0.2867, -0.828658, 0.0,
    -0.228559, -0.228965, -0.946222, 0.0,    -0.10194, -0.65706, -0.746914, 0.0,
    0.0689193, -0.678236, 0.731605, 0.0,    0.401019, -0.754026, 0.52022, 0.0,
    -0.742141, 0.547083, -0.387203, 0.0,    -0.00210603, -0.796417, -0.604745, 0.0,
    0.296725, -0.409909, -0.862513, 0.0,    -0.260932, -0.798201, 0.542945, 0.0,
    -0.641628, 0.742379, 0.192838, 0.0,    -0.186009, -0.101514, 0.97729, 0.0,
    0.106711, -0.962067, 0.251079, 0.0,    -0.743499, 0.30988, -0.592607, 0.0,
    -0.795853, -0.605066, -0.0226607, 0.0,    -0.828661, -0.419471, -0.370628, 0.0,
    0.0847218, -0.489815, -0.8677, 0.0,    -0.381405, 0.788019, -0.483276, 0.0,
    0.282042, -0.953394, 0.107205, 0.0,    0.530774, 0.847413, 0.0130696, 0.0,
    0.0515397, 0.922524, 0.382484, 0.0,    -0.631467, -0.709046, 0.313852, 0.0,
    0.688248, 0.517273, 0.508668, 0.0,    0.646689, -0.333782, -0.685845, 0.0,
    -0.932528, -0.247532, -0.262906, 0.0,    0.630609, 0.68757, -0.359973, 0.0,
    0.577805, -0.394189, 0.714673, 0.0,    -0.887833, -0.437301, -0.14325, 0.0,
    0.690982, 0.174003, 0.701617, 0.0,    -0.866701, 0.0118182, 0.498689, 0.0,
    -0.482876, 0.727143, 0.487949, 0.0,    -0.577567, 0.682593, -0.447752, 0.0,
    0.373768, 0.0982991, 0.922299, 0.0,    0.170744, 0.964243, -0.202687, 0.0,
    0.993654, -0.035791, -0.106632, 0.0,    0.587065, 0.4143, -0.695493, 0.0,
    -0.396509, 0.26509, -0.878924, 0.0,    -0.0866853, 0.83553, -0.542563, 0.0,
    0.923193, 0.133398, -0.360443, 0.0,    0.00379108, -0.258618, 0.965972, 0.0,
    0.239144, 0.245154, -0.939526, 0.0,    0.758731, -0.555871, 0.33961, 0.0,
    0.295355, 0.309513, 0.903862, 0.0,    0.0531222, -0.91003, -0.411124, 0.0,
    0.270452, 0.0229439, -0.96246, 0.0,    0.563634, 0.0324352, 0.825387, 0.0,
    0.156326, 0.147392, 0.976646, 0.0,    -0.0410141, 0.981824, 0.185309, 0.0,
    -0.385562, -0.576343, -0.720535, 0.0,    0.388281, 0.904441, 0.176702, 0.0,
    0.945561, -0.192859, -0.262146, 0.0,    0.844504, 0.520193, 0.127325, 0.0,
    0.0330893, 0.999121, -0.0257505, 0.0,    -0.592616, -0.482475, -0.644999, 0.0,
    0.539471, 0.631024, -0.557476, 0.0,    0.655851, -0.027319, -0.754396, 0.0,
    0.274465, 0.887659, 0.369772, 0.0,    -0.123419, 0.975177, -0.183842, 0.0,
    -0.223429, 0.708045, 0.66989, 0.0,    -0.908654, 0.196302, 0.368528, 0.0,
    -0.95759, -0.00863708, 0.288005, 0.0,    0.960535, 0.030592, 0.276472, 0.0,
    -0.413146, 0.907537, 0.0754161, 0.0,    -0.847992, 0.350849, -0.397259, 0.0,
    0.614736, 0.395841, 0.68221, 0.0,    -0.503504, -0.666128, -0.550234, 0.0,
    -0.268833, -0.738524, -0.618314, 0.0,    0.792737, -0.60001, -0.107502, 0.0,
    -0.637582, 0.508144, -0.579032, 0.0,    0.750105, 0.282165, -0.598101, 0.0,
    -0.351199, -0.392294, -0.850155, 0.0,    0.250126, -0.960993, -0.118025, 0.0,
    -0.732341, 0.680909, -0.0063274, 0.0,    -0.760674, -0.141009, 0.633634, 0.0,
    0.222823, -0.304012, 0.926243, 0.0,    0.209178, 0.505671, 0.836984, 0.0,
    0.757914, -0.56629, -0.323857, 0.0,    -0.782926, -0.339196, 0.52151, 0.0,
    -0.462952, 0.585565, 0.665424, 0.0,    0.61879, 0.194119, -0.761194, 0.0,
    0.741388, -0.276743, 0.611357, 0.0,    0.707571, 0.702621, 0.0752872, 0.0,
    0.156562, 0.819977, 0.550569, 0.0,    -0.793606, 0.440216, 0.42, 0.0,
    0.234547, 0.885309, -0.401517, 0.0,    0.132598, 0.80115, -0.58359, 0.0,
    -0.377899, -0.639179, 0.669808, 0.0,    -0.865993, -0.396465, 0.304748, 0.0,
    -0.624815, -0.44283, 0.643046, 0.0,    -0.485705, 0.825614, -0.287146, 0.0,
    -0.971788, 0.175535, 0.157529, 0.0,    -0.456027, 0.392629, 0.798675, 0.0,
    -0.0104443, 0.521623, -0.853112, 0.0,    -0.660575, -0.74519, 0.091282, 0.0,
    -0.0157698, -0.307475, -0.951425, 0.0,    -0.603467, -0.250192, 0.757121, 0.0,
    0.506876, 0.25006, 0.824952, 0.0,    0.255404, 0.966794, 0.00884498, 0.0,
    0.466764, -0.874228, -0.133625, 0.0,    0.475077, -0.0682351, -0.877295, 0.0,
    -0.224967, -0.938972, -0.260233, 0.0,    -0.377929, -0.814757, -0.439705, 0.0,
    -0.305847, 0.542333, -0.782517, 0.0,    0.26658, -0.902905, -0.337191, 0.0,
    0.0275773, 0.322158, -0.946284, 0.0,    0.0185422, 0.716349, 0.697496, 0.0,
    -0.20483, 0.978416, 0.0273371, 0.0,    -0.898276, 0.373969, 0.230752, 0.0,
    -0.00909378, 0.546594, 0.837349, 0.0,    0.6602, -0.751089, 0.000959236, 0.0,
    0.855301, -0.303056, 0.420259, 0.0,    0.797138, 0.0623013, -0.600574, 0.0,
    0.48947, -0.866813, 0.0951509, 0.0,    0.251142, 0.674531, 0.694216, 0.0,
    -0.578422, -0.737373, -0.348867, 0.0,    -0.254689, -0.514807, 0.818601, 0.0,
    0.374972, 0.761612, 0.528529, 0.0,    0.640303, -0.734271, -0.225517, 0.0,
    -0.638076, 0.285527, 0.715075, 0.0,    0.772956, -0.15984, -0.613995, 0.0,
    0.798217, -0.590628, 0.118356, 0.0,    -0.986276, -0.0578337, -0.154644, 0.0,
    -0.312988, -0.94549, 0.0899272, 0.0,    -0.497338, 0.178325, 0.849032, 0.0,
    -0.101136, -0.981014, 0.165477, 0.0,    -0.521688, 0.0553434, -0.851339, 0.0,
    -0.786182, -0.583814, 0.202678, 0.0,    -0.565191, 0.821858, -0.0714658, 0.0,
    0.437895, 0.152598, -0.885981, 0.0,    -0.92394, 0.353436, -0.14635, 0.0,
    0.212189, -0.815162, -0.538969, 0.0,    -0.859262, 0.143405, -0.491024, 0.0,
    0.991353, 0.112814, 0.0670273, 0.0,    0.0337884, -0.979891, -0.196654, 0.0
]

X_NOISE_GEN = 1619
Y_NOISE_GEN = 31337
Z_NOISE_GEN = 6971
SEED_NOISE_GEN = 1013
SHIFT_NOISE_GEN = 8


def value_noise_3d(x, y, z, seed):
    n = (
                X_NOISE_GEN * x +
                Y_NOISE_GEN * y +
                Z_NOISE_GEN * z +
                SEED_NOISE_GEN * seed
        ) & 0x7fffffff

    n = (n >> 13) ^ n
    res = (n * (n * n * 60493 + 19990303) + 1376312589) & 0x7fffffff
    return 1 - (res / 1073741824)


class Voronoi:
    """
    Noise module that outputs Voronoi cells.

    In mathematics, a **Voronoi cell** is a region containing all the
    points that are closer to a specific **seed point** than to any
    other seed point.  These cells mesh with one another, producing
    polygon-like formations.

    By default, this noise module randomly places a seed point within
    each unit cube.  By modifying the **frequency** of the seed points,
    an application can change the distance between seed points.  The
    higher the frequency, the closer together this noise module places
    the seed points, which reduces the size of the cells.  To specify the
    frequency of the cells, set the frequency parameter.

    This noise module assigns each Voronoi cell with a random constant
    value from a coherent-noise function.  The **displacement value**
    controls the range of random values to assign to each cell.  The
    range of random values is +/- the displacement value.  To specify the
    displacement value, set the displacement parameter.

    To modify the random positions of the seed points, set the seed parameter
    to something different.

    This noise module can optionally add the distance from the nearest
    seed to the output value.  To enable this feature, set enable_distance
    to True. This causes the points in the Voronoi cells
    to increase in value the further away that point is from the nearest
    seed point.

    Voronoi cells are often used to generate cracked-mud terrain
    formations or crystal-like textures

    This noise module requires no source modules.
    """
    def __init__(self, displacement=1, enable_distance=False, frequency=1, seed=0):
        self.displacement = displacement
        self.enable_distance = enable_distance
        self.frequency = frequency
        self.seed = seed

    def __getitem__(self, pos):
        x,y,z = pos
        x *= self.frequency
        y *= self.frequency
        z *= self.frequency

        x_int = int( x ) if (x > 0) else int( x ) - 1
        y_int = int( y ) if (y > 0) else int( y ) - 1
        z_int = int( z ) if (z > 0) else int( z ) - 1

        min_dist = 2147483647.0
        x_can = 0
        y_can = 0
        z_can = 0

        for z_cur in range( z_int - 2, z_int + 2 ):
            for y_cur in range( y_int - 2, y_int + 2 ):
                for x_cur in range( x_int - 2, x_int + 2 ):
                    x_pos = x_cur + value_noise_3d( x_cur, y_cur, z_cur, self.seed )
                    y_pos = y_cur + value_noise_3d( x_cur, y_cur, z_cur, self.seed + 1 )
                    z_pos = z_cur + value_noise_3d( x_cur, y_cur, z_cur, self.seed + 2 )

                    x_dist = x_pos - x
                    y_dist = y_pos - y
                    z_dist = z_pos - z
                    dist = x_dist * x_dist + y_dist * y_dist + z_dist * z_dist

                    if dist < min_dist:
                        min_dist = dist
                        x_can = x_pos
                        y_can = y_pos
                        z_can = z_pos
        value = 0

        if self.enable_distance:
            x_dist = x_can - x
            y_dist = y_can - y
            z_dist = z_can - z

            value = (math.sqrt(x_dist * x_dist + y_dist * y_dist + z_dist * z_dist)) *\
                math.sqrt(3) - 1

        return value + (self.displacement * value_noise_3d( math.floor( x_can ),
                                                            math.floor( y_can ),
                                                            math.floor( z_can ), 0 ))

# v = Voronoi()
# import time
# chk_a = time.time()
# for i in range(64*16):
#     a = v[(23.32,234.423,4324.33)]
# print(time.time()-chk_a)
