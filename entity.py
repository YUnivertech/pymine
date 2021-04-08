from game_utilities import *

# ! def initialize( self , _renderer , _chunk_buffer , _serializer , _player , _camera , _screen ):

# !    self.renderer       = _renderer
# !    self.chunk_buffer   = _chunk_buffer
# !    self.serializer     = _serializer
# !    self.player         = _player
# !    self.camera         = _camera
# !    self.screen         = _screen

# class Hitbox:
#     def __init__( self ):
#         pass
#
#
# class ItemEntity:
#     def __init__( self ):
#         pass
#
#     def draw( self ):
#         pass
#
#
# class Entity:
#     def __init__(self, pos, chunkBuffer, entityBuffer, width, height, health=100):
#         self.pos          = pos
#         self.chunk_buffer = chunkBuffer
#         self.entity_buffer = entityBuffer
#         self.health       = health
#         self.grounded     = True
#         self.friction     = DEFAULT_FRICTION
#         self.vel          = [0.0, 0.0]
#         self.acc          = [0.0, 0.0]
#         self.width        = width
#         self.height       = height
#         self.surf         = pygame.Surface((self.width, self.height))
#         self.surfPos      = lambda: [ self.pos[0] - (PLYR_WIDTH*0.5), self.pos[1] + (PLYR_HEIGHT*0.5) ]
#         self.hitting      = False
#         self.placing      = False
#
#         self.le           = lambda off, p=self.pos: (p[0] - (self.width * 0.5) + off[0], p[1] + off[1])    # Left
#         self.ri           = lambda off, p=self.pos: (p[0] + (self.width * 0.5) + off[0], p[1] + off[1])    # Right
#         self.bo           = lambda off, p=self.pos: (p[0] + off[0], p[1] - (self.height * 0.5) + off[1])    # Bottom
#         self.up           = lambda off, p=self.pos: (p[0] + off[0], p[1] + (self.height * 0.5) + off[1])    # Top
#         self.lb           = lambda off, p=self.pos: (p[0] - (self.width * 0.5) + off[0], p[1] - (self.height * 0.5) + off[1])    # Left bottom
#         self.lu           = lambda off, p=self.pos: (p[0] - (self.width * 0.5) + off[0], p[1] + (self.height * 0.5) + off[1])    # Left top
#         self.rb           = lambda off, p=self.pos: (p[0] + (self.width * 0.5) + off[0], p[1] - (self.height * 0.5) + off[1])    # Right bottom
#         self.ru           = lambda off, p=self.pos: (p[0] + (self.width * 0.5) + off[0], p[1] + (self.height * 0.5) + off[1])
#
#         # In the following lambda functions, 'p' means position which is a tuple
#         self.currChunk    = lambda p: int(math.floor(p[0] / CHUNK_WIDTH_P))
#         self.currChunkInd = lambda p: int( self.currChunk(p) - self.chunk_buffer.positions[0] )
#         self.xPosChunk    = lambda p: int(p[0] // TILE_WIDTH - self.currChunk(p) * CHUNK_WIDTH)
#         self.yPosChunk    = lambda p: int(p[1] // TILE_WIDTH)
#         self.tile         = lambda p: self.chunk_buffer[self.currChunkInd( p )][self.yPosChunk( p )][self.xPosChunk( p )]
#
#     # def le(self, off, pos=None):
#     #     if not pos: pos = self.pos
#     #     return pos[0] - (self.width * 0.5) + off[0], pos[1] + off[1]
#     #
#     # def ri(self, off, pos=None):
#     #     if not pos: pos = self.pos
#     #     return pos[0] + (self.width * 0.5) + off[0], pos[1] + off[1]
#     #
#     # def bo(self, off, pos=None):
#     #     if not pos: pos = self.pos
#     #     return pos[0] + off[0], pos[1] - (self.height * 0.5) + off[1]
#     #
#     # def up(self, off, pos=None):
#     #     if not pos: pos = self.pos
#     #     return pos[0] + off[0], pos[1] + (self.height * 0.5) + off[1]
#     #
#     # def lb(self, off, pos=None):
#     #     if not pos: pos = self.pos
#     #     return pos[0] - (self.width * 0.5) + off[0], pos[1] - (self.height * 0.5) + off[1]
#     #
#     # def lu(self, off, pos=None):
#     #     if not pos: pos = self.pos
#     #     return pos[0] - (self.width * 0.5) + off[0], pos[1] + (self.height * 0.5) + off[1]
#     #
#     # def rb(self, off, pos=None):
#     #     if not pos: pos = self.pos
#     #     return pos[0] + (self.width * 0.5) + off[0], pos[1] - (self.height * 0.5) + off[1]
#     #
#     # def ru(self, off, pos=None):
#     #     if not pos: pos = self.pos
#     #     return pos[0] + (self.width * 0.5) + off[0], pos[1] + (self.height * 0.5) + off[1]
#
#     def calc_friction(self):
#         if self.tile( self.lb( (0, -1) ) ) == 0:
#             self.friction = AIR_FRICTION
#         else:
#             self.friction = tiles.TILE_ATTR[self.tile( self.lb( (0, -1) ) )][FRICTION]
#
#     def move_left(self):
#         self.acc[0] = -self.friction * 2
#
#     def move_right(self):
#         self.acc[0] = self.friction * 2
#
#     def move_down(self):
#         pass
#
#     def jump(self):
#         self.vel[1] = JUMP_VEL
#         self.acc[1] = -GRAVITY_ACC
#         self.grounded = False
#
#     def checkUp(self, pos):
#         if self.tile( self.lu( (0, 0), pos ) ) != 0 or self.tile( self.ru( (0, 0), pos ) ) != 0 or self.tile( self.up( (0, 0), pos ) ) != 0:
#             return False
#         else: return True
#
#     def checkLeft(self, pos):
#         if self.tile( self.lu( (0, 0), pos ) ) != 0 or self.tile( self.lb( (0, 0), pos ) ) != 0 or self.tile( self.le( (0, 0), pos ) ) != 0:
#             return False
#         else: return True
#
#     def checkRight(self, pos):
#         if self.tile( self.rb( (0, 0), pos ) ) != 0 or self.tile( self.ru( (0, 0), pos ) ) != 0 or self.tile( self.ri( (0, 0), pos ) ) != 0:
#             return False
#         else: return True
#
#     def checkGround(self, pos):
#         if self.tile( self.lb( (0, 0), pos ) ) != 0 or self.tile( self.rb( (0, 0), pos ) ) != 0 or self.tile( self.bo( (0, 0), pos ) ) != 0:
#             self.grounded = True
#             return False
#         else:
#             self.grounded = False
#             return True
#
#     def check(self, i, dt, pos):
#         if i == 0:
#             if self.vel[0]+self.acc[0]*dt > 0:  res = self.checkRight(pos)
#             else:   res = self.checkLeft(pos)
#         else:
#             if self.vel[1]+self.acc[1]*dt > 0:  res = self.checkUp(pos)
#             else:   res = self.checkGround(pos)
#         return res
#
#     def hit( self ):
#         pass
#
#     def get_hit( self ):
#         pass
#
#
# class Player(Entity):
#
#     def __init__( self, screen, pos, chunkBuffer, entityBuffer, eventHandler, keyState, mouseState, cursorPos, friction):
#         super().__init__(pos, chunkBuffer, entityBuffer, PLYR_WIDTH, PLYR_HEIGHT, friction)
#
#         self.eventHandler = eventHandler
#         self.keyState = keyState
#         self.mouseState = mouseState
#         self.cursorPos = cursorPos
#         self.inventory = Inventory(screen, INV_COLS, INV_ROWS)
#         self.tangibility = 0
#
#     def run( self ):
#         self.acc[0] = 0
#         self.acc[1] = 0
#         self.hitting = False
#         self.placing = False
#         if self.keyState[pygame.K_a] and not self.keyState[pygame.K_d]:
#             self.move_left( )
#         elif self.keyState[pygame.K_d] and not self.keyState[pygame.K_a]:
#             self.move_right( )
#
#         if self.keyState[pygame.K_s] and not self.keyState[pygame.K_w]:
#             self.move_down( )
#         elif self.grounded and self.keyState[pygame.K_w] and not self.keyState[pygame.K_s]:
#             self.jump()
#
#         if self.keyState[pygame.K_e]:
#             self.inventory.isEnabled = not self.inventory.isEnabled
#             self.keyState[pygame.K_e] = False
#
#     def update( self, dt ):
#         nextPos = self.pos.copy( )
#         self.calc_friction( )
#         self.checkGround( self.pos )
#         if not self.grounded: self.acc[1] = -GRAVITY_ACC
#         for i in range( 0, 2 ):
#             nextVel = self.vel[i] + self.acc[i] * dt
#             if nextVel >= abs( self.friction * dt ):
#                 self.vel[i] -= self.friction * dt
#             elif nextVel <= -abs( self.friction * dt ):
#                 self.vel[i] += self.friction * dt
#             else:
#                 self.vel[i] = 0
#                 self.acc[i] = 0
#
#             self.acc[i] = MAX_ACC * 2 if (self.acc[i] > MAX_ACC * 2) else -MAX_ACC * 2 if (self.acc[i] < -MAX_ACC * 2) else self.acc[i]
#             self.vel[i] += self.acc[i] * dt
#             if self.vel[i] < -MAX_VEL * (1 - self.friction * 0.2):
#                 self.vel[i] = -MAX_VEL * (1 - self.friction * 0.2)
#             elif self.vel[i] > MAX_VEL * (1 - self.friction * 0.2):
#                 self.vel[i] = MAX_VEL * (1 - self.friction * 0.2)
#             nextPos[i] += self.vel[i] * SCALE_VEL * dt
#             move = self.check( i, dt, nextPos )
#             nextPos = self.pos.copy( )
#             if move:    self.pos[i] += self.vel[i] * SCALE_VEL * dt
#             else:       self.vel[i] = 0
#
#         if self.hitting and not self.placing :
#             chunk = math.floor(self.cursorPos[0] / CHUNK_WIDTH_P)
#             chunkInd = chunk - self.chunk_buffer.positions[0]
#             x = (self.cursorPos[0] // TILE_WIDTH) - chunk * CHUNK_WIDTH
#             y = (self.cursorPos[1] // TILE_WIDTH)
#             block = self.chunk_buffer[ chunkInd][ y][ x]
#             state = self.chunk_buffer[ chunkInd].breakBlockAt( x, y, 10, dt )
#             self.eventHandler.tileBreakFlag = True
#             self.eventHandler.tileBreakIndex = chunkInd
#             self.eventHandler.tileBreakPos[0] = x
#             self.eventHandler.tileBreakPos[1] = y
#             if state:   # The block was broken
#                 self.entity_buffer.addItem( block, self.cursorPos.copy( ), chunkInd )
#
#         elif self.placing:
#             chunk = math.floor(self.cursorPos[0] / CHUNK_WIDTH_P)
#             chunkInd = chunk - self.chunk_buffer.positions[0]
#             x = (self.cursorPos[0] // TILE_WIDTH) - chunk * CHUNK_WIDTH
#             y = (self.cursorPos[1] // TILE_WIDTH)
#             toPlace = self.inventory.getSelectedItem()
#             dist = math.sqrt(pow(self.pos[0]-self.cursorPos[0], 2)+pow(self.pos[1]-self.cursorPos[1], 2))
#             if toPlace and dist > PLYR_HEIGHT:
#                 res = self.chunk_buffer[chunkInd].placeBlockAt( x, y, toPlace )
#                 if res: self.inventory.remItemPos( 1, self.inventory.itemHeld )
#
#             self.eventHandler.tilePlaceFlag = True
#             self.eventHandler.tilePlaceIndex = chunkInd
#             self.eventHandler.tilePlacePos[0] = x
#             self.eventHandler.tilePlacePos[1] = y
#
#     def pick( self ):
#         l = self.entity_buffer.pickItem( )
#         for item in l: self.inventory.addItem(item, 1)
#
#     def save( self, serializer ):
#         li = [self.inventory.items, self.inventory.quantities]
#         li = pickle.dumps(li)
#         serializer.savePlayer(1, li)
#
#     def load( self, serializer):
#         li = serializer.loadPlayer(1)
#         if li:
#             li = pickle.loads(li)
#             self.inventory.items = li[0]
#             self.inventory.quantities = li[1]
#
#
# class Projectile(Entity):
#     def __init__( self, pos, chunkBuffer, entityBuffer, width, height ):
#         super( ).__init__( pos, chunkBuffer, entityBuffer, width, height )
#         pass
#
#
# class Slime(Entity):
#     def __init__( self, pos, chunkBuffer, entityBuffer, width, height ):
#         super( ).__init__( pos, chunkBuffer, entityBuffer, width, height )
#         pass
#
#     def run( self ):
#         pass
#
#
# class Zombie(Entity):
#     def __init__( self, pos, chunkBuffer, entityBuffer, width, height ):
#         super( ).__init__( pos, chunkBuffer, entityBuffer, width, height )
#         pass
#
#     def run( self ):
#         pass
#
#

