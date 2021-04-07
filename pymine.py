from chunk import *
from entity import *
import time

# # Initalize pygame and start the clock
# pygame.init()
# clock = pygame.time.Clock()

def start_game():
    while 1:
        mode = input("1 for singleplayer, 2 for multiplayer, 3 for settings, 4 for credits: ")
        if mode != 1: print("Sorry, not yet implemented")
        else:
            world_list = []
            print("Selected singplayer", "List of worlds:-", world_list, sep='\n')

            while 1:
                opt = input("1 to select world, 2 to create world, 3 to delete world: ")
                name = input("Enter name of world: ")
                if opt == 2:
                    if name in world_list:
                        print("World already exists")
                        continue
                    return name , opt
                elif opt == 1:
                    if name not in world_list:
                        print("World does not exist")
                        continue
                    return name , opt
                elif opt == 3:
                    if name not in world_list:
                        print("World does not exist")
                        continue
                    # Just delete this world

key_states              = {}
button_states           = {}

# Screen variables
display_sz              = [ 400 , 300 ]
framerate               = 0

# Create the main window
screen                  = pygame.display.set_mode( display_sz , pygame.RESIZABLE )
pygame.display.set_caption( "Pymine" )
pygame.display.set_icon( pygame.image.load( "../Resources/Default/gameIcon.png" ) )

# # Convert all images to optimized form
# tiles.loadImageTable( )
# items.loadImageTable( )

# ---------- CREATION OF ALL MANAGERS ---------- #

# Chunk Buffer
buffer_width            = ( pygame.display.Info().current_w // CHUNK_WIDTH_P ) + 1
buffer_width            = buffer_width if buffer_width % 2 else buffer_width + 1
chunk_buffer = ChunkBuffer( buffer_width )

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
