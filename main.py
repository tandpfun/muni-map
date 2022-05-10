import time
from requests import get
import json
from math import radians, cos, sin, asin, sqrt
import board
import neopixel

pixel_pin = board.D21
num_pixels = 60

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=neopixel.GRBW)

pixels.fill((0, 0, 255))
pixels.show()
time.sleep(5)
pixels.fill(0)
pixels.show()

def dist(lat1, long1, lat2, long2):
    """
    Replicating the same formula as mentioned in Wiki
    """
    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    # haversine formula 
    dlon = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km 

pixel_locations = {
  0: (37.755265, -122.462680),
  1: (37.787849, -122.403262),
  2: (0.787849, -10.403262)
}

route = 'KT'
url='https://retro.umoiq.com/service/publicJSONFeed?command=vehicleLocations&a=sf-muni&r=' + route

while True:
  positionData = get(url).json()
  vehicles = positionData['vehicle']

  for train in vehicles:
    if train['predictable'] == 'true':

      distances = {}
      for key in pixel_locations:
        pixel = pixel_locations[key]
        distances[key] = dist(float(train['lat']), float(train['lon']), pixel[0], pixel[1])

      closest_light = sorted(distances.items(), key=lambda x: x[1])[0][0]
      pixels[closest_light] = (0, 0, 255)
      
      print('KT ' + train['lat'] + ', ' + train['lon'] + ' => ' + str(closest_light))
  pixels.show()
  time.sleep(9)