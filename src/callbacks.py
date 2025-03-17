# src/callbacks.py

import pandas as pd
import altair as alt
from dash import callback, Output, Input
import dash_bootstrap_components as dbc
from functools import lru_cache

# Import data and style references
from .data import df, pollutants, india_map, city_df
from .components import sidebar_background_color


@lru_cache(maxsize=32)
def get_filtered_data(cities_tuple, start_date_str, end_date_str):
    """Caches filtered data to improve performance."""
    start_date = pd.to_datetime(start_date_str)
    end_date = pd.to_datetime(end_date_str)
    
    mask = (
        df["City"].isin(cities_tuple) &
        (df["Datetime"] >= start_date) &
        (df["Datetime"] <= end_date)
    )
    return df.loc[mask].copy()

# =============== Line Chart ===============
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
                    legendX=80, legendY=10,
                    direction='horizontal',
                    titleAnchor='middle')),
                opacity=alt.value(0.8),
                tooltip=["Datetime:T", f"{col_escaped}:Q", "City:N"]
            )
            +
            alt.Chart(df_line_chart_mean).mark_line(color="black").encode(
                x=alt.X("Datetime:T", title="Date"),
                y=y_column,
                color=alt.Color("City:N", 
                                scale=alt.Scale(domain=["Average"],
                                                range=['black']),
                                legend=alt.Legend(
                                    title='',
                                    orient='none',
                                    legendX=20, legendY=10,
                                    direction='horizontal',
                                    titleAnchor='middle')
                                ),
                tooltip=["Datetime:T", f"{col_escaped}:Q"]
            )
        ).resolve_scale(
            color='independent'
        ).properties(
            title=f"{col} Over Time",
            height=270,
            width=515
        ).to_dict()
    )

# =============== Correlation Plot ===============
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

    if filtered_df.empty:
        chart = alt.Chart().mark_bar()
    else:
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
                height=270
            )
            .configure_view(strokeWidth=0)
        )
    return chart.to_dict()

# =============== India map ======================

@callback(
    Output('geo_map', 'spec'),
    Input('placeholder', 'value')
    # Input('city', 'value')
)
def update_geo_map(selected_cities):
    select = alt.selection_point(fields=["City"], name="select_region")
    india_chart = alt.Chart(india_map).mark_geoshape(
        fill='lightgray', stroke='black'
    ).encode().project('mercator').properties(
        width=400,
        height=310
    )

    city_points = alt.Chart(city_df).mark_point(fill="blue", size=100).encode(
        longitude=alt.Longitude('Longitude:Q'),
        latitude=alt.Latitude('Latitude:Q'),
        tooltip=[alt.Tooltip('City:N', title='City')]
    ).project('mercator').add_params(select)

    city_with_selection = city_points.encode(
        opacity=alt.condition(select, alt.value(0.8), alt.value(0.2))
    )

    # Create a text layer for city labels
    city_df_2 = city_df.copy()
    city_df_2.loc[4, 'Longitude'] = 70
    city_labels = alt.Chart(city_df_2).mark_text(
        align='left', dx=7, dy=7, fontSize=14, color='black'
    ).encode(
        longitude=alt.Longitude('Longitude:Q'),
        latitude=alt.Latitude('Latitude:Q'),
        text=alt.Text('City:N')
    ).project('mercator')

    final_chart = (india_chart + city_with_selection + city_labels).properties(
    ).configure(background=sidebar_background_color)
    return final_chart.interactive().to_dict()

# =============== Stacked Bar Plot ===============
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
            y=alt.Y('count:Q', title="Count"),
            color=alt.Color("AQI_Bucket:N", legend=alt.Legend(
                title='',
                orient='top',
                legendX=20, legendY=10,
                direction='horizontal',
                titleAnchor='middle')),
            tooltip=['AQI_Bucket', 'count:Q']
        )
        .properties(
            title=alt.TitleParams("AQI Bucket Frequency"),
            width=380,
            height=500
        )
        .configure_view(strokeWidth=0)
    )
    return chart.to_dict()

# =============== Cards for Percentage Change & AQI Bucket ===============
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

    if city_filtered_df.empty:
        card_percentage = [
            dbc.CardHeader(""),
            dbc.CardBody("No Data Available")
        ]
        card_aqi = [
            dbc.CardHeader(""),
            dbc.CardBody("No Data Available")
        ]
    else:
        start_pollution = city_filtered_df[city_filtered_df['Datetime']
                                        == start_date][pollutant].mean()
        end_pollution = city_filtered_df[city_filtered_df['Datetime']
                                        == end_date][pollutant].mean()
        perc_change = (end_pollution - start_pollution) / start_pollution
        perc_change = round(perc_change * 100, 1)
        most_freq = date_filtered_df["AQI_Bucket"].mode()[0]

        card_percentage = [
            dbc.CardHeader(f'Percent Change in {pollutant}'),
            dbc.CardBody(perc_change)
        ]
        card_aqi = [
            dbc.CardHeader("Most Frequent AQI Bucket"),
            dbc.CardBody(most_freq)
        ]
    return card_percentage, card_aqi

# =============== City Filter Update Based on Map Click ===============
@callback(
    Output('city', 'value'),
    Input('geo_map', 'signalData')
)
def update_city_filter(clicked_region):
    bool_check = clicked_region
    if bool_check:
        if clicked_region.get("select_region"):
            value = clicked_region['select_region']['City']
        else:
            value = city_df['City']
    else:
        value = city_df['City']
    return value
