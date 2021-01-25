# Competitive_Pricing_Analysis

In this project I collected and analysed pricing data for over 950 properties in Newquay, Cornwall across 3 websites throughout 2021.

## Technologies
### Python
- BeautifulSoup4
- Pandas
- Matplotlib

## Collection
Firstly, I created an automated web scraper using BeautifulSoup4, to pull the price, type, and room characteristics of self-catering properties that sleep a minimum of 4 adults in Newquay. I then scraped the websites of 3 of the leading providers in the area, airbnb.com, aspects.com and booking.com. In total I collected over 21,000 data points from the end of January 2021 to the end of December 2021 and save them to .csv ready for analysis.

## Analysis
After collection I used Pandas to clean the dataset removing any unreadable characters, outliers that were clear mistakes, and editing non-numerical prices. Once the data set was cleaned I used Pandas to aggregate the data and used Matplotlib to plot the findings as seen below.

![Average Price Per Week (£)](/analysis/graphs/average.png)
![Average Price Per Week (£)](/analysis/graphs/min.png)
