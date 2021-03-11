import sys

import requests
from bokeh.plotting import figure
from dotenv import load_dotenv, find_dotenv

sys.path.insert(0, '.')

from panel_app.constants import API_KEY_TOMTOM, base_url_tomtom
from panel_app.route_viz import create_label_df, create_legs_df, create_bokeh_figure, default_altair

from typing import Dict, Tuple
import pandas as pd
import numpy as np
import panel as pn
import panel.widgets as pnw
import param
import altair as alt
import logging
from panel_app.maps_url import concat_latlongs, rearrange_waypoints, construct_gmaps_urls
from panel_app.default_dest import DEFAULT_DEST
from panel_app.here_service_utils import _geocode_destination_here, _pull_lat_long_here, \
    _pull_address_here
from bokeh.models import AutocompleteInput

alt.data_transformers.disable_max_rows()
pn.extension("vega")

logger_bc = logging.getLogger(__name__)
logger_bc.setLevel(logging.DEBUG)

load_dotenv(find_dotenv())


def generateAutocompleteWidget(destination_number=1, initial_value="", name=None, placeholder=None):
    if name is None:
        name = f'Destination {destination_number}'
    if placeholder is None:
        placeholder = 'Enter Location'
    autocomplete = AutocompleteInput(
        name=name, completions=['test'], title=name,
        min_characters=3, value=initial_value, placeholder=placeholder)

    def autocomplete_callback(attr, old, new):
        if (len(new) > 0):
            pass

    autocomplete.on_change('value_input', autocomplete_callback)

    return autocomplete


def _pull_value_wlist(widget):
    '''
    Helper function to pull values from a widget
    Args:
        widget:

    Returns:

    '''
    return widget.value


def create_destination_inputs(n=2, prev_destinations=None, init_vals=None):
    '''
    Creates a bank of destination text input widgets

    Args:
        n:
        prev_destinations:
        init_vals:

    Returns:

    '''
    if init_vals is not None:
        assert len(init_vals) == n
    else:
        init_vals = [""] * n

    if prev_destinations is None:
        wlist = []
        for i in range(n):
            name_widget = f"Destination {i + 1}"

            widget = pn.widgets.TextInput(name=name_widget, value=init_vals[i])
            wlist.append(widget)

    else:
        wlist = prev_destinations
        n_old = len(prev_destinations)
        print(f"Nold: {n_old} , new: {n}")

        if n > n_old:
            for i in range(n_old, n):
                name_widget = f"Destination {i + 1}"
                widget = pn.widgets.TextInput(name=name_widget, value="")
                wlist.append(widget)
        else:
            wlist = wlist[0:n]

    widget_all = pn.Column(*wlist)
    return widget_all, wlist


def clean_space_callback(target, event):
    target.value = event.new.strip('\n')

# Pre-createe some default destination widgets
destinations_pane_default, destinations_wlist_default = create_destination_inputs(
    n=len(DEFAULT_DEST), prev_destinations=None, init_vals=DEFAULT_DEST
)


