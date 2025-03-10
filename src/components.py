# src/components.py
from datetime import date
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_vega_components as dvc

# Title and color settings
title = [html.H1('POLLUTANT AND AIR QUALITY IN INDIAN CITIES')]
title_background_color = '#f2bf30'
sidebar_background_color = '#b38d24'

# Empty chart containers (the actual chart specs will be set in callbacks.py)
line_chart = dvc.Vega(id='line', spec={})
corr_chart = dvc.Vega(id='correlation-graph', spec={})
stack_chart = dvc.Vega(id='stacked-graph', spec={})
map_plot = dvc.Vega(id='geo_map', spec={})

# Card containers
card_perc = dbc.Card(
    id='card-percentage',
    style={"width": "11rem"},
    className="border-0 bg-transparent text-center"
)
card_aqi = dbc.Card(
    id='card-aqi',
    style={"width": "11rem", "margin-right": "30px"},
    className="border-0 bg-transparent text-center"
)

# Sidebar layout
sidebar = dbc.Col(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H5('Date'),
                    html.Div(
                        dcc.DatePickerRange(
                            id='date_range',
                            start_date=date(2015, 1, 1),
                            end_date=date(2024, 12, 24),
                            min_date_allowed=date(2015, 1, 1),
                            max_date_allowed=date(2024, 12, 24),
                            start_date_placeholder_text='MM/DD/YYYY',
                            end_date_placeholder_text='MM/DD/YYYY',
                            initial_visible_month=date(2024, 12, 31)
                        ),
                        style={'margin-bottom': '20px'}
                    ),
                    html.H5('Pollutant'),
                    dcc.Dropdown(
                        id='col',
                        options=[
                            {'label': p, 'value': p}
                            for p in [
                                'AQI', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx',
                                'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene'
                            ]
                        ],
                        value='AQI',
                        placeholder='Select pollutant...'
                    ),
                    html.Br(),
                    html.H5('Cities'),
                    dcc.Dropdown(
                        id='city',
                        options=[
                            {'label': c, 'value': c}
                            for c in [
                                'Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'
                            ]
                        ],
                        value=['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'],
                        multi=True,
                        placeholder='Select cities...'
                    ),
                    html.Br(),
                    dbc.Col(map_plot)
                ],
            ),
        ),
        dbc.Row(
            [
                html.P([
                    """This dashboard provides user-friendly visualizations to help
                    environmental researchers track air quality trends, including
                    AQI and other pollution metrics, from 2015 to 2024. For more
                    information or to get involved, visit our """,
                    html.A("Github repository.",
                           href="https://github.com/UBC-MDS/DSCI-532_2025_23_AQI-Dashboard",
                           target="_blank")
                ]),
                html.P("""Created by Sarah Eshafi, Jay Mangat, Zheng He, and Ci Xu.
                          Last updated March 1, 2025""")
            ],
            style={'margin-top': 'auto'}  # Align to the bottom
        )
    ],
    md=10,
    style={
        'background-color': sidebar_background_color,
        'padding': 15,
        'padding-bottom': 0,
        'height': '90vh',
        'display': 'flex',
        'flex-direction': 'column',
    }
)
