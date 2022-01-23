# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import argparse
import math
import asyncio
def rainbow(unused_addr,args,volume):
    rainbow_cycle(0.05)
import math
import random
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 960

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
mode = 0
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.8, auto_write=False, pixel_order=ORDER
)


def clean():
    for i in range(num_pixels):
        pixels[i] = (0,0,0)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def breath(s,c,t):
    counter = 0

    while(counter<=(180*t)):
        print(c,c[0],c[1],c[2])
        for i in range(num_pixels):
            f = abs(math.sin(math.radians(counter)))
            pixels[i] = (math.floor(c[0]*f),math.floor(c[1]*f),math.floor(c[2]*f))
        pixels.show()
        time.sleep(s)
        counter+=1

def wipe(s,c):
    for counter in range(num_pixels):
        print(counter)
        pixels[counter]=c
        time.sleep(s)
        pixels.show()

def blink(s,c):
    counter = 0
    f = 1
    while counter<=300:
        counter+=1
        time.sleep(s)
        for i in range(num_pixels):
            if random.randint(0,2)==1:
                pixels[i]=(math.floor(0*f),math.floor(0*f),math.floor(0*f))
            else:
                if i%2==0:
                    pixels[i]=(math.floor(c[0]*f),math.floor(c[1]*f),math.floor(c[2]*f))
                else:
                    k = math.floor(random.randint(0,255))
                    pixels[i]=(math.floor(k*f),math.floor(k*f),math.floor(k*f))

        pixels.show()

def blank(s):
    clean()
    pixels.show()
    time.sleep(s)

def triangleWipe(num,s):
    if(num == 0):
        for i in range(0,259):
            pixels[i] = (255,255,255)
            pixels.show()
            time.sleep(s)
    elif(num==1):
        for i in range(593,852):
            pixels[i] = (255,255,255)
            pixels.show()
            time.sleep(s)
    elif(num==2):
        for i in range(265,586):
            pixels[i] = (255,255,255)
            pixels.show()
            time.sleep(s)
        for i in range(858,925):
            pixels[i] = (255,255,255)
            pixels.show()
            time.sleep(s)

def triangleBreath(num,s,c,t):
    counter = 0
    while(counter<=(180*t)):
        clean()
        f = abs(math.sin(math.radians(counter)))
        if(num == 0):
            for i in range(0,259):
                if random.randint(0,2)==1:
                    pixels[i]=(math.floor(255*f),math.floor(255*f),math.floor(255*f))
                else:
                    pixels[i] = (math.floor(c[0]*f),math.floor(c[1]*f),math.floor(c[2]*f))
            pixels.show()
            time.sleep(s)
        elif(num==1):
            for i in range(593,852):
                if random.randint(0,2)==1:
                    pixels[i]=(math.floor(255*f),math.floor(255*f),math.floor(255*f))
                else:
                    pixels[i] = (math.floor(c[0]*f),math.floor(c[1]*f),math.floor(c[2]*f))
            pixels.show()
            time.sleep(s)
        elif(num==2):
            for i in range(265,586):
                if random.randint(0,2)==1:
                    pixels[i]=(math.floor(255*f),math.floor(255*f),math.floor(255*f))
                else:
                    pixels[i] = (math.floor(c[0]*f),math.floor(c[1]*f),math.floor(c[2]*f))
            for i in range(858,925):
                if random.randint(0,2)==1:
                    pixels[i]=(math.floor(255*f),math.floor(255*f),math.floor(255*f))
                else:
                    pixels[i] = (math.floor(c[0]*f),math.floor(c[1]*f),math.floor(c[2]*f))
            pixels.show()
            time.sleep(s)
        counter+=1


clean()
while True:
    blink(0.01,(100,100,200))
    triangleBreath(0,0.01,(100,100,120),1)
    triangleBreath(1,0.01,(100,100,120),1)
    triangleBreath(2,0.01,(100,100,120),1)

    #breath(0.005,(50,50,230),5)
    #blank(5)
    #breath(0.005,(245,121,66),2)
    #blank(5)
    #wipe(0.01,(150,150,150))
    #blank(5)
    #wipe(0.01,(0,0,0))
    #clean()
    #blueBlink()
    #blueBlink()
    #blueBlink()
    #blueBlink()
    #pixels[925]=(255,255,255)
    #pixels.show()
