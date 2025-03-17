# src/app.py

from dash import Dash
import dash_bootstrap_components as dbc

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
app.title = "Air Quality Dashboard"
server = app.server  # Required for deployment on Render

# Import layout and callbacks AFTER initializing the app
from src.components import layout
import src.callbacks  # Ensure callbacks are loaded

# Set the layout
app.layout = layout

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
