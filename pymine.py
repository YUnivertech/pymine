from chunk import *
from entity import *
import time

key_states              = {}
button_states           = {}

# Screen variables
display_sz              = [ 1200 , 600 ]
framerate               = 0

# Create the main window
screen                  = pygame.display.set_mode( display_sz , pygame.RESIZABLE )
pygame.display.set_caption( "Pymine" )
pygame.display.set_icon( pygame.image.load( "Resources/Default/gameIcon.png" ) )

# Create GUI based menus
worlds = os.listdir("Worlds") + ['hello', 'bye']*3
gui_manager = pygame_gui.UIManager(display_sz)

# Start-up menu
def init_menu_1( display_size, _manager ):
    panel_topleft = ( 80 , 60 )
    panel_dim = ( display_size[0] - 160 , display_size[1] - 120 )
    panel_dim = (1000, 600)
    print(display_size, panel_dim)

    btn_topleft = ( 10 , 10 )
    btn_dim = ( 100 , 50 )

    # panel = UIPanel(pygame.Rect(( 100, 30 ), ( 200, 200 ) ), 1, gui_manager)
    panel = UIPanel( pygame.Rect( panel_topleft, panel_dim ), 1, _manager)
    btn = UIButton( pygame.Rect( btn_topleft, btn_dim ), 'Singleplayer' , _manager , panel)
    return panel, btn

# Singleplayer menu
def init_menu_2( display_size ):
    global gui_manager

    panel_topleft = ( 80 , 60 )
    panel_dim = ( display_size[0] - 80 , display_size[1] - 60 )

    panel = UIPanel( pygame.Rect( (100, 30), (200, 200) ), 1, gui_manager )
    pos = (25, 10)
    sel_list = UISelectionList( pygame.Rect( pos, (150, 100) ), worlds, gui_manager, container=panel )
    btn1 = UIButton( pygame.Rect( (50, 110), (100, 25) ), "Create", gui_manager, panel )
    btn2 = UIButton( pygame.Rect( (50, 140), (100, 25) ), "Delete", gui_manager, panel )
    btn3 = UIButton( pygame.Rect( (50, 170), (100, 25) ), "Back", gui_manager, panel )
    return panel, sel_list, btn1, btn2, btn3

# Create world menu
def init_menu_3( display_size ):
    panel = UIPanel( pygame.Rect( (100, 30), (200, 200) ), 1, gui_manager )
    text_entry = UITextEntryLine(pygame.Rect((25, 10), (150, 100)), gui_manager, panel)
    return panel, text_entry

# Delete world menu
def init_menu_4( display_size ):
    pass

menu_2, choice, btn_1, btn_2, btn_3 = None, None, None, None, None
menu_1, btn = init_menu_1(display_sz, gui_manager)

menu_background = pygame.Surface( display_sz )
menu_background.fill("#0000FF")

# menu_3 , entry = init_menu_3(display_sz)
running = True

while running:
    dt = clock.tick( 60 ) / 1000.0
    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            display_sz[0] , display_sz[1] = screen.get_width() , screen.get_height()

            menu_background = pygame.Surface( display_sz )
            menu_background.fill("#0000FF")

            gui_manager.set_window_resolution( display_sz )
            menu_1.kill()
            menu_1, btn = init_menu_1(display_sz, gui_manager)

        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == btn:
                    menu_1.kill()
                    menu_2, choice, btn_1, btn_2, btn_3 = init_menu_2(display_sz)
                elif event.ui_element == btn_1: # Create World button
                    pass
                elif event.ui_element == btn_2: # Delete World button
                    pass
                elif event.ui_element == btn_3: # Back button
                    menu_2.kill()
                    menu_1, btn = init_menu_1(display_sz)

            elif event.user_type == pygame_gui.UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION:
                if event.ui_element == choice:
                    print( 'Test button pressed', event.text )

        gui_manager.process_events( event )
    gui_manager.update(dt)
    screen.blit( menu_background , (0,0))
    gui_manager.draw_ui(screen)
    pygame.display.update()


# ---------- CREATION OF ALL MANAGERS ---------- #

