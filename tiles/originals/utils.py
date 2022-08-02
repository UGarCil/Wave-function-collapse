# A suite of tools to manage sprite's resolution
# purp. create a new folder with the image of each sprite scaled at the desired resolution


# Modules
import os
from os.path import join as jn
import cv2

# CONSTANTS
PATH = os.getcwd()
itemRef = "none.png"


# Data def. RES
# res_% = int
# % is resolution
# interp. resolution of Arkanoid blocks
res_16 = 16
res_32 = 32
res_64 = 64
res_128 = 128
res_256 = 256


# Data def. LORES
# lores = [RES, RES, ...]
# interp. list of resolutions to tranform images
lores0 = [res_16]
lores1 = lores0 + [res_32]
lores2 = lores1 + [res_128]
lores3 = lores2 + [res_256]


# Data def. LOSPR
# lospr = [str, str, str]
# interp. list of sprites to resize
lospr0 = []
lospr1 = [spr for spr in os.listdir(PATH) if spr.endswith('.png')]


# Func. def. getMaxWidth()
# Signature: WIDTHS, <accumulator> -> <accumulator>
# purp. get index of the highest item number in the list

def getMaxWidth(WIDTHS, acc, poin):
    if acc == len(WIDTHS):
        return(poin)
    else:
        if WIDTHS[acc] > WIDTHS[poin]:
            score = getMaxWidth(WIDTHS, acc+1 ,acc)
        else:
            score = getMaxWidth(WIDTHS, acc+1 ,poin)
    return(score)


# Func. def. getMinWidth()
# Signature: WIDTHS, <accumulator> -> <accumulator>
# purp. get index of the highest item number in the list

def getMinWidth(WIDTHS, acc, poin):
    if acc == len(WIDTHS):
        return(poin)
    else:
        if WIDTHS[acc] < WIDTHS[poin]:
            score = getMinWidth(WIDTHS, acc+1 ,acc)
        else:
            score = getMinWidth(WIDTHS, acc+1 ,poin)
    return(score)


# Func. def. scale()
# Signature: <cv2.image>, I_MAXWIDTH -> (int, int, int)
# purp. calculate the ratio at which the sprites will need to be multiplied to scale them at the same size
def scale(spr, res):
    sc = res/spr.shape[1]
    # new_w = int((im.shape[1] / WIDTHS[REFWIDTH])*res)
    # new_h = int((im.shape[1]/im.shape[0])*new_w)
    return(sc)
    


# Func. def. newDims()
# Signature: <cv2.image>, SCALE -> (int, int, int)
# purp. calculate the ratio at which the sprites will need to be multiplied to scale them at the same size
def newDims(im, SCALE):
    new_w = int(im.shape[1]*SCALE)
    new_h = int(im.shape[0]*SCALE)
    return((new_w, new_h))

# Func. def. changeRes()
# Signature: LOSPR, RES, PATHS -> None
# purp. change the resolution of the given sprites

def changeRes(lospr, res, PATH):

    # Get the block's width, which will be the reference for the game's size
    for spr in lospr:
        if itemRef in spr:
            spr = cv2.imread(jn(PATH,spr), cv2.IMREAD_UNCHANGED)
            SCALE = scale(spr, res)
            break
    
    
    for spr in lospr:
        im_name = jn(PATH,spr)
        im = cv2.imread(im_name, cv2.IMREAD_UNCHANGED)
        new_dims = newDims(im, SCALE)
        im = cv2.resize(im, new_dims)
        file_name = f"{spr}"
        print(file_name)
        cv2.imwrite(jn(new_dir, file_name), im)


lores = lores3 + [res_64]

for res in lores:
    new_dir = jn(PATH, f"res_{str(res)}")
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    changeRes(lospr1, res, PATH)


