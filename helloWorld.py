import time, pygame_gui, entity
from pygame_gui.elements import UIButton
from pygame_gui.elements.ui_text_box import UITextBox
from Renderer import *

# Screen variables
displaySize = [400, 300]
framerate   = 0

# Camera variables
camera      = [0, CHUNK_HEIGHT_P//2]
prevCamera  = [0, 0]
cameraBound = True

# Create chunk buffer and chunk-position buffer
bufferWidth = 1 + (pygame.display.Info().current_w//CHUNK_WIDTH_P) + 1
if bufferWidth % 2 == 0: bufferWidth += 1
chunkBuffer = ChunkBuffer(bufferWidth, 0, "world1")
del bufferWidth
entityBuffer = entity.EntityBuffer(chunkBuffer, chunkBuffer.serializer, None)
chunkBuffer.entityBuffer = entityBuffer

# Create and display window
screen = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
pygame.display.set_caption("Hello World!")
pygame.display.set_icon(pygame.image.load("Resources/Default/gameIcon.png"))

# Convert all images to optimized form
tiles.loadImageTable()
# items.loadImageTable()

for i in range(len(chunkBuffer)):
    chunkBuffer[i].draw()

# Input handling containers
eventHandler = entity.ClientEventHandler()

# Player variables
player = entity.Player(screen, [0, 3000], chunkBuffer, entityBuffer, eventHandler, eventHandler.keyStates, eventHandler.mouseState, eventHandler.cursorPos, DEFAULT_FRICTION)
player.load(chunkBuffer.serializer)
currChunk = prevChunk = deltaChunk = 0
inventoryVisible = False
entityBuffer.plyr = player

# Initialize the renderer
Renderer.initialize(chunkBuffer, entityBuffer, camera, player, displaySize, screen)

def takeCommand( ):
    global cameraBound
    command = input(">> ")
    command = command.split()
    if command[0] == 'add':
        player.inventory.addItem(eval(command[1], globals(), locals()), eval(command[2]))
    elif command[0] == 'rem':
        player.inventory.remItemStack(eval(command[1], globals(), locals()), eval(command[2]))

# game loop
prev = time.time()
dt = 0
running = True

def ui_init( displaySize ):
    manager = pygame_gui.UIManager(displaySize, 'theme.json')
    pos = (displaySize[0]-30, 40)
    btn = UIButton(pygame.Rect(pos, (25, 25)), "i", manager, object_id="Testbutton", tool_tip_text="Game Details")
    box_pos = (displaySize[0]//2 - 100, displaySize[1]//2 - 105)
    text = "A - Move left<br>D - Move right<br>W - Jump<br>Left click - break<br>Middle click - place<br>E - Toggle inventory<br>Arrow keys - move in the inventory to select item"
    text_box = UITextBox(text, pygame.Rect(box_pos, (200 , 210)), manager )
    return tuple((manager, pos, btn, box_pos, text_box))

gui_manager, btn_pos, info_btn, textbox_pos, textbox = ui_init(displaySize)
textbox.kill()
textbox_state = False

while running:
    # event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == info_btn:
                    textbox_state = not textbox_state
                    if textbox_state:
                        gui_manager, btn_pos, info_btn, textbox_pos, textbox = ui_init(displaySize)
                    else:
                        textbox.kill()
        elif event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_SLASH: takeCommand()
            elif event.key == pygame.K_e:     inventoryVisible = not inventoryVisible
            elif event.key == pygame.K_DOWN:  player.inventory.itemHeld[1] = (player.inventory.itemHeld[1] + 1) % INV_ROWS
            elif event.key == pygame.K_UP:    player.inventory.itemHeld[1] = (player.inventory.itemHeld[1] - 1 + INV_ROWS) % INV_ROWS
            elif event.key == pygame.K_RIGHT: player.inventory.itemHeld[0] = (player.inventory.itemHeld[0] + 1) % INV_COLS
            elif event.key == pygame.K_LEFT:  player.inventory.itemHeld[0] = (player.inventory.itemHeld[0] - 1 + INV_COLS) % INV_COLS
            else:                             eventHandler.addKey( event.key )

        elif event.type == pygame.KEYUP:           eventHandler.remKey( event.key )
        elif event.type == pygame.MOUSEMOTION:     eventHandler.addMouseMotion( event, camera, displaySize )
        elif event.type == pygame.MOUSEBUTTONDOWN: eventHandler.addMouseButton( event.button )
        elif event.type == pygame.MOUSEBUTTONUP:   eventHandler.remMouseButton( event.button )
        elif event.type == pygame.VIDEORESIZE:
            eventHandler.addWindowResize( )
            gui_manager, btn_pos, info_btn, textbox_pos, textbox = ui_init( (screen.get_width(), screen.get_height()) )
            if not textbox_state: textbox.kill()

        gui_manager.process_events(event)
    if cameraBound:
        player.run()
        camera[0] += ( player.pos[0] - camera[0] ) * LERP_C
        camera[1] += ( player.pos[1] - camera[1] ) * LERP_C
        eventHandler.cameraMovementFlag = True
    else:
        if eventHandler.keyStates[pygame.K_a]  : camera[0] -= SCALE_VEL * dt
        elif eventHandler.keyStates[pygame.K_d]  : camera[0] += SCALE_VEL * dt

        if eventHandler.keyStates[pygame.K_w]  : camera[1] += SCALE_VEL * dt
        elif eventHandler.keyStates[pygame.K_s]  : camera[1] -= SCALE_VEL * dt
        eventHandler.cameraMovementFlag = True

    now = time.time( )
    dt = now - prev
    prev = now
    player.driveUpdate( dt )
    Renderer.updateCam()
    currChunk = math.floor(camera[0]/CHUNK_WIDTH_P)
    deltaChunk = currChunk - prevChunk
    prevChunk = currChunk
    if deltaChunk != 0:
        # eventHandler.chunkShiftFlag = True # server must be notified
        eventHandler.loadChunkIndex = chunkBuffer.shiftBuffer(deltaChunk)
        entityBuffer.shift(deltaChunk)
        chunkBuffer[eventHandler.loadChunkIndex].draw()

    if eventHandler.tileBreakFlag :
        chunkBuffer[eventHandler.tileBreakIndex].draw((eventHandler.tileBreakPos[0], eventHandler.tileBreakPos[1], eventHandler.tileBreakPos[0] + 1, eventHandler.tileBreakPos[1] + 1))
        eventHandler.tileBreakFlag = False

    if eventHandler.tilePlaceFlag :
        chunkBuffer[eventHandler.tilePlaceIndex].draw((eventHandler.tilePlacePos[0], eventHandler.tilePlacePos[1], eventHandler.tilePlacePos[0] + 1, eventHandler.tilePlacePos[1] + 1))
        eventHandler.tilePlaceFlag = False

    if eventHandler.windowResizeFlag:
        displaySize[0] = screen.get_width()
        displaySize[1] = screen.get_height()
        Renderer.updateRefs()
        eventHandler.windowResizeFlag = False

    if eventHandler.cameraMovementFlag: Renderer.updateScreen( )
    if inventoryVisible:   player.inventory.draw( )
    gui_manager.update(dt)
    gui_manager.draw_ui(screen)
    pygame.display.update()     # Updating the screen

chunkBuffer.saveComplete()
player.save(chunkBuffer.serializer)
chunkBuffer.serializer.stop()
pygame.display.quit()
