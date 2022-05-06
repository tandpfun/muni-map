import time
import board
import neopixel

pixel_pin = board.D21
num_pixels = 60

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=True, pixel_order=neopixel.GRBW)

i=0
while True:
  i = i + 1
  pixels[i % 60] = (0, 0, 255)
  pixels[(i - 2) % 60] = (0, 0, 0)
  time.sleep(.25)