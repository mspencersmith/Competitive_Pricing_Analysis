import csv
import re
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

class WebScraper:
    """Scrapes holiday websites and returns name, price, type of accommodation, number of rooms"""

    def __init__(self, filename, url, website, checkin, checkout=None, page=None, write=False):
        self.url = url
        self.website = website
        self.filename = filename
        self.checkin = checkin
        self.checkout = checkout
        self.page = page
        self.MorePages = True
        if write:
            self.edit_file('w') # Writes header
        if page:        
            self.create_url() #Creates url for extra pages
        self.scrape()

    def scrape(self):
        """Scrapes website outputs to csv"""
        soup = self.get_response()
        self.page_check(soup) # Checks if page number is in web page range

        for item in soup.select(self.block): # Selects block of html where attributes are stored for all websites
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
            in_year, in_month, in_day = self.boo_date(self.checkin)
            out_year, out_month, out_day = self.boo_date(self.checkout)
            self.url = f'https://www.booking.com/searchresults.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaFCIAQGYAQm4ARfIAQ_YAQHoAQH4AQuIAgGoAgO4Aq7B__4FwAIB0gIkNTIyZjhlMDItNWM3ZC00YzQ5LThlYzAtYmEzN2QyMzk0Zjlj2AIG4AIB&tmpl=searchresults&ac_click_type=b&ac_position=0&checkin_month={in_month}&checkin_monthday={in_day}&checkin_year={in_year}&checkout_month={out_month}&checkout_monthday={out_day}&checkout_year={out_year}&class_interval=1&dest_id=-2604050&dest_type=city&from_sf=1&group_adults=4&group_children=0&iata=NQY&label_click=undef&nflt=ht_id%3D201%3Bht_id%3D220%3Bht_id%3D213%3B&no_rooms=2&order=price&percent_htype_apt=1&raw_dest_type=city&room1=A%2CA&room2=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&srpvid=0f5708e2731a0009&ss=Newquay%2C%20Cornwall%2C%20United%20Kingdom&ss_raw=newq&ssb=empty&top_ufis=1&rows=25&offset='
            self.url = f'{self.url}{self.page}'
    
    def boo_date(self, date):
        """Sets month and day to correct format for booking.com"""
        year = date[:4]
        if date[5] == '0': # Days cannot start with 0
            month = date[6]
        else:
            month = date[5:7]
        if date[8] == '0':
            day = date[9] # Months cannot start with 0
        else:
            day = date[8:10]
        return year, month, day

    def page_check(self, soup):
        """Checks whether page is in web page range"""
        if self.website == 'airbnb': # Checks if Airbnb page is in range
            check = '._1h559tl'
            total_pattern = re.compile(r'(\d+)') # Only digits
            for item in soup.select(check):
                count = int(item.get_text().split(' ')[0]) # Count of items so far
                total = item.get_text().split(' ')[4] # Total number of items
                total = total_pattern.search(total) # Ensures there is no +
                total = int(total.group(1))
                if count > total:
                    self.MorePages = False
        else:
            if not soup.select(self.block): # Checks if Apects and Booking page is in range
                self.MorePages = False

    def edit_file(self, mode, encode=False):
        """Writes or appends to file"""
        if encode:
            with open(self.filename, mode, newline='', encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([self.checkin, self.website, self.name, self.price, self.accommodation, self.rooms])
        else:
            with open(self.filename, mode, newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                if mode == 'w':
                    csv_writer.writerow(['date', 'website', 'name', '£_price', 'accommodation', 'rooms'])
                elif mode == 'a':
                    csv_writer.writerow([self.checkin, self.website, self.name, self.price, self.accommodation, self.rooms])

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
        return soup
   
    def get_attr(self, item):
        if self.website == 'aspects':
            self.get_attr_asp(item)
        elif self.website == 'airbnb':
            self.get_attr_air(item)
        elif self.website == 'booking':
            self.get_attr_boo(item)

    def get_attr_asp(self, item):
        """Gets attributes for aspects"""
        self.name = item.select('.property-name')[0].get_text().strip().split('\r')[0]
        self.price = item.select('.property-price')[0].get_text().strip().split(' ')[0]
        self.accommodation = None # No Accommodation type given
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
