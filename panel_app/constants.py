import os

from bokeh.models import WMTSTileSource

if not('API_KEY_TOMTOM' in os.environ.keys()):
    raise ValueError('Please define environmental variable API_KEY_TOMTOM before using the Booze Cruise! Check out '
                     'README.md for details...')
else:
    API_KEY_TOMTOM = os.environ.get('API_KEY_TOMTOM')

if not('API_KEY_HERE' in os.environ.keys()):
    raise ValueError('Please define environmental variable API_KEY_HERE before using the Booze Cruise! Check out '
                     'README.md for details...')
else:
    API_KEY_HERE = os.environ.get('API_KEY_HERE')

base_url_tomtom = 'https://api.tomtom.com/routing/1/calculateRoute'

WIDTH_DEFAULT = 1000
HEIGHT_DEFAULT = 150
N_RANDOM_DAYS = 7
FRAC = 0.5

# Bokeh-related contants:
tile_options = {
    'url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{Z}/{Y}/{X}.png',
    'attribution': """
'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom,
Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL,
Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
    """}
OSM_tile_source = WMTSTileSource(**tile_options)
waypoint_url = 'https://upload.wikimedia.org/wikipedia/commons/8/88/Map_marker.svg'
# Waypoint size
w_image=25
h_image=600/390*w_image
tooltips = [
    ("Address","@label"),
]
