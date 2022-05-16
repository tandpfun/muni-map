import time
from requests import get
import json
from math import radians, cos, sin, asin, sqrt
import board
import neopixel

pixel_pin = board.D21
num_pixels = 31

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=.8, auto_write=False, pixel_order=neopixel.GRBW)

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
  8: (37.7538473, -122.4440256),
  9: (37.7592647, -122.4430856),
  10: (37.7617466, -122.4391838),
  11: (37.7636388, -122.4332611),
  12: (37.7693226, -122.4261534),
  13: (37.7693226, -122.4261534),
  14: (37.7843925, -122.4103136),
  15: (37.7870418, -122.4059329),
  16: (37.7877065, -122.4038310),
  17: (37.7923252, -122.4004900),
  18: (37.7899545, -122.3899130),
  19: (37.7832515, -122.3890722),
  20: (37.7736165, -122.3883198),
  21: (37.7655312, -122.3899130),
  22: (37.7610894, -122.3882771),
  23: (37.7549432, -122.3884968),
  24: (37.7549432, -122.3884968),
  25: (37.7451210, -122.3880985),
  26: (37.7398820, -122.3904242),
  27: (37.7335996, -122.3889836),
  28: (37.7287449, -122.3941174),
  29: (37.7229074, -122.3960203),
  30: (37.7229074, -122.3960203),
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
      closest_light_distance = sorted(distances.items(), key=lambda x: x[1])[0][1]

      

      if 'dirTag' in train.keys():
        if train['dirTag'] == "KT___I_F20":
          dirColor = (150, 0, 0)
        else:
          dirColor = (0, 0, 255)
      else:
        dirColor = (255, 255, 0)

      pixels[closest_light] = dirColor
      
      print('KT ' + train['lat'] + ', ' + train['lon'] + ' => ' + str(closest_light) + ' ' + str(closest_light_distance))
  pixels.show()
  time.sleep(10)