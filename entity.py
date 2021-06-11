import math
import pickle
import time
from typing import Tuple, Union

import pygame
import pygame.freetype

import chunk
import constants as consts
import game_utilities as utils

class ItemEntity:

    def __init__( self, _pos, _id, _entity_buffer ):
        """Initializes the ItemEntity object.

        Args:
            _pos (list): World position of the surface of the ItemEntity in x-y coordinate system. Also referred to as the position of the ItemEntity.
            _id (int): Type of the ItemEntity.
            _entity_buffer (EntityBuffer): Reference to the EntityBuffer object.
        """
        self.pos            = _pos
        self.get_pos        = lambda : self.pos

        self.id             = _id
        self.entity_buffer  = _entity_buffer

        self.get_texture    = lambda : consts.ITEM_TABLE[self.id]
        self.draw           = lambda : None

    def run( self, _dt ):
        pass

    def update( self, _dt ):
        pass

    def save( self ):
        """Converts the ItemEntity into a list of attributes to be saved.

        Returns:
            list: List of attributes to be saved.
        """
        return [ItemEntity, self.pos, self.id]


class Entity:

    def __init__( self, _pos, _entity_buffer, _inventory, _width, _height, _hitbox, _bottom_left, _range, _health = 100 ):
        """Initializes the Entity object.

        Args:
            _pos (list): World position of the Surface of the Entity. Also referred to as the position of the Entity.
            _entity_buffer (EntityBuffer): Reference to the EntityBuffer object.
            _inventory (Inventory): Reference to the Inventory object.
            _width (int): Width of the Entity's Surface.
            _height (int): Height of the Entity's Surface.
            _hitbox (list): Relative hitbox of the Entity.
            _bottom_left (Tuple[ int, int ]): Bottom left point of the Entity's hitbox.
            _health (int, optional): Health of the Entity. Defaults to 100.
        """
        self.pos                    = _pos
        self.get_pos                = lambda : self.pos

        self.entity_buffer          = _entity_buffer
        self.inventory              = _inventory

        self.health                 = _health
        self.range                  = _range

        self.friction               = consts.DEFAULT_FRICTION
        self.vel                    = [0.0, 0.0]
        self.acc                    = [0.0, 0.0]

        self.width                  = _width
        self.height                 = _height
        self.rel_hitbox             = _hitbox
        self.bottom_left            = _bottom_left

        self.grounded               = True
        self.tangibility            = False

        # In the following lambda functions, 'p' means position which is a tuple
        self.hitbox                 = lambda p: [(p[0]+i[0], p[1]+i[1]) for i in self.rel_hitbox]
        self.friction_point         = lambda p: [p[ 0 ] + self.bottom_left[ 0 ], p[ 1 ] + self.bottom_left[ 1 ]]
        self.tile                   = lambda p: self.entity_buffer.get_tile(p)

        self.held_item_index        = [0, 0]        # The index of the held item in the inventory (x, y)
        self.get_held_index         = lambda : self.held_item_index
        self.get_held_item          = lambda : self.inventory.items[self.held_item_index[1]][self.held_item_index[0]]
        self.get_held_quan          = lambda : self.inventory.quantities[self.held_item_index[1]][self.held_item_index[0]]

        self.sel_item               = [None, 0]    # The selected item and its quantity

        self.interaction_mode       = 1            # 0 for walls, 1 for tiles

        self.texture_strct          = TextureStructEntity( self.width, self.height )
        self.get_texture            = lambda : self.texture_strct.texture

    def change_interation( self ):
        self.interaction_mode = 1 - self.interaction_mode

    def move_held_hor( self, _amt = 1 ):
        self.held_item_index[0] = ( self.held_item_index[0] + _amt + consts.INV_COLS ) % consts.INV_COLS

    def move_held_to( self, _pos ):
        self.held_item_index[0] = _pos

    def move_held_ver( self, _amt = 1 ):
        self.held_item_index[1] = ( self.held_item_index[1] + _amt + consts.INV_ROWS ) % consts.INV_ROWS

    def eject_held_item( self, _pos = None ):
        pass

    def eject_sel_item( self, _pos, _quantity ):

        if self.sel_item[0] is None or self.sel_item[1] <= 0: return None

        x           = consts.get_x_pos_chunk( _pos )
        y           = consts.get_y_pos_chunk( _pos )

        ind         = consts.get_curr_chunk( _pos )
        pos         = x, y, ind

        for i in range( _quantity ):
            self.entity_buffer.add_item_entity( self.sel_item[0], pos )

        self.sel_item[1] -= _quantity
        if self.sel_item[1] <= 0:
            self.sel_item[0] = None

    def calc_friction( self ):
        """Updates the Entity's friction based on the tile in contact with
            the bottom left point in the entity's hitbox.
        """
        try:
            tile = self.tile( (self.friction_point(self.pos)[ 0 ], self.friction_point(self.pos)[ 1 ] - 1) )
            consts.dbg( 0, "IN CALC FRICTION - TILE:", tile )
            self.friction = consts.TILE_ATTR[ tile ][ consts.tile_attr.FRICTION ]
        except Exception as e:
            consts.dbg(0, "IN CALC FRICTION - EXCEPTION", e)
            self.friction = consts.AIR_FRICTION

    def move_left(self):
        self.acc[0] = -self.friction * 2

    def move_right(self):
        self.acc[0] = self.friction * 2

    def move_up( self ):
        self.acc[1] = self.friction * 2

    def move_down(self):
        self.acc[1] = -self.friction * 2

    def jump(self):
        self.vel[1]   = consts.JUMP_VEL
        self.acc[1]   = -consts.GRAVITY_ACC
        self.grounded = False

    def check_ground(self, _pos):
        """Checks whether the entity's bottom line of hitbox is touching a tile.

        Args:
            _pos (list): Position of the entity from which the hitbox is calculated.

        Returns:
            bool: True if the entity is touching a tile else False.
        """
        hitbox = self.hitbox(_pos)
        for point in hitbox:
            point2 = (point[0], point[1] - 1)
            if self.tile(point2) != consts.tiles.air:
                self.grounded = True
                return None
        self.grounded = False

    def check(self, _pos):
        """Checks whether the hitbox of the Entity collides with a tile.

        Args:
            _pos (list): Position of the entity from which the hitbox is computed.

        Returns:
            bool: True if the hitbox is colliding else False.
        """
        # For every corresponding tile between hitbox endpoints including the endpoints,
        # check that the hitbox and the tile don't intersect
        if self.tangibility:
            return True
        hitbox = self.hitbox( _pos )
        for point in hitbox:
            consts.dbg( 1, "IN CHECK - ENTERED FOR LOOP" )
            if self.tile(point) != consts.tiles.air:
                consts.dbg( 1, "CHECK RETURNED FALSE" )
                return False
        consts.dbg( 1, "CHECK RETURNED TRUE" )
        return True

    def left_click( self, _dt, _cursor_pos ):
        function = consts.l_use_hand
        which_item = self.get_held_item()
        if which_item:
            function = consts.ITEM_ATTR[which_item][consts.item_attr.L_USE]

        pos_x           = consts.get_x_pos_chunk(_cursor_pos)
        pos_y           = consts.get_y_pos_chunk(_cursor_pos)

        which_chunk     = consts.get_curr_chunk(_cursor_pos) - self.entity_buffer.chunk_buffer.get_start_chunk_ind()

        function( pos_x, pos_y, which_chunk, self.entity_buffer.chunk_buffer, self.entity_buffer, _dt )

    def right_click( self, _dt, _cursor_pos ):
        function = consts.r_use_hand
        which_item = self.get_held_item()
        if which_item:
            function = consts.ITEM_ATTR[which_item][consts.item_attr.R_USE]

        pos_x           = consts.get_x_pos_chunk(_cursor_pos)
        pos_y           = consts.get_y_pos_chunk(_cursor_pos)

        which_chunk     = consts.get_curr_chunk(_cursor_pos) - self.entity_buffer.chunk_buffer.get_start_chunk_ind()

        function( pos_x, pos_y, which_chunk, self.entity_buffer.chunk_buffer, self.entity_buffer, _dt )

    def hit( self ):
        pass

    def get_hit( self ):
        pass

    def pick( self ):
        items = self.entity_buffer.pick_item( self.pos.copy(), self.range )
        if items:
            consts.dbg(1, "ITEMS TO PICK:", items)
        for item in items: self.inventory.add_item(item.id, 1)

    def update( self, _dt ):
        """Updates the Entity's position, velocity and state.

        Args:
            _dt (float): Time passed between previous and current iteration.
        """
        self.pick()
        consts.dbg( 1, "IN ENTITY - ENTERING UPDATE" )
        dt2 = _dt
        _dt  = 1 / (consts.MAX_VEL * consts.SCALE_VEL)
        while dt2 > 0:
            if dt2 <= _dt:
                _dt  = dt2
                dt2 = 0
            else:
                dt2 -= _dt
            consts.dbg( 0, "IN UPDATE WHILE LOOP - AFTER CALCULATING - DT:", _dt )
            consts.dbg( 0, "IN UPDATE WHILE LOOP - AFTER CALCULATING - DT2:", dt2 )
            consts.dbg( 1, "INSIDE UPDATE WHILE LOOP" )
            self.calc_friction( )
            consts.dbg( 0, "IN UPDATE WHILE LOOP - AFTER CALCULATING - FRICTION:", self.friction )
            self.check_ground( self.pos )
            if consts.GRAVITY_ACC and (not self.grounded): self.acc[1] = -consts.GRAVITY_ACC
            consts.dbg( 0, "IN UPDATE - AT START - PLAYER VEL:", self.vel )
            consts.dbg( 0, "IN UPDATE - AT START - PLAYER ACC:", self.acc )
            for i in range( 0, 2 ):
                next_pos = self.pos.copy( )
                next_vel = self.vel[ i ] + self.acc[ i ] * _dt
                if next_vel >= abs( self.friction * _dt ):
                    self.vel[ i ] -= self.friction * _dt
                elif next_vel <= -abs( self.friction * _dt ):
                    self.vel[ i ] += self.friction * _dt
                else:
                    self.vel[ i ] = 0
                    self.acc[ i ] = 0

                    if self.acc[ i ] > consts.MAX_ACC * 2:
                        self.acc[ i ] = consts.MAX_ACC * 2
                    elif self.acc[ i ] < -consts.MAX_ACC * 2:
                        self.acc[ i ] = -consts.MAX_ACC * 2

                self.vel[ i ] += self.acc[ i ] * _dt
                if self.vel[ i ] < -consts.MAX_VEL * (1 - self.friction * 0.2):
                    self.vel[ i ] = -consts.MAX_VEL * (1 - self.friction * 0.2)
                elif self.vel[ i ] > consts.MAX_VEL * (1 - self.friction * 0.2):
                    self.vel[ i ] = consts.MAX_VEL * (1 - self.friction * 0.2)

                next_pos[ i ] += self.vel[ i ] * consts.SCALE_VEL * _dt
                move = self.check( next_pos )
                if move:
                    if (i == 0) or (i == 1 and consts.CHUNK_HEIGHT_P >= next_pos[ i ] >= 0):
                        self.pos[ i ] += self.vel[ i ] * consts.SCALE_VEL * _dt
                    if consts.CHUNK_HEIGHT_P < self.pos[ 1 ]:
                        self.pos[ 1 ] = consts.CHUNK_HEIGHT_P
                        consts.dbg( -1, "IN UPDATE WHILE LOOP - IN MOVE - POS > MAX HEIGHT" )
                    elif 0 > self.pos[ 1 ]:
                        self.pos[ 1 ] = 0
                        consts.dbg( -1, "IN UPDATE WHILE LOOP - IN MOVE - POS < MIN HEIGHT" )
                else:
                    self.vel[ i ] = 0
            if self.vel == [0, 0]: break


