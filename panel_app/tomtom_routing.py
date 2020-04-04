import json

import requests_cache

from panel_app.default_dest import DEFAULT_LATLONG
from panel_app.here_service_utils import _geocode_destination_here, _pull_lat_long_here
from panel_app.maps_url import concat_latlongs, rearrange_waypoints, construct_gmaps_urls

requests_cache.install_cache('tomtom_cache', backend='sqlite', expire_after=3600)

latlongs_original = DEFAULT_LATLONG
base_url = 'https://api.tomtom.com/routing/1/calculateRoute'
API_KEY = '***REMOVED***'
# Start at the Bow, and finish there !
start_loc = "1402 9 Ave SE, Calgary"
end_loc = '2313 15a st se calgary'
start = _pull_lat_long_here(_geocode_destination_here(start_loc))
end = _pull_lat_long_here(_geocode_destination_here(end_loc))

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
