# src/callbacks.py
from dash import callback, Output, Input
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc

# Import data
from .data import df, pollutants, india_map, city_df

# ====================== Line Chart ======================
@callback(
    Output('line', 'spec'),
    [
        Input('col', 'value'),
        Input('city', 'value'),
        Input('date_range', 'start_date'),
        Input('date_range', 'end_date')
    ]
)
def create_line_chart(col, city, start_date, end_date):
    print("\n🔍 --- DEBUG INFO ---")
    print("Selected Pollutant:", col)
    print("Selected Cities:", city)
    print("Date Range:", start_date, end_date)

    if col is None:
        print("⚠️ WARNING: No pollutant selected. Using default 'AQI'.")
        col = "AQI"

    if col not in df.columns:
        print(f"ERROR: '{col}' column not found in DataFrame!")
        return {}

    df_city_filter = df[df["City"].isin(city)]
    df_date_filtered = df_city_filter[
        (df_city_filter["Datetime"] >= start_date)
        & (df_city_filter["Datetime"] <= end_date)
    ]

    if df_date_filtered.empty:
        print("⚠️ WARNING: No data available after filtering!")
        return {}

    # Choose frequency based on date range length
    date_length = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
    if date_length < 31:
        freq = "D"
    elif date_length < 400:
        freq = "W"
    elif date_length < 1200:
        freq = "MS"
    else:
        freq = "QS"

    df_line_chart = df_date_filtered.groupby(
        [pd.Grouper(key="Datetime", freq=freq), "City"]
    ).mean(numeric_only=True).reset_index()

    df_line_chart_mean = (
        df_line_chart.groupby(pd.Grouper(key="Datetime", freq=freq))
        .mean(numeric_only=True)
        .reset_index()
    )
    df_line_chart_mean['City'] = "Average"

    # Handle dot-notation columns like PM2.5
    col_escaped = col.replace(".", "_")
    df_line_chart = df_line_chart.rename(columns={col: col_escaped})
    df_line_chart_mean = df_line_chart_mean.rename(columns={col: col_escaped})

    y_column = alt.Y(
        f"{col_escaped}:Q",
        title=f"{col} Concentration",
        scale=alt.Scale(zero=False)
    )

    return (
        (
            alt.Chart(df_line_chart).mark_line().encode(
                x=alt.X("Datetime:T", title="Date"),
                y=y_column,
                color=alt.Color("City:N", title="Legend"),
                opacity=alt.value(0.5),
                tooltip=["Datetime:T", f"{col_escaped}:Q", "City:N"]
            )
            + alt.Chart(df_line_chart_mean).mark_line(color="black").encode(
                x=alt.X("Datetime:T", title="Date"),
                y=y_column,
                tooltip=["Datetime:T", f"{col_escaped}:Q"]
            )
        )
        .properties(
            title=f"{col} Over Time (Black = average)",
            height=170,
            width=300
        )
        .to_dict()
    )

# ====================== Correlation Plot ======================
@callback(
    Output('correlation-graph', 'spec'),
    [
        Input('date_range', 'start_date'),
        Input('date_range', 'end_date'),
        Input('city', 'value')
    ]
)
def update_correlation_plot(start_date, end_date, selected_cities):
    filtered_df = df[(df['Datetime'] >= start_date) & (df['Datetime'] <= end_date)]
    if isinstance(selected_cities, list):
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]
    filtered_df = filtered_df[pollutants].dropna()

    if filtered_df.empty:
        return alt.Chart(pd.DataFrame()).mark_text(
            text="No data to show"
        ).properties(width=300, height=150).to_dict()

    corr_matrix = filtered_df.corr()
    aqi_correlations = corr_matrix['AQI'].drop('AQI').reset_index()
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
            width=300,
            height=150
        )
        .configure_view(strokeWidth=0)
    )
    return chart.to_dict()