class Player(Entity):

    def __init__( self, _pos ):
        """Initializes the Player object.

        Args:
            _pos (list): World position of the surface of the Player in x-y coordinate system. Also referred to as the position of the Player.
        """

        # Set all references to main managers
        self.chunk_buffer: Union[ None, chunk.ChunkBuffer ] = None
        self.entity_buffer: Union[ None, EntityBuffer ]     = None
        self.renderer: Union[ None, utils.Renderer ]        = None
        self.serializer: Union[None , utils.Serializer]     = None
        self.camera: Union[None, list]                      = None

        self.key_state: Union[None, dict]      = None
        self.mouse_state: Union[None, dict]    = None
        self.cursor_pos: Union[None, list]     = None
        self.inventory: Union[None, Inventory] = None

        self.tangibility   = False
        x_off              = 0
        y_off              = 0
        self.up            = [ (x + x_off, y_off) for x in range( 0, consts.PLYR_HITBOX_WIDTH - 1, 16 ) ] + [ (consts.PLYR_HITBOX_WIDTH - 1 + x_off, y_off) ]
        self.left          = [ (x_off, -y + y_off) for y in range( 0, consts.PLYR_HITBOX_HEIGHT - 1, 16 ) ] + [ (x_off, -consts.PLYR_HITBOX_HEIGHT + 1 + y_off) ]
        self.right         = [ (consts.PLYR_HITBOX_WIDTH - 1 + x_off, -y + y_off) for y in range( 0, consts.PLYR_HITBOX_HEIGHT - 1, 16 ) ] + [ (consts.PLYR_HITBOX_WIDTH - 1 + x_off, -consts.PLYR_HITBOX_HEIGHT + 1 + y_off) ]
        self.bottom        = [ (x + x_off, -consts.PLYR_HITBOX_HEIGHT + 1 + y_off) for x in range( 0, consts.PLYR_HITBOX_WIDTH - 1, 16 ) ] + [ (consts.PLYR_HITBOX_WIDTH - 1 + x_off, -consts.PLYR_HITBOX_HEIGHT + 1 + y_off) ]
        self.rel_hitbox    = self.up + self.right + self.bottom + self.left
        self.bottom_left   = self.bottom[0]
        self.range         = consts.PLYR_RANGE
        self.pos           = _pos  # World pos of surface in x-y-z coords
        # self.hitbox        = [(0, 0), (PLYR_HITBOX_WIDTH, 0), (PLYR_HITBOX_WIDTH, -PLYR_HITBOX_HEIGHT), (0, -PLYR_HITBOX_HEIGHT)]

    def initialize( self, _chunk_buffer, _entity_buffer, _renderer, _serializer, _key_state, _mouse_state, _cursor_pos, _mouse_pos ):
        """Passes all the required references to the Player

        Args:
            _chunk_buffer (chunk.ChunkBuffer): Reference to the ChunkBuffer object
            _entity_buffer ([type]): Reference to the EntityBuffer object
            _renderer (utils.Renderer): Reference to the Renderer object
            _serializer (utils.Serializer): Reference to the Serializer object
            _key_state (dict): Reference to the dictionary containing the state of the keys
            _mouse_state (dict): Reference to the dictionary containing the state of the mouse buttons
            _cursor_pos (list): Reference to the position of the cursor
        """

        # Set all references to main managers
        self.chunk_buffer  = _chunk_buffer
        self.entity_buffer = _entity_buffer
        self.renderer      = _renderer
        self.serializer    = _serializer

        self.key_state     = _key_state
        self.mouse_state   = _mouse_state
        self.cursor_pos    = _cursor_pos
        self.mouse_pos      = _mouse_pos

        self.tangibility   = False
        self.inventory     = Inventory( consts.INV_COLS, consts.INV_ROWS )

        self.load()
        super().__init__( self.pos, self.entity_buffer, self.inventory, consts.PLYR_WIDTH, consts.PLYR_HEIGHT, self.rel_hitbox, self.bottom_left, self.range )

        self.inventory.held_item_index = self.held_item_index

    def run( self, _dt ):
        """Updates the Player's variables to handle the user's input.

        Args:
            _dt (float): Time passed between previous and current iteration.
        """
        self.acc[ 0 ] = 0
        self.acc[ 1 ] = 0
        self.hitting  = False
        self.placing  = False
        if self.key_state[ pygame.K_a ] and not self.key_state[ pygame.K_d ]:
            consts.dbg( 1, "IN RUN - MOVING LEFT" )
            self.move_left( )
            self.texture_strct.run_left( _dt )
        elif self.key_state[ pygame.K_d ] and not self.key_state[ pygame.K_a ]:
            consts.dbg( 1, "IN RUN - MOVING RIGHT" )
            self.move_right( )
            self.texture_strct.run_right( _dt )
        else:
            self.texture_strct.run_static()

        if self.key_state[ pygame.K_s ] and not self.key_state[ pygame.K_w ]:
            consts.dbg( 1, "IN RUN - MOVING DOWN" )
            self.move_down( )
        elif (self.tangibility or self.grounded) and self.key_state[ pygame.K_w ] and not self.key_state[ pygame.K_s ]:
            consts.dbg( 1, "IN RUN - MOVING UP" )
            self.jump( )

        if self.mouse_state[ pygame.BUTTON_LEFT ]:
            consts.dbg( 1, "IN RUN - LEFT MOUSE BUTTON PRESSED")
            self.left_click( _dt, self.cursor_pos )

        if self.mouse_state[ pygame.BUTTON_RIGHT ]:
            consts.dbg( 1, "IN RUN - RIGHT MOUSE BUTTON PRESSED")
            self.right_click( _dt, self.cursor_pos )

    def left_click( self, _dt, _cursor_pos ):

        if self.inventory.enabled:
            max_down    = 40 * self.inventory.rows
            max_right   = 40 * self.inventory.cols

            if self.mouse_pos[0] < max_right and  self.mouse_pos[1] < max_down:
                curr_row    = round( self.mouse_pos[1] / 40 ) - 1
                curr_col    = round( self.mouse_pos[0] / 40 ) - 1

                if curr_row >= 0 and curr_col >= 0 and self.sel_item[0] is not None:
                    if self.inventory.get_item_at( [curr_col, curr_row] ) == None:
                        self.inventory.items[curr_row][curr_col] = self.sel_item[0]

                    if self.sel_item[0] == self.inventory.get_item_at( [curr_col, curr_row] ):
                        to_rem = 1
                        if self.key_state[pygame.KMOD_CTRL]:
                            to_rem              = self.sel_item[1]

                        # max_val = consts.ITEM_ATTR[self.sel_item[0]][consts.item_attr.MAX_STACK]
                        max_val = 64
                        to_rem = min( to_rem, max_val - self.inventory.get_quantity_at( [curr_col, curr_row] ) )
                        self.inventory.quantities[curr_row][curr_col] += to_rem
                        self.sel_item[1] -= to_rem

                        if self.sel_item[1] == 0: self.sel_item[0] = None

            elif self.sel_item[0] is not None:
                quantity    = 1
                if self.key_state[pygame.KMOD_CTRL]:
                    quantity = self.sel_item[1]

                pos         = list( map( int, self.cursor_pos ) )
                pos[1]      +=consts.TILE_WIDTH

                self.eject_sel_item( pos, quantity )

        else:
            function = consts.l_use_hand
            which_item = self.get_held_item()
            if which_item:
                function = consts.ITEM_ATTR[which_item][consts.item_attr.L_USE]

            pos_x           = consts.get_x_pos_chunk(_cursor_pos)
            pos_y           = consts.get_y_pos_chunk(_cursor_pos)

            which_chunk     = consts.get_curr_chunk(_cursor_pos) - self.entity_buffer.chunk_buffer.get_start_chunk_ind()

            function( pos_x, pos_y, which_chunk, self.entity_buffer.chunk_buffer, self.entity_buffer, _dt )

    def right_click( self, _dt, _cursor_pos ):

        if self.inventory.enabled:
            max_down    = 40 * self.inventory.rows
            max_right   = 40 * self.inventory.cols

            if self.mouse_pos[0] < max_right and  self.mouse_pos[1] < max_down:
                curr_row    = round( self.mouse_pos[1] / 40 ) - 1
                curr_col    = round( self.mouse_pos[0] / 40 ) - 1

                which_item  = self.inventory.get_item_at( [curr_col, curr_row] )

                if curr_row >= 0 and curr_col >= 0 and which_item is not None:

                    if self.sel_item[0] == None:
                        self.sel_item[0]    = which_item

                    if self.sel_item[0] == self.inventory.get_item_at( [curr_col, curr_row] ):
                        # if self.sel_item[1] < consts.ITEM_ATTR[which_item][consts.item_attr.MAX_STACK]:
                        to_add = 1
                        if self.key_state[pygame.KMOD_CTRL]:
                            to_add              = self.inventory.get_quantity_at( [curr_col, curr_row] )

                        self.sel_item[1]    += to_add
                        self.inventory.rem_item_pos( [curr_col, curr_row], to_add )

        else:
            function = consts.r_use_hand
            which_item = self.get_held_item()
            if which_item:
                function = consts.ITEM_ATTR[which_item][consts.item_attr.R_USE]

            pos_x           = consts.get_x_pos_chunk(_cursor_pos)
            pos_y           = consts.get_y_pos_chunk(_cursor_pos)

            which_chunk     = consts.get_curr_chunk(_cursor_pos) - self.entity_buffer.chunk_buffer.get_start_chunk_ind()

            function( pos_x, pos_y, which_chunk, self.entity_buffer.chunk_buffer, self.entity_buffer, _dt )

    def save( self ):
        """Saves the Player's attributes in the database.
        """
        li = [self.inventory.items, self.inventory.quantities, self.inventory.local_item_table, self.pos]
        li = pickle.dumps( li )
        self.serializer.save_player( 1, li )

    def load( self ):
        """Gets the Player's attributes from the database.
        """
        li = self.serializer.load_player( 1 )
        if li:
            li                              = pickle.loads( li )
            self.inventory.items            = li[0]
            self.inventory.quantities       = li[1]
            self.inventory.local_item_table = li[2]
            self.pos = li[3]

    def end( self ):
        pass


