from Chunk import *

'''
Translations
    From                        To
1   array-space                 chunk-space
    coordinates in the array    coordinates in the chunk
2   chunk-space                 world-space
    coordinates in the chunk    coordinates in the world (absolute coordinates)
3   world-space                 camera-space
    coordinates in the world    coordinates relative to camera
4   camera-space                screen-space
    coordinates in the array    coordinates on the display
'''

chunkBuffer = None
player = None
camera = None
displaySize = None
screen = None
midpoint = None
upperIndex = None
lowerIndex = None
numLeft = None
numRight = None


def initialize(achunkBuffer, acamera, aplayer, adisplaySize, ascreen):
    global chunkBuffer, player, camera, displaySize, screen
    chunkBuffer, player, camera, displaySize, screen = achunkBuffer, aplayer, acamera, adisplaySize, ascreen

    updateRefs()


def render():
    """
        Renders given chunks onto given surface
        Requires chunks, cameraCoors, playerCoors, displaySize as sequences
    """
    global chunkBuffer, player, camera, displaySize, screen
    rects = []

    rightWalker = midpoint  # goes from midpoint to length-1 (both inclusive)
    leftWalker = midpoint - 1  # goes from midpoint-1 to 0 (both inclusive)

    numRightDone = numLeftDone = 0
    coors = [0, 0]

    screen.fill((30, 175, 250))

    flag = True
    while flag:
        absoluteChunkIndex = chunkBuffer.positions[leftWalker]
        curChunkRef = chunkBuffer[leftWalker]
        leftWalker -= 1

        for j in range(CHUNK_WIDTH - 1, -1, -1):
            coors[0] = arrayToScreen_x(j, absoluteChunkIndex)

            for i in range(lowerIndex, upperIndex + 1):
                coors[1] = arrayToScreen_y(i) - TILE_WIDTH
                curTileRef = curChunkRef.blocks[i][j]

                if curTileRef is not 0: rects.append(screen.blit(TILE_TABLE[curTileRef], coors))

            numLeftDone += 1
            if numLeftDone > numLeft:
                flag = False
                break

    flag = True
    while flag:
        absoluteChunkIndex = chunkBuffer.positions[rightWalker]
        curChunkRef = chunkBuffer[rightWalker]
        rightWalker += 1

        for j in range(0, CHUNK_WIDTH):
            coors[0] = arrayToScreen_x(j, absoluteChunkIndex)

            for i in range(lowerIndex, upperIndex + 1):
                coors[1] = arrayToScreen_y(i) - TILE_WIDTH
                curTileRef = curChunkRef.blocks[i][j]

                if curTileRef is not 0: rects.append(screen.blit(TILE_TABLE[curTileRef], coors))

            numRightDone += 1
            if numRightDone > numRight:
                flag = False
                break

    # Temporary player crosshair rendering

    playercoors = player.copy()
    graphToCamera(playercoors)
    cameraToScreen(playercoors)

    rects.append(pygame.draw.circle(screen, (255, 50, 50), playercoors, 2))
    return rects


def arrayToChunk_x(x):
    return x * TILE_WIDTH


def arrayToChunk_y(y):
    return y * TILE_WIDTH


def chunkToGraph_x(x, chunkInd):
    # From chunk-space to absolute-space
    return x + chunkInd * CHUNK_WIDTH * TILE_WIDTH


def chunkToGraph_y(y):
    # From chunk-space to absolute-space
    # Redundant function
    return y


def graphToCamera_x(x):
    # From absolute-space to camera-space
    return x - camera[0]


def graphToCamera_y(y):
    # From absolute-space to camera-space
    return y - camera[1]


def cameraToScreen_x(x):
    # From camera-space to screen-space
    return x + displaySize[0] * 0.5


def cameraToScreen_y(y):
    # From camera-space to screen-space
    return displaySize[1] * 0.5 - y


def arrayToScreen_x(x, chunkInd):
    return cameraToScreen_x(graphToCamera_x(chunkToGraph_x(arrayToChunk_x(x), chunkInd)))


def arrayToScreen_y(y):
    return cameraToScreen_y(graphToCamera_y(arrayToChunk_y(y)))


def arrayToChunk(coor):
    # From array-space to chunk-space
    coor[0] *= TILE_WIDTH
    coor[1] *= TILE_WIDTH


def chunkToGraph(coor, chunkInd):
    # From chunk-space to absolute-space
    coor[0] += (chunkInd * CHUNK_WIDTH * TILE_WIDTH)
    coor[1] = coor[1]


def graphToCamera(coor):
    # From absolute-space to camera-space
    coor[0] -= camera[0]
    coor[1] -= camera[1]


def cameraToScreen(coor):
    # From camera-space to screen-space
    coor[0] += displaySize[0] * 0.5
    coor[1] = displaySize[1] * 0.5 - coor[1]


def chunkToScreen(coor, chunkInd):
    arrayToChunk(coor)
    chunkToGraph(coor, chunkInd)
    graphToCamera(coor)
    cameraToScreen(coor)


def updateSize():
    global midpoint, numRight, numLeft, displaySize, chunkBuffer
    midpoint = int((len(chunkBuffer) - 1) * 0.5)

    numRight = (displaySize[0] * 0.5) / TILE_WIDTH + CHUNK_WIDTH
    numLeft = (displaySize[0] * 0.5) / TILE_WIDTH


def updateCam():
    global lowerIndex, upperIndex, camera, displaySize
    lowerIndex = int(max((camera[1] - displaySize[1] * 0.5) / TILE_WIDTH, 0))
    upperIndex = int(min((camera[1] + displaySize[1] * 0.5) / TILE_WIDTH, CHUNK_HEIGHT - 1))


def updateRefs():
    global midpoint, numRight, numLeft, lowerIndex, upperIndex, camera, chunkBuffer, displaySize
    midpoint = int((len(chunkBuffer) - 1) * 0.5)

    numRight = (displaySize[0] * 0.5) / TILE_WIDTH + CHUNK_WIDTH
    numLeft = (displaySize[0] * 0.5) / TILE_WIDTH

    lowerIndex = int(max((camera[1] - displaySize[1] * 0.5) / TILE_WIDTH, 0))
    upperIndex = int(min((camera[1] + displaySize[1] * 0.5) / TILE_WIDTH, CHUNK_HEIGHT - 1))
