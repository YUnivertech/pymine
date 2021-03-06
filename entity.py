# from shapely.geometry import Polygon
from game_utilities import *

# ! def initialize( self , _renderer , _chunk_buffer , _serializer , _player , _camera , _screen ):

# !    self.renderer       = _renderer
# !    self.chunk_buffer   = _chunk_buffer
# !    self.serializer     = _serializer
# !    self.player         = _player
# !    self.camera         = _camera
# !    self.screen         = _screen


class ItemEntity:
    def __init__( self ):
        pass

    def draw( self ):
        pass


class Entity:
    def __init__(self, _pos, _entity_buffer, _width, _height, _hitbox, _health=100):
        self.pos          = _pos
        self.entity_buffer = _entity_buffer
        self.health       = _health
        self.friction     = DEFAULT_FRICTION
        self.vel          = [0.0, 0.0]
        self.acc          = [0.0, 0.0]
        self.width        = _width
        self.height       = _height
        self.rel_hitbox   = _hitbox
        self.surf         = pygame.Surface((self.width, self.height))
        self.surf_pos     = lambda: [self.pos[0] - (PLYR_WIDTH * 0.5), self.pos[1] + (PLYR_HEIGHT * 0.5)]
        self.hitting      = False
        self.placing      = False

        # In the following lambda functions, 'p' means position which is a tuple
        self.hitbox         = lambda p: [p+i for i in self.rel_hitbox]
        self.tile           = lambda p: self.entity_buffer.get_tile(p)

    def collide( self, p1, p2 ):
        return False

    def calc_friction(self):
        return TILE_ATTR[self.tile((self.pos[0], self.pos[1] - 16))][tile_attr.FRICTION]

    def move_left(self):
        self.acc[0] = -self.friction * 2

    def move_right(self):
        self.acc[0] = self.friction * 2

    def move_down(self):
        pass

    def jump(self):
        self.vel[1] = JUMP_VEL
        self.acc[1] = -GRAVITY_ACC
        self.grounded = False

    def check_up(self, pos):
        pass

    def check_left(self, pos):
        pass

    def check_right(self, pos):
        pass

    def check_ground(self, pos):
        pass

    def check(self, pos):
        # For every corresponding tile between hitbox endpoints including the endpoints,
        # check that the hitbox and the tile don't intersect
        hitbox = self.hitbox( pos )
        for point in hitbox:
            if self.collide( self.tile( point ), hitbox ):
                return False
        return True

    def hit( self ):
        pass

    def get_hit( self ):
        pass


