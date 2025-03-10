## components.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from datetime import date

# Chart Components
title = [html.H1('POLLUTANT AND AIR QUALITY IN INDIAN CITIES')]
title_background_color = '#4868ff'
sidebar_background_color = '#d5d5d5'

line_chart = dvc.Vega(id='line', spec={})
corr_chart = dvc.Vega(id='correlation-graph', spec={})
stack_chart = dvc.Vega(id='stacked-graph', spec={})
map_plot = dvc.Vega(id='geo_map', spec={})
card_perc = dbc.Card(id='card-percentage',
                     style={"width": "11rem"}, className="border-0 bg-transparent text-center")
card_aqi = dbc.Card(id='card-aqi', style={"width": "11rem",
                    "margin-right": "30px"}, className="border-0 bg-transparent text-center")

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
                        ['AQI', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3',
                         'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene'],
                        'AQI',
                        placeholder='Select pollutant...',
                        id='col'
                    ),
                    html.Br(),
                    html.H5('Cities'),
                    dcc.Dropdown(
                        ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'],
                        ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'],
                        multi=True,
                        placeholder='Select cities...',
                        id='city'
                    ),
                    html.Br(),
                    dbc.Col(map_plot)
                ],
            ),
        ),
        dbc.Row([
            html.P([
                """This dashboard helps environmental researchers track air
                quality trends in India from 2015 to 2024. For more
                information or to get involved, visit our """,
                html.A("Github repository.",
                       href="https://github.com/UBC-MDS/DSCI-532_2025_23_AQI-Dashboard",
                       target="_blank")
            ]),
            html.P("""Created by Sarah Eshafi, Jay Mangat, Zheng He, and Ci Xu.
                   Last updated March 1, 2025""")
        ],
            style={
                'margin-top': 'auto'
            }
        )
    ],
    md=10,
    style={
        'background-color': '#d5d5d5',
        'padding': 15,
        'padding-bottom': 0,
        'height': '90vh',
        'display': 'flex',
        'flex-direction': 'column',
    }
)

# Layout
layout = html.Div([
    dbc.Row(
        dbc.Col(
            title
        ),
        style={
            'backgroundColor': title_background_color,
            'padding-top': '2vh',
            'padding-bottom': '2vh',
            'min-height': '10vh',
        }
    ),
    dbc.Row([
        dbc.Col(sidebar),
        dbc.Col([
            dbc.Row([line_chart],
                    style={
                        'padding-top': '2vh',
                        'padding-bottom': '2vh',
                        'min-height': '39vh'}
                    ),
            dbc.Row(corr_chart)
        ]),
        dbc.Col([
            dbc.Row([card_aqi,
                     card_perc],
                     style={
                        'padding-top': '8vh',
                        'padding-bottom': '4vh',
                        'min-height': '39vh'
                    }),
            dbc.Row(stack_chart)
        ])
    ])
])
