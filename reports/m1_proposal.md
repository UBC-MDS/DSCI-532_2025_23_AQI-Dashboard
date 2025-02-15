# Motivation and purpose

The primary target audience for the Air Quality Dashboard is the general public, including residents of India who are interested in or concerned about air pollution trends and insights in India. Air pollution is a significant public health concern in India, with pollutants such as PM2.5, PM10, NO2, SO2, and CO contributing to potential respiratory diseases and threats to biodiversity.

Despite air quality data being released over the years, there is a lack of public and interactive dashboards that allow people to explore trends, compare different regions, analyze the impact of pollutants over time, and help the general public become more health-conscious.

This dashboard provides user-friendly visualizations to help the general public track air quality trends, including AQI and other pollution metrics, from 2015 to 2024. It also includes a heatmap showing comparisons across different cities, enabling users to identify regions with high pollution distribution within a specified date range. Additionally, the dashboard offers an interactive chart displaying the relative rankings of cities—from best to worst pollution levels—within a selected date range.

Overall, this dashboard will help the general public stay informed and raise awareness about air quality trends, identify pollution hotspots, and make safer daily choices by providing easy-to-understand visualizations, real time alerts, and health recommendations. It empowers users to track changes over time and understand how pollutants impact air quality, thereby promoting healthier living decisions.

# Description of the data

The dataset we're using contains air quality information for 5 cities in India over the span of 10 years. The data itself is taken hourly (\~432,000 lines) but we're planning on converting it to daily values to cut down on the processing we have to do (24x smaller). In addition to AQI the dataset also includes measurements for various greenhouse gases over the same time frame.

Using this data we plan to create a informative and easy to understand dashboard that will show the fluctuations in the air quality of the 5 cities over time. By doing this, we hope the general public becomes interested in their local air quality. We also plan on deriving the cumulative change over the user's specified time period in the various gases and AQI allowing users to see if there’s been an overall increase of decrease.

# Research questions and usage scenarios

This dashboard aims to help the Indian general public understand long-term air quality trends in their cities. It answers key questions such as how air quality has changed over the past decade, which months have the worst pollution levels, and which pollutants contribute the most to poor air quality. Users can also compare pollution trends across cities and identify seasonal patterns.

Raj is a working professional and father of two in Delhi. He has heard some news about smog in his city and is concerned about the impact of air pollution on his family’s health. Using the dashboard, he filters for Delhi and explores AQI trends over the past 10 years. He compares the trend to other cities and examines how pollution levels vary by season. He filters through the different pollutant data on the dashboard and identifies PM2.5 as a major contributor, and notices that winter months consistently have the worst air quality. After analyzing the data, he decides to limit outdoor activities for his children during peak pollution months. He also shares his findings with a local advocacy group pushing for cleaner public transportation and stricter air quality regulations.

# App sketch and description

![alt text](../img/sketch.png)

Our dashboard provides an interactive analysis of air quality trends in India over the past decade. Users can select up to five cities and adjust the time period of interest through dynamic filters. The dashboard features the Air Quality Index (AQI) and key pollutants contributing to air pollution.

To visualize trends effectively, we utilize bar charts and line charts, illustrating variations in AQI and pollutant levels over time. Additionally, two key insight cards highlight critical information, including the percentage increase in AQI and the most influential pollutants correlated with AQI fluctuations.

This interactive tool enables users to explore air quality patterns, identify key contributing factors, and gain actionable insights into pollution trends across different cities in India.
