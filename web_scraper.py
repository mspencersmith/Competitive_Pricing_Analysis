import csv
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

class WebScraper:
    """Scrapes holiday websites and returns name, price, type of accommodation, number of rooms"""

    def __init__(self, filename, url, website, page=None, write=False):
        self.url = url
        self.website = website
        self.filename = filename
        self.page = page
        self.write = write
        if page:        
            self.create_url() #Creates url for extra pages
        self.scrape()

    def scrape(self):
        """Scrapes website outputs to csv"""
        if self.write:
            self.edit_file('w') # Writes header

        response, soup = self.get_response()
        
        for item in soup.select(self.block): # Selects block of html attributes are stored
            try:
                self.get_attr(item)
                self.edit_file('a') # Appends to file
            except UnicodeEncodeError as e:
                print(e)
                self.get_attr(item)
                self.edit_file('a', encode=True) # Appends to file with encoding

    def create_url(self):
        """Creates url for extra pages"""
        if self.website == 'aspects':
            self.url = f'{self.url}/page/{self.page}'
        elif self.website == 'airbnb':
            self.url = f'{self.url}&items_offset={self.page}&section_offset=3'
        elif self.website == 'booking':
            self.url = 'https://www.booking.com/searchresults.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaFCIAQGYAQm4ARfIAQ_YAQHoAQH4AQuIAgGoAgO4Aq7B__4FwAIB0gIkNTIyZjhlMDItNWM3ZC00YzQ5LThlYzAtYmEzN2QyMzk0Zjlj2AIG4AIB&tmpl=searchresults&ac_click_type=b&ac_position=0&checkin_month=12&checkin_monthday=25&checkin_year=2021&checkout_month=1&checkout_monthday=1&checkout_year=2022&class_interval=1&dest_id=-2604050&dest_type=city&from_sf=1&group_adults=4&group_children=0&iata=NQY&label_click=undef&nflt=ht_id%3D201%3Bht_id%3D220%3Bht_id%3D213%3B&no_rooms=2&order=price&percent_htype_apt=1&raw_dest_type=city&room1=A%2CA&room2=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&srpvid=0f5708e2731a0009&ss=Newquay%2C%20Cornwall%2C%20United%20Kingdom&ss_raw=newq&ssb=empty&top_ufis=1&rows=25&offset='
            self.url = f'{self.url}{self.page}'
    
    def edit_file(self, mode, encode=False):
        """Writes or appends to file"""
        if encode:
            with open(self.filename, mode, newline='', encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([self.name, self.price, self.accommodation, self.rooms])
        else:
            with open(self.filename, mode, newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                if mode == 'w':
                    csv_writer.writerow(['name', 'price', 'accommodation', 'rooms'])
                elif mode == 'a':
                    csv_writer.writerow([self.name, self.price, self.accommodation, self.rooms])

    def get_response(self):
        """"Gets headers and response"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        if self.website == 'aspects':
            self.block = '.property-box-inner'
        elif self.website == 'airbnb':
            self.block = '._8s3ctt'
        elif self.website == 'booking':
            self.block = '.sr_property_block'
        return response, soup
   
    def get_attr(self, item):
        if self.block == '.property-box-inner':
            self.get_attr_asp(item)
        elif self.block == '._8s3ctt':
            self.get_attr_air(item)
        elif self.block == '.sr_property_block':
            self.get_attr_boo(item)

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
