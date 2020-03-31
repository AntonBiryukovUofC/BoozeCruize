from panel_app.default_dest import DEFAULT_LATLONG
import requests

latlongs = DEFAULT_LATLONG
base_url = 'https://api.tomtom.com/routing/1/calculateRoute'
API_KEY = '***REMOVED***'
# Start at the Bow, and finish there !
start = [51.0480293, -114.0640164]
end = start
latlongs = [start] + latlongs + [end]
latlong_base = [f'{x[0]},{x[1]}' for x in latlongs]
latlong_concat = ':'.join(latlong_base)
url_locations = f'{base_url}/{latlong_concat}/json'

params = {'key':API_KEY,
          'travelMode': 'car',
          'computeBestOrder': 'true',
          'traffic': 'true',
          'instructionsType':'text',
          'computeTravelTimeFor':'all',
          }

response = requests.get(url_locations, params=params)

