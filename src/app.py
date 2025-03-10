# src/app.py
from dash import Dash, html
import dash_bootstrap_components as dbc

# Import UI components
from .components import (
    title,
    sidebar,
    line_chart,
    corr_chart,
    stack_chart,
    card_aqi,
    card_perc,
    sidebar_background_color,
    title_background_color
)

# Import the callbacks (must be imported so that Dash recognizes them)
from . import callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
server = app.server

# Define the layout
app.layout = html.Div([
    dbc.Row(
        dbc.Col(title),
        style={
            'backgroundColor': title_background_color,
            'padding-top': '2vh',
            'padding-bottom': '2vh',
            'min-height': '10vh',
        }
    ),
    dbc.Row([
        sidebar,  # Left sidebar
        dbc.Col([
            dbc.Row([card_aqi, card_perc]),
            dbc.Row([line_chart]),
            dbc.Row([corr_chart])
        ]),
        dbc.Col(stack_chart)  # Right column for the stacked bar chart
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)

