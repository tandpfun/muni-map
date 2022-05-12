import time
from requests import get
import json
from math import radians, cos, sin, asin, sqrt
import board
import neopixel

pixel_pin = board.D21
num_pixels = 60

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=.5, auto_write=False, pixel_order=neopixel.GRBW)

pixels.fill((0, 170, 255))
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
  0: (37.7230964, -122.4502238),
  1: (37.7260713, -122.4679468),
  2: (37.7367822, -122.4700100),
  3: (37.7393242, -122.4650617),
  4: (37.7404289, -122.4658876),
  5: (37.7462629, -122.4605402),
  6: (37.7504174, -122.4541490),
  7: (37.7511191, -122.4529176),
  8: (37.7521660, -122.4456180)
}

route = 'KT'
url='https://retro.umoiq.com/service/publicJSONFeed?command=vehicleLocations&a=sf-muni&r=' + route

while True:
  positionData = get(url).json()
  vehicles = positionData['vehicle']

  pixels.fill(0)

  for train in vehicles:
    if train['predictable'] == 'true':

      distances = {}
      for key in pixel_locations:
        pixel = pixel_locations[key]
        distances[key] = dist(float(train['lat']), float(train['lon']), pixel[0], pixel[1])

      closest_light = sorted(distances.items(), key=lambda x: x[1])[0][0]

      dirColor = (0, 0, 255)

      if train['dirTag'] == "KT___I_F20":
        dirColor = (255, 0, 0)

      pixels[closest_light] = dirColor
      
      print('KT ' + train['lat'] + ', ' + train['lon'] + ' => ' + str(closest_light))
  pixels.show()
  time.sleep(10)