# Chunk Buffer
buffer_width            = ( pygame.display.Info().current_w // CHUNK_WIDTH_P ) + 1
buffer_width            = buffer_width if buffer_width % 2 else buffer_width + 1
chunk_buffer            = ChunkBuffer( buffer_width )

# Entity Buffer
entity_buffer           = EntityBuffer( buffer_width )

# Player
player                  = Player()

# Renderer
renderer                = Renderer()

# Serializer
serializer              = Serializer()

# Camera
camera                  = [ 0, CHUNK_HEIGHT_P // 2 ]
prev_cam                = [ 0 , 0 ]
cam_bound               = True

# ---------- INITIALIZE MANAGERS ---------- #

# Chunk Buffer
chunk_buffer.initialize( entity_buffer , renderer , serializer , player , camera , screen )

# Entity Buffer
# entity_buffer.initialize( chunk_buffer , renderer , serializer , player , camera , screen )

# Player
player.initialize( chunk_buffer , renderer , serializer , entity_buffer , camera , screen )

# Renderer
renderer.initialize( entityBuffer , chunk_buffer , serializer , player , camera , screen , display_sz)

# Serializer
serializer.initialize()

# Main loop
running                 = True
prev                    = time.time()
dt                      = 0

curr_chunk              = 0
prev_chunk              = 0
delta_chunk             = 0

while running:

    for event in pygame.event.get():

        if      event.type == pygame.QUIT:      running = False

        elif    event.type == pygame.KEYDOWN:   key_states[event.key] = True
        elif    event.type == pygame.KEYUP:     key_states[event.key] = False

        elif    event.type == pygame.MOUSEMOTION:       pass
        elif    event.type == pygame.MOUSEBUTTONDOWN:   button_states[event.button] = True
        elif    event.type == pygame.MOUSEBUTTONUP:     button_states[event.button] = False

        elif    event.type == pygame.VIDEORESIZE:

            display_sz[0] , display_sz[1] = screen.get_width() , screen.get_height()
            renderer.update_size()


    now = time.time()
    dt = now - prev
    prev = now

    #     player.driveUpdate( dt )

    if cam_bound:
        camera[0] += ( player.pos[0] - camera[0] ) * LERP_C
        camera[1] += ( player.pos[1] - camera[1] ) * LERP_C
    else :
        pass # Move the camera around only

    renderer.update_camera()

    curr_chunk = math.floor( camera[0] / CHUNK_WIDTH_P )
    delta_chunk = curr_chunk - prev_chunk
    prev_chunk = curr_chunk

    if delta_chunk:
        pass # entity buffer and chunk_buffer must be notified

    pygame.display.update()


chunk_buffer.save()
player.save( serializer )
serializer.stop()
pygame.display.quit()

# ! ------------------------------
#             if      event.key == pygame.K_c :              Renderer.setShaders()
#             elif    event.key == pygame.K_n :              cameraBound = not cameraBound # This should free the camera from being fixed to the player
#             elif    event.key == pygame.K_SLASH :          takeCommand()
#             elif    event.key == pygame.K_e :              inventoryVisible = not inventoryVisible
#             elif    event.key == pygame.K_DOWN:            player.inventory.itemHeld[1] = (player.inventory.itemHeld[1] + 1) % INV_ROWS
#             elif    event.key == pygame.K_UP:              player.inventory.itemHeld[1] = (player.inventory.itemHeld[1] - 1 + INV_ROWS) % INV_ROWS
#             elif    event.key == pygame.K_RIGHT:           player.inventory.itemHeld[0] = (player.inventory.itemHeld[0] + 1) % INV_COLS
#             elif    event.key == pygame.K_LEFT:            player.inventory.itemHeld[0] = (player.inventory.itemHeld[0] - 1 + INV_COLS) % INV_COLS

#     if(deltaChunk != 0):
#         #eventHandler.chunkShiftFlag = True # server must be notified
#         chk_a = time.time()
#         eventHandler.loadChunkIndex = chunkBuffer.shiftBuffer(deltaChunk)
#         print(entityBuffer.entities)
#         entityBuffer.shift(deltaChunk)
#         print(entityBuffer.entities)
#         print('shift buffer time:', (time.time()-chk_a)*1000)
#         chk_a = time.time()
#         chunkBuffer[eventHandler.loadChunkIndex].draw()
#         print('draw time:', (time.time()-chk_a)*1000)
#         chk_a = time.time()
#         chunkBuffer.renderLightmap(eventHandler.loadChunkIndex)
#         print('render light time:', (time.time()-chk_a)*1000)
