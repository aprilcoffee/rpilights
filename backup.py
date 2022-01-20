# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import argparse
import math
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc.osc_server import AsyncIOOSCUDPServer
import asyncio
def rainbow(unused_addr,args,volume):
    rainbow_cycle(0.05)
def print_volume_handler(unused_addr,args,volume):
    print("[{0}] ~{1}".format(args[0],volume))
def print_compute_handler(unused_addr,args,volume):
    try:
        print("[{0}]~{1}".format(args[0],args[1](volume)))
    except ValueError: pass


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 300

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
)


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


parser =argparse.ArgumentParser()
parser.add_argument("--ip",default="0.0.0.0",help="the ip")
parser.add_argument("--port",type=int,default=5005,help="port")
args=parser.parse_args()

dis = dispatcher.Dispatcher()
dis.map("/1/push1",rainbow,"RainBOW")
dis.map("/1/push2",print_volume_handler,"Volume")
dis.map("/3",print_compute_handler,"Log volume",math.log)

#server=osc_server.ThreadingOSCUDPServer((args.ip,args.port),dis)
#server = AsyncIOOSCUDPServer((args.ip,args.port),dispatcher,asyncio.get_event_loop())
#server.serve()
async def init_main():
    server=AsyncIOOSCUDPServer((args.ip,args.port),dis,asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()

    await loop()
    transport.close()

async def loop():
    # Comment this line out if you have RGBW/GRBW NeoPixels
    #pixels.fill((255, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # Comment this line out if you have RGBW/GRBW NeoPixels
    #pixels.fill((0, 255, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0, 0))
    #pixels.show()
    #time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    #pixels.fill((255, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255, 0))
    pixels.show()
    #while True:
    #    await asyncio.sleep(0.1)
    #    rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step

    #server.serve()
#asyncio.run(init_main())
while True:   
    pixels.fill((100, 0, 200, 0))
    pixels.show()
    time.sleep(0.1)
    pixels.fill((100,100,200,0))
    pixels.show()
    time.sleep(0.1)


