import altair as alt
import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import factor_cmap, dodge, jitter
import itertools
import numpy as np
from bokeh.models import WMTSTileSource, ResetTool, WheelZoomTool, PanTool, HoverTool, ColumnDataSource

from panel_app.constants import waypoint_url, OSM_tile_source, WIDTH_DEFAULT, HEIGHT_DEFAULT
from pyproj import Proj, transform


def reproject_coordinates(input_projection, output_projection, input_x, input_y, suffix=' Transformed'):
    """Reproject coordinate series
    Arguments:
        input_projection {string} -- Input Coordinate System descriptor (e.g. 'epsg:4267' for NAD27)
        output_projection {string} -- Output Coordinate System descriptor (e.g. 'epsg:26910' for NAD83)
        input_x {pandas.Series or list-like} -- Array of x values in input CRS
        input_y {pandas.Series or list-like} -- Array of y values in input CRS
    Keyword Arguments:
        suffix {str} -- Appended to original name of input x and y columns (default: {' Transformed'})
    Returns:
        pandas.DataFrame -- Dataframe with two columns: output_x and output_y
    """
    print(f'Converting from {input_projection} to {output_projection}')
    # The 'init=' generates a warning, but transform fails if it is not used!
    output_x, output_y = transform(Proj(init=input_projection, preserve_units=False),
                                   Proj(init=output_projection, preserve_units=False), input_x.to_list(),
                                   input_y.to_list())
    return pd.DataFrame(data={f'{input_x.name}{suffix}': output_x, f'{input_y.name}{suffix}': output_y})


def create_label_df(start_point, end_point, latlongs_original_optimal, sorted_addresses,
                    start_location, end_location):
    df_label_original = pd.DataFrame({'latitude': [x[0] for x in latlongs_original_optimal],
                                      'longitude': [x[1] for x in latlongs_original_optimal],
                                      'label': sorted_addresses})
    df_start_end = pd.DataFrame({'latitude': [start_point[0], end_point[0]],
                                 'longitude': [start_point[1], end_point[1]],
                                 'label': [start_location, end_location]})
    df_label = pd.concat([df_label_original, df_start_end])

    new_coords_labels = reproject_coordinates('epsg:4326', 'epsg:3857', df_label['longitude'], df_label['latitude'],
                                              suffix='_new')
    df_label['Longitude'] = new_coords_labels['longitude_new'].values
    df_label['Latitude'] = new_coords_labels['latitude_new'].values

    return df_label


def create_legs_df(response_json):
    list_df_pts = []
    leg_list = response_json['routes'][0]['legs']
    for i in range(len(leg_list)):
        df = pd.DataFrame(leg_list[i]['points'])
        df['leg'] = i
        df['pt_num'] = np.arange(df.shape[0])
        list_df_pts.append(df)
    df_all_pts = pd.concat(list_df_pts)
    new_coords = reproject_coordinates('epsg:4326', 'epsg:3857', df_all_pts['longitude'], df_all_pts['latitude'],
                                       suffix='_new')

    df_all_pts['Longitude'] = new_coords['longitude_new'].values
    df_all_pts['Latitude'] = new_coords['latitude_new'].values

    return df_all_pts


def create_bokeh_figure(df_all_pts, df_label):
    df_label['url'] = waypoint_url
    w_image = 25
    h_image = 600 / 390 * w_image

    df_all_pts['leg'] = df_all_pts['leg'].astype(str)
    df_source_labels = ColumnDataSource(df_label)
    unique_legs = df_all_pts['leg'].astype(str).unique().tolist()

    # range bounds supplied in web mercator coordinates
    xrange = (df_all_pts['Longitude'].round(decimals=2).min(),
              df_all_pts['Longitude'].round(decimals=2).max())
    yrange = (df_all_pts['Latitude'].round(decimals=2).min(),
              df_all_pts['Latitude'].round(decimals=2).max())
    tooltips = [
        ("Address", "@label"),
    ]
    tools = [ResetTool(), PanTool(), WheelZoomTool()]
    p = figure(x_range=xrange,
               y_range=yrange,
               # tooltips=tooltips,
               x_axis_type="mercator", y_axis_type="mercator",
               plot_width=1000, plot_height=800,
               tools=tools
               )
    p.add_tile(OSM_tile_source)
    # p.add_tile(OSM_tile_source)

    # Add lines:
    for leg in unique_legs:
        df_sub_source = ColumnDataSource(df_all_pts[df_all_pts['leg'] == leg])
        p.line(x='Longitude', y='Latitude',
               color='cornflowerblue',
               source=df_sub_source,
               line_width=3)
        p.line(x='Longitude', y='Latitude',
               color='cornflowerblue',
               source=df_sub_source,
               line_width=15, alpha=0.3)

    circle_renderer = p.circle(x='Longitude', y='Latitude',
                               fill_color='white',
                               fill_alpha=0.05,
                               line_color='midnightblue',
                               line_alpha=0.01,
                               source=df_source_labels,
                               size=100,
                               # hover_line_color='black',
                               line_width=0)
    tool_circle_hover = HoverTool(renderers=[circle_renderer],
                                  tooltips=tooltips)
    p.image_url(url='url', anchor='bottom_center', x='Longitude', y='Latitude', w=w_image, h=h_image,
                source=df_source_labels, w_units='screen', h_units='screen')
    p.text(x='Longitude', y=jitter('Latitude', mean=500, width=1000), text='label', source=df_source_labels,
           text_color='midnightblue')
    p.add_tools(tool_circle_hover)

    p.xaxis.axis_label = 'Longitude'
    p.yaxis.axis_label = 'Latitude'
    p.xaxis.visible = False
    p.yaxis.visible = False

    return p


def default_altair(lines=False):
    data = pd.DataFrame({"x": np.random.randn(100), "y": np.random.randn(100)})
    if lines:
        ch = (
            alt.Chart(data=data, width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT)
                .encode(x="x", y="y")
                .mark_line()
        )
    else:
        ch = (
            alt.Chart(data=data, width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT)
                .encode(x="x", y="y")
                .mark_point()
        )

    return ch


def construct_address(address):
    return f'{address.get("houseNumber", "")} {address.get("street")} {address["city"]}'.lower().strip()