# ====================== Geo Map ======================
@callback(
    Output('geo_map', 'spec'),
    Input('city', 'value')
)
def update_geo_map(selected_cities):
    import altair as alt

    base_map = alt.Chart(india_map).mark_geoshape(
        fill='lightgray', stroke='black'
    ).encode(
        tooltip=[alt.Tooltip('ADMIN:N', title='Region')]
    ).project('mercator').properties(
        width=260,
        height=210
    )

    filtered_cities = city_df[city_df['City'].isin(selected_cities)]

    city_points = alt.Chart(filtered_cities).mark_point(
        fill="blue",
        size=100
    ).encode(
        longitude='Longitude:Q',
        latitude='Latitude:Q',
        tooltip=[alt.Tooltip('City:N', title='City')]
    ).project('mercator')

    final_chart = (base_map + city_points).properties(
        title="Select Cities"
    ).configure(background='#b38d24')  # or any preferred color
    return final_chart.to_dict()

# ====================== Data Cards ======================
@callback(
    [
        Output('card-percentage', 'children'),
        Output('card-aqi', 'children')
    ],
    [
        Input('col', 'value'),
        Input('city', 'value'),
        Input('date_range', 'start_date'),
        Input('date_range', 'end_date')
    ]
)
def update_cards(pollutant, selected_cities, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    if isinstance(selected_cities, str):
        selected_cities = [selected_cities]

    city_filtered_df = df[df['City'].isin(selected_cities)]
    date_filtered_df = city_filtered_df[
        (city_filtered_df['Datetime'] >= start_date)
        & (city_filtered_df['Datetime'] <= end_date)
    ]

    # This exact match might return NaN if no records match precisely
    start_pollution = city_filtered_df[city_filtered_df['Datetime'] == start_date][pollutant].mean()
    end_pollution = city_filtered_df[city_filtered_df['Datetime'] == end_date][pollutant].mean()

    if pd.isna(start_pollution) or pd.isna(end_pollution) or (start_pollution == 0):
        perc_change = 0
    else:
        perc_change = (end_pollution - start_pollution) / start_pollution

    # Most frequent AQI Bucket
    if date_filtered_df.empty or date_filtered_df["AQI_Bucket"].dropna().empty:
        most_freq = "N/A"
    else:
        mode_vals = date_filtered_df["AQI_Bucket"].mode()
        most_freq = mode_vals[0] if not mode_vals.empty else "N/A"

    card_percentage = [
        dbc.CardHeader(f'% Change in {pollutant}'),
        dbc.CardBody(f'{perc_change * 100:.1f}%')
    ]
    card_aqi = [
        dbc.CardHeader("Most Frequent AQI Bucket"),
        dbc.CardBody(most_freq)
    ]
    return card_percentage, card_aqi

# ====================== Stacked Bar ======================
@callback(
    Output('stacked-graph', 'spec'),
    [
        Input('date_range', 'start_date'),
        Input('date_range', 'end_date'),
        Input('city', 'value')
    ]
)
def update_stacked_plot(start_date, end_date, selected_cities):
    filtered_df = df[
        (df['Datetime'] >= start_date)
        & (df['Datetime'] <= end_date)
    ]
    if isinstance(selected_cities, list):
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]

    if filtered_df.empty:
        return alt.Chart(pd.DataFrame()).mark_text(
            text="No data to show"
        ).properties(width=300, height=150).to_dict()

    filtered_df = filtered_df.groupby(["City", "AQI_Bucket"]).size().reset_index(name="count")

    chart = (
        alt.Chart(filtered_df)
        .mark_bar()
        .encode(
            x='City:N',
            y='count:Q',
            color='AQI_Bucket:N',
            tooltip=['AQI_Bucket', 'count:Q']
        )
        .properties(
            title=alt.TitleParams("AQI Bucket Frequency"),
            width=300,
            height=150
        )
        .configure_view(strokeWidth=0)
    )
    return chart.to_dict()