class Player(Entity):

    def __init__( self, _screen, _chunk_buffer, _entity_buffer, key_state, mouse_state, cursor_pos):
        hitbox = []
        pos = [0,0]
        super().__init__(pos, _entity_buffer, PLYR_WIDTH, PLYR_HEIGHT, hitbox)

        self.keyState = key_state
        self.mouseState = mouse_state
        self.cursorPos = cursor_pos
        self.inventory = Inventory(_screen, INV_COLS, INV_ROWS)
        self.tangibility = 0

    def run( self ):
        self.acc[0] = 0
        self.acc[1] = 0
        self.hitting = False
        self.placing = False
        if self.keyState[pygame.K_a] and not self.keyState[pygame.K_d]:
            self.move_left( )
        elif self.keyState[pygame.K_d] and not self.keyState[pygame.K_a]:
            self.move_right( )

        if self.keyState[pygame.K_s] and not self.keyState[pygame.K_w]:
            self.move_down( )
        elif self.grounded and self.keyState[pygame.K_w] and not self.keyState[pygame.K_s]:
            self.jump()

        if self.keyState[pygame.K_e]:
            self.inventory.isEnabled = not self.inventory.isEnabled
            self.keyState[pygame.K_e] = False

    def update( self, dt ):
        dt2 = dt
        dt = 16 / (MAX_VEL * SCALE_VEL)
        while dt2 > 0:
            if dt2 <= dt:
                dt = dt2
                dt2 = 0
            if self.vel == [0, 0]: break
            dt2 -= dt
            self.calc_friction( )
            # self.check_ground( self.pos )
            # if not self.grounded: self.acc[1] = -GRAVITY_ACC
            for i in range( 0, 2 ):
                next_pos = self.pos.copy( )
                next_vel = self.vel[i] + self.acc[i] * dt
                if next_vel >= abs( self.friction * dt ):
                    self.vel[i] -= self.friction * dt
                elif next_vel <= -abs( self.friction * dt ):
                    self.vel[i] += self.friction * dt
                else:
                    self.vel[i] = 0
                    self.acc[i] = 0

                self.acc[i] = MAX_ACC * 2 if (self.acc[i] > MAX_ACC * 2) else -MAX_ACC * 2

                self.vel[i] += self.acc[i] * dt
                if self.vel[i] < -MAX_VEL * (1 - self.friction * 0.2):
                    self.vel[i] = -MAX_VEL * (1 - self.friction * 0.2)
                elif self.vel[i] > MAX_VEL * (1 - self.friction * 0.2):
                    self.vel[i] = MAX_VEL * (1 - self.friction * 0.2)

                next_pos[i] += self.vel[i] * SCALE_VEL * dt
                move = self.check( next_pos )
                if move:
                    self.pos[i] += self.vel[i] * SCALE_VEL * dt
                else:
                    self.vel[i] = 0

        # if self.hitting and not self.placing :
        #     chunk = math.floor(self.cursorPos[0] / CHUNK_WIDTH_P)
        #     chunkInd = chunk - self.chunk_buffer.positions[0]
        #     x = (self.cursorPos[0] // TILE_WIDTH) - chunk * CHUNK_WIDTH
        #     y = (self.cursorPos[1] // TILE_WIDTH)
        #     block = self.chunk_buffer[ chunkInd][ y][ x]
        #     state = self.chunk_buffer[ chunkInd].breakBlockAt( x, y, 10, dt )
        #     self.eventHandler.tileBreakFlag = True
        #     self.eventHandler.tileBreakIndex = chunkInd
        #     self.eventHandler.tileBreakPos[0] = x
        #     self.eventHandler.tileBreakPos[1] = y
        #     if state:   # The block was broken
        #         self.entity_buffer.addItem( block, self.cursorPos.copy( ), chunkInd )
        #
        # elif self.placing:
        #     chunk = math.floor(self.cursorPos[0] / CHUNK_WIDTH_P)
        #     chunkInd = chunk - self.chunk_buffer.positions[0]
        #     x = (self.cursorPos[0] // TILE_WIDTH) - chunk * CHUNK_WIDTH
        #     y = (self.cursorPos[1] // TILE_WIDTH)
        #     toPlace = self.inventory.getSelectedItem()
        #     dist = math.sqrt(pow(self.pos[0]-self.cursorPos[0], 2)+pow(self.pos[1]-self.cursorPos[1], 2))
        #     if toPlace and dist > PLYR_HEIGHT:
        #         res = self.chunk_buffer[chunkInd].placeBlockAt( x, y, toPlace )
        #         if res: self.inventory.remItemPos( 1, self.inventory.itemHeld )
        #
        #     self.eventHandler.tilePlaceFlag = True
        #     self.eventHandler.tilePlaceIndex = chunkInd
        #     self.eventHandler.tilePlacePos[0] = x
        #     self.eventHandler.tilePlacePos[1] = y

    def pick( self ):
        l = self.entity_buffer.pickItem( )
        for item in l: self.inventory.addItem(item, 1)

    def save( self, serializer ):
        li = [self.inventory.items, self.inventory.quantities]
        li = pickle.dumps(li)
        serializer.savePlayer(1, li)

    def load( self, serializer):
        li = serializer.loadPlayer(1)
        if li:
            li = pickle.loads(li)
            self.inventory.items = li[0]
            self.inventory.quantities = li[1]


class Projectile(Entity):
    def __init__( self, pos, _entity_buffer, width, height ):
        super( ).__init__( pos, _entity_buffer, width, height )
        pass


class Slime(Entity):
    def __init__( self, pos, _entity_buffer, width, height ):
        super( ).__init__( pos, _entity_buffer, width, height )
        pass

    def run( self ):
        pass


class Zombie(Entity):
    def __init__( self, pos, _entity_buffer, width, height ):
        super( ).__init__( pos, _entity_buffer, width, height )
        pass

    def run( self ):
        pass


