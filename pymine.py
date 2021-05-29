import math
import os
import time

import opensimplex
import pygame
import pygame.freetype
import pygame_gui
from pygame_gui.elements import UIButton, UIPanel, UITextEntryLine
from pygame_gui.elements.ui_selection_list import UISelectionList

import chunk
import constants as consts
import entity
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
                if event.key == pygame.K_t:
                    player.tangibility = not player.tangibility
                    consts.dbg( 0, "PLAYER TANGIBILITY CHANGED:", player.tangibility )
                if event.key == pygame.K_g:
                    if key_states.get( pygame.KMOD_SHIFT ):
                        consts.GRAVITY_ACC = -0.98
                    else:
                        consts.GRAVITY_ACC = 0 if consts.GRAVITY_ACC else 0.98
                    consts.dbg( 0, "GRAVITY ACC CHANGED:", consts.GRAVITY_ACC )
                if event.key == pygame.K_v:
                    if key_states.get( pygame.KMOD_SHIFT ):
                        consts.SCALE_VEL /= 2
                    else:
                        consts.SCALE_VEL *= 2
                    consts.dbg( 0, "SCALE VEL CHANGED:", consts.SCALE_VEL )
                key_states[ event.key ] = True

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
            if key_states[pygame.K_b]:
                prev_debug = consts.DBG
                consts.DBG = 0 if key_states[pygame.K_0 ] else 1 if key_states[pygame.K_1 ] else 2 if key_states[pygame.K_2 ] else consts.DBG[0 ]
                if consts.DBG != prev_debug: consts.dbg( 0, "--------------- DEBUG :", consts.DBG, "---------------" )
            if      key_states[pygame.K_c] :              utils.Renderer.setShaders( )
            elif    key_states[pygame.K_n] :              cam_bound = not cam_bound
            elif    key_states[pygame.K_DOWN]:            player.inventory.itemHeld[1] = (player.inventory.itemHeld[1] + 1) % consts.INV_ROWS
            elif    key_states[pygame.K_UP]:              player.inventory.itemHeld[1] = (player.inventory.itemHeld[1] - 1 + consts.INV_ROWS) % consts.INV_ROWS
            elif    key_states[pygame.K_RIGHT]:           player.inventory.itemHeld[0] = (player.inventory.itemHeld[0] + 1) % consts.INV_COLS
            elif    key_states[pygame.K_LEFT]:            player.inventory.itemHeld[0] = (player.inventory.itemHeld[0] - 1 + consts.INV_COLS) % consts.INV_COLS
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

            new_side , num_chunks = chunk_buffer.shift(delta_chunk)
            entity_buffer.shift(delta_chunk)

            for i in range( num_chunks ):
                chunk_buffer[new_side + i].draw()

        renderer.paint_screen()
        if( player.inventory.enabled ): renderer.paint_inventory()
        pygame.display.update()

    chunk_buffer.save()
    player.save()
    serializer.stop()


menu_1, singleplayer_btn, multiplayer_btn, settings_btn, credits_btn = None, None, None, None, None
menu_2, world_list, create_world_btn, delete_world_btn, menu_2_back_btn = None, None, None, None, None
menu_3, create_world_text_entry, menu_3_back_btn = None, None, None

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
    global menu_2, world_list, create_world_btn, delete_world_btn, menu_2_back_btn
    menu_2_dim = (400, 420)
    menu_2_pos = ((display_size[ 0 ] - menu_2_dim[ 0 ]) / 2, (display_size[ 1 ] - menu_2_dim[ 1 ]) / 2)

    world_list_pos = (45, 30)
    world_list_dim = (menu_2_dim[ 0 ] - 2 * world_list_pos[ 0 ], 160)

    create_world_btn_pos = (60, world_list_pos[1] + world_list_dim[1] + 10)
    create_world_btn_dim = (menu_2_dim[ 0 ] - 2 * create_world_btn_pos[ 0 ], 50)

    delete_world_btn_pos = (60, create_world_btn_pos[1] + create_world_btn_dim[1] + 10)
    delete_world_btn_dim = (menu_2_dim[ 0 ] - 2 * delete_world_btn_pos[ 0 ], 50)

    menu_2_back_btn_pos = (60, delete_world_btn_pos[1] + delete_world_btn_dim[1] + 10)
    menu_2_back_btn_dim = (menu_2_dim[ 0 ] - 2 * menu_2_back_btn_pos[ 0 ], 50)

    menu_2 = UIPanel( pygame.Rect( menu_2_pos, menu_2_dim ), 1, _manager )
    world_list = UISelectionList( pygame.Rect( world_list_pos, world_list_dim ), worlds, _manager, container=menu_2 )
    create_world_btn = UIButton( pygame.Rect( create_world_btn_pos, create_world_btn_dim ), "Create", _manager, menu_2 )
    delete_world_btn = UIButton( pygame.Rect( delete_world_btn_pos, delete_world_btn_dim ), "Delete", _manager, menu_2 )
    menu_2_back_btn = UIButton( pygame.Rect( menu_2_back_btn_pos, menu_2_back_btn_dim ), "Back", _manager, menu_2 )

