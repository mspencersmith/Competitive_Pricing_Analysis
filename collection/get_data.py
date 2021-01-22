import csv
import json
import os.path
import time
from web_scraper import WebScraper
from tqdm import tqdm
from pathlib import Path


start = time.time()

BASE_DIR = Path(__file__).resolve().parent.parent
output_file = os.path.join(BASE_DIR, 'data/pricing_date.csv')

WebScraper.edit_file('_', output_file, 'w')

with open('dates.json') as f:
    dates = json.load(f)

checkins = dates['checkin']
checkouts = dates['checkout']

for checkin, checkout in zip(checkins, checkouts):

    asp_url = f'https://www.aspects-holidays.co.uk/cottages/in/newquay/start/{checkin}/sleeps/4/los/7/sorting/price-ascending'
    print(f'\n\nAppending aspects.com data for {checkin}')
    WebScraper(output_file, asp_url, 'aspects', checkin) # First page
    for i in tqdm(range(2, 101)):
        asp = WebScraper(output_file, asp_url, 'aspects', checkin, page=i)
        if not asp.MorePages:
            break

    air_url = f'https://www.airbnb.co.uk/s/Fistral-Beach--Newquay/homes?tab_id=home_tab&refinement_output_files%5B%5D=%2Fhomes&checkin={checkin}&checkout={checkout}&adults=4&source=structured_search_input_header&search_type=filter_change&ne_lat=50.45471946276464&ne_lng=-5.009513859244635&sw_lat=50.36223875919588&sw_lng=-5.140892040057679&zoom=12&search_by_map=true&place_id=ChIJD2v36sUPa0gRPb4zR4nEyrk'
    print(f'\n\nAppending airbnb.com data for {checkin}')
    WebScraper(output_file, air_url, 'airbnb', checkin, checkout) # First page
    for i in tqdm(range(20, 2001, 20)): # Offset starts at 20 amd increases by 20
        air = WebScraper(output_file, air_url, 'airbnb', checkin, checkout, i)
        if not air.MorePages:
            break

    in_year, in_month, in_day = WebScraper.boo_date('_', checkin)
    out_year, out_month, out_day = WebScraper.boo_date('_', checkout)
    boo_url = f'https://www.booking.com/searchresults.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaFCIAQGYAQm4ARfIAQ_YAQHoAQH4AQuIAgGoAgO4Aq7B__4FwAIB0gIkNTIyZjhlMDItNWM3ZC00YzQ5LThlYzAtYmEzN2QyMzk0Zjlj2AIG4AIB&sid=333f4c345becd6ba8ddebb42f1635dc2&tmpl=searchresults&ac_click_type=b&ac_position=0&checkin_month={in_month}&checkin_monthday={in_day}&checkin_year={in_year}&checkout_month={out_month}&checkout_monthday={out_day}&checkout_year={out_year}&class_interval=1&dest_id=-2604050&dest_type=city&dtdisc=0&from_sf=1&group_adults=4&group_children=0&iata=NQY&inac=0&index_postcard=0&label_click=undef&no_rooms=2&order=price&percent_htype_apt=1&postcard=0&raw_dest_type=city&room1=A%2CA&room2=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&srpvid=af3004af35b70105&ss=Newquay%2C%20Cornwall%2C%20United%20Kingdom&ss_all=0&ss_raw=newq&ssb=empty&sshis=0&top_ufis=1&nflt=ht_id%3D201%3Bht_id%3D220%3Bht_id%3D213%3B&rsf='
    print(f'\n\nAppending booking.com data for {checkin}')
    WebScraper(output_file, boo_url, 'booking', checkin, checkout) # First page
    for i in tqdm(range(25, 2501, 25)): # Offset starts at 25 and increases by 25 
        boo = WebScraper(output_file, boo_url, 'booking', checkin, checkout, i)
        if not boo.MorePages:
            break
    
    time.sleep(30)

finish = time.time()
secs = round((finish - start), 2)
print(f"\nTotal time taken {secs}s")
