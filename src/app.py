# src/app.py
from dash import Dash
import dash_bootstrap_components as dbc
import dash_vega_components as dvc

app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
app.title = "Air Quality Dashboard"
server = app.server

# Import the layout and callbacks after app is created
from src.components import layout
from src import callbacks  # references callbacks.py so those are registered

app.layout = layout

if __name__ == '__main__':
    app.run(debug=True)
