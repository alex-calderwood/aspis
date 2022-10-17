import random
import board
import time
import neopixel
import sys


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
			

def neo(strip, index, color, wait_ms=50):
	"""light up one pixel."""
	strip.setPixelColor(0, color)
	strip.show()
	#time.sleep(wait_ms/1000.0)		

def new():
	pass

pixels = neopixel.NeoPixel(board.D18, 5, pixel_order=neopixel.RGB)
# pixels.fill((0, 125, 125))
pixels[0] = (255, 255, 255)
pixels[1] = (255, 0, 0)
pixels[2] = (0, 255, 0)
pixels[3] = (0, 0, 255)
pixels[4] = (0, 255, 255)
pixels.show()

exit()

n = 5
r = 0
g = 0
b = 0
a = 5

while True:
	for p in range(n):
		r += random.randint(0, a)
		r %= 256
		g += random.randint(0, 2*a)
		g %= 256
		b += random.randint(0, 3*a)
		b %= 256
		print(p, r, g, b)
		pixels[p] = (r, g, b)
	
	time.sleep(0.1)

def old():
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	print('Press Ctrl-C to quit.')
	#while True:
	print(sys.argv)
	
	
	print ('Welcome, Press Ctrl-C to quit.')

	strip.begin()
	index = sys.argv[1]

	color = sys.argv[2].split(",")
	green = int(color[0])
	red = int(color[1])
	blue = int(color[2])
	#print "count: " + str(count)	
	neo(strip, index, Color(green,red,blue))

if __name__ == "__main__":
	new()	