class Projectile(Entity):

    def __init__( self, _pos, _entity_buffer, _width, _height ):
        self.pos = _pos
        self.width  = _width
        self.height = _height
        self.rel_hitbox = [ ]
        self.rel_hitbox_calc = [ [_point[0]*math.cos(self.angle) - _point[1]*math.sin(self.angle), _point[0]*math.sin(self.angle) + _point[1]*math.cos(self.angle)] for _point in self.rel_hitbox ]
        self.angle = 0.0
        self.rotation_point = [ ]
        self.vel = []
        self.acc = []
        super( ).__init__( _pos, _entity_buffer, _width, _height, self.hitbox )
        pass

    def update( self , _dt):
        self.vel[1] = self.vel[1] - consts.GRAVITY_ACC * _dt
        self.angle = math.atan( self.vel[1]/self.vel[0] )
        pass


class Slime(Entity):
    def __init__( self, _pos, _entity_buffer ):
        self.pos = _pos
        self.entity_buffer = _entity_buffer
        self.width  = consts.PLYR_WIDTH
        self.height = consts.PLYR_HEIGHT
        x_off = 0
        y_off = 0
        self.cooldown = 2
        self.HITBOX_WIDTH = 30
        self.HITBOX_HEIGHT = 18
        self.range = 3 * consts.TILE_WIDTH
        self.up = [ (x + x_off, y_off) for x in range( 0, self.HITBOX_WIDTH - 1, 16 ) ] + [ (self.HITBOX_WIDTH - 1 + x_off, y_off) ]
        self.left = [ (x_off, -y + y_off) for y in range( 0, self.HITBOX_HEIGHT - 1, 16 ) ] + [ (x_off, -self.HITBOX_HEIGHT + 1 + y_off) ]
        self.right = [ (self.HITBOX_WIDTH - 1 + x_off, -y + y_off) for y in range( 0, self.HITBOX_HEIGHT - 1, 16 ) ] + [ (self.HITBOX_WIDTH - 1 + x_off, -self.HITBOX_HEIGHT + 1 + y_off) ]
        self.bottom = [ (x + x_off, -self.HITBOX_HEIGHT + 1 + y_off) for x in range( 0, self.HITBOX_WIDTH - 1, 16 ) ] + [ (self.HITBOX_WIDTH - 1 + x_off, -self.HITBOX_HEIGHT + 1 + y_off) ]
        self.rel_hitbox = self.up + self.right + self.bottom + self.left
        self.bottom_left = self.bottom[ 0 ]
        self.inventory = Inventory( 1, 1 )
        super( ).__init__( self.pos, self.entity_buffer, self.inventory, self.width, self.height, self.rel_hitbox, self.bottom_left, self.range )
        self.get_texture = lambda : consts.slime

    def run( self, _dt ):
        self.acc = [0, 0]
        player_pos = self.entity_buffer.player.pos
        if self.grounded:
            self.vel = [0, 0]
            self.cooldown = max(0, self.cooldown - _dt)
            if not self.cooldown:
                consts.dbg(1, "IN RUN - SLIME TOUCHED GROUND")
                # self.vel = [0, 0]
                self.jump()
                self.cooldown = 2
        else:
            if not self.grounded:
                if player_pos[0] > self.pos[0]:
                    consts.dbg( 1, "SLIME - IN RUN - MOVING RIGHT" )
                    self.vel[0] = 0.5
                elif player_pos[0] < self.pos[0]:
                    consts.dbg( 1, "SLIME - IN RUN - MOVING LEFT" )
                    self.vel[0] = -0.5

    def save(self):
        return [Slime, self.pos]


