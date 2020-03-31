#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Provides Funcationality to build a Google Maps URL
https://developers.google.com/maps/documentation/urls/guide#directions-action
"""

import urllib.parse

def _encode_address(address_string):
    return urllib.parse.quote_plus(address_string,safe='')

def _encode_waypoints(waypoints):
    encoded_waypoints =  map(_encode_address, waypoints)
    print(encoded_waypoints)
    return '|'.join(encoded_waypoints)

def build_map_url(origin,waypoints,destination = None,travelmode='driving'):

    origin = _encode_address(origin)
    if destination is None:
        destination = origin
    else:
        destination = _encode_address(origin)
    
    waypoints = _encode_waypoints(waypoints)

    url = "https://www.google.com/maps/dir/?api=1"
    url += "&origin="+origin
    url += "&destination="+destination
    url += "&waypoints="+waypoints
    url += "&dir_action=navigate"

    return url

# print(
#     build_map_url(
#         origin="4407 1 Street Calgary, Alberta",
#         waypoints=[
#             "500 Centre Street SE Calgary, Alberta",
#             "88 Canada Olympic Rd SW, Calgary, AB"
#             ]
#     )
# )
#https://www.google.com/maps/dir/?api=1&origin=4407+1+Street+Calgary%2C+Alberta&destination=4407+1+Street+Calgary%2C+Alberta&waypoints=500+Centre+Street+SE+Calgary%2C+Alberta|88+Canada+Olympic+Rd+SW%2C+Calgary%2C+AB&dir_action=navigate


