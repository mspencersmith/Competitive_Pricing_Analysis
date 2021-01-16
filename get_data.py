import time
from web_scraper import WebScraper
from tqdm import tqdm

start = time.time()

f = 'data/test.csv'
print(f'Writing to {f}..')


asp_url = 'https://www.aspects-holidays.co.uk/cottages/in/newquay/start/2021-12-25/sleeps/4/los/7/sorting/price-ascending'
WebScraper(f, asp_url, 'aspects', write=True)
print('\n\nAppending aspects.com data')
for i in tqdm(range(2, 4)):
    WebScraper(f, asp_url, 'aspects', i)

air_url = 'https://www.airbnb.co.uk/s/Fistral-Beach--Newquay/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin=2021-12-25&checkout=2022-01-01&adults=4&source=structured_search_input_header&search_type=filter_change&ne_lat=50.45471946276464&ne_lng=-5.009513859244635&sw_lat=50.36223875919588&sw_lng=-5.140892040057679&zoom=12&search_by_map=true&place_id=ChIJD2v36sUPa0gRPb4zR4nEyrk'
WebScraper(f, air_url, 'airbnb')
print('\n\nAppending airbnb.com data')
for i in tqdm(range(20, 301, 20)): # Offset starts at 20 amd increases by 20
    WebScraper(f, air_url, 'airbnb', i)

boo_url = 'https://www.booking.com/searchresults.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaFCIAQGYAQm4ARfIAQ_YAQHoAQH4AQuIAgGoAgO4Aq7B__4FwAIB0gIkNTIyZjhlMDItNWM3ZC00YzQ5LThlYzAtYmEzN2QyMzk0Zjlj2AIG4AIB&sid=333f4c345becd6ba8ddebb42f1635dc2&tmpl=searchresults&ac_click_type=b&ac_position=0&checkin_month=12&checkin_monthday=25&checkin_year=2021&checkout_month=1&checkout_monthday=1&checkout_year=2022&class_interval=1&dest_id=-2604050&dest_type=city&dtdisc=0&from_sf=1&group_adults=4&group_children=0&iata=NQY&inac=0&index_postcard=0&label_click=undef&no_rooms=2&order=price&percent_htype_apt=1&postcard=0&raw_dest_type=city&room1=A%2CA&room2=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&srpvid=af3004af35b70105&ss=Newquay%2C%20Cornwall%2C%20United%20Kingdom&ss_all=0&ss_raw=newq&ssb=empty&sshis=0&top_ufis=1&nflt=ht_id%3D201%3Bht_id%3D220%3Bht_id%3D213%3B&rsf='
WebScraper(f, boo_url, 'booking')
for i in tqdm(range(25, 51, 25)): # Offset starts at 25 and increases by 25 
    WebScraper(f, boo_url, 'booking', i)

finish = time.time()
secs = round((finish - start), 2)
print(f"\nTotal time taken {secs}s")

