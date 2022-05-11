L=0

import board
import neopixel

pixel_pin = board.D21
num_pixels = 60

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=neopixel.GRBW)

pixels.fill(0)
pixels[L] = (0, 0, 255)
pixels.show()