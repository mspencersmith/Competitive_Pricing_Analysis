import csv
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

class WebScraper:
    """Scrapes holiday websites and returns name, price, type of accommodation, number of rooms"""

    def aspects(self, filename, url, page=None, write=False):
        """Scraper for https://www.aspects-holidays.co.uk/"""
        self.url = url
        if write:
            self._edit_file(filename, 'w')        
        else:
            self._set('asp', page)
        response, soup = self._get_response(self.url)
        
        for item in soup.select('.property-box-inner'):
            try:
                self.get_attr_asp(item) # Gets aspects attributes
                self._edit_file(filename, 'a')
            except UnicodeEncodeError as e:
                print(e)
                self.get_attr_asp(item)
                self._edit_file(filename, 'a', encode=True)

    def airbnb(self, filename, url, offset=None, write=False):
        """Scraper for https://www.airbnb.co.uk/"""
        self.url = url
        if write:
            self._edit_file(filename, 'w')
        else:
            self._set('air', offset)
        response, soup = self._get_response(self.url)
        
        for item in soup.select('._8s3ctt'):
            try:
                self.get_attr_air(item) # Gets airbnb attributes
                self._edit_file(filename, 'a')
            except UnicodeEncodeError as e:
                print(e)
                self.get_attr_air(item)
                self._edit_file(filename, 'a', encode=True)


    def booking(self, filename, url, offset=None, write=False):
        """Scraper for https://booking.com/"""
        self.url = url
        if write:
            self._edit_file(filename, 'w')
        else:
            self._set('boo', offset)
        response, soup = self._get_response(self.url)
        
        for item in soup.select('.sr_property_block'):
            try:
                self.get_attr_boo(item) # Gets booking.com attributes
                self._edit_file(filename, 'a')
            except UnicodeEncodeError as e:
                print(e)
                self.get_attr_boo(item)
                self._edit_file(filename, 'a', encode=True)
    
    def _get_response(self, url):
        """"Gets headers and response"""
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        return response, soup

    def _set(self, site, page):
        """Sets mode to write or append and sets append url"""
        if site == 'asp':
            self.url = f'{self.url}/page/{page}'
        elif site == 'air':
            self.url = f'{self.url}&items_offset={page}&section_offset=3'
        elif site == 'boo':
            self.url = 'https://www.booking.com/searchresults.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaFCIAQGYAQm4ARfIAQ_YAQHoAQH4AQuIAgGoAgO4Aq7B__4FwAIB0gIkNTIyZjhlMDItNWM3ZC00YzQ5LThlYzAtYmEzN2QyMzk0Zjlj2AIG4AIB&tmpl=searchresults&ac_click_type=b&ac_position=0&checkin_month=12&checkin_monthday=25&checkin_year=2021&checkout_month=1&checkout_monthday=1&checkout_year=2022&class_interval=1&dest_id=-2604050&dest_type=city&from_sf=1&group_adults=4&group_children=0&iata=NQY&label_click=undef&nflt=ht_id%3D201%3Bht_id%3D220%3Bht_id%3D213%3B&no_rooms=2&order=price&percent_htype_apt=1&raw_dest_type=city&room1=A%2CA&room2=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&srpvid=0f5708e2731a0009&ss=Newquay%2C%20Cornwall%2C%20United%20Kingdom&ss_raw=newq&ssb=empty&top_ufis=1&rows=25&offset='
            self.url = f'{self.url}{page}'

    def _edit_file(self, filename, mode, encode=False):
        if encode:
            with open(filename, mode, newline='', encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([self.name, self.price, self.accommodation, self.rooms])
        else:
            with open(filename, mode, newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                if mode == 'w':
                    csv_writer.writerow(['name', 'price', 'accommodation', 'rooms'])
                elif mode == 'a':
                    csv_writer.writerow([self.name, self.price, self.accommodation, self.rooms])

    def get_attr_asp(self, item):
        """Gets attributes for aspects"""
        self.name = item.select('.property-name')[0].get_text().strip().split('\r')[0]
        self.price = item.select('.property-price')[0].get_text().strip().split(' ')[0]
        self.accommodation = 'Aspects property' # No Accommodation type given
        self.rooms = item.select('.property-toptrumps')[0].get_text().strip()

    def get_attr_air(self, item):
        """Gets attributes for air bnb"""
        self.name = item.a['aria-label']
        self.price = item.select('._ebe4pze')[0].get_text().strip().split(' ')[0]
        self.accommodation = item.select('._b14dlit')[0].get_text().strip()
        self.rooms = item.select('._kqh46o')[0].get_text().strip()

    def get_attr_boo(self, item):
        """Gets attributes for booking.com"""
        self.name = item.select('.sr-hotel__name')[0].get_text().strip()
        self.price = item.select('.bui-price-display__value')[0].get_text().strip()
        self.accommodation = item.select('.room_link')[0].get_text().strip()
        self.rooms = ''
        for i in item.select('.c-unit-configuration__item'): # Rooms is given as a list
            self.rooms = self.rooms + i.get_text().strip() + ' '