class EntityBuffer:

    def __init__( self , _len ):

        self.len            = _len

        # References to other managers (must be provided in main)
        self.chunk_buffer   = None
        self.player         = None
        self.renderer       = None
        self.serializer     = None
        self.player         = None

        # Reference to camera and screen surface
        self.camera         = None
        self.screen         = None

        self.get_curr_chunk = lambda p: int( math.floor( p[0] / CHUNK_WIDTH_P ) )
        self.get_curr_chunk_ind = lambda p: int( self.get_curr_chunk( p ) - self.chunk_buffer.positions[0] )
        self.get_x_pos_chunk = lambda p: int( p[0] // TILE_WIDTH - self.get_curr_chunk( p ) * CHUNK_WIDTH )
        self.get_y_pos_chunk = lambda p: int( p[1] // TILE_WIDTH )
        self.get_tile = lambda p: self.chunk_buffer[self.get_curr_chunk_ind( p )][self.get_y_pos_chunk( p )][self.get_x_pos_chunk( p )]

    def initialize( self , _chunk_buffer , _player , _renderer , _serializer , _camera , _screen ):

        # Set all references to main managers
        self.chunk_buffer   = _chunk_buffer
        self.player         = _player
        self.renderer       = _renderer
        self.serializer     = _serializer
        self.camera         = _camera
        self.screen         = _screen

    def add_player( self ):
        pass

    def add_entity( self ):
        pass

    def hit( self ):
        pass

    def pick_item( self ):
        pass

    def entity_in_range( self ):
        pass

    def update( self ):
        pass

    def draw( self ):
        pass

    def shift( self, d):
        pass


class Inventory:

    def __init__( self , _cols , _rows ):

        # ! Magic numbers are being used here

        self.items              = [ [ None for j in range( _cols ) ] for i in range( _rows ) ]
        self.quantities         = [ [ 0 for j in range( _cols ) ] for i in range( _rows ) ]

        self.positions          = {}
        self.local_item_table   = []

        self.sel_pos            = 0
        self.sel_item           = [ None , 0 ]
        self.item_held          = [ 0 , 0 ]

        self.cols               = _cols
        self.rows               = _rows

        self.surf               = pygame.surface( ( 800 , 500 ) , flags = pygame.SRCALPHA )

    def add_item( self, _item , _quantity ):
        """ Adds the supplied item to the inventory the supplied number of items homogenously
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

                if self.quantities[y][x] is 0: empty_slots.append( [ x , y ] )

                if self.items[y][x] == _item and self.quantities[y][x] < 64:
                    max_fit = min( _quantity, 64 - self.quantities[y][x] )
                    self.quantities[y][x] += max_fit
                    _quantity -= max_fit
                    if _quantity is 0: return None

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
        """ Removes the supplied number of occourences of the supplied item from the inventory from all around
            If the supplied count exceeds the total count, then only the total count is removed
            The number of items which could successfully be removed are returned

        Args:
            _item (int): The item which is to be removed
            _quantity (int): The quantity of the item to be removed

        Returns:
            int: The number of items which could succesfully be removed
        """

        for x in range( self.cols ):

            for y in range( self.rows ):

                if self.items[y][x] == _item:

                    to_remove = min( self.quantities[y][x] , _quantity )
                    print(to_remove)
                    self.quantities[y][x] -= to_remove
                    _quantity -= to_remove
                    if self.quantities[y][x] <= 0: self.items[y][x] = None
                    if _quantity <= 0: return True

        return _quantity

    def rem_item_pos( self, _quantity, _pos ):
        """ Removes a given quantity of items from a given position
            If the supplied quantity is equal to/exceeds the present quantity, only the present quantity is removed
            The number of items which could succesfully be removed are returned

        Args:
            _quantity (int): The number of items to be removed
            _pos (list): The position from which to remove the given quantity (in coloumn , row  format)

        Returns:
            int: The count of the items which were succesfully removed
        """

        to_remove = min( self.quantities[_pos[1]][_pos[0]] , _quantity )
        self.quantities[_pos[1]][_pos[0]] -= to_remove

        if self.quantities[_pos[1]][_pos[0]] <= 0: self.items[_pos[1]][_pos[0]] = None

        return to_remove

    def get_selected_item( self ):
        """Returns the ID of the item which is currently selected

        Returns:
            int: The ID of the item which is currently selected
        """


        return self.items[self.itemHeld[1]][self.itemHeld[0]]

    def get_selected_quantity( self ):
        """Returns the quantity of the item at the position currently being selected (not held)

        Returns:
            int: The quantity of the items being held
        """

        return self.quantities[self.itemHeld[1]][self.itemHeld[0]]

    def draw( self ):
        """ Draws the Inventory on to its own surface
        """

        # ! LOTS OF MAGIC NUMBERS
        slot    = ITEM_TABLE[ slot ]
        coors   = [ 0 , 0 ]

        for x , coors[0] in zip( range( self.cols ) , range( 40 * self.cols ) ):

            for y , coors[1] in zip( range( self.rows ) , range( 40 * self.rows) ):

                self.surf.blit( slot , coors )

                # self.surf.blit( INV_FONT.render( str(self.quantities[y][x]), (0, 0, 0) )[0], coors )
                # self.surf.blit( INV_FONT.render( tiles.TILE_NAMES.get(self.items[y][x], 'X'), (0, 0, 0) )[0], [coors[0], coors[1] + 12] )