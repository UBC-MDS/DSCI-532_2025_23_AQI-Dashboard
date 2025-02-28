from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from datetime import date
import pandas as pd
import altair as alt

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
server = app.server

# Import data
df = pd.read_csv('data/raw/city_day.csv', parse_dates=["Datetime"])
df["Datetime"] = pd.to_datetime(df["Datetime"])

# Layout
app.layout = html.Div([
    html.H1('AIR POLLUTANT AND AIR QUALITY IN INDIAN CITIES'),
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
    html.Br(),
    dcc.Dropdown(['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3',
                  'Benzene', 'Toluene', 'Xylene', 'AQI'], 'AQI',
                  placeholder='Select pollutant...', id='col'),
    html.Br(),
    dcc.Dropdown(['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'], 
        ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore'], multi=True,
        placeholder='Select cities...', id='city'),
    dvc.Vega(id='line', spec={}),
])


# Server side callbacks/reactivity
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
        (df_city_filter["Datetime"] >= start_date) & (df_city_filter["Datetime"] <= end_date)
        ]

    date_length = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
    if date_length < 14:
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
        chart_title = "AQI Concentration Over Time"
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
        ).properties(title=chart_title).to_dict()
    )


# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)