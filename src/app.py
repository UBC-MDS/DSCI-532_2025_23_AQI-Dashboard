from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from datetime import date
import pandas as pd
import altair as alt
import geopandas as gpd

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
server = app.server

# Import data
df = pd.read_csv('data/raw/city_day.csv', parse_dates=["Datetime"])
df["Datetime"] = pd.to_datetime(df["Datetime"])

# Pollutants List
pollutants = ['AQI', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2',
              'O3', 'Benzene', 'Toluene', 'Xylene']

# Load India map
india_map = gpd.read_file("data/map/ne_110m_admin_0_countries.shp")
india_map = india_map[india_map['ADMIN'] == "India"]

# Manually defining city coordinates
city_coords = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946}
}
city_df = pd.DataFrame([{"City": k, "Latitude": v["lat"],
                       "Longitude": v["lon"]} for k, v in city_coords.items()])

# Chart Components
title = [html.H1('POLLUTANT AND AIR QUALITY IN INDIAN CITIES')]
global_widgets = [
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
    dcc.Dropdown(pollutants, 'AQI',
                 placeholder='Select pollutant...', id='col'),
    html.Br(),
    html.H5('Cities'),
    dcc.Dropdown(['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'],
                 ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'], multi=True,
                 placeholder='Select cities...', id='city')
]


line_chart = dvc.Vega(id='line', spec={})
corr_chart = dvc.Vega(id='correlation-graph', spec={})
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
                    dcc.Dropdown(),
                    html.Br(),
                    dcc.Dropdown(),
                    html.Br(),
                    dbc.Col(map_plot)
                ],
            ),
        ),
        dbc.Row([
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
            style = {
                'margin-top': 'auto'  # Align to bottom
                
            }
        )
    ],
    md=10,
    style={
        'background-color': '#e6e6e6',
        'padding': 15,  # Padding top,left,right,botoom
        'padding-bottom': 0,  # Remove bottom padding for footer
        'height': '90vh',  # vh = "viewport height" = 90% of the window height
        'display': 'flex',  # Allow children to be aligned to bottom
        'flex-direction': 'column',  # Allow for children to be aligned to bottom
    }
)

# Layout
app.layout = html.Div([
    dbc.Row(dbc.Col(title)),
    dbc.Row([
        dbc.Col(sidebar),
        dbc.Col(global_widgets, md=4),
        dbc.Col([
            dbc.Row([card_aqi,
                     card_perc]),
            dbc.Row([line_chart]),
        ])
    ]),
    dbc.Row([
        dbc.Col("", md=4),
        dbc.Col(corr_chart)
    ])
])


# Server side callbacks/reactivity
# Line Chart
@callback(
    Output('line', 'spec'),
    [Input('col', 'value'),
     Input('city', 'value'),
     Input('date_range', 'start_date'),
     Input('date_range', 'end_date')]
)
def create_line_chart(col, city, start_date, end_date):
    df_city_filter = df[df["City"].isin(city)]
    df_date_filtered = df_city_filter[
        (df_city_filter["Datetime"] >= start_date) & (
            df_city_filter["Datetime"] <= end_date)
    ]

    date_length = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
    if date_length < 31:
        freq = "D"
    elif date_length < 400:
        freq = "W"
    elif date_length < 1200:
        freq = "MS"
    else:
        freq = "QS"

    df_line_chart = df_date_filtered.groupby([pd.Grouper(key="Datetime",
                                                         freq=freq),
                                              "City"]).mean(numeric_only=True).reset_index()
    df_line_chart_mean = df_line_chart.groupby(
        pd.Grouper(key="Datetime", freq=freq)
    ).mean(numeric_only=True).reset_index()
    df_line_chart_mean['City'] = "Average"

    if col == "AQI":
        y_title = "AQI"
        chart_title = "AQI Over Time (Black = average)"
    else:
        y_title = col + " Concentration"
        chart_title = col + " Concentration Over Time"

    return (
        (
            alt.Chart(df_line_chart).mark_line().encode(
                x=alt.X("Datetime:T", title="Date"),
                y=alt.Y(col+":Q", title=y_title, scale=alt.Scale(zero=False)),
                color=alt.Color("City:N", title="Legend"),
                opacity=alt.value(0.5),
                tooltip=["Datetime:T", "AQI:Q", "City:N"]
            ) +
            alt.Chart(df_line_chart_mean).mark_line(color="black").encode(
                x=alt.X("Datetime:T", title="Date"),
                y=alt.Y(col+":Q", title=y_title, scale=alt.Scale(zero=False)),
                tooltip=["Datetime:T", "AQI:Q"]
            )
        ).properties(
            title=chart_title,
            height=170,
            width=300
        ).to_dict()
    )

