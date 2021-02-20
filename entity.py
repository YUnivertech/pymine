from constants import *
import tiles, items
import math, Chunk
import gameUtilities

class ItemEntity:
    def __init__(self, id, pos, width, height):
        self.id = id
        self.pos = pos
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.surfPos = lambda : [ int(self.pos[0] - self.width//2), int(self.pos[1] + self.height//2) ]

    def draw( self ):
        self.surf.blit(tiles.TILE_TABLE.get(self.id, tiles.bedrock), [0, 0])
        # puts the texture of the block itself onto my surface

class Entity:

    def __init__(self, pos:list, chunkBuffer:Chunk.ChunkBuffer, entityBuffer, width:int, height, friction:float, health:int=100, grounded:bool=True):
        """[summary]

        Args:
            pos (list): [description]
            chunkBuffer (Chunk.ChunkBuffer): [description]
            width (float): [description]
            height (float): [description]
            friction (float): [description]
            health (int, optional): [description]. Defaults to 100.
            grounded (bool, optional): [description]. Defaults to True.
        """

        self.pos         = pos
        self.chunkBuffer = chunkBuffer
        self.entityBuffer     = entityBuffer
        self.friction    = friction
        self.health      = health
        self.grounded    = grounded

        # self.itemHeld     = None
        self.vel         = [0.0, 0.0]
        self.acc         = [0.0, 0.0]

        self.width       = width
        self.height      = height

        self.surf        = pygame.Surface((self.width, self.height))
        self.surfPos     = lambda: [ self.pos[0] - (PLYR_WIDTH*0.5), self.pos[1] + (PLYR_HEIGHT*0.5) ]

        self.hitting     = False
        self.placing     = False

        # In the following lambda functions, 'p' means position which is a tuple
        self.currChunk    = lambda p: int(math.floor(p[0] / CHUNK_WIDTH_P))
        self.currChunkInd = lambda p: int(self.currChunk(p) - self.chunkBuffer.positions[0])
        self.xPosChunk    = lambda p: int(p[0] // TILE_WIDTH - self.currChunk(p) * CHUNK_WIDTH)
        self.yPosChunk    = lambda p: int(p[1] // TILE_WIDTH)
        self.tile         = lambda p: self.chunkBuffer[self.currChunkInd(p)][self.yPosChunk(p)][self.xPosChunk(p)]

    def le(self, off:tuple, pos=None):
        if not pos:
            pos = self.pos
        return pos[0] - (self.width * 0.5) + off[0], pos[1] + off[1]

    def ri(self, off:tuple, pos=None):
        if not pos:
            pos = self.pos
        return pos[0] + (self.width * 0.5) + off[0], pos[1] + off[1]

    def bo(self, off:tuple, pos=None):
        if not pos:
            pos = self.pos
        return pos[0] + off[0], pos[1] - (self.height * 0.5) + off[1]

    def up(self, off:tuple, pos=None):
        if not pos:
            pos = self.pos
        return pos[0] + off[0], pos[1] + (self.height * 0.5) + off[1]

    def lB(self, off:tuple, pos=None):
        if not pos:
            pos = self.pos
        return pos[0] - (self.width * 0.5) + off[0], pos[1] - (self.height * 0.5) + off[1]

    def lU(self, off:tuple, pos=None):
        if not pos:
            pos = self.pos
        return pos[0] - (self.width * 0.5) + off[0], pos[1] + (self.height * 0.5) + off[1]

    def rB(self, off:tuple, pos=None):
        if not pos:
            pos = self.pos
        return pos[0] + (self.width * 0.5) + off[0], pos[1] - (self.height * 0.5) + off[1]

    def rU(self, off:tuple, pos=None):
        if not pos:
            pos = self.pos
        return pos[0] + (self.width * 0.5) + off[0], pos[1] + (self.height * 0.5) + off[1]

    def driveUpdate(self, dt:float):
        dt2 = dt
        t = 16 / (MAX_VEL*SCALE_VEL)
        while self.vel != [0,0] and dt2 >= t:
            dt2 -= t
            self.update(t)
        else:
            self.update(dt2)

    def update(self, dt:float):

        nextPos = self.pos.copy()
        self.calcFriction()
        self.checkGround( self.pos )
        if not self.grounded: self.acc[1] = -GRAVITY_ACC
        for i in range(0, 2):
            nextVel = self.vel[i] + self.acc[i]*dt

            if nextVel >= abs(self.friction*dt):
                self.vel[i] -= self.friction*dt
            elif nextVel <= -abs(self.friction*dt):
                self.vel[i] += self.friction*dt
            else:
                self.vel[i] = 0
                self.acc[i] = 0

            self.acc[i] = MAX_ACC*2 if(self.acc[i] > MAX_ACC*2) else -MAX_ACC*2 if(self.acc[i] < -MAX_ACC*2) else self.acc[i]

            self.vel[i] += self.acc[i] * dt
            if self.vel[i] < -MAX_VEL*(1-self.friction*0.2): self.vel[i] = -MAX_VEL*(1-self.friction*0.2)
            elif self.vel[i] > MAX_VEL*(1-self.friction*0.2): self.vel[i] = MAX_VEL*(1-self.friction*0.2)
            nextPos[i] += self.vel[i] * SCALE_VEL * dt

            move = self.check( i, dt , nextPos)
            nextPos = self.pos.copy()
            if move: self.pos[i] += self.vel[i] * SCALE_VEL * dt
            else: self.vel[i] = 0

    def calcFriction(self):
        if self.tile(self.lB((0,-1))) == 0:
            self.friction = AIR_FRICTION
        else:
            self.friction = tiles.TILE_ATTR[self.tile(self.lB((0,-1)))][FRICTION]

    def moveLeft(self):
        self.acc[0] = -self.friction * 2

    def moveRight(self):
        self.acc[0] = self.friction * 2

    def moveDown(self):
        pass

    def jump(self):
        self.vel[1] = JUMP_VEL
        self.acc[1] = -GRAVITY_ACC
        self.grounded = False

    def checkUp(self, pos:list):
        if self.tile(self.lU((0,0), pos)) != 0 or self.tile(self.rU((0,0), pos)) != 0 or self.tile(self.up((0,0), pos)) != 0:
            return False
        else:
            return True

    def checkLeft(self, pos:list):
        if self.tile(self.lU((0,0), pos)) != 0 or self.tile(self.lB((0,0), pos)) != 0 or self.tile(self.le((0,0), pos)) != 0:
            return False
        else:
            return True

    def checkRight(self, pos:list):
        if self.tile(self.rB((0,0), pos)) != 0 or self.tile(self.rU((0,0), pos)) != 0 or self.tile(self.ri((0,0), pos)) != 0:
            return False
        else:
            return True

    def checkGround(self, pos:list):
        if self.tile(self.lB((0,0), pos)) != 0 or self.tile(self.rB((0,0), pos)) != 0 or self.tile(self.bo((0,0), pos)) != 0:
            self.grounded = True
            return False
        else:
            self.grounded = False
            return True

    def check(self, i:int, dt:float, pos:list):
        if i == 0:
            if self.vel[0]+self.acc[0]*dt > 0:
                res = self.checkRight(pos)
            else:
                res = self.checkLeft(pos)
        else:
            if self.vel[1]+self.acc[1]*dt > 0:
                res = self.checkUp(pos)
            else:
                res = self.checkGround(pos)
        return res

class Player(Entity):

    def __init__( self , screen , pos:list, chunkBuffer:Chunk.ChunkBuffer, entityBuffer, eventHandler, keyState, mouseState, cursorPos, friction:float, health:int=100, grounded:bool=True):
        super().__init__(pos, chunkBuffer, entityBuffer, PLYR_WIDTH, PLYR_HEIGHT, friction, health, grounded)

        self.eventHandler = eventHandler

        self.keyState = keyState
        self.mouseState = mouseState
        self.cursorPos = cursorPos

        self.inventory = Inventory(screen, INV_COLS, INV_ROWS)

        self.tangibility = 0
        # 0 means intangible
        # 1 means interacting with blocks
        # 2 means interacting with walls

    def run( self ):

        self.acc[0] = 0
        self.acc[1] = 0

        self.hitting = False
        self.placing = False

        if self.keyState[pygame.K_a] and not self.keyState[pygame.K_d]:
            self.moveLeft()
        elif self.keyState[pygame.K_d] and not self.keyState[pygame.K_a]:
            self.moveRight()

        if self.keyState[pygame.K_s] and not self.keyState[pygame.K_w]:
            self.moveDown()
        elif self.grounded and self.keyState[pygame.K_w] and not self.keyState[pygame.K_s]:
            self.jump()

        if self.keyState[pygame.K_e]:
            self.inventory.isEnabled = not self.inventory.isEnabled
            self.keyState[pygame.K_e] = False

        if self.keyState[pygame.K_q]:
            self.drop()
            print('DROPPING')

        if self.mouseState[1]:  # left is there
            self.hitting = True

        if self.mouseState[2]:  # middle is there
            self.placing = True

        if self.mouseState[3]:  # right is there
            pass
        if self.mouseState[4]:  # scroll up
            pass
        if self.mouseState[5]:  # scroll down
            pass

        self.pick()

    def update( self, dt:float ):
        """[summary]

        Args:
            dt (float): [description]
        """

        nextPos = self.pos.copy( )
        self.calcFriction( )
        self.checkGround( self.pos )
        if not self.grounded: self.acc[1] = -GRAVITY_ACC
        for i in range( 0, 2 ):
            nextVel = self.vel[i] + self.acc[i] * dt

            if nextVel >= abs( self.friction * dt ):
                self.vel[i] -= self.friction * dt
            elif nextVel <= -abs( self.friction * dt ):
                self.vel[i] += self.friction * dt
            else:
                self.vel[i] = 0
                self.acc[i] = 0

            self.acc[i] = MAX_ACC * 2 if (self.acc[i] > MAX_ACC * 2) else -MAX_ACC * 2 if (self.acc[i] < -MAX_ACC * 2) else self.acc[i]

            self.vel[i] += self.acc[i] * dt
            if self.vel[i] < -MAX_VEL * (1 - self.friction * 0.2):
                self.vel[i] = -MAX_VEL * (1 - self.friction * 0.2)
            elif self.vel[i] > MAX_VEL * (1 - self.friction * 0.2):
                self.vel[i] = MAX_VEL * (1 - self.friction * 0.2)
            nextPos[i] += self.vel[i] * SCALE_VEL * dt

            move = self.check( i, dt, nextPos )
            nextPos = self.pos.copy( )
            # print(move)
            if move:
                self.pos[i] += self.vel[i] * SCALE_VEL * dt
            else:
                self.vel[i] = 0

        if self.hitting and not self.placing :
            chunk = math.floor(self.cursorPos[0] / CHUNK_WIDTH_P)
            chunkInd = chunk - self.chunkBuffer.positions[0]

            x = (self.cursorPos[0] // TILE_WIDTH) - chunk * CHUNK_WIDTH
            y = (self.cursorPos[1] // TILE_WIDTH)

            block = self.chunkBuffer[ chunkInd ][ y ][ x ]
            state = self.chunkBuffer[ chunkInd ].breakBlockAt( x, y, 10, dt)
            self.chunkBuffer[ chunkInd ].breakWallAt( x, y, 10, dt)

            # self.chunkBuffer[ chunkInd ][y][x] = tiles.air
            # self.chunkBuffer[ chunkInd ].walls[y][x] = tiles.air

            self.eventHandler.tileBreakFlag = True

            self.eventHandler.tileBreakIndex = chunkInd
            self.eventHandler.tileBreakPos[0] = x
            self.eventHandler.tileBreakPos[1] = y

            if state: # The block was broken
                print(block)
                # self.entityBuffer.addItem( block, [self.cursorPos[0], self.cursorPos[1]], chunkInd)
                self.entityBuffer.addItem( block, self.cursorPos.copy(), chunkInd)

            # print(chunk, chunkInd, x, y, sep='\t')

        elif self.placing:
            chunk = math.floor(self.cursorPos[0] / CHUNK_WIDTH_P)
            chunkInd = chunk - self.chunkBuffer.positions[0]

            x = (self.cursorPos[0] // TILE_WIDTH) - chunk * CHUNK_WIDTH
            y = (self.cursorPos[1] // TILE_WIDTH)

            # i need to get the first item from the inventory and just simply place that
            toPlace = self.inventory.getSelectedItem()

            dist = math.sqrt( pow( self.pos[0] - self.cursorPos[0], 2 ) + pow( self.pos[1] - self.cursorPos[1], 2 ) )
            if toPlace and dist > PLYR_HEIGHT:
                print('PLACING!', tiles.TILE_NAMES[toPlace])
                res = self.chunkBuffer[chunkInd].placeBlockAt( x, y, toPlace)
                if res: self.inventory.remItemPos( 1, self.inventory.itemHeld )

            self.eventHandler.tilePlaceFlag = True

            self.eventHandler.tilePlaceIndex = chunkInd
            self.eventHandler.tilePlacePos[0] = x
            self.eventHandler.tilePlacePos[1] = y

            # if (x, y, True) in self.chunkBuffer[ chunkInd].TILE_TABLE_LOCAL: print("True")
            # else: print("False")

    def pick( self ):
        l = self.entityBuffer.pickItem()
        for item in l: self.inventory.addItem(item, 1)


class Inventory:

    def __init__( self, screen, cols:int, rows:int ):

        self.screen = screen

        self.items      = [ [ None for j in range( 0, cols ) ] for i in range( 0, rows ) ]
        self.quantities = [ [ 0 for j in range( 0, cols ) ] for i in range( 0, rows ) ]
        self.positions  = {}

        self.ITEM_TABLE_LOCAL = []

        self.selPos     = 0
        self.selItem    = [None, 0]

        self.itemHeld   = [0, 0]

        self.isEnabled = False

    def addItem( self, i, q ):
        firstEmpty = None
        for x in range(INV_COLS):
            for y in range(INV_ROWS):
                if firstEmpty == None and self.quantities[y][x] == 0: firstEmpty = [x, y]
                if self.items[y][x] == i and self.quantities[y][x] < 64:
                    maxFit = min([q, 64 - self.quantities[y][x], 64])
                    self.quantities[y][x] += maxFit
                    q -= maxFit
                    if q == 0: return None
        if q > 0 and firstEmpty != None:
            maxFit = min(64, q)
            q -= maxFit
            self.items[firstEmpty[1]][firstEmpty[0]] = i
            self.quantities[firstEmpty[1]][firstEmpty[0]] = maxFit
            if q > 0: self.addItem( i, q )

    def addItemPos( self, item:int, quantity:int, pos:list ):

        if self.items[pos[1]][pos[0]] != item:

            self.selItem[0] = self.items[ pos[1] ][ pos[0] ]
            self.selItem[1] = self.quantities[ pos[1] ][ pos[0] ]

            self.items[ pos[1] ][ pos[0] ] = item
            self.quantities[ pos[1] ][ pos[0] ] = quantity

        else:

            self.items[pos[1]][pos[0]] = item
            self.items[pos[1]][pos[0]] = item

            if self.quantities[pos[1]][pos[0]] + quantity > items.ITEM_ATTR[item][MAX_STACK]:

                self.selItem[0] = item
                self.selItem[1] = self.quantities[pos[1]][pos[0]] + quantity - items.ITEM_ATTR[item][MAX_STACK]

                self.quantities[pos[1]][pos[0]] = items.ITEM_ATTR[item][MAX_STACK]

            else:

                self.selItem[0] = None
                self.selItem[1] = 0

                self.quantities[pos[1]][pos[0]] += quantity

    def remItemStack( self, item:int, quantity:int ):
        for x in range(INV_COLS):
            for y in range(INV_ROWS):
                if self.items[y][x] == item:
                    toRemove = min(self.quantities[y][x], quantity)
                    print(toRemove)
                    self.quantities[y][x] -= toRemove
                    quantity -= toRemove
                    if self.quantities[y][x] <= 0: self.items[y][x] = None
                    if quantity <= 0: return True

        if quantity != 0: return False
        return True

    def remItemPos( self, quantity:int, pos:list):
        toRemove = min(self.quantities[pos[1]][pos[0]], quantity)
        self.quantities[pos[1]][pos[0]] -= toRemove
        if self.quantities[pos[1]][pos[0]] <= 0: self.items[pos[1]][pos[0]] = None

    def getSelectedItem( self ):
        return self.items[self.itemHeld[1]][self.itemHeld[0]]

    def getSelectedQuantity( self ):
        return self.quantities[self.itemHeld[1]][self.itemHeld[0]]

    def draw( self ):

        slot = items.ITEM_TABLE[items.slot]
        coors = [16, 16] # ! MAGIC NUMBERS

        for x in range(0, INV_COLS):
            for y in range(0, INV_ROWS):
                self.screen.blit(slot, coors)
                self.screen.blit( INV_FONT.render( str(self.quantities[y][x]), (0, 0, 0) )[0], coors )
                self.screen.blit( INV_FONT.render( items.ITEM_NAMES.get(self.items[y][x], 'X'), (0, 0, 0) )[0], [coors[0], coors[1] + 12] )

                coors[1]+= 40   #! MAGIC NUMBER
            coors[1] = 16
            coors[0] +=40       #! MAGIC NUMBER


class ClientEventHandler:

    def __init__( self ):

        self.playerMovementFlag = False
        self.cameraMovementFlag = False

        self.windowResizeFlag = False

        self.keyInFlag = False
        self.keyStates      =   { pygame.K_w : False, pygame.K_a : False, pygame.K_s : False, pygame.K_d : False, pygame.K_e : False, pygame.K_q : False }

        self.mouseInFlag = False
        self.mouseState     =   { 1 : False, 2 : False, 3 : False, 4 : False, 5 : False }

        self.mouseCursorFlag = False
        self.mousePos       =   [0, 0]
        self.cursorPos      =   [0, 0]

        self.entityMovementFlag = False
        self.entitySpawnedFlag = False
        self.entityDespawnFlag = False

        self.chunkShiftFlag = False
        self.loadChunkIndex =   None
        self.saveChunkIndex =   None

        self.tileBreakFlag = False
        self.tileBreakIndex = -1
        self.tileBreakPos = [-1, -1]

        self.tilePlaceFlag = False
        self.tilePlaceIndex = -1
        self.tilePlacePos = [-1, -1]

        self.tileAlterFlag = False
        self.tileAlterPos = [-1, -1]

    def addKey( self, key ):
        if key in self.keyStates:
            self.keyInFlag = True
            self.keyStates[key] = True

    def remKey( self, key ):
        if key in self.keyStates:
            self.keyInFlag = True
            self.keyStates[key] = False

    def addMouseMotion( self, event, camera, displaySize ):
        self.mouseInFlag = True
        self.mousePos[0] = event.pos[0]
        self.mousePos[1] = event.pos[1]
        self.cursorPos[0] = int(camera[0]) + self.mousePos[0] - displaySize[0]//2
        self.cursorPos[1] = int(camera[1]) + displaySize[1]//2 - self.mousePos[1]

    def addMouseButton( self, button ):
        # 1 for left, 2 for middle, 3 for right, 4 for scroll up and 5 for scroll down
        mouseInFlag = True
        self.mouseState[ button ] = True

    def remMouseButton( self, button ):
        mouseInFlag = True
        self.mouseState[ button ] = False

    def addWindowResize( self ):
        self.windowResizeFlag = True

    def addCameraMotion( self ):
        self.cameraMovementFlag = True


class EntityBuffer:
    def __init__( self, cB:Chunk.ChunkBuffer, s:gameUtilities.Serializer, player):
        self.chunkBuffer = cB
        self.serializer  = s
        self.length = self.chunkBuffer.length
        self.len = 0

        self.entities = [[] for i in range(self.length)]
        self.mousePos       =   [0, 0]
        self.plyr = player
        # self.entities = { }
        # self.mousePos       =   [0, 0]

    def addItem(self, item, pos, index):
        ie = ItemEntity(item, pos,16, 16,)
        self.entities[index].append(ie)
        # 0 is the index of the chunk in the chunk buffer in which it was broken

    def addEntity(self, e:Entity):
        self.entities[e.currChunkInd(e.pos)].append(e)

    def shift( self, d):
        if d < 0:       # Player has moved left
            # self.serializer.setEntity(self.chunkBuffer.positions[-1]+1, self.entities[-1])
            del self.entities[-1]
            # li = self.serializer.getEntity(self.chunkBuffer.positions[0])
            li = None
            if li is None:
                self.entities.insert(0, [])
            else:
                self.entities.insert(0, li)
        elif d > 0:     # Player has moved right
            # self.serializer.setEntity(self.chunkBuffer.positions[0]-1, self.entities[0])
            del self.entities[0]
            # li = self.serializer.getEntity(self.chunkBuffer.positions[-1])
            li = None
            if li is None:
                self.entities.insert(len(self.entities), [])
            else:
                self.entities.insert(len(self.entities), li)

    def update( self ):
        for i in self.entities:
            for j in i:
                j.update()

    def pickItem( self ):
        l = []
        toDel = []
        for group in self.entities:
            for e in range(len(group)):
                entity = group[e]
                dist = math.sqrt( pow( self.plyr.pos[0] - entity.pos[0], 2 ) + pow( self.plyr.pos[1] - entity.pos[1], 2 ) )
                if dist <= PLYR_RANGE:
                    l.append(entity.id)
                    toDel.append(e)

            for i in toDel: del group[i]
            toDel = []
        return l

    def draw( self ):
        for group in self.entities:
            for entity in group:
                entity.draw()