# Create world menu
def init_menu_3( display_size, _manager ):
    global menu_3, create_world_text_entry, menu_3_back_btn
    menu_3_dim = (400, 420)
    menu_3_pos = ((display_size[ 0 ] - menu_3_dim[ 0 ]) / 2, (display_size[ 1 ] - menu_3_dim[ 1 ]) / 2)

    create_world_text_entry_pos = (60, 30)
    create_world_text_entry_dim = (menu_3_dim[0] - 2*create_world_text_entry_pos[0], 100)

    menu_3_back_btn_pos = (60, create_world_text_entry_pos[ 1 ] + create_world_text_entry_dim[ 1 ] + 10)
    menu_3_back_btn_dim = (menu_3_dim[ 0 ] - 2 * menu_3_back_btn_pos[ 0 ], 50)

    menu_3 = UIPanel( pygame.Rect( menu_3_pos, menu_3_dim ), 1, _manager )
    create_world_text_entry = UITextEntryLine( pygame.Rect( create_world_text_entry_pos, create_world_text_entry_dim ), _manager, menu_3 )
    menu_3_back_btn = UIButton( pygame.Rect( menu_3_back_btn_pos, menu_3_back_btn_dim ), "Back", _manager, menu_3 )

# Delete world menu
def init_menu_4( display_size ):
    pass


init_menu_1(display_sz, gui_manager)

menu_background = pygame.Surface( display_sz )
menu_background.fill("#0000FF")

menu_running = True

while menu_running:
    dt = consts.clock.tick( 60 ) / 1000.0
    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            menu_running = False
        elif event.type == pygame.VIDEORESIZE:
            display_sz[0] = screen.get_width()
            display_sz[1] = screen.get_height()

            menu_background = pygame.Surface( display_sz )
            menu_background.fill("#0000FF")

            # gui_manager = pygame_gui.UIManager(display_sz, "temptheme.json")
            gui_manager.clear_and_reset()
            gui_manager.set_window_resolution( display_sz )

            if menu_1:
                menu_1.kill()
                init_menu_1( display_sz, gui_manager )
            if menu_2:
                menu_2.kill()
                init_menu_2( display_sz, gui_manager )

        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == singleplayer_btn:
                    menu_1.kill()
                    menu_1 = None
                    init_menu_2( display_sz, gui_manager )
                elif event.ui_element == create_world_btn: # Create World button
                    menu_2.kill( )
                    menu_2 = None
                    init_menu_3(display_sz, gui_manager)
                elif event.ui_element == delete_world_btn: # Delete World button
                    pass
                elif event.ui_element == menu_2_back_btn: # Back button
                    menu_2.kill()
                    menu_2 = None
                    init_menu_1( display_sz, gui_manager )
                elif event.ui_element == menu_3_back_btn: # Back button
                    menu_3.kill()
                    menu_2 = None
                    init_menu_2(display_sz, gui_manager)

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
                    menu_2.kill( )
                    menu_2 = None
                    init_menu_1( display_sz, gui_manager )

        gui_manager.process_events( event )
    gui_manager.update(dt)
    screen.blit( menu_background , (0,0))
    gui_manager.draw_ui(screen)
    pygame.display.update()

pygame.display.quit()
