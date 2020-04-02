from typing import List, Tuple, Dict

from panel_app.default_dest import DEFAULT_LATLONG, DEFAULT_DEST
import requests
import json

from panel_app.maps_url import build_map_url, concat_latlongs, rearrange_waypoints, construct_gmaps_urls

latlongs_original = DEFAULT_LATLONG
base_url = 'https://api.tomtom.com/routing/1/calculateRoute'
API_KEY = '***REMOVED***'
# Start at the Bow, and finish there !
start = (51.0480293, -114.0640164)
end = start
latlongs = [start] + latlongs_original + [end]
latlong_concat = concat_latlongs(latlongs)

url_locations = f'{base_url}/{latlong_concat}/json'
params = {'key': API_KEY,
          'travelMode': 'car',
          'computeBestOrder': 'true',
          'traffic': 'true',
          'instructionsType': 'text',
          'computeTravelTimeFor': 'all',
          }
#response = requests.get(url_locations, params=params)
#with open('./example_data/routing_tomtom_out.json','w') as f:
#    json.dump(response.json(),f)

# Load results from disk:
with open('./example_data/routing_tomtom_out.json') as f:
    response_json = json.load(f)
# response_json = response.json()
# Pull optimal order:
optimized_id_dict = response_json['optimizedWaypoints']
print(optimized_id_dict)

latlongs_original_optimal  = rearrange_waypoints(response_json)

latlongs_optimal = [start] + latlongs_original_optimal + [end]

print(f'Before optimization: {latlongs_original}')
print(f'After optimization: {latlongs_original_optimal}')
batches, urls = construct_gmaps_urls(latlongs_optimal, waypoints_batch_size=10)
print(urls)