class Zombie(Entity):
    def __init__( self, _pos, _entity_buffer ):
        self.width  = 10
        self.height = 10
        self.hitbox = [ ]
        super( ).__init__( _pos, _entity_buffer, self.width, self.height, self.hitbox)
        pass

    def run( self ):
        pass

    def update( self ):
        pass


class EntityBuffer:

    def __init__( self ):
        """Initializes the EntityBuffer object.
        """

        # References to other managers (must be provided in main)
        self.chunk_buffer       = None
        self.player             = None
        self.renderer           = None
        self.serializer         = None
        self.player             = None

        # Reference to camera and screen surface
        self.camera             = None
        self.screen             = None

        self.entities           = []
        self.other_plyrs        = []
        self.len                = None

        self.get_curr_chunk_ind = lambda p: int( consts.get_curr_chunk( p ) - self.chunk_buffer.get_start_chunk_ind() )
        # self.get_tile           = lambda p: self.chunk_buffer.chunks[self.get_curr_chunk_ind( p )].blocks[consts.get_y_pos_chunk( p )][consts.get_x_pos_chunk( p )]

    def get_tile( self, p ):
        curr_chunk_ind = self.get_curr_chunk_ind( p )
        curr_chunk = self.chunk_buffer.chunks[ curr_chunk_ind ]
        tiles_at_y_pos = curr_chunk.blocks[ consts.get_y_pos_chunk( p ) ]
        tile = tiles_at_y_pos[ consts.get_x_pos_chunk( p ) ]
        return tile

    def initialize( self , _chunk_buffer, _renderer, _serializer, _player, _camera, _screen ):
        """Passes all the required references to the EntityBuffer object.

        Args:
            _chunk_buffer (chunk.ChunkBuffer): Reference to the ChunkBuffer object.
            _renderer (utils.Renderer): Reference to the Renderer object.
            _serializer (utils.Serializer): Reference to the Serializer object.
            _player (Player): Reference to the Player object.
            _camera (list): Reference to the camera.
            _screen (pygame.Surface): Reference to the screen.
        """

        # Set all references to main managers
        self.chunk_buffer = _chunk_buffer
        self.player       = _player
        self.renderer     = _renderer
        self.serializer   = _serializer
        self.camera       = _camera
        self.screen       = _screen

        self.len          = self.chunk_buffer.len
        self.entities     = [ self.load( self.chunk_buffer.get_start_chunk_ind() + i ) for i in range( self.len ) ]

    def add_player( self ):
        # To be implemented in multiplayer
        pass

    def add_entity( self, _entity ):
        """Adds the given Entity or ItemEntity to the EntityBuffer's entity list.

        Args:
            _entity (Entity | ItemEntity): Entity or ItemEntity object to be added.
            _ind (int): Index at which the Entity or ItemEntity is to be added.
        """
        _ind = self.get_curr_chunk_ind(_entity.get_pos().copy())
        consts.dbg(1, "ADD ENTITY INDEX:", _ind)
        self.entities[_ind].append(_entity)

    def add_item_entity( self, _id, _pos ):
        """Adds the given ItemEntity to the EntityBuffer's entity list.

        Args:
            _id (int): The type of the ItemEntity to be added.
            _pos (list): The position including the index at which the ItemEntity is to be added.
        """
        x, y, ind = _pos
        x += consts.CHUNK_WIDTH * ind

        x *= consts.TILE_WIDTH
        y *= consts.TILE_WIDTH

        ind -= self.chunk_buffer.get_start_chunk_ind()

        pos = [x, y]

        item_entity = ItemEntity( pos, _id, self )
        self.add_entity( item_entity )

    def load_player( self ):
        pass

    def save_player( self ):
        pass

    def save( self, _entities, _index ):
        """Saves the given list of entities in the database at the given index.

        Args:
            _entities (list): List of entities to be saved.
            _index (int): Index of database at which the entities are to be saved.
        """
        raw_entities = [ ]
        for entity in _entities:
            raw_entities.append( entity.save( ) )
        pickled_raw_entities = pickle.dumps( raw_entities )
        self.serializer.set_entity( _index, pickled_raw_entities )

    def load( self, _index ):
        """Loads the list of entities from the database at the given index.

        Args:
            _index (int): Index of database from which the entities are to be loaded.

        Returns:
            list: List of entities loaded from the database.
        """
        entities = [ ]
        pickled_raw_entities = self.serializer.get_entity( _index )
        if pickled_raw_entities:
            raw_entities = pickle.loads( pickled_raw_entities )
            for entity in raw_entities:
                entity_obj = entity[0](*entity[1::], self)
                entities.append( entity_obj )
        return entities

    def save_complete( self ):
        """Saves the complete EntityBuffer's list of entities in the database.
        """
        for i in range(self.len):
            self.save(self.entities[i], self.chunk_buffer.get_start_chunk_ind() + i)

    def hit( self ):
        pass

    def pick_item( self, _pos, _range ):
        items = []
        for index in range( self.len - 1, -1, -1 ):
            for entity_ind in range( len( self.entities[ index ] ) - 1, -1, -1 ):
                entity = self.entities[ index ][ entity_ind ]
                if (isinstance( entity, ItemEntity )) and (consts.dist_between_points( entity.pos, _pos ) <= _range):
                    items.append( entity )
                    consts.dbg(1, "ENTITY BUFFER BEFORE PICK ITEM:", self.entities)
                    self.entities[ index ].pop( entity_ind )
        return items

    def item_in_range( self, _pos, _range ):
        pass

    def entity_in_range( self ):
        pass

    def update_ind( self, _entity, _new_index ):
        pass

    def update( self, _dt ):
        update_index_entities = []
        index = 0
        entities_copy = [self.entities[_ind].copy() for _ind in range(self.len)]
        while index < self.len:
            entity_ind = 0
            while entity_ind < len( entities_copy[index] ):
                entity = entities_copy[ index ][ entity_ind ]
                prev_entity_ind = entity_ind
                entity_ind += 1
                if entity not in self.entities[ index ]:
                    continue

                # prev_entity_pos = entity.get_pos( ).copy( )
                chk_a = time.time()
                entity.run( _dt )
                entity.update( _dt )
                consts.dbg(1, "ENTITY UPDATE TIME TAKEN(in milliseconds):", (time.time()-chk_a)*1000)
                new_index = self.get_curr_chunk_ind(entity.get_pos())
                if new_index != prev_entity_ind:
                    self.entities[ index ].remove( entity )
                    update_index_entities.append( entity )
            index += 1

        for entity in update_index_entities:
            consts.dbg(1, "UPDATE ENTITY INDEX:", update_index_entities)
            index = self.get_curr_chunk_ind(entity.get_pos())
            consts.dbg(1, "NEW INDEX OF ENTITY:", index)
            self.entities[index].append(entity)

    def draw( self ):
        pass

    def shift( self, _delta_chunk ):
        """Updates the EntityBuffer's list of entities based on the player's movement.

        Args:
            _delta_chunk (int): Number of chunks the Player crossed after the previous iteration.
        """
        prev_entities = self.entities.copy()
        if _delta_chunk > 0:
            for i in range( _delta_chunk ):
                self.entities.append(self.load(self.chunk_buffer.get_end_chunk_ind() + i + 1))
                self.save(self.entities[i], self.chunk_buffer.get_start_chunk_ind() + i)
                self.entities.pop(0)
        else:
            for i in range( abs( _delta_chunk ) ):
                self.entities.insert(i, self.load( self.chunk_buffer.get_start_chunk_ind() - i - 1))
                self.save(self.entities[-i-1], self.chunk_buffer.get_end_chunk_ind() - i)
                self.entities.pop(-1)
        if self.entities != prev_entities:
            consts.dbg(1, "ENTITY BUFFER - END OF SHIFT - ENTITIES LIST:", self.entities)


