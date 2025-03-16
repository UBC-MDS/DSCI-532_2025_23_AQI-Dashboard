---
editor_options: 
  markdown: 
    wrap: sentence
---

In this milestone, we overhauled the presentation of our dashboard to improve clarity, usability, and overall effectiveness.
For major changes, we replaced the dropdown-based city selection with an interactive map widget (#76), allowing users to visually explore AQI data by selecting locations directly on the map.
This provides a more intuitive user experience compared to a static dropdown.
Additionally, we optimized chart sizes, which previously appeared smaller than necessary with excessive whitespace.
We resized and repositioned the charts, considering the use of cards to better frame them (#77) and ensure they do not overlap.

For minor improvements, we discussed about text prompts for empty charts to inform users when no data is available for a selected range (#78).
However, we don't think it would add much insights.
Instead, we made a default to not having options to show the empty charts.
The dashboard title was restyled to improve aesthetics and clarity (#79), while the sidebar was adjusted to stretch the full height of the dashboard (#80) to create a visually balanced layout.
To enhance readability, we refined the formatting of data charts by improving spacing and alignment (#81).
Additionally, we addressed a long-standing issue where the black average line was missing from the legend, ensuring that users can now correctly interpret this critical reference (#82).
We also implemented more consistent color styling across the dashboard to unify the theme and enhance contrast (#83).
Finally, we resolved a callback bug in pollutant selection, ensuring that the dashboard properly updates even when no pollutant is selected (#84).

One of Joel’s comments was to refine the stacked bar chart to display AQI bucket labels across selected cities and time ranges.
We successfully implemented this, but after analyzing the data, we found that the distribution of AQI buckets did not change significantly over time.
Despite this, the stacked bar chart remains a valuable visualization for understanding AQI trends across different cities.
If time permits, we plan to further investigate possible insights from this dataset.

Another major refinement was improving the legend placement for our line plot.
Initially, the average AQI line was not included in the legend due to the way we structured our backend plotting logic.
Instead of integrating it directly into the legend, we added a clear label in the chart title to ensure users understood its significance.
While this is a temporary fix, adding the average to the legend remains an improvement we’d like to implement in the future.

We found that lecture materials on effective visualizations and user-friendly design were particularly helpful in improving our dashboard.
Feedback on switching from a dropdown to an interactive map made the selection process more intuitive, and expanding chart sizes significantly improved readability.
One challenge we faced was adding the black average line to the legend, which we addressed with a title label as a temporary fix.
More structured guidance on handling multi-layered visualizations in Altair would have been helpful.
Overall, peer feedback and iterative improvements greatly enhanced our dashboard’s clarity and usability.
