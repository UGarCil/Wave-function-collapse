# WAVE FUNCTION COLLAPSE WITH TILE SOCKETS AND RULE ABSTRACTION
# .:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:
# Algorithm:
# In computer graphics, Wave Function Collapse (WFC) is an algorithm used to
# auto-generate mosaics using a simple set of rules, applied using the principle
# of lowest entropy.
# When a tile has been placed in the screen at a particular position, it's said that
# its entropy reaches 0, because we are completely certain on the identity of
# such tile.

# The identity of a tile modifies the system. Neighbor tiles have a decline in their
# entropy values as well as a result from the restrictions imposed by the identity
# of the previously collapsed tile

# In an original version of this alogorithm each rotation of the same tile was considered
# as a unique tile. This version attemps to increase the abstraction by having a single tile
# that is instead rotated. Each of the sides of a potential tile will have "sockets",
# represented as combinations of 3 letters (given the design of the tiles).

# Regardless of its orientation (RIGHT, DOWN, LEFT, UP) in the tile, each socket is compared
# with that of a collapsed neighbor to determine if a tile is compatible


# With the rotation of a tile, we also change the relativeA position of the sockets in a list

import pygame
from tile import *
import random   
# .:.:.:.:.:.:.:.:.:.:.:.:.:.: DATA DEIFNITIONS .:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:
ROWS = 20
COLS = 30

DIMS = (COLS * RES, ROWS*RES)


# Variables required by pygame
display = pygame.display.set_mode(DIMS)
clock = pygame.time.Clock()
FPS = 120

# DD. GRID
# tileRow = [[TILE, ...], ...]
# interp. a grid of tiles
grid = [[Tile(col * RES, row * RES, "none") for col in range(COLS)] for row in range(ROWS)]


# DD. TILE
# tile = Tile()
# interp. a tile to be rendered in the scene
tile_1 = Tile(0 * RES, 0*RES, "1")


# .:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:
# FD render()
# purp. render the characters in the screen
def render():
    display.fill("red")
    [[display.blit(tile.pyImage, (tile.x, tile.y)) for tile in row] for row in grid]  #draw the grid
    pygame.display.flip()
    clock.tick(FPS)

def inputMan():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()



def updateGrid():
    # FD. updateNeighbours()
    # purp. identify the neighbours and their socket values
    def updateNeighbours():
        for row,tileRow in enumerate(grid):
            for col,tile in enumerate(tileRow):
                hasRIGHT_neigh = False
                hasDOWN_neigh = False
                hasLEFT_neigh = False
                hasUP_neigh = False
                if tile.entropy != 0:
                    # get the identity of the neighboring tiles. The following cases do not follow the standard rules
                    # if this is the first row
                    if row == 0:
                        #   if this is the first column
                        if col == 0:
                            hasRIGHT_neigh = True
                            hasDOWN_neigh = True
                        #   if this is the last column
                        elif col == len(tileRow)-1:
                            hasDOWN_neigh = True
                            hasLEFT_neigh = True
                        else:
                            hasRIGHT_neigh = True
                            hasDOWN_neigh = True
                            hasLEFT_neigh = True
                    # if this is the last row
                    elif row == len(grid)-1:
                        #   if this is the first column
                        if col == 0:
                            hasRIGHT_neigh = True
                            hasUP_neigh = True
                        #   if this is the last column
                        elif col == len(tileRow)-1:
                            hasLEFT_neigh = True
                            hasUP_neigh = True
                        else:
                            hasRIGHT_neigh = True
                            hasLEFT_neigh = True
                            hasUP_neigh = True

                    else:
                        if col == 0:
                            hasRIGHT_neigh = True
                            hasDOWN_neigh = True
                            hasUP_neigh = True
                        elif col == len(tileRow)-1:
                            hasDOWN_neigh = True
                            hasLEFT_neigh = True
                            hasUP_neigh  = True
                        else:
                            hasRIGHT_neigh = True
                            hasDOWN_neigh = True
                            hasLEFT_neigh = True
                            hasUP_neigh = True

                    # update each NEIGHBOUR in the tile
                    if hasRIGHT_neigh:
                        tile_RIGHT = grid[row][col+1]
                        tile.neig_RIGHT = {"COLLAPSED":tile_RIGHT.collapsed, "SOCKET":tile_RIGHT.socketsCollapsed[2], "POSITION":"RIGHT"}
                    if hasDOWN_neigh:
                        tile_DOWN = grid[row+1][col]
                        tile.neig_DOWN = {"COLLAPSED":tile_DOWN.collapsed, "SOCKET":tile_DOWN.socketsCollapsed[3], "POSITION":"DOWN"}
                    if hasLEFT_neigh:
                        tile_LEFT = grid[row][col-1]
                        tile.neig_LEFT = {"COLLAPSED":tile_LEFT.collapsed, "SOCKET":tile_LEFT.socketsCollapsed[0], "POSITION":"LEFT"}
                    if hasUP_neigh:
                        tile_UP = grid[row-1][col]
                        tile.neig_UP = {"COLLAPSED":tile_UP.collapsed, "SOCKET":tile_UP.socketsCollapsed[1], "POSITION":"UP"}

                    
                    
                    
                    

    # FD. updateEntropy()
    # purp. update the entropy of a tile by calculating the valid tiles for every neighbour. This process is substractive. If a new
    # neighbour is found that has a subset of the current set of tile.potentialTiles, then keep making the list shorter
    # The entropy is updated inside the class function that is being called.
    def updateEntropy():
        for tileRow in grid:
            for tile in tileRow:
                # for each tile in the grid, if the entropy is not zero, take all the neighbours of this cell and filter the list of
                # potential tiles to be available
                if tile.entropy != 0:
                    tile.update_LOTILE_REFERENCE()
                    # input()
                    
    
    # FD. calculateLowestEntropy():
    # Signature: None -> int
    # purp. calculate the lowest entropy in the entire grid
    def calculateLowestEntropy():
        lowestEntropy = None
        for row,tileRow in enumerate(grid):
            for col,tile in enumerate(tileRow):
                if tile.entropy != 0:
                    if lowestEntropy is None or tile.entropy <= lowestEntropy:
                        lowestEntropy = tile.entropy
        return(lowestEntropy)


    # FD. selectTile():
    # Signature: None -> tile
    # purp. use the value of the lowest entropy to select a tile with the lowest entropy
    def selectTile():
        candidateTiles = []
        for row,tileRow in enumerate(grid):
            for col,tile in enumerate(tileRow):
                if tile.entropy == lowestEntropy:
                    candidateTiles.append(tile)
        if len(candidateTiles)>0:
            return(candidateTiles[0])

    
    updateNeighbours()
    updateEntropy()
    lowestEntropy = calculateLowestEntropy()
    tile = selectTile()

    # collapse the tile
    if tile != None:
        tile.collapse()

def initialize(seed=(0,0), name="0"):
    grid[seed[1]][seed[0]] = Tile(seed[0] * RES, seed[1] * RES, name)
    grid[seed[1]][seed[0]].entropy = 0
    grid[seed[1]][seed[0]].collapsed = True
    for tile in originalTiles:
        if tile["NAME"] == name:
            grid[seed[1]][seed[0]].socketsCollapsed = tile["SOCKETS"]

initialize((5,5),"15")

while "running":
    render()
    inputMan()
    updateGrid()
