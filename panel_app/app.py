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


class ReactiveForecastDashboard(param.Parameterized):
    title = pn.pane.Markdown('# Booze Cruise YYC')
    # Add a widget that picks the environment and bucket
    number_dest = param.Integer(5,label='Select number of destinations', bounds=(0, 15))
    progress_bar = pnw.misc.Progress(active=False, bar_color='light', value=None, width_policy='max',
                                     sizing_mode='stretch_width')
    date_custom_map = {}
    get_locations_action = pnw.Button(name="Get Locations", button_type='primary')
    get_best_route_action = pnw.Button(name="Get Best Route", button_type='default')

    all_dates_forecast = default_altair()
    default_plot = pn.Pane(default_altair())

    # Create a reusable Paginator
    #@param.depends('bucket_string', 'env_string')
    def get_listing_s3(self):
        pass

    def panel(self):
        self.get_locations_action.on_click(lambda x: print(x))
        self.get_best_route_action.on_click(lambda x: print(x))

        widgets_ = self.param
        buttons_ = pn.Column(self.get_locations_action, self.get_best_route_action)
        progress_bar = pn.Pane(self.progress_bar, sizing_mode='stretch_width', width_policy='max')
        result = pn.Row(pn.Column(self.title, widgets_,buttons_,
                                  progress_bar),
                        pn.Column(self.default_plot,
                                  sizing_mode='stretch_width', width_policy='max'),
                        sizing_mode='stretch_width')
        return result


res = ReactiveForecastDashboard(name='').panel()
res.servable()
