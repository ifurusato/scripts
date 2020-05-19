#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 by Murray Altheim. All rights reserved. This file is part of
# the Robot Operating System project and is released under the "Apache Licence, 
# Version 2.0". Please see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2020-05-19
# modified: 2020-05-19
# see:      https://robots.org.nz/2020/05/19/four-corners/
# This script is used as a possible solution for the Four Corners Competition,
# as a way for a robot to locate the trajectory to a distant target.
#

import math, colorsys, traceback
import picamera
import picamera.array
from picamera.array import PiRGBArray

from colorama import init, Fore, Style
init()

PINK_RGB = [151, 55, 180] # hue = 286

def color_distance(e0, e1):
    hsv0 = colorsys.rgb_to_hsv(e0[0], e0[1], e0[2])
    hsv1 = colorsys.rgb_to_hsv(e1[0], e1[1], e1[2])
    dh = min(abs(hsv1[0]-hsv0[0]), 360-abs(hsv1[0]-hsv0[0])) / 180.0
    ds = abs(hsv1[1]-hsv0[1])
    dv = abs(hsv1[2]-hsv0[2]) / 255.0
    distance = math.sqrt(dh*dh+ds*ds+dv*dv)
    return distance


def print_row(image, y):
    print(Fore.WHITE + '{:d}\t'.format(y) + Fore.BLACK, end='')
    for x in reversed(range(0,image.shape[1])):
        _rgb = image[y,x]
        dist = color_distance(_rgb, PINK_RGB)
        _hilite = get_hilite(dist)
        print(_hilite + "▪", end='')
    print(Style.RESET_ALL)


def get_hilite(dist):
        if  dist < 0.025:
            return Fore.MAGENTA + Style.BRIGHT
        elif dist < 0.05:
            return Fore.MAGENTA + Style.NORMAL
        elif dist < 0.08:
            return Fore.RED + Style.BRIGHT
        elif dist < 0.10:
            return Fore.RED + Style.NORMAL
        elif dist < 0.15:
            return Fore.YELLOW + Style.BRIGHT
        elif dist < 0.2:
            return Fore.YELLOW + Style.NORMAL
        elif dist < 0.3:
            return Fore.GREEN + Style.BRIGHT
        elif dist < 0.4:
            return Fore.GREEN + Style.NORMAL
        elif dist < 0.5:
            return Fore.CYAN + Style.NORMAL
        elif dist < 0.6:
            return Fore.BLUE + Style.BRIGHT
        elif dist < 0.7:
            return Fore.BLUE + Style.NORMAL
        elif dist < 0.8:
            return Fore.BLACK + Style.NORMAL
        else:
            return Fore.BLACK + Style.DIM


# ..............................................................................

try:
    print(Fore.CYAN + 'starting...' + Style.RESET_ALL)

    # don't necessarily process the whole image (it takes a long time)
    _start_row = 180 # the bottom row of the image to be processed
    _end_row   = 260 # the top row of the image to be processed

    with picamera.PiCamera() as camera:
        with PiRGBArray(camera) as output:
            camera.resolution = (640, 480)
            camera.capture(output, 'rgb')
            image = output.array
            print(Fore.YELLOW + 'Captured {:d}x{:d} image\n'.format(image.shape[1], image.shape[0]) + Style.RESET_ALL)
            _width = image.shape[1]
            _height = image.shape[0]
            print(Fore.YELLOW + 'Captured size {:d}x{:d} image'.format(_width, _height) + Style.RESET_ALL)
            for _row in reversed(range(_start_row + 1,_end_row + 1)):
                print_row(image, _row)

except picamera.PiCameraMMALError:
    print(Fore.RED + Style.BRIGHT + 'could not get camera: in use by another process.' + Style.RESET_ALL)
except Exception:
    print(Fore.RED + Style.BRIGHT + 'error starting ros: {}'.format(traceback.format_exc()) + Style.RESET_ALL)

print(Fore.CYAN + 'complete.' + Style.RESET_ALL)

