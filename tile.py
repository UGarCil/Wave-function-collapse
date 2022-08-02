from numpy import place
import pygame
import random
from importMeta import getMeta as gM
# CONSTANTS
RES = 32
PATH = "./tiles/"





# DD. ORIGINAL_TILES
# originalTiles = [TILE_REFERENCE, ...]
# interp. the original set of reference tiles
# originalTiles = [tileRef_0, tileRef_1,tileRef_2, tileRef_3]
originalTiles = gM(PATH)

# DD. POSSIBLE_SOCKETS
# ALLCONFIGURATIONS = [TILE_REFERENCE]
# interp. a list containing all the versions of all tiles of reference in all rotations. Each unique configuration is saved once
ALLCONFIGURATIONS = []

for tileRef in originalTiles:
    for rotation in range(4):
        newConfiguration = ["" for x in range(4)]
        for idx,socket in enumerate(tileRef["SOCKETS"]):
            newConfiguration[(idx+rotation)%len(newConfiguration)] = socket
        
        if tileRef["FIXED"]:
            newTileRef = {"NAME":tileRef["NAME"],"SOCKETS":newConfiguration, "ROTATION":0}
        else:
            newTileRef = {"NAME":tileRef["NAME"], "SOCKETS":newConfiguration, "ROTATION":rotation}
        ALLCONFIGURATIONS.append(newTileRef)


# CD. TILE
# tile = Tile()
# a tile to be rendered in the grid
class Tile():

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.pyImage = pygame.image.load(f"{PATH}res_{RES}/{self.name}.png")
        self.rect = self.pyImage.get_rect()
        self.rect.topleft = (self.x, self.y)
                


        # DD. LOTILE_REFERENCE
        # self.potentialTiles = []
        # self.potentialTiles = [self.tileRef_1, \
        #                        self.tileRef_2, \
        #                        self.tileRef_3, \
        #                        self.tileRef_4, \
        #                        self.tileRef_5, \
        #                        self.tileRef_6]
        self.potentialTiles = ALLCONFIGURATIONS

        # DD. COLLAPSED
        # self.collapsed = bool
        # interp. whether a tile is collapsed or not
        self.collapsed = False


        # DD. SOCKETS_WHEN_COLLAPSED
        # self.socketsCollapsed = [str, ..., n=4]
        # interp. the final set of sockets when the tile is collapsed
        self.socketsCollapsed = ["" for i in range(4)]

        # DD. ENTROPY
        # self.entropy = int
        # interp. count of potential tiles our general tile can take before it is collapsed
        self.entropy = len(ALLCONFIGURATIONS)

        # DD. NEIGHBOUR
        # self.neig_% = {"COLLAPSED":bool, "SOCKET":str, "POSITION":str}
        # interp. the identity of the neighbor at any given frame will determine the rotation of the "SOCKETS" from a given TILE_REFERENCE
        # - COLLAPSED: whether a given neighbour is collapsed
        # - SOCKET:    identity of the socket facing our current tile
        # - POSITION:  the position of the neighbour relative to our current tile
        self.neig_RIGHT = {"COLLAPSED":None, "SOCKET":None, "POSITION":None}
        self.neig_DOWN = {"COLLAPSED":None, "SOCKET":None, "POSITION":None}
        self.neig_LEFT = {"COLLAPSED":None, "SOCKET":None, "POSITION":None}
        self.neig_UP = {"COLLAPSED":None, "SOCKET":None, "POSITION":None}


    # FD. socketMatch()
    # Signature: socket, socketMatch -> bool
    # purp. determine if two sockets complement each other
    def socketMatch(self,socket, targetSocket):
        for idx_letter,_ in enumerate(socket):   #For each letter in this socket
            #fill the list of matchingSockets based on the complementaerity of the letters in the socket
            if socket[idx_letter] != targetSocket[-(idx_letter+1)]:
                return False
        return True
                        


    # FD. update_LOTILE_REFERENCE()
    # Signature: 
    # purp. filter the list of potentialTiles to extract those that fit in a given socket
    def update_LOTILE_REFERENCE(self):
        # Go through each of neighbours available
        placeHolderTileSet = []
        # For each of the potential tiles, evaluate if this configuration and tile matches the sockets of all the collapsed neighbours
        for potTile in self.potentialTiles:
            validTile = True
            if self.neig_RIGHT["COLLAPSED"] and not self.socketMatch(potTile["SOCKETS"][0], self.neig_RIGHT["SOCKET"]):
                validTile = False
            if self.neig_DOWN["COLLAPSED"] and not self.socketMatch(potTile["SOCKETS"][1], self.neig_DOWN["SOCKET"]):
                validTile = False
            if self.neig_LEFT["COLLAPSED"] and not self.socketMatch(potTile["SOCKETS"][2], self.neig_LEFT["SOCKET"]):
                validTile = False
            if self.neig_UP["COLLAPSED"] and not self.socketMatch(potTile["SOCKETS"][3], self.neig_UP["SOCKET"]):
                validTile = False
            
            if validTile:
                placeHolderTileSet.append(potTile)
        self.potentialTiles = placeHolderTileSet
        



        seenTiles = []
        for tile in self.potentialTiles:
            if tile["NAME"] not in seenTiles:
                seenTiles.append(tile["NAME"])
        self.entropy = len(seenTiles)








    # FD. collapse()
    # purp. collapse the tile by selecting a random candidate tile from the potential tiles, change the rotation relative to neighbors and update the list socketsCollapsed
    def collapse(self):
        # the list self.potentialTiles contains a list of the unique tiles available for a given spot already. We simpy need to pick one and apply the rotation to the
        # tile
        self.collapsed = True
        potTile = random.choice(self.potentialTiles)
        self.name = potTile["NAME"]
        self.pyImage = pygame.image.load(f"{PATH}res_{RES}/{self.name}.png")
        self.socketsCollapsed = potTile["SOCKETS"]
        self.entropy = 0
        self.pyImage = pygame.transform.rotate(self.pyImage, -potTile["ROTATION"] * 90)





        
        
        

            

            



                    


    





    
        