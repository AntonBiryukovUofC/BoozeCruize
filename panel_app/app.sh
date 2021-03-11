#!/bin/sh

export PYTHONPATH=$PYTHONPATH:/usr/src/app/
export BOKEH_ALLOW_WS_ORIGIN="*"
panel serve /usr/src/app/panel_app/app.py
