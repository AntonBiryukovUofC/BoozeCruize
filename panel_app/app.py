import pandas as pd
import numpy as np
import panel as pn
import panel.widgets as pnw
import param
import altair as alt

alt.data_transformers.disable_max_rows()
pn.extension('vega')
DEV_BUCKET = 'abiryukov'
FRAC = 0.5
WIDTH_DEFAULT = 1000
HEIGHT_DEFAULT = 150
N_RANDOM_DAYS = 7


def default_altair(lines=False):
    data = pd.DataFrame({'x': np.random.randn(100),
                         'y': np.random.randn(100)})
    if lines:
        ch = alt.Chart(data=data, width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT).encode(x='x', y='y').mark_line()
    else:
        ch = alt.Chart(data=data, width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT).encode(x='x', y='y').mark_point()

    return ch


def create_destination_inputs(n=2, prev_destinations=None):
    if prev_destinations is None:
        wlist = []
        for i in range(n):
            name_widget = f'Destination {i + 1}'
            widget = pn.widgets.TextInput(name=name_widget, value='')
            wlist.append(widget)

    else:
        wlist = prev_destinations
        n_old = len(prev_destinations)
        if n > n_old:
            for i in range(n_old + 1, n):
                name_widget = f'Destination {i + 1}'
                widget = pn.widgets.TextInput(name=name_widget, value='')
                wlist.append(widget)
        else:
            print(f'Nold: {n_old} , new: {n}')
            wlist = wlist[0:n]

    widget_all = pn.Column(*wlist)
    return widget_all, wlist

def geocode_destinations(x):
    print(x)
    pass

def find_best_route(x):
    print(x)
    pass


class ReactiveForecastDashboard(param.Parameterized):
    title = pn.pane.Markdown('# Booze Cruise YYC')
    # Add a widget that picks the environment and bucket
    number_dest = param.Integer(5, label='Select number of destinations', bounds=(0, 15))
    progress_bar = pnw.misc.Progress(active=False, bar_color='light', value=None, width_policy='max',
                                     sizing_mode='stretch_width')

    date_custom_map = {}
    get_locations_action = pnw.Button(name="Get Locations", button_type='primary')
    get_best_route_action = pnw.Button(name="Get Best Route", button_type='default')
    destinations_pane, destinations_wlist = create_destination_inputs(n=5, prev_destinations=None)

    all_dates_forecast = default_altair()
    default_plot = pn.Pane(default_altair())

    # Create a reusable Paginator
    # @param.depends('bucket_string', 'env_string')
    def get_listing_s3(self):
        pass

    @param.depends('number_dest', watch=True)
    def change_destinations_number(self):
        print(self.number_dest)
        new_destinations = create_destination_inputs(n=self.number_dest,
                                                     prev_destinations=self.destinations_wlist)
        self.destinations_pane, self.destinations_wlist = new_destinations[0], new_destinations[1]
        print(self.destinations_wlist)
        return self.destinations_pane

    def panel(self):
        self.get_locations_action.on_click(lambda x: geocode_destinations(x))
        self.get_best_route_action.on_click(lambda x: find_best_route(x))

        widgets_ = self.param
        buttons_ = pn.Column(self.get_locations_action, self.get_best_route_action)
        progress_bar = pn.Pane(self.progress_bar, sizing_mode='stretch_width', width_policy='max')
        result = pn.Row(pn.Column(self.title, widgets_, buttons_, self.change_destinations_number,
                                  progress_bar),
                        pn.Column(self.default_plot,
                                  sizing_mode='stretch_width', width_policy='max'),
                        sizing_mode='stretch_width')
        return result


res = ReactiveForecastDashboard(name='').panel()
res.servable()
