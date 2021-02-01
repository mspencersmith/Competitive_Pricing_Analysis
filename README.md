# Self-Catering Accommodation Analysis

In this project I gathered and analysed pricing data for over 950 properties in Newquay, Cornwall across 3 websites throughout 2021.

## Technologies
### Python
- BeautifulSoup4
- Pandas
- Matplotlib

## Collection
Firstly, I created an automated web scraper (web_scaper.py, get_data.py) using BeautifulSoup4, to pull the price, type, and room characteristics of self-catering properties that sleep a minimum of 4 adults in Newquay. In total I collected over 21,000 data points from the end of January 2021 to the end of December 2021 and saved them to .csv ready for analysis.

## Analysis
After collection I used Pandas to clean the dataset removing any unreadable characters, outliers that were clear mistakes, and editing non-numerical prices as seen in clean_data.py and clean.py. Once the data set was cleaned I used Pandas to aggregate the data (average.py) and used Matplotlib to plot the findings as seen below (all_prop_graphs.py, room_graphs.py).

![Average Price Per Week (£)](/analysis/graphs/average.png)
![Average Price Per Week (£)](/analysis/graphs/average_bedrooms.png)
![Average Price Per Week (£)](/analysis/graphs/min.png)
![Average Price Per Week (£)](/analysis/graphs/minimum_bedrooms.png)
