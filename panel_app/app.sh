#!/bin/sh

export BOKEH_ALLOW_WS_ORIGIN="*"
panel serve /usr/src/app/app.py 
