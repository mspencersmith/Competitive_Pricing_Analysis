import csv
import json
import re
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

class WebScraper:
    """Scrapes holiday websites and returns name, price, type of accommodation, number of rooms"""

    def __init__(self, filename, url, website, checkin, checkout=None, page=None):
        self.url = url
        self.website = website
        self.filename = filename
        self.checkin = checkin
        self.checkout = checkout
        self.page = page
        self.MorePages = True
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
                self.edit_file(self.filename, 'a') # Appends to file
            except UnicodeEncodeError as e:
                print(e)
                self.get_attr(item)
                self.edit_file(self.filename, 'a', encode=True) # Appends to file with encoding

    def create_url(self):
        """Creates url for extra pages"""
        if self.website == 'website1':
            self.url = f'{self.url}/page/{self.page}'
        elif self.website == 'website2':
            self.url = f'{self.url}&items_offset={self.page}&section_offset=3'
        elif self.website == 'website3':
            with open('urls.json') as f:
                url = json.load(f)
            in_year, in_month, in_day = self.web3_date(self.checkin)
            out_year, out_month, out_day = self.web3_date(self.checkout)
            self.url = url['web3+'].format(in_month=in_month, in_day=in_day, in_year=in_year, out_month=out_month, out_day=out_day, out_year=out_year)
            self.url = f'{self.url}{self.page}'
    
    def web3_date(self, date):
        """Sets month and day to correct format for website3"""
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
        if self.website == 'website2': # Checks if website2 page is in range
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
            if not soup.select(self.block): # Checks if website1 and website3 page is in range
                self.MorePages = False

    def edit_file(self, filename, mode, encode=False):
        """Writes or appends to file"""
        if encode:
            with open(filename, mode, newline='', encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([self.checkin, self.website, self.name, self.price, self.accommodation, self.rooms])
        else:
            with open(filename, mode, newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                if mode == 'w':
                    csv_writer.writerow(['date', 'website', 'name', 'price_GBP', 'accommodation', 'rooms'])
                elif mode == 'a':
                    csv_writer.writerow([self.checkin, self.website, self.name, self.price, self.accommodation, self.rooms])

    def get_response(self):
        """"Gets headers and response"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        if self.website == 'website1':
            self.block = '.property-box-inner'
        elif self.website == 'website2':
            self.block = '._8s3ctt'
        elif self.website == 'website3':
            self.block = '.sr_property_block'
        return soup
   
    def get_attr(self, item):
        if self.website == 'website1':
            self.get_attr_1(item)
        elif self.website == 'website2':
            self.get_attr_2(item)
        elif self.website == 'website3':
            self.get_attr_3(item)

    def get_attr_1(self, item):
        """Gets attributes for website1"""
        self.name = item.select('.property-name')[0].get_text().strip().split('\r')[0]
        self.price = item.select('.property-price')[0].get_text().strip().split(' ')[0]
        self.accommodation = None # No Accommodation type given
        self.rooms = item.select('.property-toptrumps')[0].get_text().strip()

    def get_attr_2(self, item):
        """Gets attributes for air bnb"""
        self.name = item.a['aria-label']
        self.price = item.select('._ebe4pze')[0].get_text().strip().split(' ')[0]
        self.accommodation = item.select('._b14dlit')[0].get_text().strip()
        self.rooms = item.select('._kqh46o')[0].get_text().strip()

    def get_attr_3(self, item):
        """Gets attributes for website3.com"""
        self.name = item.select('.sr-hotel__name')[0].get_text().strip()
        self.price = item.select('.bui-price-display__value')[0].get_text().strip()
        self.accommodation = item.select('.room_link')[0].get_text().strip()
        self.rooms = ''
        for i in item.select('.c-unit-configuration__item'): # Rooms is given as a list
            self.rooms = self.rooms + i.get_text().strip() + ' '