# Correlation Plot


@app.callback(
    Output('correlation-graph', 'spec'),
    [Input('date_range', 'start_date'),
     Input('date_range', 'end_date'),
     Input('city', 'value')]
)
def update_correlation_plot(start_date, end_date, selected_cities):
    # Filter Data
    filtered_df = df[(df['Datetime'] >= start_date)
                     & (df['Datetime'] <= end_date)]

    # Filter Cities
    if isinstance(selected_cities, list):
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]

    # Keep Only Pollutant & AQI Columns
    filtered_df = filtered_df[pollutants].dropna()

    # Compute Correlation Matrix
    correlation_matrix = filtered_df.corr()

    # Extract AQI Correlation with Other Pollutants
    aqi_correlations = correlation_matrix['AQI'].drop('AQI').reset_index()
    aqi_correlations.columns = ['Pollutant', 'Correlation']

    chart = (
        alt.Chart(aqi_correlations)
        .mark_bar()
        .encode(
            # , axis=alt.Axis(labelFontSize=14, titleFontSize=16, titleFontWeight='bold')
            x=alt.X("Pollutant:N", title="Pollutant", sort="-y"),
            # , axis=alt.Axis(labelFontSize=14, titleFontSize=16, titleFontWeight='bold')
            y=alt.Y("Correlation:Q", title="Correlation with AQI"),
            tooltip=["Pollutant", "Correlation"]
        )
        .properties(
            # , fontSize=20, fontWeight='bold'
            title=alt.TitleParams("Correlation of Pollutants with AQI"),
            width=300,
            height=150
        )
        .configure_view(strokeWidth=0)
    )
    return chart.to_dict()

# Map of India


@callback(
    Output('geo_map', 'spec'),
    Input('city', 'value')
)
def update_geo_map(selected_cities):
    # Base map of India using the shapefile
    india_chart = alt.Chart(india_map).mark_geoshape(
        fill='lightgray', stroke='black'
    ).encode(
        tooltip=[alt.Tooltip('ADMIN:N', title='Region')]
    ).project('mercator').properties(
        width=260,
        height=210
    )

    # Filter city_df based on selected cities
    filtered_cities = city_df[city_df['City'].isin(selected_cities)]

    # Plot blue dots for cities using their coordinates
    city_points = alt.Chart(filtered_cities).mark_point(fill="blue", size=100).encode(
        longitude=alt.Longitude('Longitude:Q'),
        latitude=alt.Latitude('Latitude:Q'),
        tooltip=[alt.Tooltip('City:N', title='City')]
    ).project('mercator')

    final_chart = (india_chart + city_points).properties(
        title="Select Cities"
    ).configure(background='#AAAAAA') #change this to match sidebar's color

    return final_chart.to_dict()

# Data cards


@callback(
    [Output('card-percentage', 'children'),
     Output('card-aqi', 'children')],
    [Input('col', 'value'),
     Input('city', 'value'),
     Input('date_range', 'start_date'),
     Input('date_range', 'end_date')]
)
def update_cards(pollutant, selected_cities, start_date, end_date):
    # Ensure dates are converted properly
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if isinstance(selected_cities, str):
        selected_cities = [selected_cities]

    city_filtered_df = df[df['City'].isin(selected_cities)]
    date_filtered_df = city_filtered_df[
        (city_filtered_df['Datetime'] >= start_date) & (
            city_filtered_df['Datetime'] <= end_date)
    ]
    start_pollution = city_filtered_df[
        city_filtered_df['Datetime'] == start_date
    ][pollutant].mean()
    end_pollution = city_filtered_df[
        city_filtered_df['Datetime'] == end_date
    ][pollutant].mean()
    perc_change = (end_pollution-start_pollution) / start_pollution
    most_freq = date_filtered_df["AQI_Bucket"].mode()[0]

    card_percentage = [
        dbc.CardHeader(f'% Change in {pollutant}'),
        dbc.CardBody(f'{perc_change * 100:.1f}%')
    ]
    card_aqi = [
        dbc.CardHeader("Most Frequent AQI Bucket"),
        dbc.CardBody(most_freq)
    ]
    return card_percentage, card_aqi


# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)
