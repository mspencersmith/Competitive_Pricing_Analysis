import csv
import json
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

class WebScraper:
    """Scrapes holiday websites and returns name, price, type of accommodation, number of rooms"""

    def __init__(self, url, website, checkin, checkout=None, page=None):
        self.url = url
        self.website = website
        self.checkin = checkin
        self.checkout = checkout
        self.page = page
        self.MorePages = True
        if page:        
            self.create_url() #Creates url for extra pages

    def scrape(self, filename):
        """Scrapes website outputs to csv"""
        soup, block = self.get_response()
        self.page_check(soup, block) # Checks if page number is in web page range
        with open(filename, 'a', newline='', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            for item in soup.select(block): # Selects block of html where attributes are stored for all websites
                name, price, accommodation, rooms = self.get_attr(item)
                csv_writer.writerow([self.checkin, self.website, name, price, accommodation, rooms])

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

    def page_check(self, soup, block):
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
            if not soup.select(block): # Checks if website1 and website3 page is in range
                self.MorePages = False

    def get_response(self):
        """"Gets headers and response"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        if self.website == 'website1':
            block = '.property-box-inner'
        elif self.website == 'website2':
            block = '._8s3ctt'
        elif self.website == 'website3':
            block = '.sr_property_block'
        return soup, block
   
    def get_attr(self, item):
        if self.website == 'website1':
            name, price, accommodation, rooms = self.get_attr_1(item)
        elif self.website == 'website2':
            name, price, accommodation, rooms = self.get_attr_2(item)
        elif self.website == 'website3':
            name, price, accommodation, rooms = self.get_attr_3(item)
        return name, price, accommodation, rooms

    def get_attr_1(self, item):
        """Returns attributes for website1"""
        name = item.select('.property-name')[0].get_text().strip().split('\r')[0]
        price = item.select('.property-price')[0].get_text().strip().split(' ')[0]
        accommodation = None # No Accommodation type given
        rooms = item.select('.property-toptrumps')[0].get_text().strip()
        return name, price, accommodation, rooms

    def get_attr_2(self, item):
        """Returns attributes for website2"""
        name = item.a['aria-label']
        price = item.select('._ebe4pze')[0].get_text().strip().split(' ')[0]
        accommodation = item.select('._b14dlit')[0].get_text().strip()
        rooms = item.select('._kqh46o')[0].get_text().strip()
        return name, price, accommodation, rooms

    def get_attr_3(self, item):
        """Returns attributes for website3"""
        name = item.select('.sr-hotel__name')[0].get_text().strip()
        price = item.select('.bui-price-display__value')[0].get_text().strip()
        accommodation = item.select('.room_link')[0].get_text().strip()
        rooms = ''
        for i in item.select('.c-unit-configuration__item'): # Rooms is given as a list
            rooms = rooms + i.get_text().strip() + ' '
        return name, price, accommodation, rooms
