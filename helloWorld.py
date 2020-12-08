import sys
from pygame.locals import *
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

# Initialize pygame and start clock
pygame.init()
clock = pygame.time.Clock()

# Create and display window
screen = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
pygame.display.set_caption("Hello World!")
pygame.display.set_icon(pygame.image.load("Resources/Default/gameIcon.png"))

# Convert all images to optimized form
tiles.loadImageTable()
items.loadImageTable()

# Create chunk buffer and chunk-position buffer
chunkBuffer = ChunkBuffer(11, 0, "world1")

# Input handling containers
eventHandler = entity.ClientEventHandler()

# Player variables
player = entity.Player([0, 0], chunkBuffer, eventHandler, eventHandler.keyStates, eventHandler.mouseState, eventHandler.cursorPos, DEFAULT_FRICTION)
currChunk = prevChunk = deltaChunk = 0

# Initialize the renderer
Renderer.initialize(chunkBuffer, camera, player, displaySize, screen)
dt = 0

def takeCommand( ):
    global cameraBound
    command = input(">> ")

    what = ""
    cntr = 4
    for i in command[4::]:
        cntr += 1
        if(i == ' '): break
        what = what + i

    if(what == "shader"):
        if(command[0] == 's'):
            Renderer.isShader = exec(command[cntr::])
        elif(command[0] == 'g'):
            print(Renderer.isShader)
    elif(what == "cameraRoam"):
        if(command[0] == 's'):
            cameraBound = exec(command[cntr::])
        elif(command[0] == 'g'):
            print(not cameraBound)

# game loop

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
            else :                                         eventHandler.addKey( event.key )

        elif    event.type == pygame.KEYUP :               eventHandler.remKey( event.key )

        elif    event.type == pygame.MOUSEMOTION :         eventHandler.addMouseMotion( event, camera, displaySize )

        elif    event.type == pygame.MOUSEBUTTONDOWN :     eventHandler.addMouseButton( event.button )

        elif    event.type == pygame.MOUSEBUTTONUP :       eventHandler.remMouseButton( event.button )

        elif    event.type == pygame.VIDEORESIZE :         eventHandler.addWindowResize( )

    # Player movement handling
    if  eventHandler.keyInFlag or eventHandler.mouseInFlag :

        if cameraBound:
            player.run()
            #if(player.inventory.isEnabled): Renderer.renderInv()

        else:
            if      eventHandler.keyStates[pygame.K_a]  : camera[0] -= SCALE_VEL * dt
            elif    eventHandler.keyStates[pygame.K_d]  : camera[0] += SCALE_VEL * dt

            if      eventHandler.keyStates[pygame.K_w]  : camera[1] += SCALE_VEL * dt
            elif    eventHandler.keyStates[pygame.K_s]  : camera[1] -= SCALE_VEL * dt

            eventHandler.addCameraMotion()

        eventHandler.mouseInFlag, eventHandler.keyinFlag = False, False

    # camera movement handling
    if  cameraBound :
        camera[0] += ( player.pos[0] - camera[0] ) * LERP_C
        camera[1] += ( player.pos[1] - camera[1] ) * LERP_C

        if  int(prevCamera[0] - camera[0]) or int(prevCamera[1] - camera[1])    : eventHandler.addCameraMotion()

    player.update( dt )

    if eventHandler.tileBreakFlag :
        chunkBuffer[eventHandler.tileBreakIndex].draw((eventHandler.tileBreakPos[0], eventHandler.tileBreakPos[1], eventHandler.tileBreakPos[0] + 1, eventHandler.tileBreakPos[1] + 1))
        Renderer.updateScreen()
        eventHandler.tileBreakFlag = False

    elif eventHandler.tilePlaceFlag :
        Renderer.renderChunk( eventHandler.tilePlaceIndex, (eventHandler.tilePlacePos[0] - 2, eventHandler.tilePlacePos[1] - 2, eventHandler.tileBreakPos[0]  + 2, eventHandler.tilePlacePos[1] + 2) )
        Renderer.updateScreen()
        eventHandler.tilePlaceFlag = False

    if(eventHandler.cameraMovementFlag):

        Renderer.updateCam()
        Renderer.updateScreen()

        prevCamera[0], prevCamera[1] = camera[0], camera[1]

        currChunk = math.floor(camera[0]/CHUNK_WIDTH_P)
        deltaChunk = currChunk - prevChunk
        prevChunk = currChunk

        if(deltaChunk != 0):

            #eventHandler.chunkShiftFlag = True # server must be notified
            eventHandler.loadChunkIndex = chunkBuffer.shiftBuffer(deltaChunk)
            chunkBuffer[eventHandler.loadChunkIndex].draw()

        eventHandler.cameraMovementFlag = False

    if(eventHandler.windowResizeFlag):

        displaySize[0] = screen.get_width()
        displaySize[1] = screen.get_height()

        Renderer.updateRefs()
        Renderer.updateScreen()

        eventHandler.windowResizeFlag = False

    pygame.display.update()     # Updating the screen

    # Framerate calculation
    dt = clock.tick(0) / 1000
    #framerate = 1 / max(dt, 0.001)
    #print(framerate)


chunkBuffer.saveComplete()
chunkBuffer.serializer.stop()
pygame.display.quit()
