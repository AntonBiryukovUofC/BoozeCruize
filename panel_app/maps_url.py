#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Provides Funcationality to build a Google Maps URL
https://developers.google.com/maps/documentation/urls/guide#directions-action
"""

import requests


def build_map_url(origin, waypoints, destination=None, travelmode='driving'):
    if destination is None:
        destination = origin

    payload = {
        'origin': origin,
        'waypoints': '|'.join(waypoints),
        'destination': destination,
        'travelmode': travelmode,
        'dir_action': 'navigate'
    }

    r = requests.get('https://www.google.com/maps/dir/?api=1', params=payload)

    return (r)

# print(
#     build_map_url(
#         origin="4407 1 Street Calgary, Alberta",
#         waypoints=[
#             "500 Centre Street SE Calgary, Alberta",
#             "88 Canada Olympic Rd SW, Calgary, AB"
#             ]
#     ).url
# )
## Response: https://www.google.com/maps/dir/?api=1&origin=4407+1+Street+Calgary,+Alberta&waypoints=500+Centre+Street+SE+Calgary,+Alberta|88+Canada+Olympic+Rd+SW,+Calgary,+AB&destination=4407+1+Street+Calgary,+Alberta&travelmode=driving&dir_action=navigate
