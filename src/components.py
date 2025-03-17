# components.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from datetime import date

# Chart Components
title = [html.H1('POLLUTANT AND AIR QUALITY IN INDIAN CITIES')]
title_background_color = '#003780'
sidebar_background_color = '#96bcff'

line_chart = dvc.Vega(id='line', spec={})
corr_chart = dvc.Vega(id='correlation-graph', spec={})
stack_chart = dvc.Vega(id='stacked-graph', spec={})
map_plot = dvc.Vega(id='geo_map', spec={}, signalsToObserve=["select_region"])
card_perc = dbc.Card(id='card-percentage',
                     style={"width": "12rem",
                            "background": sidebar_background_color,
                            "height": '15vh',
                            "color": "black"
                            },
                     className="border-0 text-center"
                     )
card_aqi = dbc.Card(id='card-aqi',
                    style={"width": "12rem",
                           "background-color": sidebar_background_color,
                           "height": '15vh',
                           "margin-right": "70px",
                           "color": "black"
                           },
                    className="border-0 text-center"
                    )
city_dropdown = dcc.Dropdown(
    ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'],
    ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'],
    multi=True,
    placeholder='Select cities...',
    id='city',
    clearable=False
    )

sidebar = dbc.Col(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H5('Date',
                            style={
                                "color": "black"
                            }
                            ),
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
                    html.H5('Pollutant',
                            style={
                                "color": "black"
                            }),
                    dcc.Dropdown(
                        ['AQI', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3',
                         'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene'],
                        'AQI',
                        placeholder='Select pollutant...',
                        id='col',
                        clearable=False
                    ),
                    html.Br(),
                    html.H5('Select Cities (hold shift + click)',
                            style={
                                "color": "black",
                                'padding-bottom': 0,
                                'margin-bottom': 0
                            }),
                    dcc.Dropdown(
                        ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'],
                        ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'],
                        multi=True,
                        placeholder='Select cities...',
                        id='city',
                        clearable=False,
                        style={'display': 'none'}
                    ),
                    dcc.Dropdown(
                        ['Delhi'],
                        ['Delhi'],
                        id='placeholder',
                        style={'display': 'none'}
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
                   Last updated March 17, 2025
                   """)
        ],
            style={
                'margin-top': 'auto',
                'padding-bottom': 10
        }
        )
    ],
    md=10,
    style={
        'background-color': sidebar_background_color,
        'padding': 15,
        'padding-bottom': 0,
        'minheight': '90vh',
        'flex-direction': 'column',
    }
)

# Layout
layout = html.Div([
    dcc.Store(id='selected-cities', data=[]),
    dbc.Row(
        dbc.Col(
            title
        ),
        style={
            'color': 'white',
            'backgroundColor': title_background_color,
            'padding-top': '2vh',
            'padding-bottom': '2vh',
            'padding-left': '3vh',
            'min-height': '10vh',
        }
    ),
    dbc.Row([
        dbc.Col(sidebar, md=4),
        dbc.Col([
            html.Div([
                dbc.Card(line_chart, style={"box-shadow": "none",
                                            "border": "none",
                                            "padding-top": "2vh"}),
                dbc.Card(corr_chart, style={"box-shadow": "none",
                                            "border": "none",
                                            "padding-top": "2vh"})
            ])
        ]),
        dbc.Col([
            dbc.Row(
                [card_aqi,
                 card_perc],
                style={
                    'padding-top': '2vh'
                }
            ),
            dbc.Row((stack_chart))
        ])
    ])
])
