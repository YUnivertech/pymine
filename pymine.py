import math, os, time

import opensimplex
import pygame
import pygame.freetype
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIPanel, UITextEntryLine
from pygame_gui.elements.ui_selection_list import UISelectionList
import send2trash

import chunk, entity
import constants as consts
import game_utilities as utils

key_states              = {}
button_states           = {}
mouse_pos               = [ 0 , 0 ]
cursor_pos              = [ 0 , 0 ]

# Screen variables
monitor_sz              = []
display_sz              = [ 800 , 600 ]
framerate               = 0

# Create the main window
monitor_sz              = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen                  = pygame.display.set_mode( display_sz , pygame.RESIZABLE )
pygame.display.set_caption( "Pymine" )
pygame.display.set_icon( pygame.image.load( "Resources/Default/gameIcon.png" ) )

utils.populate_key_states( key_states, button_states )
consts.loadImageTable( )

# Create GUI based menus
if not os.path.isdir("Worlds"): os.mkdir("Worlds") # Create worlds folder if it does not exist
worlds = os.listdir("Worlds")
for i in range(len(worlds)): worlds[i] = worlds[i][:-3] # remove .db extension
gui_manager = pygame_gui.UIManager(display_sz, "temptheme.json")

# Main Game function
def main_game_start( _world = 'World1' ):

    global key_states , button_states
    global display_sz , screen
    global framerate

    # ---------- CREATION OF ALL MANAGERS ---------- #

    # Chunk Buffer
    buffer_width            = (monitor_sz[0] // consts.CHUNK_WIDTH_P) + 4
    buffer_width            = buffer_width if buffer_width % 2 else buffer_width + 1
    chunk_buffer            = chunk.ChunkBuffer( buffer_width )

    # Entity Buffer
    entity_buffer           = entity.EntityBuffer( )

    # Player
    player                  = entity.Player( [ 0, 600 ] )

    # Renderer
    renderer                = utils.Renderer( )

    # Serializer
    serializer              = utils.Serializer( _world )

    # Noise generator
    noise_gen               = opensimplex.OpenSimplex( seed = 0 )

    # Camera
    camera                  = [ 0 , 0 ]
    prev_cam                = [ 0 , 0 ]
    cam_bound               = True

    # ---------- INITIALIZE MANAGERS ---------- #

    # Player
    player.initialize( chunk_buffer , entity_buffer , renderer , serializer , key_states , button_states , cursor_pos )

    # Chunk Buffer
    chunk_buffer.initialize( entity_buffer , renderer , serializer , player , camera , screen , noise_gen )

    # Entity Buffer
    entity_buffer.initialize( chunk_buffer , renderer , serializer , player , camera , screen )

    # Renderer
    renderer.initialize( chunk_buffer , entity_buffer , player , serializer , camera , screen , display_sz )

    curr_chunk              = chunk_buffer.positions[1]
    prev_chunk              = curr_chunk
    delta_chunk             = 0

    # Main loop
    camera[0]               = player.pos[0]
    camera[1]               = player.pos[1]
    running                 = True
    prev                    = time.time()
    dt                      = 0

    running = True

    while running:
        consts.dbg( 0, "" )
        clock = pygame.time.Clock()
        clock.tick(60)

        for event in pygame.event.get():

            mods = pygame.key.get_mods( )
            key_states[pygame.KMOD_SHIFT]   = (mods & pygame.KMOD_SHIFT) > 0
            key_states[pygame.KMOD_ALT]     = (mods & pygame.KMOD_ALT) > 0
            key_states[pygame.KMOD_CTRL]    = (mods & pygame.KMOD_CTRL) > 0

            if      event.type == pygame.QUIT:      running = False

            elif    event.type == pygame.KEYDOWN:

                # The inventory state must only be toggled when the key is pressed (not while it is being held down)
                if event.key == pygame.K_e: player.inventory.enabled = not player.inventory.enabled
                elif event.key == pygame.K_t:
                    player.tangibility = not player.tangibility
                    consts.dbg( 0, "PLAYER TANGIBILITY CHANGED:", player.tangibility )
                elif event.key == pygame.K_g:
                    if key_states.get( pygame.KMOD_SHIFT ):
                        consts.GRAVITY_ACC = -0.98
                    else:
                        consts.GRAVITY_ACC = 0 if consts.GRAVITY_ACC else 0.98
                    consts.dbg( 0, "GRAVITY ACC CHANGED:", consts.GRAVITY_ACC )
                elif event.key == pygame.K_v:
                    if key_states.get( pygame.KMOD_SHIFT ):
                        consts.SCALE_VEL /= 2
                    else:
                        consts.SCALE_VEL *= 2
                    consts.dbg( 0, "SCALE VEL CHANGED:", consts.SCALE_VEL )

                elif event.key == pygame.K_DOWN:            player.held_item_index[0] = (player.held_item_index[0] + 1) % consts.INV_ROWS
                elif event.key == pygame.K_UP:              player.held_item_index[0] = (player.held_item_index[0] - 1 + consts.INV_ROWS) % consts.INV_ROWS
                elif event.key == pygame.K_RIGHT:           player.held_item_index[1] = (player.held_item_index[1] + 1) % consts.INV_COLS
                elif event.key == pygame.K_LEFT:            player.held_item_index[1] = (player.held_item_index[1] - 1 + consts.INV_COLS) % consts.INV_COLS

                elif event.key == pygame.K_c:
                    command = input(">> ")
                    if command[0] == '.':
                        command = command.split(' ')
                        if command[0] == '.give': # Add requested item to inventory
                            which_item = eval( 'consts.items.' + command[1], globals(), locals() )
                            quantity = eval( command[2] )
                            remainder = player.inventory.add_item( which_item, quantity )
                            print('Added {} items succesfully'.format(quantity - remainder))

                key_states[ event.key ] = True

            elif    event.type == pygame.KEYUP:     key_states[event.key] = False

            elif    event.type == pygame.MOUSEMOTION:

                mouse_pos[0]    = event.pos[0]
                mouse_pos[1]    = event.pos[1]

                cursor_pos[0]   = int( camera[0] ) + mouse_pos[0] - ( display_sz[0] >> 1)
                cursor_pos[1]   = int( camera[1] ) - mouse_pos[1] + ( display_sz[1] >> 1)


            elif    event.type == pygame.MOUSEBUTTONDOWN:   button_states[event.button] = True
            elif    event.type == pygame.MOUSEBUTTONUP:     button_states[event.button] = False
            elif    event.type == pygame.MOUSEWHEEL:
                # event.y is 1 for upward motion and -1 for downward motion
                player.held_item_index[0] = (player.held_item_index + consts.INV_ROWs + event.y) % consts.INV_ROWS

            elif    event.type == pygame.VIDEORESIZE:

                display_sz[0]   = screen.get_width()
                display_sz[1]   = screen.get_height()

                renderer.update_size()

        try:
            if key_states[pygame.K_b]:
                prev_debug = consts.DBG
                consts.DBG = 0 if key_states[pygame.K_0 ] else 1 if key_states[pygame.K_1 ] else 2 if key_states[pygame.K_2 ] else consts.DBG[0 ]
                if consts.DBG != prev_debug: consts.dbg( 0, "--------------- DEBUG :", consts.DBG, "---------------" )
            if      key_states[pygame.K_c] :              utils.Renderer.setShaders( )
            elif    key_states[pygame.K_n] :              cam_bound = not cam_bound
        except Exception as e:
            consts.dbg( 0, "IN MAIN LOOP - EXCEPTION:", e )

        now = time.time()
        dt = now - prev
        prev = now

        player.run( dt )
        if player.pos != [0,0]: consts.dbg( 0, "IN MAIN LOOP - AFTER PLAYER RUN - PLAYER POS:", player.pos )
        if player.vel != [0,0]: consts.dbg( 0, "IN MAIN LOOP - AFTER PLAYER RUN - PLAYER VEL:", player.vel )
        if player.acc != [0,0]: consts.dbg( 0, "IN MAIN LOOP - AFTER PLAYER RUN - PLAYER ACC:", player.acc )
        player.update( dt )
        if player.pos != [0,0]: consts.dbg( 0, "IN MAIN LOOP - AFTER PLAYER UPDATE - PLAYER POS:", player.pos )
        if player.vel != [0,0]: consts.dbg( 0, "IN MAIN LOOP - AFTER PLAYER UPDATE - PLAYER VEL:", player.vel )
        if player.acc != [0,0]: consts.dbg( 0, "IN MAIN LOOP - AFTER PLAYER UPDATE - PLAYER ACC:", player.acc )

        if cam_bound:
            camera[0] += ( player.pos[0] - camera[0] ) * consts.LERP_C * dt
            camera[1] += ( player.pos[1] - camera[1] ) * consts.LERP_C * dt
        else :
            if key_states[pygame.K_a]:      camera[0] -= (96 * consts.TILE_WIDTH * dt)
            elif key_states[pygame.K_d]:    camera[0] += (96 * consts.TILE_WIDTH * dt)
            if key_states[pygame.K_s]:      camera[1] -= (96 * consts.TILE_WIDTH * dt)
            elif key_states[pygame.K_w]:    camera[1] += (96 * consts.TILE_WIDTH * dt)

        if      camera[1] >= renderer.camera_upper :    camera[1] = renderer.camera_upper
        elif    camera[1] <= renderer.num_ver :         camera[1] = renderer.num_ver

        renderer.update_camera()

        curr_chunk = math.floor( camera[0] / consts.CHUNK_WIDTH_P )
        delta_chunk = curr_chunk - prev_chunk
        prev_chunk = curr_chunk

        if delta_chunk:
            entity_buffer.shift( delta_chunk )
            new_side, num_chunks = chunk_buffer.shift( delta_chunk )

            for i in range( num_chunks ):
                chunk_buffer[new_side + i].draw()

        renderer.paint_screen()
        if player.inventory.enabled : renderer.paint_inventory()
        else: renderer.paint_inventory_top()
        pygame.display.update()

    chunk_buffer.save()
    player.save()
    serializer.stop()


menu_1, singleplayer_btn, multiplayer_btn, settings_btn, credits_btn = None, None, None, None, None
menu_2, world_list, new_world_btn, remove_world_btn, menu_2_back_btn = None, None, None, None, None
menu_3, create_world_text_entry, char_error_label_1, char_error_label_2, world_exists_label, create_world_btn, menu_3_back_btn = None, None, None, None, None, None, None
menu_4, info_label, delete_world_list, delete_world_btn, menu_4_back_btn = None, None, None, None, None
world_to_delete = None

# Start-up menu
def init_menu_1( display_size, _manager ):
    global menu_1, singleplayer_btn, multiplayer_btn, settings_btn, credits_btn
    menu_1_dim = (400, 420)
    menu_1_pos = ((display_size[ 0 ] - menu_1_dim[ 0 ]) / 2, (display_size[ 1 ] - menu_1_dim[ 1 ]) / 2)

    singleplayer_btn_pos = (45, 30)
    singleplayer_btn_dim = (menu_1_dim[ 0 ] - 2 * singleplayer_btn_pos[ 0 ], 75)

    multiplayer_btn_pos = (45, singleplayer_btn_pos[ 1 ] + singleplayer_btn_dim[ 1 ] + 10)
    multiplayer_btn_dim = (menu_1_dim[ 0 ] - 2 * multiplayer_btn_pos[ 0 ], 75)

    settings_btn_pos = (45, multiplayer_btn_pos[ 1 ] + multiplayer_btn_dim[ 1 ] + 10)
    settings_btn_dim = (menu_1_dim[ 0 ] - 2 * settings_btn_pos[ 0 ], 75)

    credits_btn_pos = (45, settings_btn_pos[ 1 ] + settings_btn_dim[ 1 ] + 10)
    credits_btn_dim = (menu_1_dim[ 0 ] - 2 * credits_btn_pos[ 0 ], 75)

    menu_1 = UIPanel( pygame.Rect( menu_1_pos, menu_1_dim ), 1, _manager )
    singleplayer_btn = UIButton( pygame.Rect( singleplayer_btn_pos, singleplayer_btn_dim ), 'Singleplayer', _manager, menu_1 )
    multiplayer_btn = UIButton( pygame.Rect( multiplayer_btn_pos, multiplayer_btn_dim ), 'Multiplayer', _manager, menu_1 )
    settings_btn = UIButton( pygame.Rect( settings_btn_pos, settings_btn_dim ), 'Settings', _manager, menu_1 )
    credits_btn = UIButton( pygame.Rect( credits_btn_pos, credits_btn_dim ), 'Credits', _manager, menu_1 )

# Singleplayer menu
def init_menu_2( display_size, _manager ):
    global menu_2, world_list, new_world_btn, remove_world_btn, menu_2_back_btn
    menu_2_dim = (400, 420)
    menu_2_pos = ((display_size[ 0 ] - menu_2_dim[ 0 ]) / 2, (display_size[ 1 ] - menu_2_dim[ 1 ]) / 2)

    world_list_pos = (50, 25)
    world_list_dim = (menu_2_dim[ 0 ] - 2 * world_list_pos[ 0 ], 180)

    new_world_btn_pos = (60, world_list_pos[ 1 ] + world_list_dim[ 1 ] + 10)
    new_world_btn_dim = (menu_2_dim[ 0 ] - 2 * new_world_btn_pos[ 0 ], 50)

    remove_world_btn_pos = (60, new_world_btn_pos[ 1 ] + new_world_btn_dim[ 1 ] + 10)
    remove_world_btn_dim = (menu_2_dim[ 0 ] - 2 * remove_world_btn_pos[ 0 ], 50)

    menu_2_back_btn_pos = (60, remove_world_btn_pos[ 1 ] + remove_world_btn_dim[ 1 ] + 10)
    menu_2_back_btn_dim = (menu_2_dim[ 0 ] - 2 * menu_2_back_btn_pos[ 0 ], 50)

    menu_2 = UIPanel( pygame.Rect( menu_2_pos, menu_2_dim ), 1, _manager )
    world_list = UISelectionList( pygame.Rect( world_list_pos, world_list_dim ), worlds, _manager, container=menu_2 )
    new_world_btn = UIButton( pygame.Rect( new_world_btn_pos, new_world_btn_dim ), "New World", _manager, menu_2 )
    remove_world_btn = UIButton( pygame.Rect( remove_world_btn_pos, remove_world_btn_dim ), "Remove World", _manager, menu_2 )
    menu_2_back_btn = UIButton( pygame.Rect( menu_2_back_btn_pos, menu_2_back_btn_dim ), "Back", _manager, menu_2 )

# Create world menu
def init_menu_3( display_size, _manager ):
    global menu_3, create_world_text_entry, char_error_label_1, char_error_label_2, world_exists_label, create_world_btn, menu_3_back_btn
    menu_3_dim = (400, 420)
    menu_3_pos = ((display_size[ 0 ] - menu_3_dim[ 0 ]) / 2, (display_size[ 1 ] - menu_3_dim[ 1 ]) / 2)

    create_world_text_entry_pos = (60, 50)
    create_world_text_entry_dim = (menu_3_dim[ 0 ] - 2 * create_world_text_entry_pos[ 0 ], 60)

    char_error_label_1_pos = (60, create_world_text_entry_pos[ 1 ] + create_world_text_entry_dim[ 1 ])
    char_error_label_1_dim = (menu_3_dim[ 0 ] - 2 * char_error_label_1_pos[ 0 ], 30)
    char_error_label_2_pos = (60, char_error_label_1_pos[ 1 ] + char_error_label_1_dim[ 1 ])
    char_error_label_2_dim = (menu_3_dim[ 0 ] - 2 * char_error_label_2_pos[ 0 ], 30)

    world_exists_label_pos = (60, char_error_label_2_pos[ 1 ] + char_error_label_2_dim[ 1 ] + 10)
    world_exists_label_dim = (menu_3_dim[ 0 ] - 2 * world_exists_label_pos[ 0 ], 30)

    create_world_btn_pos = (60, create_world_text_entry_pos[ 1 ] + create_world_text_entry_dim[ 1 ] + 150)
    create_world_btn_dim = (menu_3_dim[ 0 ] - 2 * create_world_text_entry_pos[ 0 ], 50)

    menu_3_back_btn_pos = (60, create_world_btn_pos[ 1 ] + create_world_btn_dim[ 1 ] + 10)
    menu_3_back_btn_dim = (menu_3_dim[ 0 ] - 2 * menu_3_back_btn_pos[ 0 ], 50)

    menu_3 = UIPanel( pygame.Rect( menu_3_pos, menu_3_dim ), 1, _manager )
    create_world_text_entry = UITextEntryLine( pygame.Rect( create_world_text_entry_pos, create_world_text_entry_dim ), _manager, menu_3 )
    create_world_text_entry.allowed_characters = consts.ALLOWED_CHARACTERS
    char_error_label_1 = UILabel( pygame.Rect( char_error_label_1_pos, char_error_label_1_dim ), "Enter the world name. Only", _manager, menu_3 )
    char_error_label_2 = UILabel( pygame.Rect( char_error_label_2_pos, char_error_label_2_dim ), "alphabets and numbers allowed", _manager, menu_3 )
    world_exists_label = UILabel( pygame.Rect( world_exists_label_pos, world_exists_label_dim ), "World already exists", _manager, menu_3)
    world_exists_label.hide()
    create_world_btn = UIButton( pygame.Rect( create_world_btn_pos, create_world_btn_dim ), "Create World", _manager, menu_3 )
    menu_3_back_btn = UIButton( pygame.Rect( menu_3_back_btn_pos, menu_3_back_btn_dim ), "Back", _manager, menu_3 )

# Delete world menu
def init_menu_4( display_size, _manager ):
    global menu_4, info_label, delete_world_list, delete_world_btn, menu_4_back_btn
    menu_4_dim = (400, 420)
    menu_4_pos = ((display_size[ 0 ] - menu_4_dim[ 0 ]) / 2, (display_size[ 1 ] - menu_4_dim[ 1 ]) / 2)

    info_label_pos = (50, 25)
    info_label_dim = (menu_4_dim[ 0 ] - 2 * info_label_pos[ 0 ], 30)

    delete_world_list_pos = (50, info_label_pos[1] + info_label_dim[1] + 20)
    delete_world_list_dim = (menu_4_dim[ 0 ] - 2 * delete_world_list_pos[ 0 ], 180)

    delete_world_btn_pos = (60, delete_world_list_pos[ 1 ] + delete_world_list_dim[ 1 ] + 30)
    delete_world_btn_dim = (menu_4_dim[ 0 ] - 2 * delete_world_btn_pos[ 0 ], 50)

    menu_4_back_btn_pos = (60, delete_world_btn_pos[ 1 ] + delete_world_btn_dim[ 1 ] + 10)
    menu_4_back_btn_dim = (menu_4_dim[ 0 ] - 2 * menu_4_back_btn_pos[ 0 ], 50)

    menu_4 = UIPanel( pygame.Rect( menu_4_pos, menu_4_dim ), 1, _manager )
    info_label = UILabel( pygame.Rect( info_label_pos, info_label_dim ), "Double-Click World to Choose", _manager, menu_4)
    delete_world_list = UISelectionList( pygame.Rect( delete_world_list_pos, delete_world_list_dim ), worlds, _manager, container=menu_4 )
    delete_world_btn = UIButton( pygame.Rect( delete_world_btn_pos, delete_world_btn_dim ), "Delete World", _manager, menu_4 )
    menu_4_back_btn = UIButton( pygame.Rect( menu_4_back_btn_pos, menu_4_back_btn_dim ), "Back", _manager, menu_4 )


init_menu_1( display_sz, gui_manager )
init_menu_2( display_sz, gui_manager )
init_menu_3( display_sz, gui_manager )
init_menu_4( display_sz, gui_manager )
menu_2.hide( )
menu_3.hide( )
menu_4.hide( )
menu_background = pygame.Surface( display_sz )
menu_background.fill( "#0000FF" )

menu_running = True

while menu_running:
    dt = consts.clock.tick( 60 ) / 1000.0
    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            menu_running = False
        elif event.type == pygame.VIDEORESIZE:
            display_sz[ 0 ] = screen.get_width( )
            display_sz[ 1 ] = screen.get_height( )

            menu_background = pygame.Surface( display_sz )
            menu_background.fill( "#0000FF" )

            gui_manager.clear_and_reset( )
            gui_manager.set_window_resolution( display_sz )

            prev_menu_1_visible = menu_1.visible
            prev_menu_2_visible = menu_2.visible
            prev_menu_3_visible = menu_3.visible
            prev_menu_4_visible = menu_4.visible

            menu_1.kill( )
            menu_2.kill( )
            menu_3.kill( )
            menu_4.kill( )

            init_menu_1( display_sz, gui_manager )
            init_menu_2( display_sz, gui_manager )
            init_menu_3( display_sz, gui_manager )
            init_menu_4( display_sz, gui_manager )

            if not prev_menu_1_visible:
                menu_1.hide( )
            if not prev_menu_2_visible:
                menu_2.hide( )
            if not prev_menu_3_visible:
                menu_3.hide( )
            if not prev_menu_4_visible:
                menu_4.hide( )

        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == singleplayer_btn:
                    menu_1.hide( )
                    menu_2.show( )
                elif event.ui_element == new_world_btn:  # Create World button
                    menu_2.hide( )
                    menu_3.show( )
                    world_exists_label.hide( )
                elif event.ui_element == create_world_btn:
                    world_name = create_world_text_entry.get_text( )
                    world_name = world_name.strip()
                    lower_case_worlds = [i.lower() for i in worlds]
                    if world_name.lower( ) not in lower_case_worlds:
                        world_exists_label.hide( )
                        if world_name:
                            create_world_text_entry.set_text("")
                            temp_serial = utils.Serializer(world_name)
                            temp_serial.stop()
                            worlds = os.listdir( "Worlds" )
                            for i in range( len( worlds ) ): worlds[ i ] = worlds[ i ][ :-3 ]  # remove .db extension
                            menu_3.hide( )
                            menu_2.kill( )
                            menu_4.kill( )
                            init_menu_2( display_sz, gui_manager )
                            init_menu_4( display_sz, gui_manager )
                            menu_4.hide( )
                    else:
                        world_exists_label.show( )
                elif event.ui_element == remove_world_btn:  # Delete World button
                    menu_2.hide( )
                    menu_4.show( )
                elif event.ui_element == delete_world_btn:
                    if world_to_delete:
                        world_path = "Worlds/" + world_to_delete + ".db"
                        if os.path.exists(world_path):
                            send2trash.send2trash(world_path)
                        worlds = os.listdir( "Worlds" )
                        for i in range( len( worlds ) ): worlds[ i ] = worlds[ i ][ :-3 ]
                        menu_2.kill( )
                        menu_4.kill( )
                        init_menu_2( display_sz, gui_manager )
                        menu_2.hide( )
                        init_menu_4( display_sz, gui_manager )
                    worlds = os.listdir( "Worlds" )
                    for i in range( len( worlds ) ): worlds[ i ] = worlds[ i ][ :-3 ]
                elif event.ui_element == menu_2_back_btn:   # Back button
                    menu_2.hide( )
                    menu_1.show( )
                elif event.ui_element == menu_3_back_btn:   # Back button
                    menu_3.hide( )
                    menu_2.show( )
                elif event.ui_element == menu_4_back_btn:   # Back button
                    menu_4.hide( )
                    menu_2.show( )
                    world_to_delete = None

            elif event.user_type == pygame_gui.UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION:
                if event.ui_element == world_list:
                    print( 'World selected:', event.text )
                    main_game_start( str( event.text ) )
                    display_sz[ 0 ] = screen.get_width( )
                    display_sz[ 1 ] = screen.get_height( )

                    menu_background = pygame.Surface( display_sz )
                    menu_background.fill( "#0000FF" )

                    gui_manager.clear_and_reset( )
                    gui_manager.set_window_resolution( display_sz )

                    prev_menu_1_visible = menu_1.visible
                    prev_menu_2_visible = menu_2.visible
                    prev_menu_3_visible = menu_3.visible
                    prev_menu_4_visible = menu_4.visible

                    menu_1.kill( )
                    menu_2.kill( )
                    menu_3.kill( )
                    menu_4.kill( )

                    init_menu_1( display_sz, gui_manager )
                    init_menu_2( display_sz, gui_manager )
                    init_menu_3( display_sz, gui_manager )
                    init_menu_4( display_sz, gui_manager )
                    menu_2.hide( )
                    menu_3.hide( )
                    menu_4.hide( )
                elif event.ui_element == delete_world_list:
                    print("World to be deleted:", event.text)
                    world_to_delete = event.text


        gui_manager.process_events( event )
    gui_manager.update( dt )
    screen.blit( menu_background, (0, 0) )
    gui_manager.draw_ui( screen )
    pygame.display.update( )

pygame.display.quit( )
