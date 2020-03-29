import logging

import requests

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

API_KEY = "***REMOVED***"
LIMIT_SEARCH_IN_PARAM = "circle:51.0447,-114.0719;r=80000"
AUTOSUGGEST_URL = "https://autosuggest.search.hereapi.com/v1/autosuggest"


def _geocode_destination_here(x: str):
    log.info(f"Geocoding query : {x}")
    payload = {"q": x, "apiKey": API_KEY, "in": LIMIT_SEARCH_IN_PARAM}
    r = requests.get(AUTOSUGGEST_URL, params=payload)
    return r.json()


def _pull_lat_long_here(x, n_entry=0):
    entry_location_data = x["items"][n_entry]
    lat, lng = (
        entry_location_data["position"]["lat"],
        entry_location_data["position"]["lng"],
    )
    return (lat, lng)


def _pull_address_here(x, n_entry=0):
    entry_location_data = x["items"][n_entry]
    address = entry_location_data["address"]
    return address
