## app.py

from dash import Dash
import dash_bootstrap_components as dbc

from .components import layout
from . import callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
server = app.server
app.layout = layout

if __name__ == '__main__':
    app.run(debug=True)
