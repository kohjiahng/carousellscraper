from selenium import webdriver
from bs4 import BeautifulSoup
import re
import logging
import os
from pool import BufferPool
from dotenv import load_dotenv

load_dotenv(override=True)

LOG_FILE = os.getenv('LOG_FILE')

# Creating log file if not exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as file:
        pass

logging.basicConfig(filename=LOG_FILE,
                    level=logging.ERROR,
                    format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                    filemode='w')

class CarousellScraper:
    def __init__(self, url):
        self.title_pool = BufferPool(100)
        self.url = url

        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument("user-agent=XXX")
        self.driver = webdriver.Chrome(options = op)

    def get_time(self, item):
        time_p = item.find('p').find_next('p')
        if not time_p:
            logging.error(f"No time found in item {item}")
            return None
        else:
            return time_p.get_text()

    def get_title(self, item):
        title_p = item.find('p',{"style":re.compile("--max-line:2|--max-line: 2;")})
        if not title_p:
            logging.error(f"No title found in item {item}")
            return None
        else:
            return title_p.get_text()

    def get_path(self, item):
        path_a = item.find('a').find_next('a')
        if not path_a:
            logging.error(f"No path found in item {item}")
            return None
        else:
            return path_a['href']
    
    def get_price(self, item):
        title_p = item.find('p',{"style":re.compile("--max-line:2|--max-line: 2;")})
        price_p = title_p.find_next('p')
        if not price_p:
            logging.error(f"No price found in item {item}")
            return None
        else:
            return price_p.get_text()

    def get_usage(self, item):
        title_p = item.find('p',{"style":re.compile("--max-line:2|--max-line: 2;")})
        price_p = title_p.find_next('p')
        usage_p = price_p.find_next('p')
        if not usage_p:
            logging.error(f"No usage found in item {item}")
        else:
            return usage_p.get_text()
        
    def get_image(self, item):
        link_a = item.find('a').find_next('a')
        image_img = link_a.find('img')
        if not image_img:
            logging.error(f"No image found in item {item}")
        else:
            return image_img['src']

    def extract_data(self, item):
        time = self.get_time(item)
        title = self.get_title(item)
        path = self.get_path(item)
        price = self.get_price(item)
        image = self.get_image(item)
        usage = self.get_usage(item)

        data = {
            "title": title,
            "time": time,
            "path": path,
            "price": price,
            "image": image,
            "usage": usage
        }
        if None in data.values():
            return None
        else:
            return data

    def get_all_items(self):
        item_regex = re.compile("listing-card-[0-9]*")
        self.driver.get(self.url)
        bs = BeautifulSoup(self.driver.page_source,features="html.parser")
        items = bs.find_all("div", {"data-testid":item_regex})

        for item in items:
            data = self.extract_data(item)
            if data:
                yield data

    def check_new_item(self, item):
        time_regex = re.compile("(\d|\d\d) seconds ago|(\d|\d\d) minutes ago") # < 1h ago
        is_new = time_regex.match(item['time']) and  self.title_pool.check(item['title'])
        self.title_pool.add(item['title'])
        return is_new

    def get_filtered_items(self):
        return filter(self.check_new_item, self.get_all_items())