class Inventory:

    def __init__( self , _cols , _rows ):

        # ! Magic numbers are being used here

        self.items              = [ [ None for j in range( _cols ) ] for i in range( _rows ) ]
        self.quantities         = [ [ 0 for j in range( _cols ) ] for i in range( _rows ) ]

        self.positions          = {}
        self.local_item_table   = []

        self.held_item_index    = [0, 0]

        self.cols               = _cols
        self.rows               = _rows

        self.surf               = pygame.Surface( (800 , 500), flags = pygame.SRCALPHA )

        self.enabled            = False

    def add_item( self, _item , _quantity ):
        """ Adds the supplied item to the inventory the supplied number of items homogeneously
            Priority is given to the slots which already contain the specified item
            The amount left over is returned

        Args:
            _item (int): The ID of the item to be added
            _quantity (int): The quantity of the item to be added

        Returns:
            int: The number of items left over at the end
        """

        empty_slots = []

        for y in range( self.rows ):

            for x in range( self.cols ):

                if self.quantities[y][x] == 0: empty_slots.append( [ x , y ] )

                if self.items[y][x] == _item and self.quantities[y][x] < 64:
                    max_fit = min( _quantity, 64 - self.quantities[y][x] )
                    self.quantities[y][x] += max_fit
                    _quantity -= max_fit
                    if _quantity == 0: return None

        if _quantity:

            num_slots = min( len( empty_slots ) , ( _quantity >> 6 ) )
            _quantity -= ( num_slots << 6 )

            for i in range( num_slots ):
                x , y = empty_slots[i]
                self.items[y][x]        = _item
                self.quantities[y][x]   = 64

            if _quantity:
                if len( empty_slots ) <= num_slots: return _quantity
                x , y = empty_slots[num_slots]
                self.items[y][x]        = _item
                self.quantities[y][x]   = _quantity

        return _quantity

    def rem_item_stack( self , _item , _quantity ):
        """ Removes the supplied number of occurrences of the supplied item from the inventory from all around
            If the supplied count exceeds the total count, then only the total count is removed
            The number of items which could successfully be removed are returned

        Args:
            _item (int): The item which is to be removed
            _quantity (int): The quantity of the item to be removed

        Returns:
            int: The number of items which could successfully be removed
        """

        for x in range( self.cols ):
            for y in range( self.rows ):

                if self.items[y][x] != _item: continue

                to_remove               = min( self.quantities[y][x] , _quantity )
                self.quantities[y][x]   -= to_remove
                _quantity               -= to_remove

                if self.quantities[y][x] <= 0: self.items[y][x] = None
                if _quantity <= 0: return True

        return _quantity

    def rem_item_pos( self, _pos, _quantity = 1 ):
        """ Removes a given quantity of items from a given position
            If the supplied quantity is equal to/exceeds the present quantity, only the present quantity is removed
            The number of items which could successfully be removed are returned

        Args:
            _quantity (int): The number of items to be removed
            _pos (list): The position from which to remove the given quantity (in column , row  format)

        Returns:
            int: The count of the items which were successfully removed
        """

        to_remove = min( self.quantities[_pos[1]][_pos[0]] , _quantity )
        self.quantities[_pos[1]][_pos[0]] -= to_remove

        if self.quantities[_pos[1]][_pos[0]] <= 0: self.items[_pos[1]][_pos[0]] = None

        return to_remove

    def draw( self ):
        """ Draws the Inventory on to its own surface
        """

        self.surf.fill( ( 0 , 0 , 0 , 0 ), [ 0 , 0 , 800 , 500 ])
        coors   = [ 0 , 0 ]

        for x , coors[0] in enumerate( range( 0 , 40 * self.cols , 40 ) ):

            for y , coors[1] in enumerate( range( 0 , 40 * self.rows , 40 ) ):

                self.surf.blit( consts.inventory_slot, coors )

                if self.quantities[y][x]:

                    quantity_text , quantity_rect = consts.INV_FONT.render( str( self.quantities[y ][x ] ), consts.INV_COLOR )
                    self.surf.blit( consts.ITEM_TABLE[self.items[y][x] ], (coors[0] + 4 , coors[1] + 4) )
                    self.surf.blit( quantity_text , ( coors[0] , coors[1] ) )

    def draw_top( self ):

        self.surf.fill( ( 0 , 0 , 0 , 0 ), [ 0 , 0 , 800 , 500 ])
        coors   = [ 0 , 0 ]
        y = 0

        for x , coors[0] in enumerate( range( 0 , 40 * self.cols , 40 ) ):

            if self.held_item_index[0] == x:
                self.surf.blit( consts.selected_slot, coors )
            else:
                self.surf.blit( consts.inventory_slot, coors )

            if self.quantities[y][x]:
                quantity_text , quantity_rect = consts.INV_FONT.render( str( self.quantities[y ][x ] ), consts.INV_COLOR )
                self.surf.blit( consts.ITEM_TABLE[self.items[y ][x ] ], (coors[0 ] + 4 , coors[1 ] + 4) )
                self.surf.blit( quantity_text , ( coors[0] , coors[1] ) )

    def get_texture( self ):
        return self.surf

    def get_item_at( self, _pos ):
        return self.items[_pos[1]][_pos[0]]

    def get_quantity_at( self, _pos ):
        return self.quantities[_pos[1]][_pos[0]]


# Structure to hold all textures of an entity and to abstract animation
class TextureStructEntity:

    def __init__( self, _width, _height ):
        # 0 is during static
        # every third of a second we need to move onto the next texture

        self.running_index = 0
        self.frames = len( consts.player_running ) >> 1
        self.center_index = self.frames

        self.texture = consts.player_running[self.center_index]

    def run_right( self, _dt ):
        self.running_index += _dt * 3
        if self.running_index > self.frames: self.running_index = 0
        self.texture = consts.player_running[self.center_index + int( self.running_index ) + 1]

    def run_left( self, _dt ):
        self.running_index += _dt * 3
        if self.running_index > self.frames: self.running_index = 0
        self.texture = consts.player_running[self.center_index - int( self.running_index ) - 1]

    def run_static( self ):
        self.texture = consts.player_running[self.center_index]
        self.running_index = 0
