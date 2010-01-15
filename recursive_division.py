#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

# Trying to implement a noise-generation like the IMSMap xscreensaver.
#   /usr/lib/misc/xscreensaver/imsmap
# Quoting that xscreensaver description:
#   "This generates random cloud-like patterns. The idea is to take four points
#   on the edge of the image, and assign each a random "elevation". Then find
#   the point between them, and give it a value which is the average of the
#   other four, plus some small random offset. Coloration is done based on
#   elevation."


from functools import partial
import random
import numpy
from numpy import array, zeros
from matplotlib import pyplot
from matplotlib import cm  # colormaps


def f1(img, randfunc=random.random):
    '''First try... This one does not quite work, but it is still pretty anyway. :)'''
    if max(img.shape)<=2:
        return
    mx = img.shape[0]/2
    my = img.shape[1]/2
    #print img.shape, mx, my
    img[mx,my] = (img[0,0] + img[0,-1] + img[-1,0] + img[-1,-1])/4 + randfunc()
    f1(img[  :mx+1,   :my+1], randfunc)
    f1(img[mx:    ,   :my+1], randfunc)
    f1(img[  :mx+1, my:    ], randfunc)
    f1(img[mx:    , my:    ], randfunc)


def f2(img, randfunc=random.random):
    '''Second try...'''
    if max(img.shape)<=1:
        return
    tx = img.shape[0]  # total x
    ty = img.shape[1]  # total y
    mx = tx/2  # mean x
    my = ty/2  # mean y
    #print img.shape, mx, my
    img[mx,my] = (img[0,0] + img[0,-1] + img[-1,0] + img[-1,-1])/4 + randfunc()
    
    cuts = [
        ((0 ,mx+1),(0 ,my+1)),
        ((mx,tx  ),(0 ,my+1)),
        ((0 ,mx+1),(my,ty  )),
        ((mx,tx  ),(my,ty  )),
    ]
    for (ax,bx),(ay,by) in cuts:
        #print (ax,bx),(ay,by)
        if (ax < bx or ay < by) and not (
            ax == 0 and bx == tx and ay == 0 and by == ty
        ):
            f2(img[ax:bx, ay:by], randfunc)


def f3(img, randfunc=random.random):
    '''Third try...'''
    if max(img.shape)<=2:
        return
    tx = img.shape[0]  # total x
    ty = img.shape[1]  # total y
    mx = tx/2  # mean x
    my = ty/2  # mean y

    #if (mx == 0 and my == 0) or (mx == tx-1 and my == ty-1):
    #    return
    #print img.shape, mx, my

    img[ 0,my] = (img[ 0, 0] + img[ 0,-1])/2 + random.random()
    img[-1,my] = (img[-1, 0] + img[-1,-1])/2 + random.random()

    img[mx, 0] = (img[ 0, 0] + img[-1, 0])/2 + random.random()
    img[mx,-1] = (img[ 0,-1] + img[-1,-1])/2 + random.random()

    img[mx,my] = (img[0,0] + img[0,-1] + img[-1,0] + img[-1,-1])/4 + randfunc()
    
    cuts = [
        ((0 ,mx+1),(0 ,my+1)),
        ((mx,tx  ),(0 ,my+1)),
        ((0 ,mx+1),(my,ty  )),
        ((mx,tx  ),(my,ty  )),
    ]
    for (ax,bx),(ay,by) in cuts:
        #print (ax,bx),(ay,by)
        if (ax < bx or ay < by) and not (
            ax == 0 and bx == tx and ay == 0 and by == ty
        ):
            f3(img[ax:bx, ay:by], randfunc)



functions = [
    # It missed many pixels but it's still interesting
    ("f1(random())", f1, random.random),

    # Looks good, but does not look uniform
    ("f2(random())", f2, random.random),
    # Great-looking cloud-like noise!
    ("f2(-0.5 to 0.5)", f2, lambda:random.random()-0.5),

    # Looks kinda grid-like
    ("f3(random())", f3, random.random),
    # Looks kinda grid-like
    ("f3(-0.5 to 0.5)", f3, lambda:random.random()-0.5),
]


def main():
    size = (128, 128)
    #colormap = cm.gray
    colormap = cm.jet

    for funcname, func, randfunc in functions:
        print funcname
        img = zeros(size)
        func(img, randfunc)
        #pyplot.imshow(img, cmap=colormap)
        #pyplot.show()
        pyplot.imsave(fname=funcname+".png", arr=img, cmap=colormap)


if __name__ == '__main__':
    main()
