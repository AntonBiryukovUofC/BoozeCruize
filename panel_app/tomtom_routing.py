from typing import List, Tuple, Dict

from panel_app.default_dest import DEFAULT_LATLONG, DEFAULT_DEST
import requests
import json

from panel_app.maps_url import build_map_url


def construct_gmaps_urls(latlongs_list, waypoints_batch_size=2):
    sub_latlong_list = []
    batches = []
    urls = []
    i = 0
    for ll in latlongs_list:
        # if (i > 4) or (i==len(latlongs_list)):
        # +2 is for origin + destination
        if len(sub_latlong_list) + 1 <= (waypoints_batch_size + 2):
            sub_latlong_list.append(ll)
        else:
            end_point = sub_latlong_list[-1]
            batches.append(sub_latlong_list)
            sub_latlong_list = [end_point, ll]
        i += 1
    # Exited for loop with the last element
    if len(sub_latlong_list) > 1:
        batches.append(sub_latlong_list)
    # Create URLs:
    for batch in batches:
        wp_list = [f'{x[0]},{x[1]}' for x in batch]
        if len(wp_list) >=3 :
            r = build_map_url(origin=wp_list[0], destination=wp_list[-1], waypoints=wp_list[1:-1])
        else:
            r = build_map_url(origin=wp_list[0], destination=wp_list[-1], waypoints=[])
        urls.append(r.url)

    return batches, urls
    # Now we have batches ready, we need to construct urls


def rearrange_waypoints(response_json):
    routes = response_json['routes'][0]
    new_x=[]
    for i in routes['guidance']['instructions']:
        if i['instructionType'] == 'LOCATION_WAYPOINT':
            new_x.append( (i['point']['latitude'],i['point']['longitude']))
    return new_x


def concat_latlongs(latlongs, separator=':'):
    latlong_base = [f'{x[0]},{x[1]}' for x in latlongs]
    latlong_concat = f'{separator}'.join(latlong_base)
    return latlong_concat


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
batches, urls = construct_gmaps_urls(latlongs_optimal, waypoints_batch_size=2)
print(urls)
