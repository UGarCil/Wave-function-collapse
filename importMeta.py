import os
from os.path import join as jn

"""
Load the metadata for a particular set of tiles to be used by the class Tile
to preload the tiles to be used by the wave function collapse
"""

# DD. TILE_REFERENCE
# tileRed = {"NAME":str,"VALID":bool, "SOCKETS":[], "VALID_SOCKETS":[]}
# interp. a template tile to incorporate into this instance of Tile()



# FD. getMeta():
# Signature: str -> list
# Purp: Get the metadata of the set of tiles specified in a given path
def getMeta(path):
    dicts = []
    with open(jn(path,"metadata.txt"),"r") as file:
        file = file.readlines()
        for line in file:
            l = line.replace("\n","")
            l = l.split("\t")
            dicts.append({"NAME":l[0], "SOCKETS":[l[1],l[2],l[3],l[4]], "ROTATION":0, "FIXED":True if l[5]=="1" else False})
    return(dicts)