from Chunk import *

class Renderer:
    @classmethod
    def initialize(cls, chunkBuffer, entityBuffer, camera, player, windowSize, screen):
        # Create references to global objects
        cls.chunkBuffer  = chunkBuffer
        cls.entityBuffer = entityBuffer
        cls.player       = player
        cls.camera       = camera
        cls.windowSize   = windowSize
        cls.screen       = screen

        # Index of the middle chunk in the chunk buffer
        cls.length       = cls.chunkBuffer.length
        cls.midChunk     = ( cls.length - 1 ) // 2

        # Update constants to reflect new References
        cls.updateRefs()

    @classmethod
    def updateScreen( cls ):
        rightWalker = cls.midChunk
        leftWalker  = cls.midChunk - 1

        # Loop to render chunks on the right of the camera (including the camera's chunk)
        while rightWalker < cls.length:
            tileWalker = 0
            # Loop to render each individual vertical slice of the chunk
            while tileWalker < CHUNK_WIDTH:
                sliceInd  = ( cls.chunkBuffer[rightWalker].index * CHUNK_WIDTH ) + tileWalker
                slicePos  = [sliceInd * TILE_WIDTH - cls.camera[0] + cls.numHor, 0]
                sliceRect = [tileWalker * TILE_WIDTH, cls.upIndex, TILE_WIDTH, cls.downIndex]
                sliceSurf = cls.chunkBuffer[rightWalker].surface.subsurface( sliceRect )
                if slicePos[0] > cls.windowSize[0]:
                    rightWalker = cls.length
                    break

                cls.screen.blit( sliceSurf, slicePos )

                tileWalker      += 1

            rightWalker     += 1

        # Loop to render chunks on the left of the camera (excluding the camera's chunk)
        while leftWalker >= 0:
            tileWalker = CHUNK_WIDTH - 1
            # Loop to render each individual vertical slice of the chunk
            while tileWalker >= 0:
                sliceInd  = ( cls.chunkBuffer[leftWalker].index * CHUNK_WIDTH ) + tileWalker
                slicePos  = [sliceInd * TILE_WIDTH - cls.camera[0] + cls.numHor, 0]
                sliceRect = [tileWalker * TILE_WIDTH, cls.upIndex, TILE_WIDTH, cls.downIndex]
                sliceSurf = cls.chunkBuffer[leftWalker].surface.subsurface( sliceRect )
                if slicePos[0] < -TILE_WIDTH:
                    leftWalker = -1
                    break

                cls.screen.blit( sliceSurf, slicePos )

                tileWalker -= 1

            leftWalker -= 1

        # Temporary player crosshair rendering
        playerCoors     = [cls.player.pos[0], cls.player.pos[1]]
        # Translate to be in camera space
        playerCoors[0] -= cls.camera[0]
        playerCoors[1] -= cls.camera[1]
        # Translate to be in screen space
        playerCoors[0] += cls.numHor
        playerCoors[1]  = cls.numVer - playerCoors[1]
        item            = cls.player.inventory.getSelectedItem()
        name, quantity  = 'Nothing', cls.player.inventory.getSelectedQuantity()
        if item and tiles.TILE_NAMES.get( item, None ):
            name = tiles.TILE_NAMES[item]

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
    def updateSize( cls ):
        cls.numHor = cls.windowSize[0] // 2
        cls.numVer = cls.windowSize[1] // 2

    @classmethod
    def updateCam( cls ):
        cls.upIndex = CHUNK_HEIGHT_P - ( cls.camera[1] + cls.numVer )
        if cls.upIndex < 0: cls.upIndex = 0
        cls.downIndex = CHUNK_HEIGHT_P - cls.upIndex
        if cls.downIndex > cls.windowSize[1]: cls.downIndex = cls.windowSize[1]

    @classmethod
    def updateRefs( cls ):
        cls.updateSize()
        cls.updateCam()
