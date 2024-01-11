from selenium import webdriver
from bs4 import BeautifulSoup
import re
import logging
import os
from pool import BufferPool
from dotenv import load_dotenv

load_dotenv(override=True)

LOG_FILE = os.getenv('LOG_FILE')

# Creating log folder and file if not exist
if not os.path.isdir('./logs'):
    os.makedirs('./logs')
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as file:
        pass

logging.basicConfig(filename=LOG_FILE,
                    level=logging.ERROR,
                    format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                    filemode='w')

url = "https://www.carousell.sg/categories/cameras-1863/?cameras_type=TYPE_POINT_AND_SHOOT%2CTYPE_DSLR%2CTYPE_MIRRORLESS&searchId=kkZNPc&canChangeKeyword=false&price_end=250&includeSuggestions=false&sort_by=3"

op = webdriver.ChromeOptions()
op.add_argument('headless')
op.add_argument("user-agent=XXX")
dr = webdriver.Chrome(options = op)

item_regex = re.compile("listing-card-[0-9]*")
time_regex = re.compile("(\d|\d\d) seconds ago|(\d|\d\d) minutes ago")

class CarousellScraper:
    def __init__(self):
        self.title_pool = BufferPool(100)
        pass

    def check(self):
        dr.get(url)
        bs = BeautifulSoup(dr.page_source,features="html.parser")
        items = bs.find_all("div", {"data-testid":item_regex})

        for item in items:
            time_p = item.find('p').find_next('p')
            title_p = item.find('p',{"style":re.compile("--max-line:2|--max-line: 2;")})
            price_p = title_p.find_next('p')
            usage_p = price_p.find_next('p')
            link_a = item.find('a').find_next('a')
            image_img = link_a.find('img')

            if not time_p:
                logging.error(f"No time found in item {item}")

            if not title_p:
                logging.error(f"No title found in item {item}")

            if not link_a:
                logging.error(f"No link found in item {item}")
            if not price_p:
                logging.error(f"No price found in item {item}")
            if not image_img:
                logging.error(f"No image found in item{item}")

            if not time_p or not title_p or not link_a or not price_p or not image_img:
                continue

            time = time_p.get_text()
            title = title_p.get_text()
            link = link_a['href']
            price = price_p.get_text()
            image = image_img['src']
            usage = usage_p.get_text()


            if not time_regex.match(time): # >= 1h ago
                continue
            if not self.title_pool.add(title):
                continue
            
            yield {
                "time": time,
                "title": title,
                "link": f"https://carousell.sg{link}",
                "price": price,
                "image": image,
                "usage": usage
            }

