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
