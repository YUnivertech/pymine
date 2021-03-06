from Old.Chunk import *


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
    def initialize(cls, chunkBuffer, entityBuffer, camera, player, windowSize, screen):

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
        cls.entityBuffer    =  entityBuffer

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

    @classmethod
    def updateScreen(  cls  ):

        """Renders the surfaces of each chunk (in the active chunk buffer) on to the window
        """

        rightWalker     =  cls.midChunk        # Goes from the index of the middle chunk to the right-most chunk
        leftWalker      =  cls.midChunk - 1    # Goes from the index of the chunk one before the middle to the left-most chunk

        # Loop to render chunks on the right of the camera (including the camera's chunk)
        while rightWalker < cls.length:

            tileWalker      =  0    # Goes from the index of the left-most to the right-most tile in the chunk

            # Loop to render each individual vertical slice of the chunk
            while tileWalker < CHUNK_WIDTH:

                sliceInd        =  ( cls.chunkBuffer[rightWalker].index * CHUNK_WIDTH ) + tileWalker   # Absoulute index of the current vertical slice
                slicePos        =  [sliceInd * TILE_WIDTH - cls.camera[0] + cls.numHor, 0]             # List containing the coordinates where the slice must be blitted on-screen

                sliceRect       =  [tileWalker * TILE_WIDTH, cls.upIndex, TILE_WIDTH, cls.downIndex]   # Rectangular region containing the "visible" area of the chunk's surface
                sliceSurf       =  cls.chunkBuffer[rightWalker].surface.subsurface( sliceRect )       # Mini-surface containing the visible region of the chunk's surface
                lightSurf       =  cls.chunkBuffer.lightSurfs[rightWalker].subsurface( sliceRect )      # Mini-surface containing the visible region of the chunk's lightmap

                if slicePos[0] > cls.windowSize[0]:     # Stop blitting if slice is beyond the right edge od the window
                    rightWalker     =  cls.length
                    break

                cls.screen.blit( sliceSurf, slicePos )
                if cls.isShader:
                    cls.screen.blit( lightSurf, slicePos, special_flags = pygame.BLEND_RGBA_MULT )
                tileWalker      += 1

            rightWalker     += 1

        # Loop to render chunks on the left of the camera (excluding the camera's chunk)
        while leftWalker >= 0:

            tileWalker      =  CHUNK_WIDTH - 1    # Goes from the index of the left-most to the right-most tile in the chunk

            # Loop to render each individual vertical slice of the chunk
            while tileWalker >= 0:

                sliceInd        =  ( cls.chunkBuffer[leftWalker].index * CHUNK_WIDTH ) + tileWalker     # Absoulute index of the current vertical slice
                slicePos        =  [sliceInd * TILE_WIDTH - cls.camera[0] + cls.numHor, 0]              # List containing the coordinates where the slice must be blitted on-screen

                sliceRect       =  [tileWalker * TILE_WIDTH, cls.upIndex, TILE_WIDTH, cls.downIndex]    # Rectangular region containing the "visible" area of the chunk's surface
                sliceSurf       =  cls.chunkBuffer[leftWalker].surface.subsurface( sliceRect )         # Mini-surface containing the visible region of the chunk's surface
                lightSurf       =  cls.chunkBuffer.lightSurfs[leftWalker].subsurface( sliceRect )       # Mini-surface containing the visible region of the chunk's lightmap

                if slicePos[0] < -TILE_WIDTH:    # Stop blitting if slice is bryond the left edge of the window
                    leftWalker      =  -1
                    break

                cls.screen.blit ( sliceSurf, slicePos )
                if cls.isShader:
                    cls.screen.blit( lightSurf, slicePos, special_flags = pygame.BLEND_RGBA_MULT )
                tileWalker      -= 1

            leftWalker      -= 1

        # Temporary player crosshair rendering
        playerCoors = [cls.player.pos[0], cls.player.pos[1]]

        # Translate to be in camera space
        playerCoors[0] -= cls.camera[0]
        playerCoors[1] -= cls.camera[1]

        # Translate to be in screen space
        playerCoors[0] += cls.numHor
        playerCoors[1] =  cls.numVer - playerCoors[1]

        item = cls.player.inventory.getSelectedItem()
        name, quantity = 'Nothing', cls.player.inventory.getSelectedQuantity()
        if item:
            if tiles.TILE_NAMES.get( item, None ):
                name = tiles.TILE_NAMES[item]
            elif items.ITEM_NAMES.get( item, None ):
                name = items.ITEM_NAMES[item]

        if name != 'Nothing': name += '  ' + str( quantity )
        toShow, rect = SC_DISPLAY_FONT.render( name , (0, 0, 0) )
        xVal = cls.screen.get_width() - toShow.get_width() - 8
        cls.screen.blit(toShow, [xVal, 16])

        # ! temporary rendering of player crosshair
        pygame.draw.rect(cls.screen, (255,50,50), pygame.Rect(playerCoors[0]-PLYR_WIDTH//2, playerCoors[1]-PLYR_HEIGHT//2, PLYR_WIDTH, PLYR_HEIGHT))
        cls.entityBuffer.draw()
        for group in cls.entityBuffer.entities:
            for entity in group:
                coors = entity.surfPos()
                coors[1] -= cls.camera[1]
                coors[1] = cls.numVer - coors[1]
                coors[0] += cls.numHor - cls.camera[0]
                cls.screen.blit( entity.surf, coors )

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

        if cls.upIndex < 0:    # If lower than zero, then make 0
            cls.upIndex     =  0

        # Height of the visible region of the slice
        cls.downIndex   =  CHUNK_HEIGHT_P - cls.upIndex

        if cls.downIndex > cls.windowSize[1]:    # If greater than height-of-window, then make height-of-window
            cls.downIndex   =  cls.windowSize[1]

    @classmethod
    def updateRefs(  cls  ):

        """Method which which re-calculates the internal data of the class to reflect changes in external references
        """

        cls.updateSize()
        cls.updateCam()