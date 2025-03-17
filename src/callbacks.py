# src/callbacks.py

import pandas as pd
import altair as alt
from dash import callback, Output, Input
import dash_bootstrap_components as dbc
from functools import lru_cache

# Import data and style references
from .data import df, pollutants, india_map, city_df
from .components import sidebar_background_color

# ✅ 缓存数据筛选，提高速度
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
    if isinstance(city, str):
        city = [city]

    df_filtered = get_filtered_data(tuple(city), str(start_date), str(end_date))

    if df_filtered.empty:
        return alt.Chart().mark_line().to_dict()

    date_length = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
    freq = "D" if date_length < 31 else "W" if date_length < 400 else "MS" if date_length < 1200 else "QS"

    grouped = df_filtered.groupby([pd.Grouper(key="Datetime", freq=freq), "City"]).mean().reset_index()
    overall_mean = grouped.groupby(pd.Grouper(key="Datetime", freq=freq)).mean().reset_index()
    overall_mean['City'] = "Average"

    col_escaped = col.replace(".", "_")
    grouped.rename(columns={col: col_escaped}, inplace=True)
    overall_mean.rename(columns={col: col_escaped}, inplace=True)

    chart = (
        alt.Chart(grouped).mark_line().encode(
            x="Datetime:T",
            y=alt.Y(f"{col_escaped}:Q", scale=alt.Scale(zero=False)),
            color="City:N",
            tooltip=["Datetime:T", f"{col_escaped}:Q", "City:N"]
        ) +
        alt.Chart(overall_mean).mark_line(color="black").encode(
            x="Datetime:T",
            y=f"{col_escaped}:Q",
            color=alt.Color("City:N", scale=alt.Scale(domain=["Average"], range=["black"]))
        )
    ).to_dict()

    return chart

# =============== Correlation Plot ===============
@callback(
    Output('correlation-graph', 'spec'),
    [Input('date_range', 'start_date'),
     Input('date_range', 'end_date'),
     Input('city', 'value')]
)
def update_correlation_plot(start_date, end_date, selected_cities):
    df_filtered = get_filtered_data(tuple(selected_cities), str(start_date), str(end_date))
    if df_filtered.empty:
        return alt.Chart().mark_bar().to_dict()

    filtered_df = df_filtered[pollutants].dropna()
    if filtered_df.empty:
        return alt.Chart().mark_bar().to_dict()

    corr_matrix = filtered_df.corr()
    aqi_corr = corr_matrix["AQI"].drop("AQI").reset_index()
    aqi_corr.columns = ["Pollutant", "Correlation"]

    chart = (
        alt.Chart(aqi_corr)
        .mark_bar()
        .encode(
            x=alt.X("Pollutant:N", sort="-y"),
            y=alt.Y("Correlation:Q", title="Correlation with AQI"),
            tooltip=["Pollutant", "Correlation"]
        )
        .properties(width=500, height=270)
        .configure_view(strokeWidth=0)
    )
    return chart.to_dict()

# =============== Stacked Bar Plot ===============
@callback(
    Output('stacked-graph', 'spec'),
    [Input('date_range', 'start_date'),
     Input('date_range', 'end_date'),
     Input('city', 'value')]
)
def update_stacked_plot(start_date, end_date, selected_cities):
    df_filtered = get_filtered_data(tuple(selected_cities), str(start_date), str(end_date))
    if df_filtered.empty:
        return alt.Chart().mark_bar().to_dict()

    df_grouped = df_filtered.groupby(["City", "AQI_Bucket"]).size().reset_index(name="count")

    chart = (
        alt.Chart(df_grouped)
        .mark_bar()
        .encode(
            x="City",
            y=alt.Y("count:Q", title="Count"),
            color=alt.Color("AQI_Bucket:N", legend=alt.Legend(title="", orient="top")),
            tooltip=["AQI_Bucket", "count:Q"]
        )
        .properties(width=400, height=300)
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
    df_filtered = get_filtered_data(tuple(selected_cities), str(start_date), str(end_date))
    
    if df_filtered.empty:
        return [
            dbc.CardHeader("No Data Available"),
            dbc.CardBody("No Data Available")
        ], [
            dbc.CardHeader("No Data Available"),
            dbc.CardBody("No Data Available")
        ]

    start_pollution = df_filtered[df_filtered['Datetime'] == start_date][pollutant].mean()
    end_pollution = df_filtered[df_filtered['Datetime'] == end_date][pollutant].mean()

    if pd.isna(start_pollution) or pd.isna(end_pollution):
        perc_change = "N/A"
    else:
        perc_change = round(((end_pollution - start_pollution) / start_pollution) * 100, 1)

    most_freq_aqi = df_filtered["AQI_Bucket"].mode()[0] if not df_filtered["AQI_Bucket"].isna().all() else "N/A"

    return [
        dbc.CardHeader(f'Percent Change in {pollutant}'),
        dbc.CardBody(f"{perc_change}%")
    ], [
        dbc.CardHeader("Most Frequent AQI Bucket"),
        dbc.CardBody(most_freq_aqi)
    ]

# =============== City Filter Update Based on Map Click ===============
@callback(
    Output('city', 'value'),
    [Input('geo_map', 'signalData')]
)
def update_city_filter(clicked_region):
    if clicked_region and clicked_region.get("select_region"):
        return clicked_region["select_region"]["City"]
    return city_df["City"].tolist()  # Default: all cities
