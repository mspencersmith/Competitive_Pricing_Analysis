# Self-Catering Accommodation Analysis

In this project I gathered and analysed pricing data for over 950 properties in Newquay, Cornwall across 3 websites throughout 2021. The target audience for this analysis is families and small groups looking for affordable accommodation.

## Technologies
### Python
- BeautifulSoup4
- Pandas
- Matplotlib

## Collection
Firstly, I created an automated web scraper (web_scaper.py, get_data.py) using BeautifulSoup4, to pull the price, type, and room characteristics of self-catering properties that sleep a minimum of 4 people in Newquay. In total I collected over 21,000 data points from the end of January 2021 to the end of December 2021 and saved them to csv format ready for analysis.

## Cleaning
After collection I cleaned the dataset removing any unreadable characters, and ensuring the price column only contained numerical values removing any addition characters (clean_data.py and clean.py). I checked for outliers using a boxplot of the prices, as seen below there are prices that are either errors or are out of the scope of affordable accommodation. I therefore further cleaned the dataset using the interquartlie range for each week. 

![Boxplot of Price (£)](/analysis/graphs/price_boxplot.png)



## Analysis
Once the data set was cleaned I used Pandas to aggregate the data (average.py) and used Matplotlib to plot the findings as seen below (all_prop_graphs.py, room_graphs.py).

![Maximum, Median, and Minimum Price Per Week(£)](/analysis/graphs/max_med_min.png)
As you can see from the graph the average price peaks in August and you can find the cheapest prices in November. If you are looking for a summer holiday and price is a limiting factor then it would be best to plan your holiday in June before the prices start trending towards the peak.

![Properties Available](/analysis/graphs/room_count.png)
As the graph shows, the more rooms you require the less availability there is throughout the year (unless you only require 1 room). If you require more than 3 rooms it would be wise to book early to avoid disappointment. Another observation to consider is the significant dip in availability in the first week of June and end of July across all categories.

![Average Price of 2-5 Bedroom Accommodation(£)](/analysis/graphs/average_bedrooms.png)
This graph shows that as you would expect in general the more bedrooms a property has the more expensive it is. However this does not hold true for 5 bedroom properties which are similar prices to 4 bedroom properties. In fact if you plan your holiday in early March or early April you can find 5 bedroom properties for the same price as 3 bedroom properties, so if you are travelling with a larger group this might be the most cost efficient time to travel.


![Minimum Price of 2-5 Bedroom Accommodation(£)](/analysis/graphs/minimum_bedrooms.png)
This graph shows the minimum price you can expect to pay for 2-5 bedroom properties throughout 2021.
