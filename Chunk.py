import pickle

import tiles, items, time
from constants import *
from opensimplex import OpenSimplex
from gameUtilities import *

from random import randint

class Chunk:

    def __init__(  self, index = 0, blocks = None, walls = None, localTable = {}  ):

        self.index            =  index
        self.TILE_TABLE_LOCAL =  localTable if localTable else {}

        self.surface = pygame.Surface( ( CHUNK_WIDTH_P, CHUNK_HEIGHT_P ) )

        if blocks is None:
            self.blocks         =  [[tiles.air for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]
            self.walls          =  [[tiles.air for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]
        else:
            self.blocks         =  blocks
            self.walls          =  walls

        self.lightMap           =  [[0 for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]

    def breakWallAt( self, x, y, tool, dt):

        if (x, y, False) not in self.TILE_TABLE_LOCAL:
            self.TILE_TABLE_LOCAL[ ( x, y, False ) ] = { }

        if HEALTH not in self.TILE_TABLE_LOCAL[ (x, y, False)]:
            self.TILE_TABLE_LOCAL[ ( x, y, False ) ][ HEALTH ] = 100

        self.TILE_TABLE_LOCAL[ ( x, y, False ) ][ HEALTH ] -= (25 * dt)

        if self.TILE_TABLE_LOCAL[ (x, y, False)][ HEALTH] <= 0:
            del self.TILE_TABLE_LOCAL[ ( x, y, False ) ]
            self.walls[y][x] = tiles.air

        return True

    def breakBlockAt( self, x, y, tool, dt):

        if (x, y, True) not in self.TILE_TABLE_LOCAL:
            self.TILE_TABLE_LOCAL[ ( x, y, True ) ] = { }

        if HEALTH not in self.TILE_TABLE_LOCAL[ (x, y, True)]:
            self.TILE_TABLE_LOCAL[ ( x, y, True ) ][ HEALTH ] = 100

        self.TILE_TABLE_LOCAL[ ( x, y, True ) ][ HEALTH ] -= (25 * dt)

        if self.TILE_TABLE_LOCAL[ (x, y, True)][ HEALTH] <= 0:
            del self.TILE_TABLE_LOCAL[ ( x, y, True ) ]
            self.blocks[y][x] = tiles.air
            return True

        return False

    def placeWallAt( self, x, y, val):

        if self.walls[y][x] != tiles.air: return False
        self.walls[y][x] = val
        return True

    def placeBlockAt( self, x, y, val):

        if self.blocks[y][x] != tiles.air: return False
        self.blocks[y][x] = val
        print(tiles.TILE_NAMES[val])
        return True

    def draw( self, rect = [0, 0, CHUNK_WIDTH, CHUNK_HEIGHT] ):

        self.surface.fill( ( 30, 150, 240 ), [rect[0] * TILE_WIDTH, TILE_WIDTH* (CHUNK_HEIGHT - rect[3]), TILE_WIDTH * (rect[2] - rect[0]), TILE_WIDTH * (rect[3] - rect[1])])

        for i in range( rect[1], rect[3] ):

            coors  =  [ 0, ( CHUNK_HEIGHT - i - 1 ) * TILE_WIDTH ]

            for j in range( rect[0], rect[2] ):

                coors[0] = j * TILE_WIDTH

                currTileRef =  self.blocks[i][j]
                currWallRef =  self.walls[i][j]

                if currTileRef > 0:
                    self.surface.blit( tiles.TILE_TABLE[currTileRef], coors )
                    if (j, i, True) in self.TILE_TABLE_LOCAL:

                        if HEALTH in self.TILE_TABLE_LOCAL[ (j, i, True)]:

                            breakState = (self.TILE_TABLE_LOCAL[ ( j, i, True ) ][ HEALTH ] * 8) / 100
                            self.surface.blit( tiles.TILE_MODIFIERS[ tiles.crack ][ 8 - int(breakState) ], coors )

                elif currWallRef > 0:
                    self.surface.blit( tiles.TILE_TABLE[currWallRef], coors )
                    if (i, j, False) in self.TILE_TABLE_LOCAL:

                        if HEALTH in self.TILE_TABLE_LOCAL[ (j, i, False)]:

                            breakState = (self.TILE_TABLE_LOCAL[ ( j, i, False ) ][ HEALTH ] * 8) / 100
                            self.surface.blit( tiles.TILE_MODIFIERS[ tiles.crack ][ 8 - int(breakState) ], coors )

    def __getitem__(  self, key  ):
        return self.blocks[key]

    def __setitem__(  self, key, value  ):
        self.blocks[key] = value

class ChunkBuffer:

    def __init__(  self, length, middleIndex, targetWorld, seed=None  ):

        # Create references to required objects
        self.serializer     =  Serializer(targetWorld)
        self.chunkGenerator =  chunkGenerator()

        # Save length and index of last item
        self.length         =  length
        self.len            =  length - 1

        # Positions of the left-most, middle and right-most chunks
        self.positions      =  [ middleIndex - self.len // 2, middleIndex, middleIndex + self.len // 2 ]

        # Create lists of required objects
        self.chunks         =  [ ]
        self.lightSurfs     =  [ ]

        self.entityBuffer = None

        # Load all objects
        for i in range( self.positions[ 0 ],  self.positions[ 2 ] + 1 ):

            retrieved           =   self.serializer[ i ]

            if retrieved is None:
                retrieved  =  Chunk( i )
                self.populateChunk( retrieved )

            else:
                li         =  pickle.loads( retrieved[ 0 ] )
                lo         =  pickle.loads( retrieved[ 1 ] )

                retrieved  =  Chunk( i, li[ 0 ], li[ 1 ], lo )

            self.chunks.append( retrieved )
            self.lightSurfs.append( pygame.Surface( ( CHUNK_WIDTH_P, CHUNK_HEIGHT_P ) ) )

    def shiftBuffer( self, deltaChunk ):

        rep = lambda num : 0 if num == 1 else -1

        # Index of the chunk to be dumped (-1 while shifting left, 0 while shifting right) and the extremity needing to be changed
        dumpIndex = rep( deltaChunk)

        # Index of the chunk to be loaded (0 while shifting left, -1 while shifting right) and the extremity needing to be changed
        loadIndex = rep( -deltaChunk )


        # Ready the tiles, walls and local table to be serialized and dump
        li                                              =  [ self.chunks[ dumpIndex ].blocks, self.chunks[ dumpIndex ].walls ]
        lo                                              =  self.chunks[ dumpIndex ].TILE_TABLE_LOCAL
        chk_b = time.time()
        self.serializer[ self.positions[ dumpIndex ] ]  =  pickle.dumps( li ), pickle.dumps( lo )

        print('random stuff time:', (time.time()-chk_b)*1000)
        # After dumping, increment the position of the dumped tile by deltaChunk
        self.positions[dumpIndex]                       += deltaChunk

        # Get references to surfaces which must be recycled
        recycleShade                                    =  self.lightSurfs[dumpIndex]

        # Start from last if shifting right otherwise from 0
        moveIndex                                       =  self.len * -dumpIndex

        chk_b = time.time()

        for i in range( 0, self.len ):

            nextMoveIndex                 =  moveIndex + deltaChunk

            self.chunks[ moveIndex ]      =  self.chunks[ nextMoveIndex ]
            self.lightSurfs[ moveIndex ]  =  self.lightSurfs[ nextMoveIndex ]

            moveIndex += deltaChunk

        print('in shift buffer for loop time:', (time.time()-chk_b)*1000)

        chk_b = time.time()

        # Recycle surfaces
        self.lightSurfs[ loadIndex ]                    =  recycleShade

        # Increment positions of the chunk to be loaded and the middle chunk by deltaChunk
        self.positions[ 1 ]                             += deltaChunk
        self.positions[ loadIndex ]                     += deltaChunk

        # Load new chunk and populate if not generated
        self.chunks[ loadIndex ]                        =  self.serializer[ self.positions[ loadIndex ] ]

        print("Random stuff time:", (time.time()-chk_b)*1000)

        if self.chunks[ loadIndex] is None:
            chk_b = time.time()
            self.chunks[ loadIndex ]      =  Chunk( self.positions[ loadIndex ] )
            self.populateChunk( self.chunks[ loadIndex ] )
            print('in shift buffer populate chunk time:', (time.time()-chk_b)*1000)

        else:
            chk_b = time.time()
            li                      =  pickle.loads( self.chunks[ loadIndex ][ 0 ] )
            lo                      =  pickle.loads( self.chunks[ loadIndex ][ 1 ] )
            self.chunks[loadIndex]  =  Chunk( self.positions[loadIndex], li[ 0 ], li[ 1 ], lo )
            print("in shift buffer serialization:", (time.time()-chk_b)*1000)

        # Form light map for newly loaded chunk and the chunk before it
        # In case of left shift, i=-1,-2 are generated
        # In case of right shift, i=0, 1 are generated
        chk_b = time.time()
        # self.formLightMap( loadIndex )
        # self.formLightMap( loadIndex - deltaChunk )
        print('in shift buffer form light map time:', (time.time()-chk_b)*1000)

        return loadIndex

    def saveComplete(self):
        for chunk in self.chunks:
            self.serializer[chunk.index] = pickle.dumps( [ chunk.blocks, chunk.walls ] ), pickle.dumps( chunk.TILE_TABLE_LOCAL )

    def __getitem__( self, key ):
        return self.chunks[key]

    def __setitem__( self, key, value ):
        self.chunks[key] = value

    def __len__( self ):
        return self.length

    def populateChunk(self, chunk):

        absouluteIndex  =   chunk.index * CHUNK_WIDTH

        for i in range(0, CHUNK_WIDTH):

            ## Lower bedrock wastes
            for j in range(0, 10):

                front, back  =  self.chunkGenerator.getLowerBedrockWastes( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back

            ## Upper bedrock wastes
            for j in range(10, 20):

                front, back   =  self.chunkGenerator.getUpperBedrockWastes( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back

            ## Lower Caves
            for j in range(20, 50):

                front, back   =  self.chunkGenerator.getLowerCaves( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back

            ## Middle Caves
            for j in range(50, 90):

                front, back    =  self.chunkGenerator.getMiddleCaves( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back

            ## Upper Caves
            for j in range(90, 120):

                front, back    =  self.chunkGenerator.getUpperCaves( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back

            ## Lower Undergrounds
            for j in range(120, 140):

                front, back    =  self.chunkGenerator.getUpperUnderground( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back

            ## Upper Undergrounds
            for j in range(140, 170):

                front, back    =  self.chunkGenerator.getUpperUnderground( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back


            absouluteIndex  +=  1


class chunkGenerator:

    def __init__(self, seed = None):

        # self.simp = OpenSimplex()
        # self.voronoi = Voronoi()
        # self.ridgedMulti = RidgedMulti()
        self.simp = OpenSimplex()

    def frontVal(self, x, y):

        #return (self.simp[x, y, 0.1] * 50)
        return ( self.simp.noise3d( x, y, 0.1 ) + 1 ) * 50

    def backVal(self, x, y):

        #return (self.simp[x, y, -0.1] * 50)
        return ( self.simp.noise3d(x, y, -0.1) + 1 ) * 50

    def getLowerBedrockWastes(self, x, y):

        if y == 0:
            return tiles.bedrock, tiles.bedrock

        else:
            front  =  self.frontVal(x * BEDROCK_LOWER_X, y * BEDROCK_LOWER_Y)
            back   =  self.backVal(x * BEDROCK_LOWER_X, y * BEDROCK_LOWER_Y)

            bedrockProbability = 50

            front = tiles.obsidian
            if front <= bedrockProbability:
                front = tiles.bedrock

            back = tiles.obsidian
            if back <= bedrockProbability:
                back = tiles.bedrock

            return front, back

    def getUpperBedrockWastes(self, x, y):

        front  =  self.frontVal(x * BEDROCK_UPPER_X, y * BEDROCK_UPPER_Y)
        back   =  self.backVal(x * BEDROCK_UPPER_X, y * BEDROCK_UPPER_Y)

        obsidianProbability = 70
        stoneProbability = 20 + obsidianProbability
        hellStoneProbability = 12.5 + stoneProbability

        if front <= obsidianProbability:
            front = tiles.obsidian
        elif front <= stoneProbability:
            front = tiles.greystone
        else:
            front = tiles.hellstone

        if back <= obsidianProbability:
            back = tiles.obsidian
        else:
            back = tiles.greystone

        return front, back

    def getLowerCaves(self, x, y):

        front  =  self.frontVal(x * CAVE_X, y * CAVE_Y)
        back   =  self.backVal(x * CAVE_X, y * CAVE_Y)

        obsidianProbability   =  20
        stoneProbability      =  obsidianProbability + 20
        graniteProbability    =  stoneProbability + 20
        limestoneProbability  =  graniteProbability + 20

        unobtaniumProbability =  limestoneProbability + 10
        diamondProbability    =  unobtaniumProbability + 7.5
        platinumProbability   =  diamondProbability + 7.5

        if front <= obsidianProbability:
            front = tiles.obsidian

        elif front <= stoneProbability:
            front = tiles.greystone

        elif front <= graniteProbability:
            front = tiles.granite

        elif front <= limestoneProbability:
            front = tiles.limestone

        elif front <= unobtaniumProbability:
            front = tiles.unobtaniumOre

        elif front <= diamondProbability:
            front = tiles.diamondOre

        else:
            front = tiles.platinumOre

        return front, back

    def getMiddleCaves(self, x, y):

        front  =  self.frontVal(x * CAVE_X, y * CAVE_Y)
        back   =  self.backVal(x * CAVE_X, y * CAVE_Y)

        stoneProbability = 30
        graniteProbability = 20 + stoneProbability
        quartzProbability = 20 + graniteProbability
        unobtaniumProbability = 10 + quartzProbability
        diamondProbability = 10 + unobtaniumProbability
        platinumProbability = 10 + diamondProbability

        if front <= stoneProbability:
            front = tiles.greystone
        elif front <= graniteProbability:
            front = tiles.granite
        elif front <= quartzProbability:
            front = tiles.quartz
        elif front <= unobtaniumProbability:
            front = tiles.unobtaniumOre
        elif front <= diamondProbability:
            front = tiles.diamondOre
        elif front <= platinumProbability:
            front = tiles.platinumOre

        if back <= stoneProbability:
            back = tiles.greystone
        elif back <= graniteProbability:
            back = tiles.granite
        elif back <= quartzProbability:
            back = tiles.quartz
        else:
            back = tiles.greystone

        return front, back

    def getUpperCaves(self, x, y):

        front  =  self.frontVal(x * CAVE_X, y * CAVE_Y)
        back   =  self.backVal(x * CAVE_X, y * CAVE_Y)

        stoneProbability = 75
        ironProbability = 12.5 + stoneProbability
        goldProbability = 12.5 + ironProbability

        back = tiles.greystone

        if front <= stoneProbability:
            front = tiles.greystone
        elif front <= ironProbability:
            front = tiles.ironOre
        elif front <= goldProbability:
            front = tiles.goldOre

        return front, back

    def getLowerUnderground(self, x, y):

        front  =  self.frontVal(x * UNDERGROUND_X, y * UNDERGROUND_Y)
        back   =  self.backVal(x * UNDERGROUND_X, y * UNDERGROUND_Y)

        gravelProbability = 20
        dirtProbability = 20 + gravelProbability
        redclayProbability = 20 + dirtProbability
        coalProbability = 20 + redclayProbability
        copperProbability = 20 + coalProbability

        if front <= gravelProbability:
            front = tiles.gravel
        elif front <= dirtProbability:
            front = tiles.browndirt
        elif front <= redclayProbability:
            front = tiles.redClay
        elif front <= coalProbability:
            front = tiles.coke
        elif front <= copperProbability:
            front = tiles.copperOre

        if back <= gravelProbability:
            back = tiles.gravel
        elif back <= dirtProbability:
            back = tiles.browndirt
        else:
            back = redclayProbability

        return front, back

    def getUpperUnderground(self, x, y):

        front  =  self.frontVal(x * UNDERGROUND_X, y * UNDERGROUND_Y)
        back   =  self.backVal(x * UNDERGROUND_X, y * UNDERGROUND_Y)

        gravelProbability = 20
        dirtProbability = 20 + gravelProbability
        redclayProbability = 20 + dirtProbability
        coalProbability = 20 + redclayProbability
        copperProbability = 20 + coalProbability

        if front <= gravelProbability:
            front = tiles.gravel
        elif front <= dirtProbability:
            front = tiles.browndirt
        elif front <= redclayProbability:
            front = tiles.redClay
        elif front <= coalProbability:
            front = tiles.coke
        elif front <= copperProbability:
            front = tiles.copperOre

        if back <= gravelProbability:
            back = tiles.gravel
        elif back <= dirtProbability:
            back = tiles.browndirt
        else:
            back = redclayProbability

        return front, back
