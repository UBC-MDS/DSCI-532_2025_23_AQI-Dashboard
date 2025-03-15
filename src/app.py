# app.py
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from datetime import date
import pandas as pd
import altair as alt
import geopandas as gpd

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
server = app.server

# Import layout and callbacks after creating app
from .components import layout
from . import callbacks

clickData = {'datum': {'City': 'Mumbai'}}

# Set the layout (replaces original app.layout = ...)
app.layout = layout

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)
