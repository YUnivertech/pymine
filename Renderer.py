from Chunk import *
import math

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

    @classmethod
    def initialize(cls, chunkBuffer, camera, player, windowSize, screen):

        """Initializes the class with references to global objects

        Args:
            chunkBuffer (chunkBuffer): Reference to the client's chunkBuffer
            camera (list): Reference to the client's camera
            player (list): Reference to the client's player
            windowSize (list): Reference to a list containing the size of the current window
            screen (Pygame.Surface): Reference to the window's surface
        """

        # Create references to global objects
        cls.chunkBuffer     =  chunkBuffer
        cls.player          =  player
        cls.camera          =  camera
        cls.windowSize      =  windowSize
        cls.screen          =  screen

        # Index of the middle chunk in the chunk buffer
        cls.length          =  cls.chunkBuffer.length
        cls.midChunk        =  ( cls.length - 1 ) // 2

        cls.isShader        =  False

        # Update constants to reflect new References
        cls.updateRefs()
        cls.renderLightmaps()

    @classmethod
    def renderFulls( cls ):
        for _ in range( cls.length ):   cls.renderFull( _ )

    @classmethod
    def renderChunks( cls ):
        for _ in range( cls.length ):   cls.renderChunk( _ )

    @classmethod
    def renderLightmaps( cls ):
        for _ in range( cls.length ):   cls.renderLightmap( _ )

    @classmethod
    def renderFull(  cls, index, rect = [ 0, 0, CHUNK_WIDTH, CHUNK_HEIGHT ] ):

        """Method to render the chunk (in the active chunk buffer) whose index has been supplied
        Args:
            index (int): Index of the chunk to be rendered
            rect (list): Rectangular region of the chunk which needs to be rendered (optional argument)
        """

        #cls.renderChunkOnly( index, rect )
        #cls.renderLightmap( index, rect )

        # Create a reference to the chunk currently being rendered (for convenience)
        currChunkRef                    =  cls.chunkBuffer[ index ]
        currSurfRef                     =  cls.chunkBuffer.surfaces[ index ]
        currLightmap                    =  cls.chunkBuffer.lightSurfs[ index ]

        lightBox                        =  pygame.Surface( ( TILE_WIDTH, TILE_WIDTH ) )

        # Fill the to-be-updated region of the surface to "clear" it
        cls.chunkBuffer.surfaces[ index ].fill( ( 30, 150, 240 ), [0, 0, CHUNK_WIDTH_P, CHUNK_HEIGHT_P] )

        for i in range( rect[1], rect[3] ):

            coors = [0, ( CHUNK_HEIGHT - i - 1 ) * TILE_WIDTH ]

            for j in range( rect[0], rect[2] ):

                coors[0] = j * TILE_WIDTH

                currTileRef =  currChunkRef[ i ][ j ]
                currWallRef =  currChunkRef.walls[ i ][ j ]
                lightIntensity       =  currChunkRef.lightMap[ i ][ j ]

                lightBox.fill( ( lightIntensity, ) * 3 )
                currLightmap.blit( lightBox, coors )

                if( currTileRef > 0 ):
                    currSurfRef.blit( tiles.TILE_TABLE[ currTileRef ], coors )
                    if( ( j, i, True ) in currChunkRef.TILE_TABLE_LOCAL ):

                        if(HEALTH in currChunkRef.TILE_TABLE_LOCAL[ ( j, i, True ) ] ):

                            breakState = (currChunkRef.TILE_TABLE_LOCAL[ ( j, i, True ) ][ HEALTH ] * 8) / 100
                            currSurfRef.blit( tiles.TILE_MODIFIERS[ tiles.crack ][ 8 - int(breakState) ], coors )

                elif( currWallRef > 0 ):
                    currSurfRef.blit( tiles.TILE_TABLE[ currWallRef ], coors )
                    if( ( i, j, False ) in currChunkRef.TILE_TABLE_LOCAL ):

                        if(HEALTH in currChunkRef.TILE_TABLE_LOCAL[ ( j, i, False ) ] ):

                            breakState = (currChunkRef.TILE_TABLE_LOCAL[ ( j, i, False ) ][ HEALTH ] * 8) / 100
                            currSurfRef.blit( tiles.TILE_MODIFIERS[ tiles.crack ][ 8 - int(breakState) ], coors )

    @classmethod
    def renderLightmap(  cls, index, rect = [0, 0, CHUNK_WIDTH, CHUNK_HEIGHT] ):

        currChunkRef                    =  cls.chunkBuffer[index]
        currLightmap                    =  cls.chunkBuffer.lightSurfs[index]

        lightBox                        =  pygame.Surface( ( TILE_WIDTH, TILE_WIDTH ) )

        for i in range( rect[1], rect[3] ):

            coors   =   [0, ( CHUNK_HEIGHT - i - 1 ) * TILE_WIDTH]

            for j in range( rect[0], rect[2] ):

                coors[0] = j * TILE_WIDTH

                lightIntensity = currChunkRef.lightMap[ i ][ j ]
                lightBox.fill( ( lightIntensity, ) * 3 )
                currLightmap.blit( lightBox, coors )

    @classmethod
    def updateScreen(  cls  ):

        """Renders the surfaces of each chunk (in the active chunk buffer) on to the window
        """

        rightWalker     =  cls.midChunk        # Goes from the index of the middle chunk to the right-most chunk
        leftWalker      =  cls.midChunk - 1    # Goes from the index of the chunk one before the middle to the left-most chunk

        # Loop to render chunks on the right of the camera (including the camera's chunk)
        while( rightWalker < cls.length ):

            tileWalker      =  0    # Goes from the index of the left-most to the right-most tile in the chunk

            # Loop to render each individual vertical slice of the chunk
            while( tileWalker < CHUNK_WIDTH ):

                sliceInd        =  ( cls.chunkBuffer[rightWalker].index * CHUNK_WIDTH ) + tileWalker   # Absoulute index of the current vertical slice
                slicePos        =  [sliceInd * TILE_WIDTH - cls.camera[0] + cls.numHor, 0]             # List containing the coordinates where the slice must be blitted on-screen

                sliceRect       =  [tileWalker * TILE_WIDTH, cls.upIndex, TILE_WIDTH, cls.downIndex]   # Rectangular region containing the "visible" area of the chunk's surface
                sliceSurf       =  cls.chunkBuffer[rightWalker].surface.subsurface( sliceRect )       # Mini-surface containing the visible region of the chunk's surface
                lightSurf       =  cls.chunkBuffer.lightSurfs[rightWalker].subsurface( sliceRect )      # Mini-surface containing the visible region of the chunk's lightmap

                if( slicePos[0] > cls.windowSize[0] ):     # Stop blitting if slice is beyond the right edge od the window
                    rightWalker     =  cls.length
                    break

                cls.screen.blit( sliceSurf, slicePos )
                if(cls.isShader):
                    cls.screen.blit( lightSurf, slicePos, special_flags = pygame.BLEND_RGBA_MULT )
                tileWalker      += 1

            rightWalker     += 1

        # Loop to render chunks on the left of the camera (excluding the camera's chunk)
        while( leftWalker >= 0 ):

            tileWalker      =  CHUNK_WIDTH - 1    # Goes from the index of the left-most to the right-most tile in the chunk

            # Loop to render each individual vertical slice of the chunk
            while( tileWalker >= 0 ):

                sliceInd        =  ( cls.chunkBuffer[leftWalker].index * CHUNK_WIDTH ) + tileWalker     # Absoulute index of the current vertical slice
                slicePos        =  [sliceInd * TILE_WIDTH - cls.camera[0] + cls.numHor, 0]              # List containing the coordinates where the slice must be blitted on-screen

                sliceRect       =  [tileWalker * TILE_WIDTH, cls.upIndex, TILE_WIDTH, cls.downIndex]    # Rectangular region containing the "visible" area of the chunk's surface
                sliceSurf       =  cls.chunkBuffer[leftWalker].surface.subsurface( sliceRect )         # Mini-surface containing the visible region of the chunk's surface
                lightSurf       =  cls.chunkBuffer.lightSurfs[leftWalker].subsurface( sliceRect )       # Mini-surface containing the visible region of the chunk's lightmap

                if( slicePos[0] < -TILE_WIDTH ):    # Stop blitting if slice is bryond the left edge of the window
                    leftWalker      =  -1
                    break

                cls.screen.blit ( sliceSurf, slicePos )
                if(cls.isShader):
                    cls.screen.blit( lightSurf, slicePos, special_flags = pygame.BLEND_RGBA_MULT )
                tileWalker      -= 1

            leftWalker      -= 1

        if(cls.player.inventory.isEnabled): Renderer.renderInv()

        # Temporary player crosshair rendering
        playerCoors = [cls.player.pos[0], cls.player.pos[1]]

        # Translate to be in camera space
        playerCoors[0] -= cls.camera[0]
        playerCoors[1] -= cls.camera[1]

        # Translate to be in screen space
        playerCoors[0] += cls.numHor
        playerCoors[1] =  cls.numVer - playerCoors[1]

        # ! temporary rendering of player crosshair
        pygame.draw.circle( cls.screen, (255,50,50), playerCoors, 2 )

    @classmethod
    def renderInv( cls ):   # todo THIS FUNCTION HAS A LOT OF MAGIC NUMBERS

        inventory = cls.player.inventory
        slot = items.ITEM_TABLE[items.slot]
        coors = [16, 16] # ! MAGIC NUMBERS

        for x in range(0, INV_COLS):
            for y in range(0, INV_ROWS):
                cls.screen.blit(slot, coors)
                # get the texture of the item stored in the current slot
                # get the count/durability of the item stored in the current slot
                # get the modifiers of the texture of the item stored in the current slot
                coors[1]+= 40   #! MAGIC NUMBER
            coors[1] = 16
            coors[0] +=40       #! MAGIC NUMBER

    @classmethod
    def updateSize(  cls  ):

        # Number of pixels to be rendered on the top and side halves of the camera
        cls.numHor         =  cls.windowSize[0] // 2
        cls.numVer         =  cls.windowSize[1] // 2

    @classmethod
    def updateCam(  cls  ):

        # Indexes of the top and bottom-most pixels of the chunk to be rendered W.R.T to the origin of the chunk-surface

        # Upper index of the visible region of each slice
        cls.upIndex     =  CHUNK_HEIGHT_P - ( cls.camera[1] + cls.numVer )

        if( cls.upIndex < 0 ):    # If lower than zero, then make 0
            cls.upIndex     =  0

        # Height of the visible region of the slice
        cls.downIndex   =  CHUNK_HEIGHT_P - cls.upIndex

        if( cls.downIndex > cls.windowSize[1] ):    # If greater than height-of-window, then make height-of-window
            cls.downIndex   =  cls.windowSize[1]

    @classmethod
    def updateRefs(  cls  ):

        """Method which which re-calculates the internal data of the class to reflect changes in external references
        """

        cls.updateSize()
        cls.updateCam()

    @classmethod
    def setShaders( cls ):
        cls.isShader = not cls.isShader


