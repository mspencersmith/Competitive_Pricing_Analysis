import csv
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

class WebScraper:
    """Scrapes holiday websites and returns name, price, type of accommodation, number of rooms"""

    def aspects(self, filename, page=None, write=False):
        """Scraper for https://www.aspects-holidays.co.uk/"""
        
        url = 'https://www.aspects-holidays.co.uk/cottages/in/newquay/start/2021-12-25/sleeps/4/los/7/sorting/price-ascending'
        
        mode, url = self._set('asp', url, page, write)
        response, soup = self._get_response(url)
        
        with open(filename, mode, newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            if write:
                csv_writer.writerow(['name', 'price', 'accommodation', 'rooms'])
            title = soup.find()
            for item in soup.select('.property-box-inner'):
                try:
                    name = item.select('.property-name')[0].get_text().strip().split('\r')[0]
                    price = item.select('.property-price')[0].get_text().strip().split(' ')[0]
                    accommodation = 'Aspects property' # No Accommodation type given
                    rooms = item.select('.property-toptrumps')[0].get_text().strip()

                except Exception as e:
                    print(e)
                
                csv_writer.writerow([name, price, accommodation, rooms])
    
    def airbnb(self, filename, offset=None, write=False):
        """Scraper for https://www.airbnb.co.uk/"""
        
        url = 'https://www.airbnb.co.uk/s/Fistral-Beach--Newquay/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin=2021-12-25&checkout=2022-01-01&adults=4&source=structured_search_input_header&search_type=filter_change&ne_lat=50.45471946276464&ne_lng=-5.009513859244635&sw_lat=50.36223875919588&sw_lng=-5.140892040057679&zoom=12&search_by_map=true&place_id=ChIJD2v36sUPa0gRPb4zR4nEyrk'
        
        mode, url = self._set('air', url, offset, write)
        response, soup = self._get_response(url)
        
        with open(filename, mode, newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            if write:
                csv_writer.writerow(['name', 'price', 'accommodation', 'rooms'])
            for item in soup.select('._8s3ctt'):
                try:
                    name = item.a['aria-label']
                    price = item.select('._ebe4pze')[0].get_text().strip().split(' ')[0]
                    accommodation = item.select('._167qordg')[0].get_text().strip()
                    rooms = item.select('._kqh46o')[0].get_text().strip()
                except Exception as e:
                    print(e)
                try:
                    csv_writer.writerow([name, price, accommodation, rooms])
                except UnicodeEncodeError as e: # This catches names with unformated characters
                    csv_writer.writerow(['invalid_name', price, accommodation, rooms])


    def booking(self, filename, offset=None, write=False):
        """Scraper for https://booking.com/"""
        url = 'https://www.booking.com/searchresults.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaFCIAQGYAQm4ARfIAQ_YAQHoAQH4AQuIAgGoAgO4Aq7B__4FwAIB0gIkNTIyZjhlMDItNWM3ZC00YzQ5LThlYzAtYmEzN2QyMzk0Zjlj2AIG4AIB&sid=333f4c345becd6ba8ddebb42f1635dc2&tmpl=searchresults&ac_click_type=b&ac_position=0&checkin_month=12&checkin_monthday=25&checkin_year=2021&checkout_month=1&checkout_monthday=1&checkout_year=2022&class_interval=1&dest_id=-2604050&dest_type=city&dtdisc=0&from_sf=1&group_adults=4&group_children=0&iata=NQY&inac=0&index_postcard=0&label_click=undef&no_rooms=2&order=price&percent_htype_apt=1&postcard=0&raw_dest_type=city&room1=A%2CA&room2=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&srpvid=af3004af35b70105&ss=Newquay%2C%20Cornwall%2C%20United%20Kingdom&ss_all=0&ss_raw=newq&ssb=empty&sshis=0&top_ufis=1&nflt=ht_id%3D201%3Bht_id%3D220%3Bht_id%3D213%3B&rsf='
        
        mode, url = self._set('boo', url, offset, write)
        response, soup = self._get_response(url)
        
        with open(filename, mode, newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            if write:
                csv_writer.writerow(['name', 'price', 'accommodation', 'rooms'])
            for item in soup.select('.sr_property_block'):
                rooms = ''
                try:
                    name = item.select('.sr-hotel__name')[0].get_text().strip()
                    price = item.select('.bui-price-display__value')[0].get_text().strip()
                    accommodation = item.select('.room_link')[0].get_text().strip()
                    for i in item.select('.c-unit-configuration__item'): # Rooms is given as a list
                        rooms = rooms + i.get_text().strip() + ' '
                except Exception as e:
                    print(e)
            
                csv_writer.writerow([name, price, accommodation, rooms])
    
    def _get_response(self, url):
        """"Gets headers and response"""
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        return response, soup

    def _set(self, site, url, page, write):
        """Sets mode to write or append and sets append url"""
        
        if write:
            mode = 'w'
        else:
            mode = 'a'
            if site == 'asp':
                url = f'{url}/page/{page}'
            elif site == 'air':
                url = f'{url}&items_offset={page}&section_offset=3'
            elif site == 'boo':
                url = 'https://www.booking.com/searchresults.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaFCIAQGYAQm4ARfIAQ_YAQHoAQH4AQuIAgGoAgO4Aq7B__4FwAIB0gIkNTIyZjhlMDItNWM3ZC00YzQ5LThlYzAtYmEzN2QyMzk0Zjlj2AIG4AIB&sid=333f4c345becd6ba8ddebb42f1635dc2&tmpl=searchresults&ac_click_type=b&ac_position=0&checkin_month=12&checkin_monthday=25&checkin_year=2021&checkout_month=1&checkout_monthday=1&checkout_year=2022&class_interval=1&dest_id=-2604050&dest_type=city&from_sf=1&group_adults=4&group_children=0&iata=NQY&label_click=undef&nflt=ht_id%3D201%3Bht_id%3D220%3Bht_id%3D213%3B&no_rooms=2&order=price&percent_htype_apt=1&raw_dest_type=city&room1=A%2CA&room2=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&srpvid=fc7a04b25c970163&ss=Newquay%2C%20Cornwall%2C%20United%20Kingdom&ss_raw=newq&ssb=empty&top_ufis=1&rows=25&offset='
                url = f'{url}{page}'

        return mode, url




f = 'data/test.csv'
print(f'Writing to {f}..')

ws = WebScraper()
ws.booking(f, write=True)
print('\nAppending booking.com data')
for i in tqdm(range(25, 51, 25)): # Offset starts at 25 amd increases by 25 
    ws.booking(f, offset=i)

# ws.aspects(f, write=True)
print('\n\nAppending aspects.com data')
for i in tqdm(range(2, 4)):
    ws.aspects(f, i)

# ws.airbnb(f, write=True)
print('\n\nAppending airbnb.com data')
for i in tqdm(range(20, 181, 20)): # Offset starts at 20 amd increases by 20
    ws.airbnb(f, offset=i)