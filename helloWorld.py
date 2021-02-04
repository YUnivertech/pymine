import sys
# from pygame.locals import *
# import pygame.locals
from Renderer import *
import time
import entity

# Screen variables
displaySize = [400, 300]
framerate = 0

# Camera variables
#camera = pygame.math.Vector2([0, CHUNK_HEIGHT_P//2])
camera = [0, CHUNK_HEIGHT_P//2]
prevCamera = [0, 0]
cameraBound = True

# Create chunk buffer and chunk-position buffer
bufferWidth = 1 + (pygame.display.Info().current_w//CHUNK_WIDTH_P) + 1
if(bufferWidth % 2 == 0): bufferWidth += 1
chunkBuffer = ChunkBuffer(bufferWidth, 0, "world1")
print(bufferWidth)
del bufferWidth

# Create and display window
screen = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
pygame.display.set_caption("Hello World!")
pygame.display.set_icon(pygame.image.load("Resources/Default/gameIcon.png"))

# Convert all images to optimized form
tiles.loadImageTable()
items.loadImageTable()

for i in range(len(chunkBuffer)):
    chunkBuffer[i].draw()
    chunkBuffer.renderLightmap(i)

# Input handling containers
eventHandler = entity.ClientEventHandler()

# Player variables
player = entity.Player(screen, [0, 3000], chunkBuffer, eventHandler, eventHandler.keyStates, eventHandler.mouseState, eventHandler.cursorPos, DEFAULT_FRICTION)
currChunk = prevChunk = deltaChunk = 0
inventoryVisible = False

# Initialize the renderer
Renderer.initialize(chunkBuffer, camera, player, displaySize, screen)

def takeCommand( ):
    global cameraBound
    command = input(">> ")
    command = command.split()

    if(command[0] == 'add'):
        player.inventory.addItem(eval(command[1], globals(), locals()), eval(command[2]))
        player.inventory.draw()


# game loop
prev = time.time()
dt = 0
running = True

while running:
#!------------------------------------------------------------------------------------------------------------------------------------------------------

    # event handling loop
    for event in pygame.event.get():

        if(event.type == pygame.QUIT):
            running = False

        elif(event.type == pygame.KEYDOWN):

            if      event.key == pygame.K_c :              Renderer.setShaders()
            elif    event.key == pygame.K_n :              cameraBound = not cameraBound # This should free the camera from being fixed to the player
            elif    event.key == pygame.K_SLASH :          takeCommand()
            elif    event.key == pygame.K_e :              inventoryVisible = not inventoryVisible
            else :                                         eventHandler.addKey( event.key )

        elif    event.type == pygame.KEYUP :               eventHandler.remKey( event.key )

        elif    event.type == pygame.MOUSEMOTION :         eventHandler.addMouseMotion( event, camera, displaySize )

        elif    event.type == pygame.MOUSEBUTTONDOWN :     eventHandler.addMouseButton( event.button )

        elif    event.type == pygame.MOUSEBUTTONUP :       eventHandler.remMouseButton( event.button )

        elif    event.type == pygame.VIDEORESIZE :         eventHandler.addWindowResize( )


    if cameraBound:
        player.run()
        camera[0] += ( player.pos[0] - camera[0] ) * LERP_C
        camera[1] += ( player.pos[1] - camera[1] ) * LERP_C


    else:
        if      eventHandler.keyStates[pygame.K_a]  : camera[0] -= SCALE_VEL * dt
        elif    eventHandler.keyStates[pygame.K_d]  : camera[0] += SCALE_VEL * dt

        if      eventHandler.keyStates[pygame.K_w]  : camera[1] += SCALE_VEL * dt
        elif    eventHandler.keyStates[pygame.K_s]  : camera[1] -= SCALE_VEL * dt

    now = time.time( )
    dt = now - prev
    prev = now
    if dt >= 0.15: print('dt:', dt)
    player.driveUpdate( dt )

    Renderer.updateCam()

    currChunk = math.floor(camera[0]/CHUNK_WIDTH_P)
    deltaChunk = currChunk - prevChunk
    prevChunk = currChunk

    if(deltaChunk != 0):
        #eventHandler.chunkShiftFlag = True # server must be notified
        chk_a = time.time()
        eventHandler.loadChunkIndex = chunkBuffer.shiftBuffer(deltaChunk)
        print('shift buffer time:', (time.time()-chk_a)*1000)
        chk_a = time.time()
        chunkBuffer[eventHandler.loadChunkIndex].draw()
        print('draw time:', (time.time()-chk_a)*1000)
        chk_a = time.time()
        chunkBuffer.renderLightmap(eventHandler.loadChunkIndex)
        print('render light time:', (time.time()-chk_a)*1000)

    if eventHandler.tileBreakFlag :
        chunkBuffer[eventHandler.tileBreakIndex].draw((eventHandler.tileBreakPos[0], eventHandler.tileBreakPos[1], eventHandler.tileBreakPos[0] + 1, eventHandler.tileBreakPos[1] + 1))
        eventHandler.tileBreakFlag = False

    if eventHandler.tilePlaceFlag :
        chunkBuffer[eventHandler.tilePlaceIndex].draw((eventHandler.tilePlacePos[0], eventHandler.tilePlacePos[1], eventHandler.tilePlacePos[0] + 1, eventHandler.tilePlacePos[1] + 1))
        eventHandler.tilePlaceFlag = False

    if(eventHandler.windowResizeFlag):

        displaySize[0] = screen.get_width()
        displaySize[1] = screen.get_height()

        Renderer.updateRefs()

        eventHandler.windowResizeFlag = False

    Renderer.updateScreen()

    if(inventoryVisible):   player.inventory.draw()

    pygame.display.update()     # Updating the screen

    # Framerate calculation

    #framerate = 1 / max(dt, 0.001)
    #print(framerate)


chunkBuffer.saveComplete()
chunkBuffer.serializer.stop()
pygame.display.quit()