class ReactiveDashboard(param.Parameterized):
    title = pn.pane.Markdown("# Booze Cruise YYC")
    # Add a widget that picks the environment and bucket
    number_dest = param.Integer(
        len(DEFAULT_DEST), label="Select number of destinations", bounds=(0, 15)
    )
    waypoints_per_batch = param.Integer(
        10, label="Waypoints per batch in Google Maps URL", bounds=(1, 12)
    )

    progress_bar = pnw.misc.Progress(
        active=False,
        bar_color="light",
        value=None,
        width_policy="max",
        sizing_mode="stretch_width",
    )

    date_custom_map: Dict = {}
    get_best_route_action = pnw.Button(name="Optimize Route", button_type="primary")
    get_batch_destinations = pnw.Button(name="Import Destinations", button_type="primary")

    destinations_pane = param.Parameter(default=destinations_pane_default)
    destinations_wlist = param.List(default=destinations_wlist_default)

    destinations_latlongs = param.List(default=[(0, 0), (0, 0)], precedence=-0.5)
    gmaps_urls = param.List(default=['', ''], precedence=-0.5)

    destinations_addresses = param.List(default=[(0, 0), (0, 0)], precedence=-0.5)
    all_dates_forecast = default_altair()
    default_plot = pn.Pane(default_altair())

    start_location = param.String(label='Departure Point')
    end_location = param.String(label='Destination Point')
    batch_import_str = pnw.TextAreaInput(name='Batch import',
                                         placeholder='Add locations here by e.g. copy-pasting from a spreadsheet',
                                         width=300,
                                         height=450,
                                         sizing_mode='scale_both'
                                         )
    is_start_equal_end = param.Boolean(default=True, label='My final destination same as Departure Point')
    start_latlong = param.Tuple(default=(0, 0), precedence=-0.5)
    end_latlong = param.Tuple(default=(0, 0), precedence=-0.5)
    df_label = param.DataFrame(precedence=-0.5, default=pd.DataFrame())
    df_all_pts = param.DataFrame(precedence=-0.5, default=pd.DataFrame())

    # Placeholder for tabs:
    tabs = pn.Tabs(('Batch Location Import', pn.Row()))

    tmp_buffer = 'Temporary buffer'

    @param.depends("number_dest", watch=True)
    def change_destinations_number(self):
        new_destinations = create_destination_inputs(
            n=self.number_dest, prev_destinations=self.destinations_wlist
        )
        self.destinations_pane, self.destinations_wlist = (
            new_destinations[0],
            new_destinations[1],
        )
        self.tabs.active = 0
        return self.destinations_pane

    def geocode_dest_list_latlong(self, event, destinations_list):
        self.progress_bar.bar_color = 'info'
        self.progress_bar.active = True

        logger_bc.info(event)
        destinations_str = [_pull_value_wlist(x) for x in destinations_list]
        logger_bc.info(f"Geocoding the destinations list: {destinations_str}")
        destinations_jsons = [_geocode_destination_here(x) for x in destinations_str]
        latlongs = [_pull_lat_long_here(x, n_entry=0) for x in destinations_jsons]
        addresses = [_pull_address_here(x, n_entry=0) for x in destinations_jsons]

        logger_bc.info(latlongs)
        logger_bc.info(addresses)

        # latlongs = [(random.randint(i, 20), random.randint(i, 40)) for i in range(len(destinations_list))]
        self.destinations_latlongs = latlongs
        self.destinations_addresses = addresses
        logger_bc.info(self.destinations_latlongs)
        logger_bc.info(self.destinations_addresses)

        self.progress_bar.bar_color = 'light'
        self.progress_bar.active = False

    @param.depends('destinations_latlongs')
    def show_latlongs(self):
        destinations_str = [_pull_value_wlist(x) for x in self.destinations_wlist]

        x = f' Length = {len(self.destinations_wlist)}, vals = {destinations_str}'
        x += f' Latlongs = {len(self.destinations_latlongs)}, vals = {self.destinations_addresses}'

        res_md = pn.pane.Markdown(x)
        return res_md

    def find_best_route(self, event, latlong_list, start_point: Tuple = (0, 0), end_point: Tuple = (0, 0)):
        '''
        Find optimal route using TomTom routing service
        :param start_point:
        :param end_point:
        :param event:
        :param latlong_list:
        :return:
        '''
        self.progress_bar.bar_color = 'info'
        self.progress_bar.active = True

        latlongs = [start_point] + latlong_list + [end_point]
        latlong_concat = concat_latlongs(latlongs)

        url_locations = f'{base_url_tomtom}/{latlong_concat}/json'
        params = {'key': API_KEY_TOMTOM,
                  'travelMode': 'car',
                  'computeBestOrder': 'true',
                  'traffic': 'true',
                  'instructionsType': 'text',
                  'computeTravelTimeFor': 'all',
                  }
        response = requests.get(url_locations, params=params)
        response_json = response.json()
        latlongs_original_optimal = rearrange_waypoints(response_json)

        sorted_addresses = self.get_ordered_addresses(latlongs_original_optimal)
        sorted_addresses_with_terminals = [self.start_location] + sorted_addresses + [self.end_location]
        _, urls = construct_gmaps_urls(sorted_addresses_with_terminals, waypoints_batch_size=10)
        self.gmaps_urls = urls

        # Prepare dataframes to feed Bokeh with
        self.df_label = create_label_df(start_point, end_point, latlongs_original_optimal,
                                        sorted_addresses=sorted_addresses,
                                        start_location=self.start_location, end_location=self.end_location)
        self.df_all_pts = create_legs_df(response_json)

        self.progress_bar.bar_color = 'light'
        self.progress_bar.active = False

    @param.depends('df_all_pts')
    def plot_bokeh(self):
        if self.df_all_pts.shape[0] > 0:
            print('Plotting bokeh')
            p = create_bokeh_figure(df_all_pts=self.df_all_pts, df_label=self.df_label)
        else:
            p = figure()
        return p

    def get_ordered_addresses(self, ordered_latlongs):
        """
        Sort geocoded addresses into optimal order
        """

        def closest_node(node, nodes):
            nodes = np.asarray(nodes)
            deltas = nodes - node
            dist_2 = np.einsum('ij,ij->i', deltas, deltas)
            return np.argmin(dist_2)

        sort_vector = [closest_node(x, self.destinations_latlongs) for x in ordered_latlongs]
        sorted_addresses = [self.destinations_addresses[x]['label'] for x in sort_vector]
        return sorted_addresses

    @param.depends('gmaps_urls')
    def show_urls(self):
        base_url_string = """
        ### The route links for navigation in Google Maps:
        
        URL
        """
        urls_links_md = [f'**[Group {i}]({u})**' for i, u in enumerate(self.gmaps_urls)]
        url_string = '/n/n'.join(urls_links_md)
        base_url_string = base_url_string.replace('URL', url_string)
        res_md = pn.pane.Markdown(base_url_string)
        print(res_md)
        return res_md

    def optimize_route(self, event):
        print(f'start_loc: {self.start_location}')
        start_latlong = _pull_lat_long_here(_geocode_destination_here(self.start_location))
        if self.is_start_equal_end:
            end_latlong = start_latlong
            self.end_latlong = start_latlong
            self.end_location = self.start_location
        else:
            end_latlong = _pull_lat_long_here(_geocode_destination_here(self.end_location))
        self.start_latlong = start_latlong
        self.end_latlong = end_latlong
        self.geocode_dest_list_latlong(event, destinations_list=self.destinations_wlist)
        self.find_best_route(event, latlong_list=self.destinations_latlongs, start_point=start_latlong,
                             end_point=end_latlong)

    def destinations_from_import_str(self, event):
        self.progress_bar.bar_color = 'info'
        self.progress_bar.active = True

        destinations_new = self.batch_import_str.value.split('\n')
        self.destinations_pane, self.destinations_wlist = create_destination_inputs(
            n=len(destinations_new), prev_destinations=None, init_vals=destinations_new
        )
        self.number_dest = len(destinations_new)
        self.progress_bar.bar_color = 'light'
        self.progress_bar.active = False

    @param.depends('is_start_equal_end')
    def start_end_widget(self):
        if self.is_start_equal_end:
            self.end_location = self.start_location
            self.end_latlong = self.start_latlong
            return pn.Column(self.param.start_location, self.param.is_start_equal_end)
        else:
            return pn.Column(self.param.start_location, self.param.is_start_equal_end, self.param.end_location)

    def panel(self):
        # Attach a callback to geocoding & optimal route search
        self.get_best_route_action.on_click(
            lambda x: self.optimize_route(x)
        )
        # Attach a callback to batch import:
        self.batch_import_str.link(self.batch_import_str, callbacks={'value': clean_space_callback})
        self.batch_import_str.value = ''
        # Attach a callback to Import Destinations button so the destinations pasted propagate into the Destinations list & sidebar
        self.get_batch_destinations.on_click(
            lambda x: self.destinations_from_import_str(x)
        )

        # Setup the sidebar:
        widgets_sliders = pn.Column(self.param.number_dest, self.param.waypoints_per_batch)
        widgets_start_end = self.start_end_widget
        buttons_ = pn.Column(self.get_best_route_action)
        progress_bar = pn.Pane(
            self.progress_bar, sizing_mode="stretch_width", width_policy="max"
        )

        # Set up tabs
        tab_bokeh = pn.Column(pn.Column(self.plot_bokeh), self.show_urls, sizing_mode="stretch_width",
                              width_policy="max")
        tab_import = pn.Row(self.batch_import_str, self.get_batch_destinations)
        self.tabs = pn.Tabs(('Optimal Route Map', tab_bokeh), ('Batch Location Import', tab_import))

        result = pn.Row(
            pn.Column(
                self.title,
                widgets_sliders,
                progress_bar,
                widgets_start_end,
                buttons_,
                self.change_destinations_number,

            ),
            self.tabs,
            sizing_mode="stretch_width",
        )
        return result


res = ReactiveDashboard(name="").panel()
res.servable()