class Shader:

    def __init__( self, parent ):

        self.parent = parent

    def shadeRetro( self, index, top=True, down=True, left=True, right=True ):

        for c in range( 0, parent.length ):
            for i in range( 0, CHUNK_HEIGHT ):
                for j in range( 0, CHUNK_WIDTH ):

                    currTileRef = parent[index][i][j]
                    currWallRef = parent[index].walls[i][j]

                    selfLuminousity  = 0

                    # if(currTileRef > 0 or currWallRef == 0):    # Front tile is present or wall is absent
                    #     selfLuminousity = TILE_ATTR[currTileRef][LUMINOSITY]
                    # elif(currWallRef > 0):                      # Front tile is absent but wall is present
                    #     selfLuminousity = TILE_ATTR[currWallRef][LUMINOSITY]

                    selfLuminousity = tiles.TILE_ATTR[currTileRef][LUMINOSITY]
                    selfIllumination = self[index].lightMap[i][j]

                    if(selfLuminousity is not 0 and selfIllumination < selfLuminousity):
                        parent[index].lightMap[i][j] = selfLuminousity
                        self.propagateRetro(index, j, i)

    def propagateRetro( self, index, x, y, top=True, right=True, bottom=True, left=True ):

        if(index < 0): index = self.length+index

        topVal      =  self[index].lightMap[y][x]-16
        rightVal    =  self[index].lightMap[y][x]-16
        bottomVal   =  self[index].lightMap[y][x]-16
        leftVal     =  self[index].lightMap[y][x]-16

        if(topVal < 0): top=False
        if(rightVal < 0): right=False
        if(bottomVal < 0): bottom=False
        if(leftVal < 0): left=False

        # Top side
        if(top):
            if(y+1 < CHUNK_HEIGHT):         #check if the next position (1 above) is valid
                if(topVal > self[index].lightMap[y+1][x]):
                    self[index].lightMap[y+1][x]   =  topVal
                    self.propogateRetro(index, x, y+1, bottom=False)

        # Bottom side
        if(bottom):
            if(y-1 >= 0):                   #check if the next position (1 below) is valid
                if(bottomVal >= self[index].lightMap[y-1][x]):
                    self[index].lightMap[y-1][x]   =  bottomVal
                    self.propogateRetro(index, x, y-1, top=False)

        # Left side
        if(left):
            if(x-1 >= 0):                   #check if the next position (1 to the left) is valid
                if(leftVal > self[index].lightMap[y][x-1]):
                    self[index].lightMap[y][x-1]   =  leftVal
                    self.propogateRetro(index, x-1, y, right=False)

            elif(index-1 >= 0):             #check if previous chunk exists in the chunk buffer
                if(leftVal > self[index-1].lightMap[y][CHUNK_WIDTH-1]):
                    self[index-1].lightMap[y][CHUNK_WIDTH-1]   =  leftVal
                    self.propogateRetro(index-1, CHUNK_WIDTH-1, y, right=False)

        # Right side
        if(right):
            if(x+1 < CHUNK_WIDTH):          #check if the next position (1 to the right) is valid
                if(rightVal > self[index].lightMap[y][x+1]):
                    self[index].lightMap[y][x+1]   =  rightVal
                    self.propogateRetro(index, x+1, y, left=False)

            elif(index+1 < self.length):    #check if next chunk exists in the chunk buffer
                if(rightVal > self[index+1].lightMap[y][0]):
                    self[index+1].lightMap[y][0]   =  rightVal
                    self.propogateRetro(index+1, 0, y, left=False)

    def shadeRadial( self ):

        luminous = None # the luminosity of the block
        sq2 = 1.414
        for index in range(0, parent.length):
            currChunkRef = self.parent[index]
            for y in range(CHUNK_HEIGHT):
                for x in range(CHUNK_WIDTH):

                    currTileRef = parent[index][y][x]
                    currWallRef = parent[index].walls[y][x]

                    if( currTileRef is luminous or currWallRef is luminous):

                        propagateRadial( index, x, y, True, True, True, True)

                        # i, j = 1, 1
                        while( y-1-i>0 and x-1-i>0 ):   #up diagonal left
                            propagateRadial( index, x-1-i, y-1-i, up=True, left=True)

                        # i, j = 1, 1
                        while( y-1-i>0 and x+1+i<CHUNK_WIDTH ): #up diagonal right
                            propagateRadial( index, x+1+i, y-1-i, up=True, right=True)

                        # i, j = 1, 1
                        while( y+1+i<CHUNK_HEIGHT and x-1-i>0 ):    #down diagonal left
                            propagateRadial( index, x-1-i, y+1+i, down=True, left=True)

                        # i, j = 1, 1
                        while( y+1+i<CHUNK_HEIGHT and x+1+i<CHUNK_WIDTH ):  #down diagonal right
                            propagateRadial( index, x+1+i, y+1+i, down=True, right=True)

    def propagateRadial( self, index, x, y, up=False, down=False, left=False, right=False ):

        currChunkRef = self.parent[index]
        valid = True       #check if valid

        if valid and lightval != 0:
            if up:
                currChunkRef[y+1][x].lightval = 0.5    #some value
                propagateRadial(y+1, x, up=True)
            if down:
                currChunkRef[y-1][x].lightval = 0.5    #some value
                propagateRadial(y-1, x, down=True)
            if right:
                currChunkRef[y][x+1].lightval = 0.5    #some value
                propagateRadial(y, x+1, right=True)
            if left:
                currChunkRef[y][x-1].lightval = 0.5     #some value
                propagateRadial(y, x-1, left=True)

