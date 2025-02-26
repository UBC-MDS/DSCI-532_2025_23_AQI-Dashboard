from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from datetime import date

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
server = app.server

# Layout
app.layout = html.Div([
    html.H1('AIR POLLUTANT AND AIR QUALITY IN INDIAN CITIES'),
    html.P('Dash converts Python classes into HTML'),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=date(2015, 1, 1),
        end_date=date(2024, 12, 24),
        min_date_allowed=date(2015, 1, 1),
        max_date_allowed=date(2024, 12, 24),
        start_date_placeholder_text='Select a date',
        end_date_placeholder_text='Select a date'
    ),
    html.Br(),
    dcc.Dropdown(['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene', 'AQI'], 
        'AQI', placeholder='Select pollutant...', id='pollutant-dropdown'),
    html.Br(),
    dcc.Dropdown(['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'], 
        ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'], multi=True,
        placeholder='Select cities...', id='city-dropdown')
])

# Server side callbacks/reactivity
# ...

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)