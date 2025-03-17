# src/callbacks.py
import pandas as pd
import altair as alt
from dash import callback, Output, Input, State
import dash_bootstrap_components as dbc
from functools import lru_cache

# Import from data.py and components.py
from src.data import df, pollutants, india_map, city_df
from src.components import sidebar_background_color

@lru_cache(maxsize=32)
def get_filtered_data(cities_tuple, start_date_str, end_date_str):
    """
    Filters the main DataFrame by city and date range.
    Caches the result to avoid repeated computation.
    """
    start_date = pd.to_datetime(start_date_str)
    end_date = pd.to_datetime(end_date_str)
    mask = (
        df["City"].isin(cities_tuple) &
        (df["Datetime"] >= start_date) &
        (df["Datetime"] <= end_date)
    )
    return df.loc[mask].copy()

@callback(
    Output('line', 'spec'),
    [
        Input('col', 'value'),
        Input('city', 'value'),
        Input('date_range', 'start_date'),
        Input('date_range', 'end_date')
    ]
)
def create_line_chart(col, selected_cities, start_date, end_date):
    # Ensure 'selected_cities' is a list
    if isinstance(selected_cities, str):
        selected_cities = [selected_cities]

    df_filtered = get_filtered_data(tuple(selected_cities), str(start_date), str(end_date))
    if df_filtered.empty:
        return alt.Chart().mark_line().to_dict()

    date_length = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
    if date_length < 31:
        freq = "D"
    elif date_length < 400:
        freq = "W"
    elif date_length < 1200:
        freq = "MS"
    else:
        freq = "QS"

    grouped = (
        df_filtered
        .groupby([pd.Grouper(key="Datetime", freq=freq), "City"])[col]
        .mean(numeric_only=True)
        .reset_index()
    )

    overall_mean = (
        grouped
        .groupby(pd.Grouper(key="Datetime", freq=freq))[col]
        .mean()
        .reset_index()
    )
    overall_mean['City'] = "Average"

    col_escaped = col.replace('.', '_')
    grouped.rename(columns={col: col_escaped}, inplace=True)
    overall_mean.rename(columns={col: col_escaped}, inplace=True)

    y_axis = alt.Y(
        f"{col_escaped}:Q",
        title=f"{col} Concentration" if col != "AQI" else "AQI",
        scale=alt.Scale(zero=False)
    )

    chart = (
        (
            alt.Chart(grouped)
            .mark_line()
            .encode(
                x=alt.X("Datetime:T", title="Date"),
                y=y_axis,
                color="City:N",
                tooltip=["Datetime:T", f"{col_escaped}:Q", "City:N"]
            )
            +
            alt.Chart(overall_mean)
            .mark_line(color="black")
            .encode(
                x="Datetime:T",
                y=y_axis,
                color=alt.Color("City:N",
                                scale=alt.Scale(domain=["Average"], range=["black"])),
                tooltip=["Datetime:T", f"{col_escaped}:Q"]
            )
        )
        .resolve_scale(color='independent')
        .properties(height=270, width=515)
        .to_dict()
    )
    return chart

# Add more callbacks for correlation, map, stacked bar, etc. as needed.
