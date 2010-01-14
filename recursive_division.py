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


import random
import numpy
from numpy import array, zeros
from matplotlib import pyplot


def f1(img):
    '''This one does not quite work, but it is still pretty anyway. :)'''
    if max(img.shape)<=2:
        return
    mx = img.shape[0]/2
    my = img.shape[1]/2
    #print img.shape, mx, my
    img[mx,my] = (img[0,0] + img[0,-1] + img[-1,0] + img[-1,-1])/4 + random.random()
    f1(img[  :mx+1,   :my+1])
    f1(img[mx:    ,   :my+1])
    f1(img[  :mx+1, my:    ])
    f1(img[mx:    , my:    ])


def f2(img):
    '''Second try... Not what I expected, but nice anyway! :)'''
    if max(img.shape)<=1:
        return
    tx = img.shape[0]  # total x
    ty = img.shape[1]  # total y
    mx = tx/2  # mean x
    my = ty/2  # mean y
    #print img.shape, mx, my
    img[mx,my] = (img[0,0] + img[0,-1] + img[-1,0] + img[-1,-1])/4 + random.random()
    
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
            f2(img[ax:bx, ay:by])


def f3(img):
    '''Third try... Now I got something that remotely looks like a noise!'''
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

    img[mx,my] = (img[0,0] + img[0,-1] + img[-1,0] + img[-1,-1])/4 + random.random()
    
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
            f3(img[ax:bx, ay:by])



functions = [
    ("f1()", f1),
    ("f2()", f2),
    ("f3()", f3),
]

for funcname, func in functions:
    print funcname
    img = zeros((128,128))
    func(img)
    pyplot.imshow(img)
    pyplot.show()