class EntityBuffer:

    def __init__( self ):

        # References to other managers (must be provided in main)
        self.chunk_buffer   = None
        self.player         = None
        self.renderer       = None
        self.serializer     = None
        self.player         = None

        # Reference to camera and screen surface
        self.camera         = None
        self.screen         = None

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

        first_empty = None

        for y in range( self._rows ):

            for x in range( self._cols ):

                if first_empty is None and self.quantities[y][x] == 0:
                    first_empty = [x, y]

                if self.items[y][x] == _item and self.quantities[y][x] < 64:
                    max_fit = min( _quantity, 64 - self.quantities[y][x], 64 )
                    self.quantities[y][x] += max_fit
                    _quantity -= max_fit
                    if not _quantity: return None

        if _quantity > 0 and first_empty is not None:

            max_fit = min( 64, _quantity )
            _quantity -= max_fit

            self.items[firstEmpty[1]][firstEmpty[0]] = _item
            self.quantities[firstEmpty[1]][firstEmpty[0]] = max_fit

            if _quantity: self.addItem( _item , _quantity )

    def rem_item_stack( self , item , quantity ):

        for x in range( self.cols ):

            for y in range( self.rows ):

                if self.items[y][x] == item:

                    to_remove = min( self.quantities[y][x] , quantity )
                    print(to_remove)
                    self.quantities[y][x] -= to_remove
                    quantity -= to_remove
                    if self.quantities[y][x] <= 0: self.items[y][x] = None
                    if quantity <= 0: return True

        return quantity == 0

    def rem_item_pos( self, _quantity, _pos ):

        to_remove = min( self.quantities[_pos[1]][_pos[0]] , _quantity )
        self.quantities[_pos[1]][_pos[0]] -= to_remove

        if self.quantities[_pos[1]][_pos[0]] <= 0: self.items[_pos[1]][_pos[0]] = None

    def get_selected_item( self ):

        return self.items[self.itemHeld[1]][self.itemHeld[0]]

    def get_selected_quantity( self ):

        return self.quantities[self.itemHeld[1]][self.itemHeld[0]]

    def draw( self ):

        # ! LOTS OF MAGIC NUMBERS
        slot    = ITEM_TABLE[ slot ]
        coors   = [ 0 , 0 ]

        for x , coors[0] in zip( range( self.cols ) , range( 40 * self.cols ) ):

            for y , coors[1] in zip( range( self.rows ) , range( 40 * self.rows) ):

                self.surf.blit( slot , coors )

                # self.surf.blit( INV_FONT.render( str(self.quantities[y][x]), (0, 0, 0) )[0], coors )
                # self.surf.blit( INV_FONT.render( tiles.TILE_NAMES.get(self.items[y][x], 'X'), (0, 0, 0) )[0], [coors[0], coors[1] + 12] )