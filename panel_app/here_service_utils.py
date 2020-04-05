import logging

import requests
import requests_cache

# Install Cache for requests:
requests_cache.install_cache('cache/tomtom_cache', backend='sqlite', expire_after=60 * 60 * 23 * 7)  # Cache for ~ 1 wk.
requests_cache.remove_expired_responses()  # Clean-up expired responses.

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

API_KEY = "***REMOVED***"
LIMIT_SEARCH_IN_PARAM = "circle:51.0447,-114.0719;r=80000"
PROXIMITY_TO_YYC = "51.0447,-114.0719,80000"
AUTOSUGGEST_URL = "https://autosuggest.search.hereapi.com/v1/autosuggest"
AUTOCOMPLETE_URL = "https://autocomplete.geocoder.ls.hereapi.com/6.2/suggest.json"

def _autocomplete_here(x: str):
    log.info(f"Autocomplete query : {x}")
    payload = {"query": x, "apiKey": API_KEY, "prox": PROXIMITY_TO_YYC}
    r = requests.get(AUTOCOMPLETE_URL, params=payload)
    data = r.json()
    if (len(data) < 1):
        return []
    return [suggestion["address"] for suggestion in data["suggestions"]]

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
