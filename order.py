import random
import board
import time
import neopixel
import sys
import math
import numpy as np


# LED strip configuration:
LED_COUNT      = 5      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
# LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
			

pixels = neopixel.NeoPixel(board.D18, 5, pixel_order=neopixel.RGB)

palettes = {
        "rainbow": [
                [0.5, 0.5, 0.5],
                [0.5, 0.5, 0.5],
                [1, 1, 1],
                [0, .33, .67],
        ],
        "warmish": [            
                [0.5, 0.5, 0.5],
                [0.5, 0.5, 0.5],
                [1.0, 0.7, 0.4],
                [0.0, 0.15, 0.2],
        ],
        "red": [
                [0.8, 0.5, 0.4],
                [0.2, 0.4, 0.2],
                [2, 1, 1],
                [0, .25, .25],
        ],
        "redblue": [
                [0.5, 0.5, 0.5],
                [0.5, 0.5, 0.5],
                [1, 1, 1],
                [0, 0.1, 0.2],
        ]  
}

def color(t, pallet="redblue"):
    a, b, c, d = palettes[pallet]
    a, b, c, d = np.array(a), np.array(b), np.array(c), np.array(d)
    c = a + b * np.cos(2 * math.pi * (c * t + d))

    return (c * 256) % 256

i = 0

while True:
	for p in range(LED_COUNT):
                i += 1
                t = (i * 0.001) % 1
                
                r, g, b = color(t)
                
                if (i % 100 == 0):
                    print(t, r, g, b)
                pixels[p] = (r, g, b)

	time.sleep(0.01)
