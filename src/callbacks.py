# callbacks.py

import pandas as pd
import altair as alt
from dash import callback, Output, Input
import dash_bootstrap_components as dbc

# Import data and style references
from .data import df, pollutants, india_map, city_df
from .components import sidebar_background_color

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

    df_line_chart = df_date_filtered.groupby([pd.Grouper(key="Datetime", freq=freq),
                                              "City"]).mean(numeric_only=True).reset_index()
    df_line_chart_mean = df_line_chart.groupby(
        pd.Grouper(key="Datetime", freq=freq)
    ).mean(numeric_only=True).reset_index()
    df_line_chart_mean['City'] = "Average"

    col_escaped = col.replace(".", "_")
    df_line_chart = df_line_chart.rename(columns={col: col_escaped})
    df_line_chart_mean = df_line_chart_mean.rename(columns={col: col_escaped})

    if col_escaped == "AQI":
        y_column = alt.Y(f"{col_escaped}:Q", title=f"{col}",
                         scale=alt.Scale(zero=False))
    else:
        y_column = alt.Y(f"{col_escaped}:Q", title=f"{col} Concentration",
                         scale=alt.Scale(zero=False))

    return (
        (
            alt.Chart(df_line_chart).mark_line().encode(
                x=alt.X("Datetime:T", title="Date"),
                y=y_column,
                color=alt.Color("City:N", legend=alt.Legend(
                    title='',
                    orient='none',
                    legendX=20, legendY=10,
                    direction='horizontal',
                    titleAnchor='middle')),
                opacity=alt.value(0.8),
                tooltip=["Datetime:T", f"{col_escaped}:Q", "City:N"]
            )
            +
            alt.Chart(df_line_chart_mean).mark_line(color="black").encode(
                x=alt.X("Datetime:T", title="Date"),
                y=y_column,
                tooltip=["Datetime:T", f"{col_escaped}:Q"]
            )
        ).properties(
            title=f"{col} Over Time (Black = average)",
            height=280,
            width=515
        ).to_dict()
    )

# Correlation Plot


@callback(
    Output('correlation-graph', 'spec'),
    [Input('date_range', 'start_date'),
     Input('date_range', 'end_date'),
     Input('city', 'value')]
)
def update_correlation_plot(start_date, end_date, selected_cities):
    filtered_df = df[(df['Datetime'] >= start_date)
                     & (df['Datetime'] <= end_date)]
    if isinstance(selected_cities, list):
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]
    filtered_df = filtered_df[pollutants].dropna()

    correlation_matrix = filtered_df.corr()
    aqi_correlations = correlation_matrix['AQI'].drop('AQI').reset_index()
    aqi_correlations.columns = ['Pollutant', 'Correlation']

    chart = (
        alt.Chart(aqi_correlations)
        .mark_bar()
        .encode(
            x=alt.X("Pollutant:N", title="Pollutant", sort="-y"),
            y=alt.Y("Correlation:Q", title="Correlation with AQI"),
            tooltip=["Pollutant", "Correlation"]
        )
        .properties(
            title=alt.TitleParams("Correlation of Pollutants with AQI"),
            width=500,
            height=280
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
    india_chart = alt.Chart(india_map).mark_geoshape(
        fill='lightgray', stroke='black'
    ).encode(
        tooltip=[alt.Tooltip('ADMIN:N', title='Region')]
    ).project('mercator').properties(
        width=260,
        height=210
    )

    filtered_cities = city_df[city_df['City'].isin(selected_cities)]
    city_points = alt.Chart(filtered_cities).mark_point(fill="blue", size=100).encode(
        longitude=alt.Longitude('Longitude:Q'),
        latitude=alt.Latitude('Latitude:Q'),
        tooltip=[alt.Tooltip('City:N', title='City')]
    ).project('mercator')

    final_chart = (india_chart + city_points).properties(
        title="Select Cities"
    ).configure(background=sidebar_background_color)

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
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if isinstance(selected_cities, str):
        selected_cities = [selected_cities]

    city_filtered_df = df[df['City'].isin(selected_cities)]
    date_filtered_df = city_filtered_df[
        (city_filtered_df['Datetime'] >= start_date) & (
            city_filtered_df['Datetime'] <= end_date)
    ]
    start_pollution = city_filtered_df[city_filtered_df['Datetime']
                                       == start_date][pollutant].mean()
    end_pollution = city_filtered_df[city_filtered_df['Datetime']
                                     == end_date][pollutant].mean()
    perc_change = (end_pollution - start_pollution) / start_pollution
    most_freq = date_filtered_df["AQI_Bucket"].mode()[0]

    card_percentage = [
        dbc.CardHeader(f'Percent Change in {pollutant}'),
        dbc.CardBody(f'{perc_change * 100:.1f}%')
    ]
    card_aqi = [
        dbc.CardHeader("Most Frequent AQI Bucket"),
        dbc.CardBody(most_freq)
    ]
    return card_percentage, card_aqi

# Stacked bar Plot


@callback(
    Output('stacked-graph', 'spec'),
    [Input('date_range', 'start_date'),
     Input('date_range', 'end_date'),
     Input('city', 'value')]
)
def update_stacked_plot(start_date, end_date, selected_cities):
    filtered_df = df[(df['Datetime'] >= start_date)
                     & (df['Datetime'] <= end_date)]
    if isinstance(selected_cities, list):
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]

    filtered_df = filtered_df.groupby(
        ["City", "AQI_Bucket"]).size().reset_index(name="count")

    chart = (
        alt.Chart(filtered_df)
        .mark_bar()
        .encode(
            x='City',
            y='count:Q',
            color=alt.Color("AQI_Bucket:N", legend=alt.Legend(
                title='',
                orient='none',
                legendX=20, legendY=10,
                direction='horizontal',
                titleAnchor='middle')),
            tooltip=['AQI_Bucket', 'count:Q']
        )
        .properties(
            title=alt.TitleParams("AQI bucket frequency"),
            width=390,
            height=525
        )
        .configure_view(strokeWidth=0)
    )
    return chart.to_dict()
