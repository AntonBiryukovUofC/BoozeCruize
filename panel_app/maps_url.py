#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Provides Funcationality to build a Google Maps URL
https://developers.google.com/maps/documentation/urls/guide#directions-action
"""

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

import time

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

def construct_gmaps_urls(latlongs_list,waypoints_batch_size=0):
    # Set-up to get url with 10 points:
    if len(latlongs_list)>=10:
        r = build_map_url(origin=latlongs_list[0], destination=latlongs_list[10], waypoints=latlongs_list[1:9])
    else:
        r = build_map_url(origin=latlongs_list[0], destination=latlongs_list[-1], waypoints=latlongs_list[1:-1])

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    driver.get(r.url)

    WebDriverWait(driver, 15).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    #driver.refresh()
    time.sleep(15)
    #WebDriverWait(driver, 15).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    #driver.save_screenshot('screenie.png')
    url = driver.current_url
    print(url)
    driver.close()

    batches = [0]
    urls = [url]

    return batches, urls


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
