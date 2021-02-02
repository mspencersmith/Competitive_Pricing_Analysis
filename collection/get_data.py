import csv
import json
import os.path
import time
from web_scraper import WebScraper
from tqdm import tqdm
from pathlib import Path

start = time.time()

BASE_DIR = Path(__file__).resolve().parent.parent
output_file = os.path.join(BASE_DIR, 'data/test.csv')

with open('dates.json') as f:
    dates = json.load(f)
with open('urls.json') as f:
    url = json.load(f)

checkins = dates['checkin']
checkouts = dates['checkout']

for checkin, checkout in zip(checkins[10:], checkouts[10:]):
    web1_url = url['web1'].format(checkin=checkin)
    print(f'\n\nAppending website1 data for {checkin}')
    web1 = WebScraper(web1_url, 'website1', checkin) # First page
    web1.scrape(output_file)
    for i in tqdm(range(2, 101)):
        web1 = WebScraper(web1_url, 'website1', checkin, page=i)
        web1.scrape(output_file)
        if not web1.MorePages:
            break

    web2_url = url['web2'].format(checkin=checkin, checkout=checkout)
    print(f'\n\nAppending website2 data for {checkin}')
    web2 = WebScraper(web2_url, 'website2', checkin, checkout) # First page
    web2.scrape(output_file)
    for i in tqdm(range(20, 2001, 20)): # Offset starts at 20 amd increases by 20
        web2 = WebScraper(web2_url, 'website2', checkin, checkout, i)
        web2.scrape(output_file)
        if not web2.MorePages:
            break
    
    in_year, in_month, in_day = WebScraper.web3_date('_', checkin)
    out_year, out_month, out_day = WebScraper.web3_date('_', checkout)
    web3_url = url['web3'].format(in_month=in_month, in_day=in_day, in_year=in_year, out_month=out_month, out_day=out_day, out_year=out_year)
    print(f'\n\nAppending website3 data for {checkin}')
    web3 = WebScraper(web3_url, 'website3', checkin, checkout) # First page
    web3.scrape(output_file)
    for i in tqdm(range(25, 2501, 25)): # Offset starts at 25 and increases by 25 
        web3 = WebScraper(web3_url, 'website3', checkin, checkout, i)
        web3.scrape(output_file)
        if not web3.MorePages:
            break
    
    time.sleep(60)

finish = time.time()
secs = round((finish - start), 2)
print(f"\nTotal time taken {secs}s")
