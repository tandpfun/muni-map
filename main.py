import time
from requests import get
import json

route = 'KT'
url='https://retro.umoiq.com/service/publicJSONFeed?command=vehicleLocations&a=sf-muni&r=' + route

while True:
  positionData = get(url).json()
  vehicles = positionData['vehicle']

  for train in vehicles:
    if train['predictable'] == 'true':
      print(train['routeTag'] + ': ' + train['lon'] + ' ' + train['lat'])
  time.sleep(9)