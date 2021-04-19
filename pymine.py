from chunk import *
from entity import *
import time

key_states              = {}
button_states           = {}
mouse_pos               = [ 0 , 0 ]
cursor_pos              = [ 0 , 0 ]

# Screen variables
display_sz              = ( 800 , 600 )
framerate               = 0

# Create the main window
screen                  = pygame.display.set_mode( display_sz , pygame.RESIZABLE )
pygame.display.set_caption( "Pymine" )
pygame.display.set_icon( pygame.image.load( "Resources/Default/gameIcon.png" ) )

populate_key_states( key_states , button_states )

# Create GUI based menus
if not os.path.isdir("Worlds"): os.mkdir("Worlds") # Create worlds folder if it doesnt exist
worlds = os.listdir("Worlds")
for i in range(len(worlds)): worlds[i] = worlds[:-3] # remove .db extension
gui_manager = pygame_gui.UIManager(display_sz, "temptheme.json")

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

# Main Game function
def main_game_start( _world = 'World1' ):

    global key_states , button_states
    global display_sz , screen
    global framerate

    # ---------- CREATION OF ALL MANAGERS ---------- #

    # Chunk Buffer
    buffer_width            = ( pygame.display.Info().current_w // CHUNK_WIDTH_P ) + 1
    buffer_width            = buffer_width if buffer_width % 2 else buffer_width + 1
    chunk_buffer            = ChunkBuffer( buffer_width )

    # Entity Buffer
    entity_buffer           = EntityBuffer( buffer_width )

    # Player
    # player                  = Player( screen , pos , chunk_buffer , entity_buffer , key_states , button_states , [] )
    player = None

    # Renderer
    renderer                = Renderer()

    # Serializer
    serializer              = Serializer( _world )

    # Camera
    camera                  = [ 0, CHUNK_HEIGHT_P // 2 ]
    prev_cam                = [ 0 , 0 ]
    cam_bound               = False

    # ---------- INITIALIZE MANAGERS ---------- #

    # Chunk Buffer
    chunk_buffer.initialize( entity_buffer , renderer , serializer , player , camera , screen )

    # Entity Buffer
    # entity_buffer.initialize( chunk_buffer , renderer , serializer , player , camera , screen )

    # Player
    # player.initialize( chunk_buffer , renderer , serializer , entity_buffer , camera , screen )

    # Renderer
    renderer.initialize( chunk_buffer , entity_buffer , player , serializer , camera , screen , display_sz)

    # Serializer
    # serializer.initialize()

    # Main loop
    running                 = True
    prev                    = time.time()
    dt                      = 0

    curr_chunk              = 0
    prev_chunk              = 0
    delta_chunk             = 0

    running = True

    while running:

        for event in pygame.event.get():

            if      event.type == pygame.QUIT:      running = False

            elif    event.type == pygame.KEYDOWN:   key_states[event.key] = True
            elif    event.type == pygame.KEYUP:     key_states[event.key] = False

            elif    event.type == pygame.MOUSEMOTION:

                mouse_pos[0]    = event.pos[0]
                mouse_pos[1]    = event.pos[1]

                cursor_pos[0]   = int( camera[0] ) + mouse_pos[0] - ( display_sz[0] >> 1)
                cursor_pos[1]   = int( camera[1] ) - mouse_pos[1] + ( display_sz[1] >> 1)


            elif    event.type == pygame.MOUSEBUTTONDOWN:   button_states[event.button] = True
            elif    event.type == pygame.MOUSEBUTTONUP:     button_states[event.button] = False
            elif    event.type == pygame.MOUSEWHEEL:        pass

            elif    event.type == pygame.VIDEORESIZE:

                display_sz[0]   = screen.get_width()
                display_sz[1]   = screen.get_height()

                renderer.update_size()

        try:
            if      key_states[pygame.K_c] :              Renderer.setShaders()
            elif    key_states[pygame.K_n] :              cam_bound = not cam_bound
            elif    key_states[pygame.K_e] :              inventoryVisible = not inventoryVisible
            elif    key_states[pygame.K_DOWN]:            player.inventory.itemHeld[1] = (player.inventory.itemHeld[1] + 1) % INV_ROWS
            elif    key_states[pygame.K_UP]:              player.inventory.itemHeld[1] = (player.inventory.itemHeld[1] - 1 + INV_ROWS) % INV_ROWS
            elif    key_states[pygame.K_RIGHT]:           player.inventory.itemHeld[0] = (player.inventory.itemHeld[0] + 1) % INV_COLS
            elif    key_states[pygame.K_LEFT]:            player.inventory.itemHeld[0] = (player.inventory.itemHeld[0] - 1 + INV_COLS) % INV_COLS
        except:
            pass

        now = time.time()
        dt = now - prev
        prev = now

        #     player.driveUpdate( dt )

        if cam_bound:
            camera[0] += ( player.pos[0] - camera[0] ) * LERP_C
            camera[1] += ( player.pos[1] - camera[1] ) * LERP_C
        else :
            if key_states[pygame.K_a]:      camera[0] -= ( TILE_WIDTH * dt )
            elif key_states[pygame.K_d]:    camera[0] += ( TILE_WIDTH * dt )
            if key_states[pygame.K_s]:      camera[1] -= ( TILE_WIDTH * dt )
            elif key_states[pygame.K_w]:    camera[1] += ( TILE_WIDTH * dt )

        renderer.update_camera()

        curr_chunk = math.floor( camera[0] / CHUNK_WIDTH_P )
        delta_chunk = curr_chunk - prev_chunk
        prev_chunk = curr_chunk

        if delta_chunk:
            new_index = chunk_buffer.shift(delta_chunk)
            entity_buffer.shift(delta_chunk)
            chunk_buffer[new_index].draw()

        renderer.paint_screen()
        pygame.display.update()

    chunk_buffer.save()
    player.save()
    serializer.stop()


# Start-up menu
def init_menu_1( display_size, _manager ):
    panel_pos = ( 10 , 10 )
    panel_dim = ( display_size[0] - 2*panel_pos[0] , display_size[1] - 2*panel_pos[1] )
    btn_pos = ( 100 , 30 )
    btn_dim = (panel_dim[0] - 2*btn_pos[0], 75)
    panel = UIPanel( pygame.Rect( panel_pos, panel_dim ), 1, _manager)
    btn = UIButton( pygame.Rect( btn_pos, btn_dim ), 'Singleplayer' , _manager , panel)
    return panel, btn

# Singleplayer menu
def init_menu_2( display_size, _manager ):
    panel_pos = ( 80 , 60 )
    panel_dim = ( display_size[0] - 2*panel_pos[0] , display_size[1] - 2*panel_pos[1] )

    panel = UIPanel( pygame.Rect( panel_pos, panel_dim ), 1, _manager )
    sel_list = UISelectionList( pygame.Rect( (25, 10), (150, 100) ), worlds, _manager, container=panel )
    btn1 = UIButton( pygame.Rect( (50, 110), (100, 25) ), "Create", _manager, panel )
    btn2 = UIButton( pygame.Rect( (50, 140), (100, 25) ), "Delete", _manager, panel )
    btn3 = UIButton( pygame.Rect( (50, 170), (100, 25) ), "Back", _manager, panel )
    return panel, sel_list, btn1, btn2, btn3

# Create world menu
def init_menu_3( display_size, _manager ):
    panel_pos = (80, 60)
    panel_dim = (display_size[0] - (panel_pos[0]<<1), display_size[1] - (panel_pos[1]<<1))
    panel = UIPanel( pygame.Rect( panel_pos, panel_dim ), 1, _manager )
    text_entry = UITextEntryLine(pygame.Rect((25, 10), (150, 100)), _manager, panel)
    return panel, text_entry

# Delete world menu
def init_menu_4( display_size ):
    pass

menu_1, btn = init_menu_1(display_sz, gui_manager)
menu_2, choice, btn_1, btn_2, btn_3 = None, None, None, None, None
menu_3, text_entry = None, None

menu_background = pygame.Surface( display_sz )
menu_background.fill("#0000FF")

menu_running = True

while menu_running:
    dt = clock.tick( 60 ) / 1000.0
    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            menu_running = False
        elif event.type == pygame.VIDEORESIZE:
            display_sz = (screen.get_width() , screen.get_height())

            menu_background = pygame.Surface( display_sz )
            menu_background.fill("#0000FF")

            # gui_manager = pygame_gui.UIManager(display_sz, "temptheme.json")
            gui_manager.clear_and_reset()
            gui_manager.set_window_resolution( display_sz )

            if menu_1:
                menu_1.kill()
                menu_1, btn = init_menu_1(display_sz, gui_manager)
            if menu_2:
                menu_2.kill()
                menu_2, choice, btn_1, btn_2, btn_3 = init_menu_2( display_sz, gui_manager )

        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == btn:
                    menu_1.kill()
                    menu_1 = None
                    # ! Uncomment the below line to restore regular functioning of menus
                    main_game_start()
                    menu_2, choice, btn_1, btn_2, btn_3 = init_menu_2(display_sz, gui_manager)
                elif event.ui_element == btn_1: # Create World button
                    menu_2.kill( )
                    menu_2 = None
                    menu_3, text_entry = init_menu_3(display_sz, gui_manager)
                elif event.ui_element == btn_2: # Delete World button
                    pass
                elif event.ui_element == btn_3: # Back button
                    menu_2.kill()
                    menu_2 = None
                    menu_1, btn = init_menu_1(display_sz, gui_manager)

            elif event.user_type == pygame_gui.UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION:
                if event.ui_element == choice:
                    print( 'Test button pressed', event.text )

        gui_manager.process_events( event )
    gui_manager.update(dt)
    screen.blit( menu_background , (0,0))
    gui_manager.draw_ui(screen)
    pygame.display.update()

pygame.display.quit()
