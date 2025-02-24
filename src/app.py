from dash import Dash, html
import dash_bootstrap_components as dbc

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

# Layout
app.layout = html.Div([
    html.H1('AIR POLLUTANT AND AIR QUALITY IN INDIAN CITIES'),
    html.P('Dash converts Python classes into HTML'),
    html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
])

# Server side callbacks/reactivity
# ...

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)